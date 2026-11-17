#!/usr/bin/env python3
"""编排：一圈完整工作循环 感知 → 推理 → 行动。cron 每 15 分钟（工作日）唤醒执行。

幂等性：state/seen_jobs.json 记录已处理岗位；只有处理成功才标记 seen，
超出单轮上限的候选留到下一轮（自然 backlog）。
首轮 bootstrap：全量岗位里只判前 bootstrap_max 个候选（给 2brain 铺底），
其余直接标 seen，避免首轮上千次 LLM 调用。
"""
import json
import sys
from datetime import datetime

from common import (CONFIG, PENDING_FILE, append_outbox, append_queue, judge_mode,
                    load_state, log_run, notify_mode, now_iso, save_state, slug)
from fetch_jobs import fetch_all
from judge import prefilter, judge_item
from screen import screen_titles
from kb import get_kb


def render_doc(item, judgment):
    """岗位 → Markdown 文档（入库 2brain 的载体）。"""
    tags = " ".join(judgment.get("tags", []))
    return f"""# {item['company']} — {item['title']}

- 优先级: {judgment['priority']} ({judgment['match']})
- 公司: {item['company']}
- 地点: {item['location'] or 'N/A'}
- 信源: {item['source']} (doc_id: {item['doc_id']})
- 原文链接: {item['detail_url']}
- 发布时间: {item.get('posted_at') or item.get('updated_at') or 'N/A'}
- 抓取时间: {now_iso()}
- JD 抓取工具: {judgment.get('jd_tool', 'none')}
- 标签: {tags}
- Visa 风险: {judgment.get('visa_risk', 'unknown')}

## AI 摘要

{judgment['summary_zh']}

判断依据：{judgment.get('reasons', '')}

## JD 原文

{judgment.get('jd_text') or '(未获取到 JD 全文)'}
"""


def interleave_by_source(items):
    """按信源轮流排序，避免单一公司独占单轮处理上限。"""
    from collections import defaultdict, deque
    buckets = defaultdict(deque)
    for it in items:
        buckets[it["source"]].append(it)
    out, queues = [], list(buckets.values())
    while queues:
        queues = [q for q in queues if q]
        for q in queues:
            if q:
                out.append(q.popleft())
    return out


LOCK_FILE = None  # set in run_once


def acquire_lock():
    """防止 cron 与手动/超时运行重叠。锁超过 45 分钟视为陈旧可抢占。"""
    import os
    import time
    from common import ROOT
    lock = ROOT / "state" / "pipeline.lock"
    if lock.exists():
        try:
            busy = lock.read_text().strip() != ""  # 空文件 = 已释放
            age = time.time() - lock.stat().st_mtime
            if busy and age < 45 * 60:
                return None
        except OSError:
            pass
    lock.parent.mkdir(exist_ok=True)
    lock.write_text(str(os.getpid()))
    return lock


def run_once():
    lock = acquire_lock()
    if lock is None:
        summary = {"ok": True, "skipped": "another run in progress"}
        log_run({"kind": "cycle", **summary})
        return summary
    try:
        return _run_once_inner(lock)
    finally:
        try:
            lock.unlink()
        except OSError:  # 某些挂载不允许删除：清空内容并回拨 mtime，等效释放
            try:
                import os as _os
                lock.write_text("")
                _os.utime(lock, (0, 0))
            except OSError:
                pass


def _run_once_inner(lock):
    state = load_state()
    bootstrap = len(state) == 0
    summary = {
        "ok": True, "bootstrap": bootstrap, "fetched": 0, "new": 0, "changed": 0,
        "prefiltered_out": 0, "screened_out": 0, "judged": 0, "P1": 0, "P2": 0, "P3": 0,
        "uploaded": 0, "notified": 0, "errors": [],
    }

    # ---- 感知 ----
    items, fetch_errors = fetch_all()
    summary["fetched"] = len(items)
    summary["errors"].extend(fetch_errors)
    if not items and fetch_errors:
        summary["ok"] = False
        log_run({"kind": "cycle", **summary})
        return summary

    # ---- 去重 / 变更检测（script）----
    todo = []
    for it in items:
        prev = state.get(it["doc_id"])
        if prev is None:
            it["event"] = "new"
            todo.append(it)
        elif prev.get("hash") != it["content_hash"]:
            it["event"] = "changed"
            todo.append(it)
    summary["new"] = sum(1 for t in todo if t["event"] == "new")
    summary["changed"] = sum(1 for t in todo if t["event"] == "changed")

    # ---- 硬过滤（script）----
    candidates = interleave_by_source([t for t in todo if prefilter(t)])
    noise = [t for t in todo if not prefilter(t)]
    summary["prefiltered_out"] = len(noise)
    for t in noise:  # 噪音直接标 seen，不入库不判断
        state[t["doc_id"]] = {"hash": t["content_hash"], "priority": None,
                              "seen_at": now_iso(), "title": t["title"]}

    # ---- stage-1 标题筛（可选；抓 JD 前先淘汰明显不合的岗位，省 Firecrawl 抓取 + 全量判级）----
    # 默认关闭；config.screen.enabled=true 时启用。fail-open：筛选故障不误杀岗位。
    screen_max = int((CONFIG.get("screen") or {}).get("max_per_run", 60))
    survivors, screened_out, screen_usage = screen_titles(candidates[:screen_max])
    candidates = survivors + candidates[screen_max:]
    summary["screened_out"] = len(screened_out)
    if screen_usage:
        summary["screen_usage"] = screen_usage
    for t in screened_out:  # 标题筛淘汰的直接标 seen，不抓 JD 不判级
        state[t["doc_id"]] = {"hash": t["content_hash"], "priority": None,
                              "seen_at": now_iso(), "title": t["title"], "screened": True}

    cap = CONFIG["judge"]["bootstrap_max"] if bootstrap else CONFIG["judge"]["max_per_run"]
    batch, overflow = candidates[:cap], candidates[cap:]
    if bootstrap:  # 首轮：溢出的候选也直接标 seen（历史存量，不值得逐个判）
        for t in overflow:
            state[t["doc_id"]] = {"hash": t["content_hash"], "priority": None,
                                  "seen_at": now_iso(), "title": t["title"]}

    # ---- agent 判级模式：把待判清单交给被唤醒的 agent（它就是用户配置的 LLM）----
    if judge_mode() == "agent":
        from enrich_jd import fetch_jd
        pending = []
        for item in batch:
            jd_text, jd_tool = fetch_jd(item["detail_url"]) if item.get("detail_url") else ("", "none")
            pending.append({"item": item, "jd_text": jd_text, "jd_tool": jd_tool})
        PENDING_FILE.parent.mkdir(exist_ok=True)
        PENDING_FILE.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in pending))
        summary["pending_judgment"] = len(pending)
        save_state(state)  # 只固化噪音/溢出；待判项不标 seen，直到 apply_judgments
        summary["backlog"] = 0 if bootstrap else len(overflow)
        log_run({"kind": "cycle", **summary})
        return summary

    # ---- api 判级模式：推理 + 行动（逐条处理，失败隔离）----
    kb = get_kb()
    for item in batch:
        j = judge_item(item)  # never raises
        summary["judged"] += 1
        summary[j["priority"]] += 1

        # 行动 1：入库（P1/P2/P3 全部沉淀）
        fname = f"{datetime.now():%Y%m%d}-{slug(item['company'])}-{slug(item['title'])}-{j['priority']}-{item['doc_id'].split(':')[-1][-6:]}.md"
        try:
            kb.upload_doc(fname, render_doc(item, j))
            summary["uploaded"] += 1
        except Exception as e:  # noqa: BLE001
            summary["errors"].append({"stage": "ingest", "doc_id": item["doc_id"],
                                      "error": str(e)[:300]})

        # 行动 2：分级通知
        try:
            if j["priority"] == "P1":
                if notify_mode() == "telegram":
                    from notify_telegram import send_p1
                    send_p1(item, j)
                else:
                    from notify_telegram import render_p1_plain
                    append_outbox("p1", render_p1_plain(item, j),
                                  {"doc_id": item["doc_id"]})
                summary["notified"] += 1
            elif j["priority"] == "P2":
                append_queue({"ts": now_iso(), "item": {k: item[k] for k in
                              ("company", "title", "location", "detail_url", "source", "doc_id")},
                              "judgment": {k: j[k] for k in
                              ("priority", "match", "summary_zh", "tags", "reasons", "visa_risk")}})
        except Exception as e:  # noqa: BLE001
            summary["errors"].append({"stage": "notify", "doc_id": item["doc_id"],
                                      "error": str(e)[:300]})

        # 处理完成才标 seen（幂等）
        state[item["doc_id"]] = {"hash": item["content_hash"], "priority": j["priority"],
                                 "seen_at": now_iso(), "title": item["title"],
                                 "event": item["event"]}

    save_state(state)
    summary["backlog"] = 0 if bootstrap else len(overflow)
    summary["ok"] = not any(e.get("stage") == "fetch" for e in summary["errors"])
    log_run({"kind": "cycle", **summary})
    return summary


if __name__ == "__main__":
    s = run_once()
    json.dump(s, sys.stdout, ensure_ascii=False, indent=1)
    sys.exit(0 if s["ok"] else 1)
