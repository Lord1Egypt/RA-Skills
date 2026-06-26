#!/usr/bin/env python3
"""Idempotent PPT task creator + poller. Exit: 0=SUBMITTED/DONE  2=PENDING  1=FAILED"""

import argparse, io, json, os, shutil, sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def _utf8_stdio():
    for a in ("stdout", "stderr"):
        s = getattr(sys, a)
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
        elif hasattr(s, "buffer"):
            setattr(sys, a, io.TextIOWrapper(s.buffer, encoding="utf-8", errors="replace", line_buffering=True))
_utf8_stdio()

from http_client import SkillHttpClient, SkillHttpError  # noqa: E402

BASE_URL     = "https://kejian365.com/api"
PPT_VIEW_URL = "https://kejian365.com/tdh-portal/#/pptSharePreView?pptId={ppt_id}&shareUser=1"
_STATE  = "task_state.json"
_PARAMS = "params.json"
_LOG    = "task.log"


def _now():  return datetime.now(timezone.utc).isoformat()
def _ts():   return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def _log(wd, msg):
    try:
        with open(os.path.join(wd, _LOG), "a", encoding="utf-8") as f:
            f.write(f"[{_ts()}] {msg}\n")
    except Exception: pass

def _load(path):
    if not os.path.exists(path): return None
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f: return json.load(f)
    except Exception: return None

def _save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_state(wd):  return _load(os.path.join(wd, _STATE))
def save_state(wd, s):
    s["updated_at"] = _now()
    _save(os.path.join(wd, _STATE), s)

def load_params(wd, pf):
    return _load(pf) if (pf and os.path.exists(pf)) else _load(os.path.join(wd, _PARAMS))


def api_create(params, token):
    for required in ("topic", "themeId", "outline"):
        if not params.get(required):
            return None, f"缺少必填参数: {required}", {}
    client = SkillHttpClient(auth_token=token, timeout=60)
    body = {k: params[k] for k in ("topic", "themeId", "outline")}
    for k in ("requirements", "material", "themeConfig", "illustrationMode", "generateType"):
        if k in params: body[k] = params[k]
    raw = client.post(f"{BASE_URL}/aippt/v1/skill/task/create", body)
    if not (raw.get("data") or {}).get("created"):
        return None, raw.get("rspDesc", "任务创建失败"), raw
    return (raw["data"] or {}).get("ppt_id", ""), "", raw

def api_status(ppt_id, token):
    return SkillHttpClient(auth_token=token, timeout=30).get(
        f"{BASE_URL}/aippt/v1/skill/ppt/{ppt_id}/status")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--params-file", default=None)
    p.add_argument("--work-dir",    required=True)
    args = p.parse_args()
    wd = args.work_dir
    Path(wd).mkdir(parents=True, exist_ok=True)

    state  = load_state(wd)
    params = load_params(wd, args.params_file)

    if args.params_file and os.path.exists(args.params_file):
        dest = os.path.join(wd, _PARAMS)
        if not os.path.exists(dest): shutil.copy2(args.params_file, dest)

    token = ((params or {}).get("authToken") or (state or {}).get("auth_token")
            or os.environ.get("KEJIAN365_AUTH_TOKEN"))
    if not token:
        print("ERROR: 缺少账号凭证", flush=True); sys.exit(1)

    # ── A: Create or retry ────────────────────────────────────────────────────
    if state is None or state.get("status") == "CREATE_FAILED":
        if not params:
            print("ERROR: 缺少任务参数", flush=True); sys.exit(1)
        _log(wd, f"创建任务: {params.get('topic')!r}")
        try:
            ppt_id, err, raw = api_create(params, token)
        except SkillHttpError as e:
            save_state(wd, {"status": "CREATE_FAILED", "error": str(e)})
            print("FAILED: 网络请求失败", flush=True)
            print(f"错误:   {e}", flush=True); sys.exit(1)

        if not ppt_id:
            save_state(wd, {"status": "CREATE_FAILED", "error": err})
            billing = (raw.get("data") or {}).get("billing_info") or {}
            if billing and not billing.get("success"):
                print("FAILED: 余额不足", flush=True)
            else:
                print("FAILED: 任务创建失败", flush=True)
            print(f"错误:   {err}", flush=True); sys.exit(1)

        view_url = PPT_VIEW_URL.format(ppt_id=ppt_id)
        _log(wd, f"创建成功: ppt_id={ppt_id}")
        save_state(wd, {"status": "PENDING", "ppt_id": ppt_id, "topic": params.get("topic", ""),
                        "view_url": view_url, "auth_token": token, "created_at": _now()})
        print("SUBMITTED: PPT 生成任务已创建", flush=True)
        print(f"主题:     {params.get('topic', '')}", flush=True)
        print(f"查看链接: {view_url}", flush=True)
        print("提示:     生成需要 5–15 分钟，请稍后查询进度", flush=True)
        sys.exit(0)

    # ── B: Terminal states ────────────────────────────────────────────────────
    ppt_id   = state.get("ppt_id", "")
    view_url = state.get("view_url") or (PPT_VIEW_URL.format(ppt_id=ppt_id) if ppt_id else "")
    status   = state.get("status", "")
    token    = token or state.get("auth_token", "")

    if status == "DONE":
        print("DONE: PPT 已生成完成", flush=True)
        print(f"主题:     {state.get('topic', '')}", flush=True)
        print(f"页数:     {state.get('total_pages', '?')} 页", flush=True)
        print(f"查看链接: {view_url}", flush=True)
        sys.exit(0)

    if status == "GENERATION_FAILED":
        print("FAILED: PPT 生成失败", flush=True)
        print(f"错误:   {state.get('error', '未知错误')}", flush=True)
        print("提示:   [INTERNAL] 删除 task_state.json 后重新运行可重试", flush=True)
        sys.exit(1)

    if not ppt_id:
        print("ERROR: 状态异常，缺少 ppt_id", flush=True)
        print("提示:   [INTERNAL] 删除 task_state.json 后重新运行", flush=True)
        sys.exit(1)

    # ── C: Poll ───────────────────────────────────────────────────────────────
    _log(wd, f"轮询: ppt_id={ppt_id}")
    try:
        result = api_status(ppt_id, token)
    except SkillHttpError as e:
        _log(wd, f"轮询失败: {e}")
        print("PENDING: 暂时无法获取进度，稍后重试", flush=True)
        sys.exit(2)

    if result.get("rspCode") != "0000":
        rsp_desc = result.get("rspDesc", "查询失败")
        _log(wd, f"轮询接口错误: {rsp_desc}")
        print(f"ERROR: {rsp_desc}", flush=True); sys.exit(1)

    data   = result.get("data") or {}
    api_st = data.get("status", "unknown")

    # Page progress from generate_pages step nodes (progress.total = step count, not pages)
    steps   = data.get("steps") or []
    pg_step = next((s for s in steps if s.get("stepId") == "generate_pages"), None)
    if pg_step and pg_step.get("nodes"):
        nodes  = pg_step["nodes"]
        p_tot  = len(nodes)
        p_done = sum(1 for n in nodes if n.get("status") == "completed")
    else:
        p_tot, p_done = "?", 0

    # Final page count from variables.页面列表 (actual output)
    page_list   = (data.get("variables") or {}).get("页面列表") or []
    final_pages = len(page_list) if page_list else p_tot

    _log(wd, f"status={api_st} pages={p_done}/{p_tot} final={final_pages}")

    if api_st == "completed":
        save_state(wd, {**state, "status": "DONE", "total_pages": final_pages, "completed_at": _now()})
        print("DONE: PPT 已生成完成", flush=True)
        print(f"主题:     {state.get('topic', '')}", flush=True)
        print(f"页数:     {final_pages} 页", flush=True)
        print(f"查看链接: {view_url}", flush=True)
        sys.exit(0)

    if api_st == "failed":
        err = data.get("error") or "未知错误"
        save_state(wd, {**state, "status": "GENERATION_FAILED", "error": err})
        print("FAILED: PPT 生成失败", flush=True)
        print(f"错误:   {err}", flush=True)
        print("提示:   [INTERNAL] 删除 task_state.json 后重新运行可重试", flush=True)
        sys.exit(1)

    if api_st == "cancelled":
        save_state(wd, {**state, "status": "GENERATION_FAILED", "error": "任务已取消"})
        print("FAILED: PPT 生成任务已取消", flush=True)
        print("提示:   [INTERNAL] 删除 task_state.json 后重新运行可重试", flush=True)
        sys.exit(1)

    # Still running
    save_state(wd, {**state, "status": api_st.upper(), "last_checked_at": _now(),
                    "pages_completed": p_done, "pages_total": p_tot})
    if pg_step and p_tot != "?":
        print(f"PENDING: 生成中，已完成 {p_done}/{p_tot} 页", flush=True)
    else:
        print("PENDING: 准备中，即将开始生成页面", flush=True)
    print(f"主题:     {state.get('topic', '')}", flush=True)
    print(f"进度:     {p_done}/{p_tot} 页已完成", flush=True)
    print(f"查看链接: {view_url}", flush=True)
    sys.exit(2)


if __name__ == "__main__":
    main()
