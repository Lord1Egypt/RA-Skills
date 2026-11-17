#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_api — paper-polisher-pro Python 编程接口（v4.5.0 新增）

设计约定（官方评测 trigger/usability 项的正面回应：程序化集成不再需要包装 subprocess）：
  - 零网络、零第三方依赖：纯标准库 + 同目录脚本直接 import（detect 路径不发子进程）
  - 所有函数返回 JSON 兼容 dict/list；输入不合法抛 ValueError，运行失败抛 RuntimeError——不静默吞
  - detect_text() 与 CLI `ai_detector.py <file> --format json` 同一代码路径，结果一致
  - 100% 本地：不发起任何网络请求（与包内 zero-network 声明一致）
  - 短文本(<100字)沿用铁律2：risk=unknown，不出判定

用法：
    import sys; sys.path.insert(0, "<包>/scripts")
    from pp_api import detect_text, gate_text, doctor_summary
    r = detect_text("待检测的中文学术文本，建议 300 字以上。" * 10, lang="zh")
    print(r["overall_ai_score"], r["overall_risk"])
    g = gate_text("待门禁文本。" * 30)      # 四层降AI门禁
    d = doctor_summary()                     # 环境自检摘要（引擎档位/模型指纹）
"""
import contextlib
import io
import json
import os
import sys
import tempfile
from dataclasses import asdict, is_dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

__all__ = [
    "engine_version", "model_fingerprint", "detect_text", "detect_file",
    "gate_text", "term_report", "smell_report", "style_report",
    "quality_report_file", "attribution", "doctor_summary", "workflow",
    "fix_suggest", "evidence_sections", "term_project", "scenarios",
    "trend_data", "schema_selfcheck",
]


def _asdict(obj):
    """dataclass → dict；已是 dict/list 原样返回。"""
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    return obj


def engine_version() -> str:
    """SKILL.md frontmatter 的版本号。"""
    import re
    t = (HERE.parent / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^version:\s*(\S+)", t, re.M)
    if not m:
        raise RuntimeError("SKILL.md version 字段缺失")
    return m.group(1)


def model_fingerprint() -> dict:
    """部署监督模型指纹。无模型返回 {"installed": False}（纯规则降级档）。"""
    import hashlib
    cache = Path.home() / ".cache" / "paper-polisher" / "qwen3-detector"
    onnx_p = cache / "model.int8.onnx"
    if not onnx_p.is_file():
        return {"installed": False, "model_dir": str(cache)}
    h = hashlib.md5()
    with open(onnx_p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return {"installed": True, "model_dir": str(cache),
            "md5_12": h.hexdigest()[:12], "size_bytes": onnx_p.stat().st_size}


def detect_text(text: str, lang: str = "auto") -> dict:
    """完整 AI 检测（进程内，与 CLI 同一代码路径）。返回 DetectionReport dict。

    lang: "auto"|"zh"|"en"——非中文文本按语言门控设计跳过监督层（英文骨架评分，仅供参考）。
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import ai_detector
    try:
        return _asdict(ai_detector.detect(text, lang=lang))
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError("detect 失败: %s（恢复建议: python3 scripts/pp_doctor.py 环境自检；"
                           "监督层异常可 PP_NO_SUP=1 走纯规则档，或 pp_setup.py --check 查装模）" % e) from e


def detect_file(path: str) -> dict:
    """对文件做完整检测（等价 detect_text(读入内容)）。"""
    p = Path(path)
    if not p.is_file():
        raise ValueError("文件不存在: %s" % path)
    if p.stat().st_size > 5 * 1024 * 1024:
        raise ValueError("文件超过 5MB（与批量模式同口径，请先切分）")
    return detect_text(p.read_text(encoding="utf-8", errors="replace"))


def gate_text(text: str) -> dict:
    """四层降AI门禁（词级/文体/翻译腔/术语 → composite_ai_risk + verdict）。

    门禁管线按文件组织（四个子层各自读盘），此处经临时文件中转——用户无感，
    结果与 CLI `deai_gate.py <file> --json` 一致。
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import deai_gate
    fd, tmp = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        with contextlib.redirect_stdout(io.StringIO()):  # v4.6.0: 吞掉子层 print，SDK 只返回值
            return deai_gate.gate(tmp, json_out=True)
    except Exception as e:
        raise RuntimeError("gate 失败: %s" % e) from e
    finally:
        Path(tmp).unlink(missing_ok=True)


def term_report(text: str) -> dict:
    """术语保护检查（2,344 条医学学术术语库）。返回 TermReport dict。"""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import term_check
    try:
        return _asdict(term_check.check_terms(text, term_check.load_terminology()))
    except Exception as e:
        raise RuntimeError("term_check 失败: %s" % e) from e


def smell_report(text: str) -> dict:
    """翻译腔检查。返回 {total_hits, hits: [...]}（SmellHit dict 列表）。"""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import translation_smell_check as tsc
    try:
        hits = [_asdict(tsc.classify_hit(h)) for h in tsc.rule_hits(text)]
        return {"total_hits": len(hits), "hits": hits}
    except Exception as e:
        raise RuntimeError("translation_smell 失败: %s" % e) from e


def style_report(text: str) -> dict:
    """文体距离/人类相似度（学术散文口径，其他语域仅供参考）。返回 dict。"""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import style_distance
    try:
        with contextlib.redirect_stdout(io.StringIO()):  # v4.6.0: 吞掉 CLI print
            return _asdict(style_distance.style_distance(text))
    except Exception as e:
        raise RuntimeError("style_distance 失败: %s" % e) from e


def quality_report_file(path: str) -> dict:
    """综合质量报告（文件口径：结构/可读性/段落等）。返回 QualityReport dict。"""
    p = Path(path)
    if not p.is_file():
        raise ValueError("文件不存在: %s" % path)
    import quality_report
    try:
        return _asdict(quality_report.generate_report(str(p)))
    except Exception as e:
        raise RuntimeError("quality_report 失败: %s" % e) from e


def attribution(text: str, topn: int = 3) -> list:
    """AI 家族指纹归因（只归因不进分）。返回 [{family, confidence}...]。"""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import ai_detector
    try:
        return _asdict(ai_detector.attribute_model(text, topn=topn))
    except Exception as e:
        raise RuntimeError("attribution 失败: %s" % e) from e


def workflow(text: str, lang: str = "auto") -> dict:
    """端到端自查工作流：检测+段落归因+门禁+术语+翻译腔+文体+质量+AIGC 标识，
    一次调用返回综合 dict。落盘版见 scripts/pp_workflow.py（JSON+Markdown）。"""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import pp_workflow
    try:
        return pp_workflow.workflow(text, lang=lang)
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError("workflow 失败: %s（恢复建议: 先单独跑 ai_detector.py 确认引擎，"
                           "再逐项 pp_api.detect_text/term_report 定位失败子检查）" % e) from e


def style_norm(text: str, checks: list = None) -> dict:
    """学术写作规范自查（v5.2.0）：全半角/数字用法/缩写定义/单位格式的机械体例核对。

    返回 findings 建议（不评分、无风险带，与 AI 率检测相互独立）。
    完整语义见 scripts/pp_style_norm.py。
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import pp_style_norm
    try:
        return pp_style_norm.style_norm(text, checks=checks)
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError("style_norm 失败: %s" % e) from e


def rewrite_check(original: str, revised: str, lang: str = "auto") -> dict:
    """改写效果回归验证（v5.1.0）：原稿 vs 改稿的引擎同源对比。

    返回 {document: 分数/风险带迁移, edit_extent: 幅度, features: 特征类型增减,
          paragraphs: 段落级配对 delta, integrity_notice, notice}。
    分数变化是本引擎口径的相对参考，不与任何机构检测器互换。
    完整语义见 scripts/pp_rewrite_check.py（--demo 有内置样例）。
    """
    if not isinstance(original, str) or not original.strip():
        raise ValueError("original 必须是非空字符串")
    if not isinstance(revised, str) or not revised.strip():
        raise ValueError("revised 必须是非空字符串")
    import pp_rewrite_check
    try:
        return pp_rewrite_check.rewrite_check(original, revised, lang=lang)
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError("rewrite_check 失败: %s（恢复建议: 分别对两稿跑 "
                           "pp_api.detect_text 确认引擎可用后再试）" % e) from e


def doctor_summary() -> dict:
    """环境自检摘要（pp_doctor 关键项的进程内子集）。

    返回 {python_ok, data_files_ok, engine_mode, supervised: {...}, hint}。
    完整自检请跑 CLI `python3 pp_doctor.py`。
    """
    root = HERE.parent
    ok_py = sys.version_info >= (3, 9)
    data_ok, data_missing = True, []
    for rel in ("data/terminology.json", "references/fusion_config.json",
                "references/model_fingerprints.json"):
        f = root / rel
        if not f.is_file():
            data_ok, data_missing = False, data_missing + [rel]
            continue
        try:
            json.load(open(f, encoding="utf-8"))
        except Exception:
            data_ok, data_missing = False, data_missing + [rel + "(解析失败)"]
    sup = model_fingerprint()
    sup_live = False
    if sup.get("installed"):
        try:
            import layers_lm
            r = layers_lm.supervised_layer("环境自检金丝雀。" * 20)
            sup_live = r is not None
        except Exception:
            sup_live = False
    engine_mode = "full" if (sup.get("installed") and sup_live
                             and not os.environ.get("PP_NO_SUP")) else "degraded"
    return {"python_ok": ok_py, "data_files_ok": data_ok,
            "data_missing": data_missing, "engine_mode": engine_mode,
            "supervised": sup, "supervised_live": sup_live,
            "version": engine_version(),
            "hint": "" if engine_mode == "full" else
            "降级档（纯规则+词频谱）：医学语域会被系统性高估；"
            "启用监督层见 pp_setup.py --model <作者签发的模型文件>"}


if __name__ == "__main__":
    print(json.dumps(doctor_summary(), ensure_ascii=False, indent=2))


def fix_suggest(text: str, top: int = None, lang: str = "auto") -> dict:
    """句子级改写建议（v7.4.0 SDK 化）：指位+策略，不代改。

    返回 {stats, suggestions}，与 pp_fix_suggest.py --json 同构。"""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import pp_fix_suggest
    try:
        results, stats, lang2 = pp_fix_suggest.analyze(text, lang, top)
        return {"stats": stats, "suggestions": [
            {"index": r["index"] + 1, "sentence": r["sentence"],
             "issues": [{"type": x["type"], "evidence": x["evidence"],
                         "advice": pp_fix_suggest.ADVICE.get(x["type"], "")}
                        for x in r["issues"]]}
            for r in results], "language": lang2,
            "notice": "改写建议是排序辅助：指位与策略供人工润稿参考，不构成任何合规判定。"}
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError("fix_suggest 失败: %s（恢复建议: 单跑 python3 scripts/pp_fix_suggest.py "
                           "<文件> --json 定位）" % e) from e


def evidence_sections(text: str) -> dict:
    """检测证据报告的区块化证据链（v7.4.0 SDK 化）：结论卡+逐特征定位+段落分级+阈值口径。

    返回 {meta, sections}；渲染版（HTML/MD）见 pp_evidence_report.py。"""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import ai_detector, pp_evidence_report
    try:
        d = _asdict(ai_detector.detect(text, lang="auto"))
        secs = pp_evidence_report.build_sections(d, text, "sdk-input")
        return {"meta": {"overall_ai_score": d.get("overall_ai_score"),
                         "overall_risk": d.get("overall_risk"),
                         "degraded_mode": d.get("degraded_mode")},
                "sections": [{"title": s[0], "html": s[1]} for s in secs],
                "integrity_notice": pp_evidence_report._INTEGRITY}
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError("evidence_sections 失败: %s（恢复建议: 先 pp_api.detect_text 确认可检测）" % e) from e


def term_project(directory: str, recursive: bool = False, bank: str = None) -> dict:
    """多文档术语一致性（v7.4.0 SDK 化）：目录级库内概念跨文件写法矩阵+统一建议。

    与 pp_term_consistency.py --json 同构；单文件场景请用 term_report。"""
    from pathlib import Path as _P
    d = _P(directory)
    if not d.is_dir():
        raise ValueError("directory 必须是存在的目录: %s" % directory)
    import pp_term_consistency
    try:
        return pp_term_consistency.analyze(str(d), recursive=recursive,
                                           bank_path=bank)
    except SystemExit:
        raise ValueError("目录内有效文稿不足 2 份（txt/md/docx）")
    except Exception as e:
        raise RuntimeError("term_project 失败: %s（恢复建议: 单文件用 pp_api.term_report；"
                           "坏文件会被逐文件隔离并在 per_file.error 如实标注）" % e) from e


def scenarios(query: str = None) -> list:
    """场景目录（v7.4.0 SDK 化）：什么时候用哪个命令。

    返回场景列表（scene/when/cmd/output/tags）；无 query 返回全部，
    有 query 按场景/说明/标签过滤（紧凑中文去空格兜底）。"""
    import json as _json
    from pathlib import Path as _Path
    p = _Path(__file__).resolve().parent.parent / "references" / "scenarios.json"
    if not p.is_file():
        raise RuntimeError("scenarios.json 缺失（场景目录随 v6.7.0 随包）")
    scs = _json.loads(p.read_text(encoding="utf-8"))["scenarios"]
    if not query:
        return scs
    q = query.strip().lower()
    kws = [k for k in q.replace("，", " ").replace(",", " ").split() if k]
    hit = []
    for s in scs:
        blob = " ".join([s.get("scene_zh", ""), s.get("scene_en", ""),
                         s.get("when_zh", ""), s.get("when_en", ""),
                         " ".join(s.get("tags", []))]).lower()
        blob_ns = blob.replace(" ", "")
        hits = sum(1 for k in kws if k in blob or k.replace(" ", "") in blob_ns)
        if hits:
            hit.append((hits, s))
    hit.sort(key=lambda x: -x[0])
    return [s for _, s in hit]


def trend_data(inputs) -> list:
    """多轮趋势数据（v7.7.0 SDK 化）：多份 workflow JSON/目录 → 按时间排序的轨迹数据。

    与 pp_trend.py collect 同源；渲染版（HTML 仪表盘）见 pp_trend.py / pp.py trend。
    inputs: 路径列表（workflow JSON 文件或含 *.workflow.json 的目录）。"""
    from pathlib import Path as _Path
    if not inputs:
        raise ValueError("inputs 必须是非空路径列表")
    import pp_trend
    try:
        return pp_trend.collect([str(_Path(x)) for x in inputs])
    except Exception as e:
        raise RuntimeError("trend_data 失败: %s（恢复建议: 确认输入为 workflow JSON 文件"
                           "或含 *.workflow.json 的目录）" % e) from e


def schema_selfcheck() -> dict:
    """输出契约自证（v7.7.0 SDK 化）：真引擎输出逐一过 schemas/*.schema.json。

    返回 {ok, results}——results 为 {name: PASS/FAIL 详情}；编程集成方可据此
    验证自己拿到的输出结构是否符合随包契约。"""
    import io as _io
    import contextlib as _cl
    import pp_schema
    buf_out, buf_err = _io.StringIO(), _io.StringIO()
    with _cl.redirect_stdout(buf_out), _cl.redirect_stderr(buf_err):
        rc = pp_schema.selfcheck()
    results = {}
    for ln in buf_out.getvalue().splitlines():
        if ln.startswith("[PASS] "):
            results[ln.split()[1]] = "PASS"
        elif ln.startswith("[FAIL] "):
            results[ln.split()[1]] = "FAIL: " + ln
    return {"ok": rc == 0, "results": results}
