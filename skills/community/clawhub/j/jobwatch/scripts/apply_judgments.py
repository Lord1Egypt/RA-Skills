#!/usr/bin/env python3
"""agent 判级模式的「行动」半程：应用 agent 写下的判级结果。

输入：queue/pending_judgment.jsonl（pipeline 产出的待判清单，含 JD 全文）
      queue/judgments.jsonl（agent 逐条写下的判级，严格 JSON 行：
        {"doc_id","match","visa_risk","summary_zh","tags","reasons"}）
动作：schema 校验（script 兜底）→ P1/P2/P3 映射 → 入库 → 通知/入队 → 标记 seen。
缺判级的条目保留待判状态，下轮重新出现——漏判不静默丢失。
"""
import json
import sys
from datetime import datetime

from common import (JUDGMENTS_FILE, PENDING_FILE, append_outbox, append_queue,
                    load_state, log_run, notify_mode, now_iso, save_state, slug)
from judge import to_priority
from kb import get_kb
from pipeline import render_doc

VALID_MATCH = {"kill_shot", "comfort_zone", "wrong_scene", "judgment_failed"}


def load_jsonl(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def main():
    pending = {x["item"]["doc_id"]: x for x in load_jsonl(PENDING_FILE)}
    judgments = {}
    invalid = 0
    for j in load_jsonl(JUDGMENTS_FILE):
        if (isinstance(j, dict) and j.get("doc_id") in pending
                and j.get("match") in VALID_MATCH and j.get("summary_zh")):
            judgments[j["doc_id"]] = j
        else:
            invalid += 1

    state = load_state()
    kb = get_kb()
    summary = {"applied": 0, "P1": 0, "P2": 0, "P3": 0, "uploaded": 0,
               "notified": 0, "left_pending": 0, "invalid": invalid, "errors": []}

    for doc_id, entry in pending.items():
        j = judgments.get(doc_id)
        if j is None:
            summary["left_pending"] += 1
            continue
        item = entry["item"]
        jd = {"priority": to_priority(j["match"], j.get("visa_risk", "unknown")),
              "match": j["match"], "visa_risk": j.get("visa_risk", "unknown"),
              "summary_zh": j["summary_zh"], "tags": j.get("tags", []),
              "reasons": j.get("reasons", ""), "judged_by": "agent",
              "jd_tool": entry.get("jd_tool", ""), "jd_text": entry.get("jd_text", "")}
        summary["applied"] += 1
        summary[jd["priority"]] += 1

        fname = f"{datetime.now():%Y%m%d}-{slug(item['company'])}-{slug(item['title'])}-{jd['priority']}-{item['doc_id'].split(':')[-1][-6:]}.md"
        try:
            kb.upload_doc(fname, render_doc(item, jd))
            summary["uploaded"] += 1
        except Exception as e:  # noqa: BLE001
            summary["errors"].append({"stage": "ingest", "doc_id": doc_id, "error": str(e)[:300]})

        try:
            if jd["priority"] == "P1":
                if notify_mode() == "telegram":
                    from notify_telegram import send_p1
                    send_p1(item, jd)
                else:
                    from notify_telegram import render_p1_plain
                    append_outbox("p1", render_p1_plain(item, jd), {"doc_id": doc_id})
                summary["notified"] += 1
            elif jd["priority"] == "P2":
                append_queue({"ts": now_iso(),
                              "item": {k: item[k] for k in ("company", "title", "location",
                                                            "detail_url", "source", "doc_id")},
                              "judgment": {k: jd[k] for k in ("priority", "match", "summary_zh",
                                                              "tags", "reasons", "visa_risk")}})
        except Exception as e:  # noqa: BLE001
            summary["errors"].append({"stage": "notify", "doc_id": doc_id, "error": str(e)[:300]})

        state[doc_id] = {"hash": item["content_hash"], "priority": jd["priority"],
                         "seen_at": now_iso(), "title": item["title"],
                         "event": item.get("event", "new")}

    save_state(state)
    # 已应用的从 pending 清掉；漏判的保留（下轮 pipeline 会重新生成清单）
    PENDING_FILE.write_text("\n".join(
        json.dumps(x, ensure_ascii=False) for x in pending.values()
        if x["item"]["doc_id"] not in judgments))
    JUDGMENTS_FILE.write_text("")
    log_run({"kind": "apply", **summary})
    return summary


if __name__ == "__main__":
    s = main()
    json.dump(s, sys.stdout, ensure_ascii=False, indent=1)
    sys.exit(0)
