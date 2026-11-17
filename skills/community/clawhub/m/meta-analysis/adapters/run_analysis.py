"""
adapters/run_analysis.py — 元分析统一调用入口（coze 唯一路径）

默认行为（coze-only）：
  调用 coze 工作流（adapters/coze_client.run_meta）完成 R 计算。
  - 认证未授权（AuthRequiredError）→ 返回明确提示，不绕过 ct-base §5 授权门控、不回退本地。
  - coze 调用失败 → 返回结构化错误（含 coze 错误原文），不再本地兜底。

本地 R 引擎（原 adapters/local_engine.py）自 2026-08-26 起已从主路径移除；
adapters/_dev/local_engine.py（调试用残留）已于 2026-09-01 按架构终态原则删除
（原则：coze 为唯一计算真相源，本地不保留计算引擎）。run_analysis 仅走 coze，绝不回退本地。

返回结果统一带 `_source` 字段：
  "coze"         — 由 coze 工作流产出
  "auth_blocked" — 未授权出站，未使用云端分析
  "coze_error"   — coze 调用失败

CLI：
  python adapters/run_analysis.py <request.json>
  request.json = {"task":..., "data":..., "params":..., "figure":...}
"""

import os
import sys
import json
import time
import uuid

# 让 coze_client / rendering 可被直接 import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from coze_client import run_stage as _coze_run_stage
from coze_client import AuthRequiredError
from coze_client import EnvelopeValidationError as _EnvelopeValidationError
from coze_client import CONTRACT_VERSION as _CONTRACT_VERSION
from coze_client import STAGE_SCHEMA_ID as _STAGE_SCHEMA_ID
# 2026-08-29：归因标识计算统一收敛到 coze_client（单一实现），避免两处逻辑漂移。
from coze_client import _default_query_origin as _coze_default_origin
from rendering import svg_to_png, render_html_report
# 2026-09-13：coze 返回 error 时的针对性诊断（HTTP 200 ≠ 任务成功，对齐 LRN-20260817-002）。
from coze_error_analyze import analyze_coze_error as _analyze_coze_error
from coze_error_analyze import render_error_analysis as _render_error_analysis
from interpretation import interpret_result as _interpret_result
from quality_advice import evaluate_quality as _evaluate_quality
# 2026-09-13：出站信封被拦截时，复用校验器的指导渲染（envelope_invalid 分支回传 _error_guidance）。
from coze_contract_validate import render_guidance as _render_contract_guidance

# 渲染计时阈值（秒）：**本地渲染阶段**（拿到 SVG → 处理 → 界面渲染完成）超过该值，
# 提示用户可切换图片文件模式（PNG 不内联 SVG，界面渲染通常更快）。
# 注意：不是 coze 计算时间（那是 coze_elapsed_seconds，仅诊断参考）。
RENDER_SVG_THRESHOLD = 30.0
# SVG 体量辅助阈值（KB）：单图超过该值即使本地处理快，界面渲染（浏览器解析 + 滚动）
# 也可能明显变慢——一并提示。默认按森林图典型 18KB 的 ~10 倍余量。
RENDER_SVG_KB_THRESHOLD = 200.0


def _check_effect_size_extreme(stats: dict) -> str | None:
    """效应量极端判定（飞书 searchlog 实证：60/281 成功记录效应量极端）。

    返回警告文本（应贴到结果上）或 None（效应量在合理范围）。
    判定阈值：
      - OR/RR/PLO/PLOGIT：estimate_exp > 10 或 < 0.1（真实比值）
      - SMD/MD/ZCOR：|estimate| > 3（标准化均值差）
    """
    if not isinstance(stats, dict):
        return None
    _sm = str(stats.get("sm") or "").upper()
    _pooled = stats.get("pooled") or {}
    _est_e = _pooled.get("estimate_exp")   # 真实比值(OR/RR/PLO)
    _est = _pooled.get("estimate")         # log 比值 或 均值差
    # OR / RR / PLO / PLOGIT：estimate_exp 为真实比值
    if _sm in ("OR", "RR", "PLO", "PLOGIT") and isinstance(_est_e, (int, float)):
        if _est_e > 10:
            return "%s=%.2f (>10)" % (_sm, _est_e)
        if _est_e < 0.1:
            return "%s=%.2f (<0.1)" % (_sm, _est_e)
    # SMD / MD / ZCOR：estimate 为标准化均值差
    if _sm in ("SMD", "MD", "ZCOR") and isinstance(_est, (int, float)):
        if abs(_est) > 3:
            return "%s=%.2f (|d|>3)" % (_sm, _est)
    return None
def run_analysis(task, data, params, figure="forest", out_dir=".", debug=False, advise=False, topic="", field="", references=None, merged_json=None, use_network=True, ref_sections=None):
    """统一分析入口（架构重构 · per-stage pipeline）。

    计算请求构造成 Block B「B1.meta_analysis」阶段信封，经 coze_client.run_stage
    发往 ct-meta2（开发期唯一站点，见 adapters/DEV_POLICY.json），coze 端图引擎
    返回 stage_result + 兼容性 result。无本地 R 兜底——coze 失败 / 未授权时返回
    结构化错误（status=error），与旧 run_meta 路径行为一致（run_stage 是 run_meta 的
    超集：旧 per-task 信封仍自动委派 run_meta，向后兼容）。

    out_dir: HTML 报告输出目录（默认当前工作目录 `.`）；由 run_meta.py 解析后传入，
             确保报告落在用户工作区，而非技能自身目录。
    debug:   同 run_stage，query_origin 带 `debug:` 前缀，隔离测试流量（飞书归因列可筛）。
    """
    # §8.6 query_origin：客户端计算主机名 SHA-256 哈希（"sha256:" + 64hex = 71 字符），
    # 随请求发送，供 coze 端归因/限流；coze 端不得兜底生成（客户端唯一真相源）。
    # 2026-08-29：计算逻辑收敛到 coze_client._default_query_origin。此处仍显式传入
    # 以保留本路径语义；即使不传，run_stage 也会自动填充。
    query_origin = _coze_default_origin()
    env = _build_compute_stage_env(task, data, params, figure, query_origin)
    try:
        res = _coze_run_stage(env, debug=debug)
        res = _normalize_stage(res)
        res["_source"] = "coze"
        # 2026-09-13：coze 返回 error（HTTP 200 但任务未成功）时，附加结构化诊断，
        # 把 notes/warnings 翻译成有针对性的「原因 + 修正动作」，供 agent / CLI 转述用户。
        if isinstance(res, dict) and res.get("status") == "error":
            try:
                _ea = _analyze_coze_error(res)
                if _ea is not None:
                    res["_error_analysis"] = _ea.as_dict()
                    res["_error_guidance"] = _render_error_analysis(_ea)
            except Exception:  # noqa: BLE001 — 诊断失败绝不阻断主结果
                pass
        # 2026-09-13 质量门防御（飞书 searchlog 实证：31/281 成功记录 quality_gate=red
        # 但顶层 status 仍为 ok/warn，消费端只看顶层就会呈现本应阻断的合并效应）。
        # coze 端 run_task.R 第 1433 行顶层 status 仅由 length(warns) 决定，quality_gate
        # 不影响顶层——这是 coze 端 bug（修复标注见 adapters/coze/src/r_engine/run_task.R）。
        # 本地防御：quality_gate=red 时强制标记 _pooled_suppress，渲染层不呈现合并效应。
        try:
            _stats = res.get("stats") or {}
            _qg = _stats.get("quality_gate") or {}
            if isinstance(_qg, dict) and _qg.get("status") == "red":
                res["_pooled_suppress"] = True
                _qg_checks = _qg.get("checks") or []
                _red_msgs = [c.get("message", "") for c in _qg_checks
                             if isinstance(c, dict) and c.get("level") == "red"]
                res["_quality_gate_red_warning"] = (
                    "⚠ 质量门红灯：合并效应不应呈现（%s）。"
                    "详见 stats.quality_gate.checks。" % "; ".join(_red_msgs[:3])
                )
                # 顶层 status 降级：若原为 ok 则改为 warn（让 CLI/渲染层识别）
                if res.get("status") == "ok":
                    res["status"] = "warn"
        except Exception:  # noqa: BLE001
            pass
        # 2026-09-13 效应量极端防御（飞书 searchlog 实证：60/281 成功记录效应量极端）。
        # coze 端已内置 Haldane 自动校正（event+0.5, n+1），无需建议用户手动加 0.5。
        # 极端效应不阻断（可能真实），但顶层 status 降为 warn，并在结果上贴 ⚠ 标记。
        # 不自动重跑——给用户看提示，用户确认后再决定是否切 Peto 法。
        try:
            _extreme_msg = _check_effect_size_extreme(res.get("stats") or {})
            if _extreme_msg:
                if res.get("status") == "ok":
                    res["status"] = "warn"
                res["_effect_size_extreme_warning"] = (
                    "⚠ 效应量极端（%s）：请复核原始数据。"
                    "coze 端已自动应用 Haldane 连续性校正；"
                    "若仍不理想，可改用 Peto 法（sm='Peto'）或广义线性混合模型（task='ipd_meta'）。"
                    "确认后请告知我切换方法重跑。" % _extreme_msg
                )
        except Exception:  # noqa: BLE001
            pass
        # 2026-09-13 结果解读引擎（统计顾问层）：基于 stats 自动生成结构化解读，
        # 包括结论、警告、后续建议、审稿人可能问的问题。贴到 _interpretation 供
        # CLI / 渲染层消费。解读失败不影响主结果。
        try:
            _interp = _interpret_result(res.get("stats") or {}, task, params)
            if _interp and any(_interp.values()):
                res["_interpretation"] = _interp
        except Exception:  # noqa: BLE001
            pass
        # 2026-09-13 质量评估（B2/B3/B4 解耦）：GRADE + 过度声明 + 质量门
        try:
            _qa = _evaluate_quality(res.get("stats") or {}, task)
            if _qa and any(_qa.values()):
                res["_quality_advice"] = _qa
        except Exception:  # noqa: BLE001
            pass
        # 2026-09-14 writing_advisor（P2a）：复用已生成的 _interpretation / _quality_advice，
        # 基于 stats + 领域模板生成发表建议；网络增强（P2b）默认开，失败优雅降级静态种子。
        if advise:
            try:
                from writing_advisor import advise_publication as _advise
                _qa = res.get("_quality_advice") or {}
                _g = _qa.get("grade") if isinstance(_qa, dict) else None
                _grade = _g.get("grade", "") if isinstance(_g, dict) else (_g if isinstance(_g, str) else "")
                # 2026-09-14：网络 Meta 的等级来自 CINeMA 六域（值域 major/some/no_concerns、
                # unclear），与 GRADE 的 High/Moderate/Low/VeryLow 不同 → 传框架名让
                # writing_advisor 输出 "CINeMA: major_concerns" 而非裸值，避免混读。
                _fw = (_qa.get("framework") if isinstance(_qa, dict) else "") or ""
                _pa = _advise(
                    res.get("stats") or {}, task, params,
                    topic=topic, field=field,
                    grade=_grade, grade_framework=_fw,
                    interpretation=res.get("_interpretation"),
                    references=references, merged_json=merged_json, use_network=use_network,
                    ref_sections=ref_sections,
                )
                if _pa:
                    res["_publication_advice"] = _pa
            except Exception:  # noqa: BLE001
                pass
        # 作为对话内联之外的"完整版"交付物；coze 返回体不变，固化在 agent 侧完成，
        # 不受 S3 链接过期与 4000 截断影响。生成失败不影响主结果。
        try:
            hp = render_html_report(res, out_dir=out_dir)
            if hp:
                res["html_report"] = hp
        except Exception:
            pass
        return res
    except _EnvelopeValidationError as e_val:
        # 2026-09-13：出站信封致命不合规（已在 POST 前拦截，未发送到云端）。
        # 把校验器给出的结构化指导原样回传，让 agent / CLI 转述用户修正，而非甩原始报错。
        _analysis = e_val.to_analysis()
        return {
            "status": "error",
            "notes": (
                "请求信封未通过 coze 契约校验，已在发送前拦截（未使用云端分析）。"
                "请按下方指导修正信封后重试。"
            ),
            "_source": "envelope_invalid",
            "_error_analysis": _analysis,
            "_error_guidance": _analysis.get("guidance", _render_contract_guidance(e_val.result)),
            "figures": [],
            "warnings": [],
        }
    except AuthRequiredError as e_auth:
        # ct-base §5 授权门控：未授权出站不阻断、也不绕过 —— 返回明确提示，由用户确认授权后重试。
        return {
            "status": "error",
            "notes": (
                f"未授权出站（ct-base §5 授权门控），本次未使用云端分析。"
                f"如同意将分析数据发送至云端，请确认授权后重试"
                f"（端点 {_coze_run_stage.__module__}）。"
            ),
            "_source": "auth_blocked",
            "_auth_required": True,
            "figures": [],
            "warnings": [],
        }
    except Exception as e_coze:
        return {
            "status": "error",
            "notes": f"coze 调用失败：{type(e_coze).__name__}: {e_coze}",
            "_source": "coze_error",
            "_coze_error": str(e_coze)[:500],
            "figures": [],
            "warnings": [],
        }


def _build_compute_stage_env(task, data, params, figure, query_origin):
    """构造 Block B 计算阶段（B1.meta_analysis）per-stage 信封。

    信封 = 计算层（task/data/params/figure，原样透传给 coze R 引擎 dispatcher）
           + 管线层（contract_version/schema/pipeline/stage/stage_context）。
    run_stage 内部 build_stage_payload 会再补 query_origin / 强制 figure.format=svg，
    若缺字段则按 default 填充。coze 端 meta_analysis 节点据管线字段走 per-stage 分支、
    回 stage_result（同时 R2 仍填充兼容 result）。
    """
    return {
        "task": task,
        "data": data,
        "params": params or {},
        "figure": figure or {},
        "contract_version": _CONTRACT_VERSION,
        "schema": _STAGE_SCHEMA_ID,
        "pipeline_id": f"run-{uuid.uuid4().hex[:8]}",
        "pipeline": {"name": "meta_analysis", "block": "B", "cfg": {}},
        "stage": {"id": "B1.meta_analysis", "index": 0, "total": 4,
                  "intent": "run", "prev_stage_id": None},
        "stage_context": {"human_decisions": [], "tool_card_outputs": [], "artifacts": []},
        "query_origin": query_origin,
    }


def _normalize_stage(res: dict) -> dict:
    """把 run_stage 返回的 stage 信封规整为 run_analysis 既有消费方
    （scripts/run_meta.py + render_html_report）期望的形状。

    parse_stage_response 在 coze 回传顶层 `result` 时已填充 status/stats/figures；
    若 coze 仅回 stage_result（无顶层 result），则从 stage_result.result 兜底抽取，
    避免下游渲染 / CLI 因缺字段而崩。
    """
    if not isinstance(res, dict):
        return res
    if res.get("status") is None:
        sr = res.get("stage_result") or {}
        inner = sr.get("result") if isinstance(sr, dict) else None
        if isinstance(inner, dict):
            for f in ("status", "stats", "figures", "warnings", "notes", "task", "repro"):
                if f in inner and f not in res:
                    res[f] = inner[f]
    if res.get("status") is None:
        # 仍缺 → 以 stage 模式视之，交由上层渲染 stage_result（不谎报 error）
        res["status"] = "ok" if res.get("mode") == "stage" else res.get("status")
    return res


def render_figures(out: dict, mode: str = "svg_inline", out_dir: str = ".",
                   titles: list | None = None) -> dict:
    """按出图模式处理 figures，返回增强后的结果 dict。

    mode:
      svg_inline（默认）— figures[].svg 原样保留，由调用方（agent）嵌入 HTML 报告展示（不再内联 widget）
      png_file          — 本地 cairosvg 将每个 SVG 转 PNG 文件存 out_dir/
                          figures 替换为 {type, format:"png", path}（更轻量、不出上下文）

    渲染计时（★ 用户要求：本地拿到 SVG 后到界面渲染完成的总时间）：
      - `render_elapsed_seconds`：本函数内 SVG 处理耗时（extract/strip/bbox/wrap/
        widget 生成 或 PNG 转换）——本地可精确测量；界面浏览器渲染部分无法在 agent
        侧计时，用 SVG 体量 `render_svg_kb` 作代理（体量越大界面渲染越慢）。
      - 若 render_elapsed_seconds > RENDER_SVG_THRESHOLD 或单图体量 >
        RENDER_SVG_KB_THRESHOLD，生成 `render_hint` 提示用户可切换 png_file 模式。
      - coze 计算/网络耗时见 `coze_elapsed_seconds`（仅诊断，**不参与**本提示）。

    Returns: 增强后的 out（新增 render_mode / render_elapsed_seconds / render_svg_kb /
             render_hint 字段）。
    """
    out = dict(out)
    _t0 = time.time()
    figs = out.get("figures") or []
    svg_kb = sum(len((f.get("svg") or "")) for f in figs) / 1024.0

    if mode == "png_file" and figs:
        os.makedirs(out_dir, exist_ok=True)
        out["figures"] = []
        for i, f in enumerate(figs):
            svg = f.get("svg") or ""
            if not svg:
                continue
            name = f.get("type") or f"fig{i + 1}"
            path = os.path.join(out_dir, f"{name}_{int(time.time())}.png")
            svg_to_png(svg, path)  # 同一处理链：strip clip → fix xml → bbox → viewBox → 光栅化
            out["figures"].append({"type": name, "format": "png", "path": path})

    out["render_elapsed_seconds"] = round(time.time() - _t0, 3)
    out["render_svg_kb"] = round(svg_kb, 1)
    out["render_mode"] = mode
    out["render_hint"] = _render_hint(out) if mode == "svg_inline" else None
    return out


def _render_hint(out: dict) -> str | None:
    """根据渲染耗时与 SVG 体量生成提示（仅 svg_inline 模式）。

    render_elapsed_seconds = 本地 SVG 处理 + widget 生成耗时（可精确测量）；
    界面浏览器渲染无法在 agent 侧计时 → 用 SVG 体量（render_svg_kb）作代理：
    体量越大，界面解析/滚动越慢。coze 计算/网络耗时（coze_elapsed_seconds）
    不参与本提示。
    """
    reasons = []
    elapsed = out.get("render_elapsed_seconds")
    if elapsed is not None and elapsed > RENDER_SVG_THRESHOLD:
        reasons.append(f"本地渲染处理耗时 {elapsed:.0f}s（> {RENDER_SVG_THRESHOLD:.0f}s 阈值）")
    svg_kb = out.get("render_svg_kb") or 0
    if svg_kb > RENDER_SVG_KB_THRESHOLD:
        reasons.append(f"SVG 体量 {svg_kb:.0f}KB（> {RENDER_SVG_KB_THRESHOLD:.0f}KB，界面渲染/滚动可能明显变慢）")
    if not reasons:
        return None
    return (
        "；".join(reasons) + "。可切换图片文件模式（figure_mode='png_file'）："
        "本地直接转 PNG 文件、不内联 SVG，界面渲染通常更快。"
    )


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="元分析统一调用（coze-only）")
    ap.add_argument("request", help="JSON 请求文件路径")
    ap.add_argument("--out-dir", default=".", help="HTML 报告输出目录（默认当前工作目录）")
    ap.add_argument("--ref-sections", default=None,
                    help="PDF 参考段落 JSON 路径（extract_sections 输出）；可选")

    a = ap.parse_args()

    req = json.load(open(a.request, encoding="utf-8"))
    _ref_secs = None
    if a.ref_sections:
        with open(a.ref_sections, encoding="utf-8") as _rf:
            _ref_secs = json.load(_rf)
    out = run_analysis(
        req.get("task"), req.get("data"), req.get("params"),
        req.get("figure"), out_dir=a.out_dir,
        ref_sections=_ref_secs,
    )
    # 2026-08-26 设计迭代：完整结果（含内联 SVG / R）落盘，供渲染模板离线复用，
    # 避免每次调整 HTML 样式都重复触发真实 coze 调用。
    import os as _os
    _ld = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "output")
    _os.makedirs(_ld, exist_ok=True)
    with open(_os.path.join(_ld, "last_run.json"), "w", encoding="utf-8") as _fh:
        json.dump(out, _fh, ensure_ascii=False, indent=2)
    # 2026-08-27 硬控制：成功时单独打印报告绝对路径（单行、不被 4000 截断吞掉），
    # 让 agent 直接 present_files，无需再跑 Bash 用 ls/grep 找报告（消灭 §0.2 禁项的物理动机）。
    _hp = out.get("html_report")
    if _hp:
        print("META_HTML_REPORT=" + os.path.abspath(_hp))
    elif out.get("status") == "error":
        print("META_STATUS=error | " + str(out.get("notes") or "")[:200])
    print(json.dumps(out, ensure_ascii=False, indent=2)[:4000])
