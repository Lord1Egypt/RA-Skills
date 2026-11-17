# -*- coding: utf-8 -*-
"""selfcheck — 包内一键自检（v5.8.0）。

目的：装完/打包后一条命令验证「包是好的」——环境、结构、核心功能冒烟、
文档对账四段全过 exit 0。发布包不含仓库 tests/，本脚本即随包可见的质量
自证入口（评测与用户都可现场复跑）。

口径：
  - 零网络、零子进程、零第三方依赖（只 import 包内模块与标准库）；
  - 不写任何文件（冒烟全部进程内内存样例）；
  - 只读包内文件（脚本/词表/文档），用于文档对账段。

用法：
  python scripts/selfcheck.py            # 人读输出，exit 0=全过 / 1=有 FAIL
  python scripts/selfcheck.py --json     # 机器可读（CI/agent 门禁）
"""
import json
import os
import re
import sys
import platform

# 承诺「不写盘」严格为真：禁字节码缓存落包内（解释器默认会写 __pycache__）
sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print("[%s] %s%s" % ("PASS" if cond else "FAIL", name,
                         ("  ← " + detail) if (detail and not cond) else ""))


def section(title):
    print("── %s ──" % title)


def main():
    argv = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv[1:]

    # ── S1 环境 ──
    section("S1 环境")
    import hxt_core
    check("S1.python", sys.version_info >= (3, 8),
          "当前 %s（需 ≥3.8）" % platform.python_version())
    check("S1.包版本", bool(re.match(r"^\d+\.\d+\.\d+$", hxt_core.__version__)),
          hxt_core.__version__)

    # ── S2 结构：核心模块可导入 + 词表可解析 + 参考文档在位 ──
    section("S2 结构")
    mods = ["hxt_core", "detect_core" if os.path.exists(os.path.join(
        HERE, "detect_core.py")) else "reporter",
        "transform", "verify", "plan", "reporter", "check_stats",
        "check_terms", "stylecheck", "learn_guards", "extract_terms",
        "compare"]
    bad = []
    for m in mods:
        try:
            __import__(m)
        except Exception as e:  # noqa: BLE001 — 自检要兜住任意导入失败
            bad.append("%s(%s)" % (m, str(e)[:40]))
    check("S2.模块导入", not bad, "、".join(bad))
    import detect  # noqa: F401 — CLI 壳单独验
    packs = []
    for pf in ("patterns_zh.json", "patterns_en.json"):
        try:
            with open(os.path.join(HERE, pf), encoding="utf-8") as f:
                packs.append((pf, len(json.load(f))))
        except Exception as e:  # noqa: BLE001
            bad.append("%s(%s)" % (pf, str(e)[:40]))
    check("S2.词表解析", not bad and all(n > 10 for _, n in packs),
          "、".join("%s=%d组" % p for p in packs))
    refs = sorted(x for x in os.listdir(os.path.join(ROOT, "references"))
                  if x.endswith(".md")) if os.path.isdir(
        os.path.join(ROOT, "references")) else []
    check("S2.参考文档", len(refs) >= 14, "实有 %d 份" % len(refs))

    # ── S3 功能冒烟（进程内样例，不落盘）──
    section("S3 冒烟")
    import transform as _tf
    import verify as _vf
    import reporter as _rp
    import plan as _pl
    import check_stats as _cst
    import check_terms as _ctm

    sample = "综上所述，本研究具有重要意义。\n\n该方案不仅提升效率而且降低成本。\n"
    fullw = _tf.normalize_fullwidth_alnum("研究于２０２５年启动。")
    enfixed, enapp = _tf.apply_auto_fixes(
        "This study utilizes the dataset.", _tf.load_fixes("en", False))
    check("S3.清理生效",
          "2025" in (fullw[0] if isinstance(fullw, tuple) else fullw)
          and enfixed != "This study utilizes the dataset." and len(enapp) >= 1,
          "fullw=%r enapp=%s" % (fullw, list(enapp)[:2]))

    r_ok = _vf.verify(sample, sample)
    check("S3.一致稿过守卫", r_ok.get("ok") is True)

    sample_n = ("研究纳入 120 例患者，随访 24 个月，P<0.05。\n" + sample)
    broken_n = sample_n.replace("120 例", "118 例")
    r_bad = _vf.verify(sample_n, broken_n)
    check("S3.改坏数据被抓", r_bad.get("ok") is not True
          and len(r_bad.get("violations", [])) >= 1,
          "violations=%s" % [v.get("check") for v in r_bad.get("violations", [])][:3])
    rem = _vf.build_remedies(sample_n, r_bad)
    html = _vf.render_report_html(r_bad, rem)
    check("S3.处方报告要素", ("违规（" in html) and ("原句锚点" in html)
          and ("修复三步" in html))

    rows = _rp.sentence_diff(sample_n, broken_n)
    check("S3.对照行号", rows and all(len(x) == 5 for x in rows))

    top, _secs, _full = _pl.build_queue(sample, lang=None)
    check("S3.句级计划", len(top) >= 1)

    badstat = "两组受试者依次为：青年 60 例（60.3%），中年 40 例（41.7%）。"
    _out, issues = _cst.run_checks(badstat)
    check("S3.统计一致性", len(issues) >= 1,
          "issues=%s" % [i.get("type", i.get("check", "?")) for i in issues][:3])

    check("S3.术语组在位", len(getattr(_ctm, "_TERM_GROUPS", [])) >= 8,
          "实有 %d 组" % len(getattr(_ctm, "_TERM_GROUPS", [])))

    dash = _rp.render_dashboard(
        {"score": 60, "level": "高"}, {"score": 10, "level": "低"},
        r_ok, "academic", [], [], [],
        meta="selfcheck")
    check("S3.体检报告渲染", "行动" in dash or "card" in dash)

    import calibrate as _cal
    _cd = os.path.join(ROOT, "references", "calib_corpus")
    try:
        _c58 = _cal.calibrate(_cd)
        _warn = any(r["signal"] == "__warning__" for r in _c58["table"])
        check("S3.阈值校准", not _c58["violations"] and not _warn,
              "violations=%s" % (_c58["violations"][:2],))
    except ValueError as e:
        check("S3.阈值校准", False, "语料缺失: %s" % str(e)[:80])

    # ── S4 文档对账（仓库闸的包内镜像——件数/版本/清单覆盖）──
    section("S4 对账")
    zh = _rd(os.path.join(ROOT, "SKILL_ZH.md"))
    en = _rd(os.path.join(ROOT, "SKILL.md"))
    perm = _rd(os.path.join(ROOT, "references", "permissions.md"))
    faq = _rd(os.path.join(ROOT, "references", "faq.md"))
    plsrc = _rd(os.path.join(HERE, "pipeline.py"))

    mz = re.search(r"功能状态（v([\d.]+)）", zh)
    me = re.search(r"Feature status \(v([\d.]+)\)", en)
    cur = hxt_core.__version__
    check("S4.双语版本行", bool(mz) and bool(me)
          and mz.group(1) == cur and me.group(1) == cur,
          "ZH=%s EN=%s 现役=%s" % (mz and mz.group(1), me and me.group(1), cur))

    writes = re.findall(r'os\.path\.join\(bdir, "(\d{2})_', plsrc)
    n_items = len(set(writes))
    mp = re.search(r"写 (?:[\d-]+ 共 )?(\d+) 个编号件", perm)
    check("S4.permissions件数", bool(mp) and int(mp.group(1)) == n_items,
          "声明=%s 实测=%d" % (mp and mp.group(1), n_items))

    regs = set(re.findall(r'_reg\(os\.path\.join\(bdir, "(\d{2}_[^"]+)"\)', plsrc))
    unreg = sorted({w for w in set(writes)
                    if not any(reg.startswith(w) for reg in regs)})
    check("S4.清单覆盖", not unreg, "未登记写点: %s" % unreg)

    loose = []
    for label, doc, pat in (("SKILL_ZH", zh, r"共 (\d+) 个编号件"),
                            ("faq", faq, r"自查包 (\d+) 件")):
        for mm in re.finditer(pat, doc):
            if int(mm.group(1)) != n_items:
                loose.append("%s=%s" % (label, mm.group(1)))
    check("S4.文档件数口径", not loose, "、".join(loose) or "全部=%d" % n_items)

    # 旧口径终扫（与 tests/check_doc_counts.py LEGACY 同源镜像——包内可见版）
    import glob as _glob
    LEGACY = ("六件套", "六件数据", "写 8 个文件", "00-09 共 10", "8 numbered items",
              "10 numbered items", "9 numbered items", "00-10 共 11", "11 numbered items",
              "九件")
    _bad = []
    for _md in _glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        _rel = os.path.relpath(_md, ROOT)
        if _rel.startswith(("tests" + os.sep, ".git" + os.sep)):
            continue
        _mt = open(_md, encoding="utf-8").read()
        for _w in LEGACY:
            if _w in _mt:
                _bad.append("%s:%s" % (_rel, _w))
    check("S4.旧口径终扫", not _bad, "、".join(_bad[:4]))

    # ── 汇总 ──
    npass = sum(1 for _, ok, _ in RESULTS if ok)
    nfail = len(RESULTS) - npass
    print("═" * 46)
    print("SUMMARY: %d PASS / %d FAIL（paper-rewriter v%s 包内自检）"
          % (npass, nfail, hxt_core.__version__))
    if as_json:
        print(json.dumps({
            "version": hxt_core.__version__,
            "pass": npass, "fail": nfail,
            "items": [{"name": n, "ok": ok, "detail": d}
                      for n, ok, d in RESULTS],
        }, ensure_ascii=False, indent=1))
    sys.exit(0 if nfail == 0 else 1)


def _rd(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    main()
