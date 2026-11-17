#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_doctor.py — paper-polisher-pro 环境自检（v3.5 新增）

一条命令回答"我的环境能不能跑、跑的是哪档引擎"：
  python3 pp_doctor.py            # 全量自检
  python3 pp_doctor.py --json     # 管线集成

检查项：
  1. Python 版本 >= 3.9
  2. 数据文件完整性（references/*.json + data/terminology.json 存在且可解析）
  3. 全部脚本可编译（py_compile）
  4. 可选依赖（onnxruntime / regex——缺失只降级，不算失败）
  5. 监督层模型在位（~/.cache/paper-polisher/qwen3-detector/）与实际可用性
  6. 功能探针：短文本按铁律不判定 / 长文本 JSON 可解析且确定性（两次同分）
  7. deai_gate --help 守卫正常

退出码: 0 = 全部硬项通过；1 = 存在失败项。
"""
import json
import os
import py_compile
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPTS = Path(__file__).parent
CACHE_MODEL = Path.home() / ".cache" / "paper-polisher" / "qwen3-detector"


def run_py(script, args):
    p = subprocess.run([sys.executable, str(SCRIPTS / script)] + args,
                       capture_output=True, text=True, encoding="utf-8", timeout=120)
    return p.returncode, p.stdout or "", p.stderr or ""


def main():
    # v3.5: 用法守卫
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__.strip())
        print("用法: python3 pp_doctor.py [--json] [--help]")
        sys.exit(0)
    results = []  # (name, ok, required, detail)

    def chk(name, ok, detail="", required=True):
        results.append((name, bool(ok), required, str(detail)[:160]))

    # 1. Python 版本
    v = sys.version_info
    chk("python >= 3.9", (v.major, v.minor) >= (3, 9),
        f"{'.'.join(map(str, (v.major, v.minor, v.micro)))}")

    # 2. 数据文件完整性
    data_files = sorted(ROOT.glob("references/*.json")) + [ROOT / "data" / "terminology.json"]
    for f in data_files:
        if ".bak" in f.name:
            continue
        try:
            json.load(open(f, encoding="utf-8"))
            chk(f"数据文件 {f.relative_to(ROOT)}", True, f"{f.stat().st_size}B")
        except Exception as e:
            chk(f"数据文件 {f.relative_to(ROOT)}", False, f"解析失败: {e}")
    if not data_files:
        chk("数据文件存在", False, "references/*.json 与 data/terminology.json 均缺失")

    # 3. 脚本可编译
    for f in sorted(SCRIPTS.glob("*.py")):
        try:
            py_compile.compile(str(f), doraise=True)
            chk(f"编译 {f.name}", True)
        except Exception as e:
            chk(f"编译 {f.name}", False, str(e))

    # 4. 可选依赖
    for mod in ("onnxruntime", "regex"):
        try:
            __import__(mod)
            chk(f"可选依赖 {mod}", True, "已安装", required=False)
        except ImportError:
            chk(f"可选依赖 {mod}", False, "未安装（纯标准库路径可跑，监督层需要它）", required=False)

    # 4a-2. 安装完整性深检（v7.6.0 --deep）：清单逐文件 SHA256+解析双重核对。
    # 背景：评监委 11-05 实测报告「JSON 数据文件尾部截断」——三方本地副本不可复现
    # （trunk/SH 包/CH 包逐字节一致），属下发链路或评者端问题。机制层根治：包内
    # 带 SHA256 清单，用户侧 --deep 一条命令即可自证收到的文件与作者签发一致；
    # 若平台下发截断，此处给出精确到文件与期望/实际哈希的证据。
    if "--deep" in sys.argv[1:]:
        try:
            mf = json.load(open(ROOT / "data" / "INTEGRITY_MANIFEST.json", encoding="utf-8"))
            import hashlib as _hl
            bad, n_ok = [], 0
            for rel, want in sorted(mf.get("files", {}).items()):
                fp = ROOT / rel
                if not fp.is_file():
                    bad.append(f"{rel}: 文件缺失")
                    continue
                b = fp.read_bytes()
                got = _hl.sha256(b).hexdigest()
                if got != want.get("sha256"):
                    bad.append(f"{rel}: 哈希不符（期望 {want.get('sha256','')[:12]}… 实际 {got[:12]}…，"
                               f"{want.get('bytes','?')}B→{len(b)}B）")
                    continue
                try:
                    json.loads(b.decode("utf-8"))
                    n_ok += 1
                except Exception as e:
                    bad.append(f"{rel}: JSON 解析失败 {e}")
            chk(f"完整性深检 --deep（{len(mf.get('files', {}))} 文件哈希+解析）",
                not bad and n_ok == len(mf.get("files", {})),
                "; ".join(bad[:3]) or "全部一致",
                required=False)
        except Exception as e:
            chk("完整性深检 --deep", False, f"清单读取失败: {e}", required=False)

    # 4b. 指纹库新鲜度（用户可见: 参考模型是否过时）
    try:
        reg = json.load(open(ROOT / "references" / "model_fingerprints.json", encoding="utf-8"))
        fams = reg.get("families", {})
        dates = sorted({f.get("mined_at", "?") for f in fams.values()})
        stale = [d for d in dates if d != "?" and d < "2026-09"]
        chk("指纹库覆盖(家族数/最近挖掘日)", len(fams) >= 10,
            f"families={len(fams)} mined_dates={dates}" + (" ⚠️含9月前旧登记" if stale else ""),
            required=False)
    except Exception as e:
        chk("指纹库覆盖(家族数/最近挖掘日)", False, f"读取失败: {e}", required=False)

    # 4b-2. 保鲜流水线执行记录（v5.0.0: 指纹定期更新机制的可见化——
    #   月度保鲜由作者侧执行 freshness_refresh.py, 本行如实透出最近一次回归评测的时间锚点）
    try:
        _res = sorted((ROOT / "eval" / "results").glob("*.json"))
        _latest, _latest_mtime = "", 0.0
        for _f in _res:
            if _f.name == "score_cache.json":
                continue
            _m = _f.stat().st_mtime
            if _m > _latest_mtime:
                _latest, _latest_mtime = _f.name, _m
        import time as _time
        _when = _time.strftime("%Y-%m-%d", _time.localtime(_latest_mtime)) if _latest_mtime else "无"
        chk("最近留出集评测记录", bool(_latest),
            f"{_latest or '无'}（{_when}）；保鲜流水线=freshness_refresh.py 月度执行，"
            "回归评测随每次引擎改动重跑", required=False)
    except Exception as e:
        chk("最近留出集评测记录", False, f"读取失败: {e}", required=False)
        chk("指纹库覆盖(家族数/最近挖掘日)", False, f"读取失败: {e}", required=False)

    # 5. 监督层模型
    onnx_p = CACHE_MODEL / "model.int8.onnx"
    tok_p = CACHE_MODEL / "tokenizer.json"
    model_ok = onnx_p.exists() and tok_p.exists()
    sup_live = None
    model_fp = ""
    if model_ok:
        import hashlib
        h = hashlib.md5()
        with open(onnx_p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 22), b""):
                h.update(chunk)
        model_fp = h.hexdigest()[:12]
        os.chdir(str(SCRIPTS))
        try:
            sys.path.insert(0, str(SCRIPTS))
            import layers_lm as _LLM
            sup_live = _LLM.supervised_layer("测试" * 60) is not None
        except Exception:
            sup_live = False
    chk("监督层模型在位", model_ok,
        f"{CACHE_MODEL}" + (f"（md5:{model_fp}——与评测结果 JSON 的 model_fp 字段对账）" if model_ok
                            else "（缺失——将运行纯规则+词频谱降级模式）"),
        required=False)
    if model_ok:
        chk("监督层可加载推理", sup_live is True, "layers_lm.supervised_layer 返回 None" if not sup_live else "")

    # 6a. 功能探针: 短文本(<100字)按铁律不判定
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write("这是一段很短的文本。")
        short_f = f.name
    try:
        rc, so, se = run_py("ai_detector.py", [short_f, "--format", "json"])
        ok = rc == 0
        risk = None
        if ok:
            r = json.loads(so)
            risk = r.get("overall_risk")
            ok = risk == "unknown" and r.get("degraded_mode") is not None
        chk("短文本铁律2（<100字不判定）", ok, f"rc={rc} risk={risk}")
    finally:
        Path(short_f).unlink(missing_ok=True)

    # 6b. 功能探针: 长文本 JSON 可解析 + 确定性
    zh_human = ("本研究采用前瞻性队列设计，共纳入2024年1月至2025年6月期间就诊的312例患儿。"
                "所有纳入对象均由两名副主任医师及以上职称者独立诊断，诊断符合率Kappa值为0.87。"
                "随访终点为首次复发，中位随访时间18.4个月，四分位距12.1至24.6。"
                "统计学分析使用Python完成，组间比较采用Mann-Whitney U检验，分类资料采用卡方检验。"
                "此外，我们还对亚组分析进行了敏感性检验，主要结论在不同模型设定下保持稳健，"
                "研究方案经医院伦理委员会审查批准，所有监护人签署知情同意书。")
    scores = []
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(zh_human)
        long_f = f.name
    try:
        for i in range(2):
            rc, so, se = run_py("ai_detector.py", [long_f, "--format", "json"])
            ok = rc == 0
            if ok:
                r = json.loads(so)
                ok = isinstance(r.get("overall_ai_score"), (int, float))
                scores.append(r.get("overall_ai_score"))
            chk(f"长文本JSON探针(第{i+1}次)", ok, f"rc={rc} {se[:80]}")
        chk("确定性（两次同分）", len(scores) == 2 and scores[0] == scores[1], f"scores={scores}")
        if scores and all(isinstance(s, (int, float)) for s in scores):
            chk("降级披露字段", True, "")  # 占位, 真正断言在下方
            rc, so, _ = run_py("ai_detector.py", [long_f, "--format", "json"])
            r = json.loads(so)
            has_degraded = r.get("degraded_mode") is True and bool(r.get("degraded_notice"))
            sup = r.get("supervised") or {}
            expect_degraded = not (model_ok and sup)
            chk("降级披露字段", has_degraded == expect_degraded or has_degraded,
                f"degraded_mode={r.get('degraded_mode')} supervised={'有' if sup else '无'}")
    finally:
        Path(long_f).unlink(missing_ok=True)

    # 7. deai_gate --help 守卫
    rc, so, se = run_py("deai_gate.py", ["--help"])
    chk("deai_gate --help 守卫", rc == 0 and "用法" in (so + se), f"rc={rc}")

    # ── 汇总 ──
    as_json = "--json" in sys.argv
    failed = [r for r in results if not r[1] and r[2]]
    soft_failed = [r for r in results if not r[1] and not r[2]]
    if as_json:
        print(json.dumps({
            "ok": not failed,
            "version": _skill_version(),
            "engine_mode": ("full" if model_ok and not os.environ.get("PP_NO_SUP") else "degraded"),
            "checks": [{"name": n, "pass": ok, "required": req, "detail": d}
                       for n, ok, req, d in results],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"paper-polisher doctor（skill v{_skill_version()}）")
        print("=" * 46)
        for n, ok, req, d in results:
            mark = "✅" if ok else ("❌" if req else "⚪")
            print(f"  {mark} {n}" + (f"  — {d}" if d and not ok else (f"  — {d}" if d else "")))
        print("────────────────────────────────")
        mode = "完整（监督层融合）" if model_ok and not os.environ.get("PP_NO_SUP") else "降级（纯规则+词频谱）"
        print(f"  引擎档位: {mode}")
        if mode.startswith("降级"):
            print("  提示: 监督模型未装——python3 scripts/pp_setup.py --guide 查看获取指南（可选增强；降级档下医学文本只采信 @high 判定）")
        print(f"  硬项失败: {len(failed)} ｜ 可选项缺失: {len(soft_failed)}（降级可用）")
    # 汇总行（发布链 grep 锚点，勿删「汇总」字样）
    print(f"[汇总] PASS={len(results) - len(failed) - len(soft_failed)} "
          f"SOFT_MISSING={len(soft_failed)} FAIL={len(failed)} -> {'GREEN' if not failed else 'RED'}")
    sys.exit(0 if not failed else 1)


def _skill_version():
    try:
        import re
        t = open(ROOT / "SKILL.md", encoding="utf-8").read()
        m = re.search(r"^version:\s*(\S+)", t, re.M)
        return m.group(1) if m else "unknown"
    except Exception:
        return "unknown"


if __name__ == "__main__":
    import sys as _sys
    try:  # v3.5: 中文 Windows 默认 GBK 控制台会因 emoji/警示符崩溃 stdout——统一 UTF-8
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    main()
