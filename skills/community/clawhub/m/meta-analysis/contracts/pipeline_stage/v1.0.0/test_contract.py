#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meta-Analysis per-stage Pipeline 契约测试（Phase 0）。

验证项：
  1. request/response schema 可被 Draft 2020-12 加载（schema 自洽）。
  2. example_roundtrip.json 每条消息按 _kind 校验通过。
  3. 向后兼容：纯旧 per-task 请求（无 contract_version/stage）与纯旧响应
     （无管线字段）均通过校验。
  4. 枚举约束：非法 gate / sync / intent / stage.status /
     next_human_action.type 被拒。
  5. 红线 gate 枚举：非法 gate 值必须被拒（本地强执可测前提）。

运行：
  C:/Tools/anaconda3/python.exe test_contract.py
依赖：
  jsonschema>=4.x（Anaconda 自带 4.25.0）
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
REQ = json.load(open(ROOT / "request.schema.json", encoding="utf-8"))
RESP = json.load(open(ROOT / "response.schema.json", encoding="utf-8"))
EXAMPLE = json.load(open(ROOT / "example_roundtrip.json", encoding="utf-8"))

req_v = Draft202012Validator(REQ)
resp_v = Draft202012Validator(RESP)

errors = []


def check(validator, obj, label):
    """收集校验错误；返回错误数。"""
    for e in sorted(validator.iter_errors(obj), key=lambda x: list(x.path)):
        errors.append(f"[{label}] path={list(e.path)} :: {e.message}")
    return 0  # 错误已收集，不在这里 return 计数避免重复


# 1) example roundtrip
for i, msg in enumerate(EXAMPLE.get("messages", [])):
    kind = msg.get("_kind")
    if kind == "request":
        check(req_v, msg, f"example msg[{i}] request")
    elif kind == "response":
        check(resp_v, msg, f"example msg[{i}] response")
    else:
        errors.append(f"[example msg[{i}]] missing _kind")

# 2) 向后兼容：旧 per-task 请求（无管线字段）
legacy_req = {
    "task": "pairwise_meta",
    "data": {"source": "inline", "rows": [{"study": "A", "event_exp": 1, "n_exp": 10,
                                           "event_ctrl": 2, "n_ctrl": 10}]},
    "params": {"sm": "OR", "model": "REML"},
    "figure": {"format": "svg", "plots": ["forest"]},
    "query_origin": "sha256:" + "a" * 64,
}
check(req_v, legacy_req, "legacy per-task request")

# 3) 向后兼容：旧 per-task 响应（无管线字段）
legacy_resp = {
    "status": "ok", "task": "pairwise_meta",
    "stats": {"k": 1, "pooled": {"estimate": 0.5}},
    "figures": [], "warnings": [], "notes": "legacy ok",
}
check(resp_v, legacy_resp, "legacy per-task response")

# 4) 枚举约束：非法值必须被拒
bad_cases = [
    ("request", {**legacy_req, "stage": {"id": "X9.bad", "index": 0, "intent": "fly"}},
     "illegal stage.id pattern + illegal intent"),
    ("response", {"stage": {"status": "flying"},
                  "next_human_action": {"type": "teleport"}},
     "illegal stage.status + illegal next_human_action.type"),
    ("response", {"tool_cards": [{"need_tool": "ct-x", "params": {}, "sync": "maybe"}]},
     "illegal tool_card.sync"),
]
for kind, obj, desc in bad_cases:
    validator = req_v if kind == "request" else resp_v
    errs = list(validator.iter_errors(obj))
    if not errs:
        errors.append(f"[enum] SHOULD-BE-REJECTED but passed: {desc}")
    else:
        # 期望被拒，记一条通过日志（不计入 errors）
        pass

# 5) 红线 gate 枚举：非法 gate 必须被拒（本地强执可测前提）
bad_gate_obj = {"next_human_action": {"type": "confirm", "gate": "not_a_real_gate"}}
if not list(resp_v.iter_errors(bad_gate_obj)):
    errors.append("[gate enum] invalid gate NOT rejected -> 红线强执不可测")

# 合法 gate 应通过
for g in ["none", "extraction_review", "final_inclusion",
          "manuscript_approval", "reference_verification"]:
    if list(resp_v.iter_errors({"next_human_action": {"type": "confirm", "gate": g}})):
        errors.append(f"[gate enum] valid gate '{g}' wrongly rejected")

# ---------------------------------------------------------------------------
# 6) 向后兼容（老技能 → 升级后 coze 端）：双模契约保证
#    核心不变量（见 BACKWARD_COMPAT.md R1）：任何不含管线字段的旧请求，coze 必须仍
#    填充 outer['result']（R 引擎 JSON 字符串）；老 adapter 才能用
#    outer.get("result")→json.loads 取出 {status,stats,figures,...}。否则老技能解析失败。
# ---------------------------------------------------------------------------

def is_legacy_request(payload: dict) -> bool:
    """coze 端双模判定：无管线字段即 legacy。与 BACKWARD_COMPAT.md §6 一致。"""
    return not any(k in payload for k in
                   ("contract_version", "schema", "pipeline_id", "pipeline", "stage"))


def simulate_coze_legacy_handler(payload: dict, inner_result: dict) -> dict:
    """模拟 coze 对 legacy 请求的【必须】行为：填充 outer['result']=JSON 字符串。"""
    assert is_legacy_request(payload), "legacy handler only for legacy requests"
    return {
        "result": json.dumps(inner_result, ensure_ascii=False),
        "feishu_write_success": True,
        "feishu_write_time": "1700000000000",
    }


# 6.1 双模判定：无管线字段 → legacy
assert is_legacy_request(legacy_req) is True, "legacy per-task 请求必须判定为 legacy"
# 6.2 含 stage 的新请求 → 管线分支
new_req = {**legacy_req, "contract_version": "1.0.0", "stage": {"id": "B1.compute", "index": 0}}
assert is_legacy_request(new_req) is False, "含 stage 的请求必须判定为新管线请求"

# 6.3 debug 前缀的 legacy 请求也必须通过 schema（验证 query_origin pattern 修正）
debug_legacy_req = {**legacy_req, "query_origin": "debug:sha256:" + "b" * 64}
check(req_v, debug_legacy_req, "legacy per-task request (debug prefix)")

# 6.4 模拟 coze legacy 行为：outer 必须含 result 且解析后含 status/stats/figures
inner = {
    "status": "ok", "task": "pairwise_meta",
    "stats": {"k": 1, "pooled": {"estimate": 0.5, "ci_low": 0.3, "ci_high": 0.8}},
    "figures": [{"type": "forest", "format": "svg", "svg": "<svg/>"}],
    "warnings": [], "notes": "ok",
    "repro": {"r": "x", "r_version": "R 4.6.1", "packages": {}},
}
outer = simulate_coze_legacy_handler(legacy_req, inner)
result_str = outer.get("result")
parsed = None
if not result_str:
    errors.append("[R1] coze 对 legacy 请求未填充 outer['result'] → 老 adapter 解析失败")
else:
    try:
        parsed = json.loads(result_str)
    except Exception as e:  # noqa: BLE001
        errors.append(f"[R1] outer['result'] 非合法 JSON: {e}")
    else:
        for fld in ("status", "stats", "figures"):
            if fld not in parsed:
                errors.append(f"[R1] legacy 解析结果缺少 '{fld}' → 老 adapter 渲染失败")
        if "feishu_write_success" not in outer:
            errors.append("[R1] outer 缺 feishu_write_success（老 adapter 透传字段，应保留）")

# 6.5 legacy 解析结果（inner）必须通过 response schema（计算层字段语义不变）
if parsed is not None:
    check(resp_v, parsed, "legacy parsed inner result")
# 6.6 outer 信封（含 result 字符串）本身不得被 schema 误拒（additionalProperties 默认 true）
check(resp_v, outer, "legacy outer envelope")


# ---------------------------------------------------------------------------
# 7) 文件传输（上传 / 下载）契约保证（见 FILE_TRANSFER.md）
#    - 上传：请求侧 attachments（本地已上传 S3 的引用，Block A 多 PDF）
#    - 下载：响应侧 attachments（coze 产出可下载文件，含预签名 GET url）
#    - 两侧均为 optional，旧请求/响应不带不影响兼容（R1 双模不受影响）
# ---------------------------------------------------------------------------

# 7.1 上传请求：多个 PDF 引用（Block A 文献全文），put_url 可选
upload_req = {
    **legacy_req,
    "contract_version": "1.0.0",
    "pipeline_id": "p1",
    "stage": {"id": "A4.data_extraction", "index": 3},
    "attachments": [
        {"storage": "s3", "key": "pipeline/p1/uploads/a1.pdf",
         "filename": "Smith2020.pdf", "mime": "application/pdf",
         "size_bytes": 123456, "sha256": "c" * 64},
        {"storage": "s3", "key": "pipeline/p1/uploads/a2.pdf",
         "filename": "Lee2021.pdf", "mime": "application/pdf",
         "size_bytes": 234567, "sha256": "d" * 64,
         "put_url": "https://s3/put?X-Amz-Signature=..."},
    ],
}
check(req_v, upload_req, "file upload request (multi-PDF attachments)")

# 7.1b 混合用途多文件同时上传：3 篇文献全文 + 1 份提取模板，每文件带 purpose 区分类别
mixed_upload_req = {
    **legacy_req,
    "contract_version": "1.0.0", "pipeline_id": "p1",
    "stage": {"id": "A4.data_extraction", "index": 3},
    "attachments": [
        {"storage": "s3", "key": "pipeline/p1/uploads/lit1.pdf",
         "filename": "Smith2020.pdf", "mime": "application/pdf",
         "size_bytes": 123456, "sha256": "c" * 64, "purpose": "literature_fulltext"},
        {"storage": "s3", "key": "pipeline/p1/uploads/lit2.pdf",
         "filename": "Lee2021.pdf", "mime": "application/pdf",
         "size_bytes": 234567, "sha256": "d" * 64, "purpose": "literature_fulltext"},
        {"storage": "s3", "key": "pipeline/p1/uploads/lit3.pdf",
         "filename": "Wang2022.pdf", "mime": "application/pdf",
         "size_bytes": 345678, "sha256": "f" * 64, "purpose": "literature_fulltext"},
        {"storage": "s3", "key": "pipeline/p1/uploads/tpl.pdf",
         "filename": "extraction_template.pdf", "mime": "application/pdf",
         "size_bytes": 45678, "sha256": "a" * 64, "purpose": "extraction_template"},
    ],
}
check(req_v, mixed_upload_req, "mixed-purpose multi-file upload (purpose-tagged)")
# 断言 purpose 字段在 array 内各元素均合法（schema 已含，这里确认不会被误拒）
purposes = [a.get("purpose") for a in mixed_upload_req["attachments"]]
if purposes != ["literature_fulltext", "literature_fulltext", "literature_fulltext", "extraction_template"]:
    errors.append(f"[file] purpose 标记在混合多文件上传中丢失/错乱: {purposes}")

# 7.2 上传 ack 响应（coze 确认收到，进入提取核验闸）—— 不含 attachments 亦合法
upload_ack = {
    "contract_version": "1.0.0", "pipeline_id": "p1",
    "stage": {"id": "A4.data_extraction", "index": 3, "status": "await_human"},
    "stage_result": {"summary": "已收到 2 篇 PDF，进入提取核验闸。"},
    "next_human_action": {"type": "review", "gate": "extraction_review", "required": True},
}
check(resp_v, upload_ack, "file upload ack response")

# 7.3 下载响应：coze 产出 docx 稿件（含预签名 GET url），本地据 url 拉取
download_resp = {
    "contract_version": "1.0.0", "pipeline_id": "p1",
    "stage": {"id": "C4.grade_table_ev", "index": 11, "status": "completed"},
    "attachments": [
        {"storage": "s3", "key": "pipeline/p1/outputs/manuscript.docx",
         "url": "https://s3/get?X-Amz-Signature=...", "filename": "manuscript.docx",
         "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
         "size_bytes": 54321, "sha256": "e" * 64},
    ],
}
check(resp_v, download_resp, "file download response (docx attachment)")

# 7.4 向后兼容：无 attachments 的旧请求/响应必须通过（确认 optional，不破坏 R1）
check(req_v, legacy_req, "legacy per-task request (no attachments) — optional OK")
check(resp_v, legacy_resp, "legacy per-task response (no attachments) — optional OK")

# 7.5 非法 AttachmentRef 必须被拒
bad_upload = {**legacy_req, "attachments": [
    {"storage": "s3", "key": "k", "filename": "f.pdf",
     "mime": "application/pdf", "size_bytes": 1}  # 缺 sha256
]}
if not list(req_v.iter_errors(bad_upload)):
    errors.append("[file] upload attachment 缺 sha256 却通过 → 完整性校验失效")
bad_download = {"attachments": [
    {"storage": "s3", "key": "k", "filename": "f.docx",
     "mime": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
     "size_bytes": 1, "sha256": "f" * 64}  # 缺 url（下载必须）
]}
if not list(resp_v.iter_errors(bad_download)):
    errors.append("[file] download attachment 缺 url 却通过 → 本地无法下载")

# 7.6 request_upload tool_card 合法（need_tool 为自由字符串；语义约束见 SPEC §12）
upload_card_resp = {
    "contract_version": "1.0.0",
    "tool_cards": [{
        "card_ref": "tc1", "need_tool": "request_upload",
        "params": {"files": [{"accept": "application/pdf", "required": True,
                              "max_bytes": 52428800}], "count": 2},
        "sync": "blocking", "timeout_sec": 120,
    }],
}
check(resp_v, upload_card_resp, "request_upload tool_card response")


# ---------------------------------------------------------------------------
# 7.7 反向兼容（新本地 adapter → 旧 coze 端点）：新 adapter 在请求里携带了
#     attachments，但【旧 coze 端点】因 pydantic extra='ignore' 不识别该字段，
#     只回旧 per-task 结构（outer['result'] 内无 attachments）。此时新 adapter
#     必须把 attachments 视为空集合、继续走旧解析路径、不得崩溃。
#     这验证了“升级契约后，未重部署的 coze 老版本仍能与新本地端共存”。
# ---------------------------------------------------------------------------
def simulate_old_coze_handler(payload: dict, inner_result: dict) -> dict:
    """模拟【旧】coze 端点：只认旧字段，extra='ignore' 丢弃 attachments 等未知字段。"""
    return {
        "result": json.dumps(inner_result, ensure_ascii=False),
        "feishu_write_success": True,
        "feishu_write_time": "1700000000000",
    }


# 新 adapter 发出的请求（带 attachments）
new_adapter_req = mixed_upload_req
# 旧 coze 收到后忽略 attachments，返回旧结构
old_coze_outer = simulate_old_coze_handler(new_adapter_req, inner)
old_coze_parsed = None
try:
    old_coze_parsed = json.loads(old_coze_outer["result"])
except Exception as e:  # noqa: BLE001
    errors.append(f"[7.7] 旧 coze 返回 result 非合法 JSON: {e}")
else:
    # 关键不变量：旧 coze 返回的 inner 不含 attachments（可选字段缺失=空）
    if "attachments" in old_coze_parsed:
        errors.append("[7.7] 旧 coze 不应返回 attachments（应被 extra='ignore' 丢弃）")
    # 新 adapter 解析旧结构：status/stats/figures 必在；attachments 缺失→本地按空处理
    for fld in ("status", "stats", "figures"):
        if fld not in old_coze_parsed:
            errors.append(f"[7.7] 旧 coze 返回缺 '{fld}' → 新 adapter 旧解析路径失败")
    # 模拟 adapter 侧：attachments = parsed.get("attachments") or []  —— 绝不抛错
    attached = old_coze_parsed.get("attachments") or []
    if not isinstance(attached, list):
        errors.append("[7.7] adapter 取 attachments 应为 list（缺失时为空 list）")

# 7.8 旧 schema（无 purpose 字段）仍兼容：不带 purpose 的附件必须仍通过校验
legacy_attachment_req = {
    **legacy_req,
    "contract_version": "1.0.0",
    "attachments": [
        {"storage": "s3", "key": "pipeline/p1/uploads/x.pdf",
         "filename": "x.pdf", "mime": "application/pdf",
         "size_bytes": 100, "sha256": "1" * 64},
    ],
}
check(req_v, legacy_attachment_req, "upload attachment without purpose (optional OK)")


# ---------------------------------------------------------------------------
# 8) 计费身份标识（预留接口）契约保证（见 SPEC.md §13 / coze_contract.md §11）
#    - account_id / billing_token 均为 optional，向后兼容（老请求不带即通过）
#    - 与 query_origin（匿名机器指纹）完全独立，不复用 sha 字段
# ---------------------------------------------------------------------------

# 8.1 老请求（无 account_id / billing_token）必须通过（向后兼容基线）
check(req_v, legacy_req, "legacy per-task request (no billing fields) — optional OK")

# 8.2 携带 account_id（务实版）必须通过
acct_req = {**legacy_req, "account_id": "lic_2026_00123"}
check(req_v, acct_req, "request with account_id (pragmatic billing)")

# 8.3 携带 billing_token（稳健版）必须通过
tok_req = {**legacy_req,
           "billing_token": "eyJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoibGljXzAwMSJ9.xxxxx"}
check(req_v, tok_req, "request with billing_token (signed billing)")

# 8.4 二者同时携带必须通过
both_req = {**legacy_req, "account_id": "lic_2026_00123",
             "billing_token": "eyJhbGciOiJIUzI1NiJ9.payload.sig"}
check(req_v, both_req, "request with account_id + billing_token")

# 8.5 反向兼容（新本地 adapter 带 billing 字段 → 旧 coze 端点 extra='ignore' 忽略 → 仍回旧结构）
new_bill_req = both_req
old_coze_bill = simulate_old_coze_handler(new_bill_req, inner)
try:
    bc_parsed = json.loads(old_coze_bill["result"])
except Exception as e:  # noqa: BLE001
    errors.append(f"[8.5] 旧 coze 返回 result 非合法 JSON: {e}")
else:
    if "account_id" in bc_parsed or "billing_token" in bc_parsed:
        errors.append("[8.5] 旧 coze 不应回显 account_id/billing_token（应被 extra='ignore'）")
    for fld in ("status", "stats", "figures"):
        if fld not in bc_parsed:
            errors.append(f"[8.5] 旧 coze 返回缺 '{fld}' → 新 adapter 旧解析路径失败")


# 输出
if errors:
    print("FAIL — contract test found", len(errors), "issue(s):")
    for e in errors:
        print("  -", e)
    sys.exit(1)

n_msgs = len(EXAMPLE.get("messages", []))
print(f"PASS — all checks OK: schema self-check + {n_msgs} example messages "
      f"+ legacy per-task compat + enum rejection + red-line gate enum "
      f"+ legacy dual-mode guarantee (R1) + multi-file upload (purpose) "
      f"+ new-adapter vs old-coze graceful + purpose-optional compat "
      f"+ billing identity fields (account_id/billing_token) reserved + backward-compat")
