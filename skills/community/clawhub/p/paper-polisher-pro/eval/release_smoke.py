#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""release_smoke.py — paper-polisher-pro 发布验收冒气电池（v3.5 起，随包发布）

设计原则（cite-holmes 五连发教训）：机器能查的必须变成机器查；断言读运行时真值，
绝不硬编码版本号。用法：
  python eval/release_smoke.py            # 全量
  python eval/release_smoke.py --fast     # 跳过重复次数多的探针

覆盖：
  A. 文档一致性     版本三处一致(SKILL.md/skill.json/发布)、frontmatter 语言断言、
                    旧营销宣称已清、文档引用的脚本都存在、触发词含 AI率
  B. 引擎行为       短文本铁律2(risk=unknown)、空文件优雅处理、确定性(两次同分)、
                    降级披露(degraded_mode/notice)、PP_NO_SUP 矩阵、英文语言门控
  C. 全脚本入口     term_check/translation_smell/quality_report/paragraph_report/
                    aigc_label_check/style_distance/deai_gate(--json)/pp_doctor
  D. CLI 纪律       --help 全部可用、缺文件报错不抛栈、deai_gate 无参数给用法
  E. 打包白名单预检  无扩展名文件/_meta.json/gif 不存在

输出: 逐项 [PASS]/[FAIL]，末行 "[汇总] ... -> GREEN/RED"；exit 0/1。
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
FAST = "--fast" in sys.argv

ZH_HUMAN = ("本研究采用前瞻性队列设计，共纳入2024年1月至2025年6月期间就诊的312例患儿。"
            "所有纳入对象均由两名副主任医师及以上职称者独立诊断，诊断符合率Kappa值为0.87。"
            "随访终点为首次复发，中位随访时间18.4个月，四分位距12.1至24.6。"
            "统计学分析使用Python完成，组间比较采用Mann-Whitney U检验，分类资料采用卡方检验。"
            "此外，我们还对亚组分析进行了敏感性检验，主要结论在不同模型设定下保持稳健，"
            "研究方案经医院伦理委员会审查批准，所有监护人签署知情同意书。")
ZH_SHORT = "这是一段很短的文本。"
EN_TEXT = ("This cohort study enrolled 312 consecutive patients between January 2024 and June 2025. "
           "Two senior physicians independently confirmed each diagnosis, with an inter-rater kappa of 0.87. "
           "The primary endpoint was first relapse, and the median follow-up was 18.4 months.")

results = []


def chk(name, ok, detail=""):
    results.append((name, bool(ok), str(detail)[:180]))
    print(("[PASS] " if ok else "[FAIL] ") + name + (f" | {detail}" if (detail and not ok) else ""))


def run_py(script, args, env_extra=None, timeout=180):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([sys.executable, str(SCRIPTS / script)] + args,
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout, env=env)
    return p.returncode, p.stdout or "", p.stderr or ""


def tmpfile(content):
    f = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
    f.write(content)
    f.close()
    return f.name


def detect_json(text, env_extra=None):
    path = tmpfile(text)
    try:
        rc, so, se = run_py("ai_detector.py", [path, "--format", "json"], env_extra=env_extra)
        return rc, (json.loads(so) if rc == 0 and so.strip() else None), se
    finally:
        Path(path).unlink(missing_ok=True)


# ───────────────────────── A. 文档一致性 ─────────────────────────
skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")
# v7.0.0 双语包自适应：CH 英文包按语言铁律不含 SKILL_ZH.md——smoke 必须在
# 两种包形态下都能跑（评监委实测点名词：英文包里 smoke 因硬读 SKILL_ZH 而失效）。
# ZH 在位=双语断言全跑；ZH 缺省=跳过并如实标注包形态。
skill_zh_path = ROOT / "SKILL_ZH.md"
HAS_ZH = skill_zh_path.is_file()
skill_zh = skill_zh_path.read_text(encoding="utf-8") if HAS_ZH else ""
skill_json = json.load(open(ROOT / "skill.json", encoding="utf-8"))

fm_md = re.match(r"^---\n(.*?)\n---\n", skill_md, re.S).group(1)
fm_zh = re.match(r"^---\n(.*?)\n---\n", skill_zh, re.S).group(1) if HAS_ZH else ""
ver_md = re.search(r"^version:\s*(\S+)", fm_md, re.M).group(1)


def has_cjk(s):
    return any("\u4e00" <= c <= "\u9fff" for c in s)

# v7.5.0 形态自检：打包副本里 HAS_ZH 恒 False（两种形态都无独立 SKILL_ZH.md），
# 按 SKILL.md 语言判形态（sh=中文版作 SKILL.md / ch=英文版）——内容断言据此分支。
FORM = "ch" if "30-second task routing" in skill_md else "sh"
IS_SH = FORM == "sh"
chk("包形态自检", FORM in ("ch", "sh"), f"FORM={FORM}")


if HAS_ZH:
    chk("版本三处一致(SKILL.md=SKILL_ZH=skill.json)",
        ver_md == re.search(r"^version:\s*(\S+)", fm_zh, re.M).group(1) == skill_json["version"],
        f"md={ver_md} json={skill_json['version']}")
else:
    chk("版本一致(SKILL.md=skill.json)［CH 英文包：SKILL_ZH 不在包内，双语断言自适应跳过］",
        ver_md == skill_json["version"],
        f"md={ver_md} json={skill_json['version']}")
chk("frontmatter 语言与形态匹配" + ("［SH 形态=中文版］" if IS_SH else ""),
    has_cjk(fm_md) if IS_SH else not has_cjk(fm_md))
chk("中文 frontmatter 含 CJK" + ("" if HAS_ZH else "［CH 英文包：自适应跳过］"),
    (not HAS_ZH) or has_cjk(fm_zh))
desc_md = " ".join(x.strip() for x in re.search(r"description: >-?\n((?:  .+\n)+)", skill_md).group(1).splitlines())
chk("EN description ≤1024 字符", len(desc_md) <= 1024, f"{len(desc_md)}")
if HAS_ZH:
    chk("ZH description ≤1024 字符",
        len(" ".join(x.strip() for x in re.search(r"description: >-?\n((?:  .+\n)+)", skill_zh).group(1).splitlines())) <= 1024)
else:
    chk("ZH description 断言［CH 英文包：自适应跳过］", True)
# v4.6.0: ZH frontmatter 增 metadata.displayName（10-05 全家族搜索审计任务要求, SH 页面一致性同步点）——EN 仍 ≤5
_k_en = len(re.findall(r"^(\w+):", fm_md, re.M))
_k_zh = len(re.findall(r"^(\w+):", fm_zh, re.M)) if HAS_ZH else 0
chk("frontmatter 键数" + ("（EN ≤5）" if not IS_SH else "（SH=中文版 ≤6）"),
    (_k_en <= 6) if IS_SH else (_k_en <= 5),
    f"EN={_k_en} ZH={_k_zh}")
_BANNED = ["全部100%检出", "10个模型测试", "100% detection rate", "detection rate: 100"]
def _banned_outside_quote(doc):
    # 旧宣称允许出现在"已删除/removed"引述行(铁律原文), 除此之外零容忍
    for line in doc.splitlines():
        if any(b in line for b in _BANNED) and not ("删" in line or "removed" in line):
            return line.strip()[:80]
    return None
chk("旧营销宣称已清(铁律引述行除外)",
    _banned_outside_quote(skill_zh) is None and _banned_outside_quote(skill_md) is None,
    f"zh={_banned_outside_quote(skill_zh)} en={_banned_outside_quote(skill_md)}")
chk("ZH 中 F1 98.3 仅出现在铁律引述(≤1处)", skill_zh.count("98.3") <= 1, f"count={skill_zh.count('98.3')}")
# v7.0.0 文档交叉一致闸（评监委 10-29 实测点名：Python 版本不一致/README 硬编码测试计数）
_req = (ROOT / "requirements.txt").read_text(encoding="utf-8") if (ROOT / "requirements.txt").is_file() else ""
_doc_py = re.findall(r"Python[ ]*3\.(\d)\+", _req + skill_md + (skill_zh if HAS_ZH else ""))
# v7.1.0 一致闸：标题禁版本化石（"v3" 标题与 7.x 实际版本脱节——评监委 10-30 点名）+ AUROC 口径锚定
_chk_title = re.search(r"^# (.+)$", skill_md, re.M)
chk("文档交叉一致: SKILL.md 标题不带版本号（版本历史管版本，标题管名字）",
    _chk_title and not re.search(r"\bv\d", _chk_title.group(1)),
    f"title={_chk_title.group(1) if _chk_title else '?'}")
# v7.2.0 一致闸补强：AUROC 1.0 残留清零（skill.json/SKILL_ZH 双处 10-31 评监委点名）
_skj = json.dumps(skill_json, ensure_ascii=False)
# v7.5.0: 架构层级数与正文一致（skill.json 曾写 11-layer 而正文已到 L12）
_l12_in_map = "L12" in skill_md or "L12" in (skill_zh if HAS_ZH else "")
chk("文档交叉一致: 架构层级计数对齐（skill.json 12-layer；正文含 L12）",
    "12-layer" in _skj and (_l12_in_map or not HAS_ZH),
    f"skj_ok={'12-layer' in _skj} l12={_l12_in_map}")
_zh_probe = skill_zh if HAS_ZH else ""
_readme_t = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
chk("文档交叉一致: AUROC 1.0 旧口径零残留（skill.json/SKILL_ZH/README 三处）",
    "AUROC 1.0" not in _skj and "AUROC 1.0" not in _zh_probe and "AUROC 1.0（作者侧实测）" not in _readme_t,
    "残留见发布日志")
# v7.2.0: eval/results 口径导航（CURRENT.md 对账——SKILL 引用的现行基线必须在表内且文件在位）
_cur = ROOT / "eval" / "results" / "CURRENT.md"
if _cur.is_file():
    _cur_t = _cur.read_text(encoding="utf-8")
    _listed = re.findall(r"`(v35ctl_[a-z0-9_.]+\.json)`", _cur_t)
    _missing = [f for f in _listed if not (ROOT / "eval" / "results" / f).is_file()]
    chk("口径导航: CURRENT.md 现行基线文件全部在位",
        bool(_listed) and not _missing, f"missing={_missing[:3]}")
    chk("口径导航: SKILL.md 引用的基线文件在 CURRENT.md 表内",
        all(f in _cur_t for f in ("v35ctl_oldgen", "v35ctl_gen2026")),
        "SKILL 引用的现行口径未入表")
    # v7.4.0 物理分层闸：results 顶层 json 必须全部在 CURRENT.md 表内（防历史文件再混存）
    _top_json = sorted(x.name for x in (ROOT / "eval" / "results").glob("*.json"))
    _uncited = [f for f in _top_json if f != "score_cache.json" and f not in _cur_t]
    chk("口径导航: results 顶层 json 全部入 CURRENT.md（物理分层对账）",
        not _uncited, f"uncited={_uncited[:3]}")
    _arch = list((ROOT / "eval" / "results" / "archive").glob("*.json"))
    chk("口径导航: archive/ 物理分层在位（历史文件已移入）",
        len(_arch) >= 25, f"archive={len(_arch)}")
    # v7.6.0 完整性清单闸：trunk 文件 vs INTEGRITY_MANIFEST 逐哈希对账
    _mf = ROOT / "data" / "INTEGRITY_MANIFEST.json"
    if _mf.is_file():
        import hashlib as _hlib
        _mfd = json.loads(_mf.read_text(encoding="utf-8"))
        _mm = []
        for _rel, _want in sorted(_mfd.get("files", {}).items()):
            _fp = ROOT / _rel
            if not _fp.is_file():
                _mm.append(f"{_rel}: 缺失")
            elif _hlib.sha256(_fp.read_bytes()).hexdigest() != _want.get("sha256"):
                _mm.append(f"{_rel}: 哈希漂移（清单过期？跑 eval/gen_integrity_manifest.py）")
        chk("完整性清单: trunk 与 INTEGRITY_MANIFEST 对账", not _mm,
            f"mismatch={_mm[:3]}")
    else:
        chk("完整性清单: INTEGRITY_MANIFEST 在位", False, "缺失")
    # v7.5.0: archive/README 口径纪律——禁旧"可复现基线"声明（10-31/11-04 两届评监委点名），必指 CURRENT.md
    _ar = ROOT / "eval" / "results" / "archive" / "README.md"
    if _ar.is_file():
        _ar_t = _ar.read_text(encoding="utf-8")
        # v7.7.0 可复现性闭环闸：生成器 --check（随包清单与生成器输出逐字节一致）
    _gen = ROOT / "eval" / "gen_integrity_manifest.py"
    if _gen.is_file() and _mf.is_file():
        _gc = subprocess.run([sys.executable, str(_gen), "--check"],
                             capture_output=True, text=True, timeout=60, cwd=str(ROOT))
        chk("可复现性闭环: gen_integrity_manifest --check 逐字节一致",
            _gc.returncode == 0, (_gc.stderr or _gc.stdout)[-160:])
    else:
        chk("可复现性闭环: 生成器在位", False, "eval/gen_integrity_manifest.py 缺失")
    _ar = ROOT / "eval" / "results" / "archive" / "README.md"
    if _ar.is_file():
        _ar_t = _ar.read_text(encoding="utf-8")
        chk("口径导航: archive/README 无旧口径声明且指向 CURRENT.md",
            "可复现基线" not in _ar_t and "CURRENT.md" in _ar_t
            and "不可作为现行口径引用" in _ar_t,
            f"has_old={'可复现基线' in _ar_t} has_pointer={'CURRENT.md' in _ar_t}")
    else:
        chk("口径导航: archive/README 在位", False, "缺失")
else:
    chk("口径导航: CURRENT.md 在位", False, "eval/results/CURRENT.md 缺失")
_auroc_md = "0.9998" in skill_md
_readme_t = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
# v7.5.0 形态自检：打包副本里 HAS_ZH 恒 False（两种形态都没有独立 SKILL_ZH.md），
# 按 SKILL.md 语言判形态（sh=中文版作 SKILL.md / ch=英文版），供内容断言形态感知。
chk("文档交叉一致: AUROC 声明锚定指纹绑定口径（0.9998 现行；README 禁裸 1.0）",
    _auroc_md and "0.9998" in _readme_t and "AUROC 1.0（作者侧实测）" not in _readme_t,
    f"md={_auroc_md} readme_ok={'0.9998' in _readme_t}")
chk("文档交叉一致: Python 最低版本统一（与 pp_doctor 门槛 3.9 同源）",
    _doc_py and all(x == "9" for x in _doc_py) and "3.8+" not in _req,
    f"declared={sorted(set(_doc_py)) or '无'}")
_readme = (ROOT / "README.md").read_text(encoding="utf-8") if (ROOT / "README.md").is_file() else ""
_bad_counts = re.findall(r"\d+\s*(?:用例|tests\b|个测试)", _readme)
chk("文档交叉一致: README 不硬编码测试计数（计数随版本增长，写法须动态）",
    not _bad_counts, f"hits={_bad_counts[:3]}")
# v7.3.0 一致闸：双语标题一致（无版本无旧营销尾注——SKILL_ZH 标题化石 10-31 评监委点名）
_t_en = re.search(r"^# (.+)$", skill_md, re.M)
_t_zh = re.search(r"^# (.+)$", skill_zh, re.M) if HAS_ZH else None
chk("文档交叉一致: 双语标题一致且无版本/旧尾注",
    _t_en and "v3" not in _t_en.group(1)
    and (not HAS_ZH or (_t_zh and _t_zh.group(1) == _t_en.group(1))),
    f"en={_t_en.group(1) if _t_en else '?'} zh={_t_zh.group(1) if _t_zh else 'NA'}")
# v7.3.0 一致闸：requirements 与文档 pip install 提及一致（regex 曾漏声明——评监委点名）
_req_mods = [m for m in ("onnxruntime", "regex", "numpy") if m + ">=" in _req]
_docs_t = skill_md + (skill_zh if HAS_ZH else "")
_missing_req = [m for m in _req_mods if m not in _docs_t]
chk("文档交叉一致: requirements 可选依赖在文档 pip install 行均有提及",
    bool(_req_mods) and not _missing_req, f"missing={_missing_req}")
chk("文档交叉一致: README 不硬编码测试计数（计数随版本增长，写法须动态）",
    not _bad_counts, f"hits={_bad_counts[:3]}")
chk("触发词含 AI率 词位" + ("（双语）" if HAS_ZH else "［CH 英文包］"),
    "AI率" in skill_md and (not HAS_ZH or "查AI率" in skill_zh))
chk("相关工具节在位" + ("（双语）" if HAS_ZH else f"［{FORM.upper()} 形态］"),
    (("## Related tools" in skill_md) if not IS_SH
     else ("## 相关工具" in skill_md))
    and (not HAS_ZH or "## 相关工具" in skill_zh))
_ADTALK = ["全家桶", "搜招牌名直达", "五件套", "论文工具家族", "Paper Toolbox family"]
_adtalk_hits = [w for w in _ADTALK if w in skill_md or w in skill_zh]
chk("导流叫卖词零残留(家族/全家桶/搜招牌名/五件套)", not _adtalk_hits, "; ".join(_adtalk_hits))
# v6.3.0: FAQ 独立成档——SKILL 保留高频三条+链接，完整分组与「具体技术问题」节在 references/faq.md
chk("FAQ 独立档案在位(SKILL 三条+faq.md 完整版" + ("（双语）" if HAS_ZH else f"［{FORM.upper()} 形态］"),
    (("## FAQ (top 3" in skill_md) if not IS_SH
     else ("## 常见问题（高频三条" in skill_md))
    and (not HAS_ZH or "## 常见问题（高频三条" in skill_zh)
    and (ROOT / "references" / "faq.md").is_file()
    and "具体技术问题" in (ROOT / "references" / "faq.md").read_text(encoding="utf-8"))
chk("脚本速查表在位(评测C维驱动" + ("（双语）" if HAS_ZH else f"［{FORM.upper()} 形态］"),
    (("Script cheat sheet" in skill_md) if not IS_SH
     else ("各脚本速查" in skill_md))
    and (not HAS_ZH or "各脚本速查" in skill_zh))
chk("FAQ 覆盖高频问法" + ("（双语）" if HAS_ZH else "［CH 英文包］"),
    "degraded_mode" in skill_md and (not HAS_ZH or ("知网" in skill_zh and "100 字" in skill_zh)))
for ref in set(re.findall(r"`?(\w+\.(?:py|json))`?", skill_md)):
    if ref.endswith(".py"):
        chk(f"文档引用脚本存在 {ref}", (SCRIPTS / ref).exists() or (ROOT / "eval" / ref).exists())

# ───────────────────────── B. 引擎行为 ─────────────────────────
rc, r, se = detect_json(ZH_SHORT)
chk("短文本铁律2: risk=unknown", rc == 0 and r and r["overall_risk"] == "unknown", f"rc={rc} risk={r and r.get('overall_risk')}")
chk("短文本含不判定提示", r and "100" in r.get("degraded_notice", "") + r.get("details", ""))

# v3.11: --batch 批处理模式探针
import shutil as _shutil
_bdir = Path(tempfile.mkdtemp())
(_bdir / "a.txt").write_text(ZH_HUMAN, encoding="utf-8")
(_bdir / "b.txt").write_text(ZH_SHORT, encoding="utf-8")
try:
    _rcb, sob, seb = run_py("ai_detector.py", ["--batch", str(_bdir), "--format", "json"])
    _okb = _rcb == 0
    if _okb:
        _jb = json.loads(sob)
        _okb = ("aggregate" in _jb and _jb["aggregate"]["files"] == 2
                and "integrity_notice" in _jb)
    chk("batch 模式(聚合+诚信字段)", _okb, f"rc={_rcb}")
finally:
    _shutil.rmtree(_bdir, ignore_errors=True)

rcn, rn, _ = detect_json(ZH_HUMAN)
# v4.1: batch CSV 探针
_cdir = Path(tempfile.mkdtemp())
(_cdir / "x.txt").write_text(ZH_HUMAN, encoding="utf-8")
_csvp = _cdir / "out.csv"
try:
    _rcc, soc, _ = run_py("ai_detector.py", ["--batch", str(_cdir), "--format", "json", "--csv", str(_csvp)])
    _okc = _rcc == 0 and _csvp.exists() and "ai_score" in _csvp.read_text(encoding="utf-8-sig")
    chk("batch CSV 输出", _okc, f"rc={_rcc}")
finally:
    _shutil.rmtree(_cdir, ignore_errors=True)

rcn, rn, _ = detect_json(ZH_HUMAN)
# v4.2: batch recursive 探针
_rdir = Path(tempfile.mkdtemp()) / "deep"
_rdir.mkdir(parents=True)
(_rdir / "nested.txt").write_text(ZH_HUMAN, encoding="utf-8")
try:
    _rcr, sor, _ = run_py("ai_detector.py", ["--batch", str(_rdir.parent), "--recursive", "--format", "json"])
    _okr = _rcr == 0 and "nested.txt" in sor and sor.count('"file"') >= 1
    chk("batch recursive 子目录遍历", _okr, f"rc={_rcr}")
finally:
    _shutil.rmtree(_rdir.parent, ignore_errors=True)

rcn, rn, _ = detect_json(ZH_HUMAN)
chk("学术样本篇章层零扰动", rcn == 0 and rn and not rn.get("discourse_hits") and rn.get("discourse_bonus", 0) == 0)

# v3.12: 层3复活+诚信覆盖探针
_TS = ("这部作品被给予了一个深刻的印象。作出了一个全面的分析。进行了认真的研究。"
       "一个优秀的方案被制定了出来，并且被实施了一个详细的计划。"
       "而在整个过程中，一个重要的角色被扮演了。本研究具有重要的理论意义。")
_fts = Path(tempfile.mkdtemp())
(_fts / "t.txt").write_text(_TS, encoding="utf-8")
try:
    _rg, gog, _ = run_py("deai_gate.py", [str(_fts / "t.txt"), "--json"])
    _ok3 = _rg == 0
    if _ok3:
        _gj = json.loads(gog)
        _n3 = _gj["layers"]["L3_translation_smell"]["note"]
        _ok3 = ("解析失败" not in _n3) and ("翻译腔命中" in _n3)
    chk("层3复活(翻译腔真实参与)", _ok3, f"note={_n3 if _ok3 else '解析失败'}")
finally:
    _shutil.rmtree(_fts, ignore_errors=True)
_int_scripts = ["style_distance.py", "translation_smell_check.py", "term_check.py", "quality_report.py"]
_int_hits = 0
_fti = tmpfile(ZH_HUMAN)
try:
    for _s in _int_scripts:
        _rci, _so, _se = run_py(_s, [_fti])
        if NOTICE_MARK := ("学术写作自查" in _so or "学术诚信" in _so):
            _int_hits += 1
    chk("诚信提示全报告覆盖(4脚本)", _int_hits == 4, f"命中 {_int_hits}/4")
finally:
    Path(_fti).unlink(missing_ok=True)

# v3.7.0: L12 篇章结构启发层探针（篇章三件套回归防护）
_DISC = ("先看一个场景。小林昨天拿到检测报告，数字比上个月低了不少。他盯着屏幕看了半天，心里直犯嘀咕："
         "这系统是不是换了比对库？同一段文字，前后两次测，一个说高一个说低。所以你看，不是谁退步了，是规则变了。"
         "把这句话记住：数字只是参考，别被一个报告定死。后来他调整了写法，第二天再测，数字果然回来了。")
rcd, rd, _ = detect_json(_DISC)
_disc_groups = sorted(h.get("group") for h in (rd or {}).get("discourse_hits", [])) if rd else []
chk("篇章三件套检出+加分", rcd == 0 and rd and rd.get("discourse_bonus", 0) >= 12
    and set(_disc_groups) >= {"钩子", "反转", "口号"}, f"groups={_disc_groups} bonus={rd and rd.get('discourse_bonus')}")
rcn, rn, _ = detect_json(ZH_HUMAN)
# v3.8: YAML 冒烟自检（doc-holmes 大忌: 行内值含"冒号+空格"致平台判"无有效 skill"）
for _nm, _fm in (("EN", fm_md), ("ZH", fm_zh)):
    _bad = [ln for ln in _fm.splitlines()
            if re.match(r"^\w+: .+", ln) and re.search(r":\s", ln.split(":", 1)[1])]
    chk(f"YAML 冒烟: {_nm} frontmatter 无行内冒号+空格", not _bad, "; ".join(_bad[:2]))
try:
    import yaml as _yaml
    for _nm, _fm in (("EN", fm_md),) if not HAS_ZH else (("EN", fm_md), ("ZH", fm_zh)):
        try:
            _parsed = _yaml.safe_load(_fm)
            _ok = isinstance(_parsed, dict) and isinstance(_parsed.get("description"), str) and len(_parsed["description"]) > 20
            chk(f"YAML 解析: {_nm} frontmatter 可解析且 description 有效", _ok)
        except Exception as _e:
            chk(f"YAML 解析: {_nm} frontmatter 可解析且 description 有效", False, str(_e)[:80])
except ImportError:
    chk("YAML 解析(pyyaml 未装, 跳过)", True)
chk("安全与行为声明节在位" + ("（双语）" if HAS_ZH else f"［{FORM.upper()} 形态］"),
    (("Safety and behavior statement" in skill_md) if not IS_SH
     else ("安全与行为声明" in skill_md))
    and (not HAS_ZH or "安全与行为声明" in skill_zh))


rc1, r1, _ = detect_json(ZH_HUMAN)
rc2, r2, _ = detect_json(ZH_HUMAN)
chk("长文本 JSON 可解析", rc1 == 0 and r1 and isinstance(r1.get("overall_ai_score"), (int, float)))
chk("确定性(两次同分)", rc1 == rc2 == 0 and r1["overall_ai_score"] == r2["overall_ai_score"],
    f"{r1 and r1.get('overall_ai_score')} vs {r2 and r2.get('overall_ai_score')}")
# v4.4.0: 模式感知——模型在位时默认态=完整模式(坏图时代的全绿恰恰因为模型死了, smoke 自己失明)
_sup_full = bool(r1 and r1.get("supervised"))
chk("降级披露一致性(模式与监督层在位互洽)", r1 and isinstance(r1.get("degraded_mode"), bool)
    and bool(r1.get("degraded_notice")) == r1["degraded_mode"]
    and r1["degraded_mode"] == (not _sup_full),
    f"degraded_mode={r1 and r1.get('degraded_mode')} supervised={'有' if _sup_full else '无'}")
# 降级警示文本: 用 PP_NO_SUP=1 强制降级态验证(与模型是否在位无关)
rc1d, r1d, _ = detect_json(ZH_HUMAN, env_extra={"PP_NO_SUP": "1"})
chk("降级警示含医学语域数字", rc1d == 0 and r1d and r1d.get("degraded_mode") is True
    and "59" in (r1d.get("degraded_notice") or ""),
    f"notice={r1d and (r1d.get('degraded_notice') or '')[:60]}")
chk("学术诚信护栏(integrity_notice)", bool(r1.get("integrity_notice")) and "披露" in r1["integrity_notice"] + r1.get("details", ""))

# v3.8: 混写预警/语域提示/编码警示探针
_MIXED = ("值得注意的是，本研究具有重要的理论意义与实践价值。首先，我们系统性地梳理了相关领域的研究脉络；"
          "其次，我们提出了一个创新性的分析框架；最后，我们的研究结论为后续研究奠定了坚实的基础。综上所述，"
          "这项研究不仅拓展了学科边界，也为实际应用提供了有力支撑。与此同时，方法的严谨性与数据的可靠性"
          "进一步增强了结论的说服力。\n\n"
          "说实话这个方案我们组里吵了三天。老张觉得采样太少，我倒觉得先跑起来再说，"
          "反正数据在那儿摆着，不行再改呗。昨天跑完第一版，效果一般般吧，但至少能看。")
rcm, rm, _ = detect_json(_MIXED)
chk("混写预警触发(mixed_signal)", rcm == 0 and rm and rm.get("mixed_signal") is True and "混写" in (rm.get("mixed_notice") or ""))
_COLLOQ = ("今天这事儿整得挺离谱的哈。早上跟老王说了这事儿，他说你咋不早讲呢，嘛呀这是。"
           "中午吃饭的时候大家又开始聊，说实话搞了半天就这么点事，挺好的结果算是落地了呗。")
rcg, rg, _ = detect_json(_COLLOQ)
chk("语域提示触发(register_hint)", rcg == 0 and rg and "口语" in (rg.get("register_hint") or ""))
rcn, rn, _ = detect_json(ZH_HUMAN)
chk("正常学术样本无误报", rcn == 0 and rn and not rn.get("mixed_signal") and not rn.get("register_hint") and not rn.get("encoding_warning"))
_gbk2 = Path(tempfile.gettempdir()) / f"pp_gbk_warn_{os.getpid()}.txt"
_gbk2.write_bytes(ZH_HUMAN.encode("utf-8", errors="replace").decode("utf-8", errors="ignore").encode("utf-8"))
try:
    _raw = (ZH_HUMAN[:40] + "\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd\ufffd") * 6
    _f2 = tmpfile(_raw)
    try:
        rcw, rw, _ = detect_json(_raw)
        chk("编码警示触发(encoding_warning)", rcw == 0 and rw and bool(rw.get("encoding_warning")))
    finally:
        Path(_f2).unlink(missing_ok=True)
finally:
    _gbk2.unlink(missing_ok=True)
rcg8, rg8, _ = detect_json(ZH_HUMAN)
_g8 = tmpfile(ZH_HUMAN)
try:
    rcgj, sog, _ = run_py("deai_gate.py", [_g8, "--json"])
    okg = rcgj == 0
    if okg:
        gj = json.loads(sog)
        okg = "layer_divergence" in gj
    chk("门禁层间分歧字段在位", okg, f"rc={rcgj}")
finally:
    Path(_g8).unlink(missing_ok=True)

# v3.6 补: CH 读取面(EN SKILL.md + skill.json)平台政策禁词表——campaign 教训固化为机器检查
# (negated integrity statements 中的 evade/evasion 属声明性用法, 刻意不在禁词表——见 SKILL.md Academic integrity 节)
_BAN = ["朱雀", "gptzero", "turnitin", "过检测", "过ai检测", "降检测率", "去ai痕迹", "humanize",
        "remove ai traces", "reduce ai detection", "过朱雀", "bypass"]
_ch_surface = (skill_md + json.dumps(skill_json, ensure_ascii=False)).lower()
_hits = [w for w in _BAN if w in _ch_surface]
chk("CH 面禁词表(朱雀/GPTZero/Turnitin/humanize/evade短语)", not _hits, "命中: " + ",".join(_hits))
chk("接口兼容: overall_ai_score 字段(管线依赖)", r1 and "overall_ai_score" in r1 and "supervised" in r1)

rc3, r3, _ = detect_json(ZH_HUMAN, env_extra={"PP_NO_SUP": "1"})
chk("PP_NO_SUP 矩阵: rc=0 且与强制降级态同分(可复现)", rc3 == 0 and r3 and r1d and
    r3["overall_ai_score"] == r1d["overall_ai_score"],
    f"no_sup={r3 and r3.get('overall_ai_score')} vs forced={r1d and r1d.get('overall_ai_score')}")

# v3.5 补: 中文 Windows GBK 环境矩阵(默认 zh-CN 控制台, 多专家对抗测试发现的 P0 回归防护)
_gbk_f = tmpfile(ZH_HUMAN)
try:
    rc, so, se = run_py("ai_detector.py", [_gbk_f, "--format", "summary"], env_extra={"PYTHONIOENCODING": "gbk"})
    chk("GBK stdout 矩阵: summary 不崩", rc == 0, f"rc={rc} {se[:80]}")
    rc, so, se = run_py("ai_detector.py", [_gbk_f, "--format", "json"], env_extra={"PYTHONIOENCODING": "gbk"})
    chk("GBK stdout 矩阵: json 不崩", rc == 0 and so.strip().startswith("{"), f"rc={rc} {se[:80]}")
    rc, so, se = run_py("deai_gate.py", [_gbk_f], env_extra={"PYTHONIOENCODING": "gbk"})
    chk("GBK stdout 矩阵: deai_gate 不崩", rc == 0, f"rc={rc} {se[:80]}")
finally:
    Path(_gbk_f).unlink(missing_ok=True)
_gbk_in = Path(tempfile.gettempdir()) / f"pp_gbk_in_{os.getpid()}.txt"
_gbk_in.write_bytes((ZH_HUMAN + "补充一句长度。") .encode("gbk"))
try:
    rc, so, se = run_py("ai_detector.py", [str(_gbk_in), "--format", "json"])
    chk("GBK 编码输入容错(rc=0)", rc == 0, f"rc={rc} {se[:80]}")
finally:
    _gbk_in.unlink(missing_ok=True)

rc4, r4, _ = detect_json(EN_TEXT)
chk("英文文本 rc=0 且语言门控披露", rc4 == 0 and r4 and "language gating" in (r4.get("degraded_notice") or ""),
    f"notice={r4 and (r4.get('degraded_notice') or '')[:60]}")

empty_f = tmpfile("")
try:
    p = subprocess.run([sys.executable, str(SCRIPTS / "ai_detector.py"), empty_f, "--format", "json"],
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    chk("空文件优雅处理", p.returncode == 0 and "unknown" in (p.stdout or ""))
finally:
    Path(empty_f).unlink(missing_ok=True)

# ───────────────────────── C. 全脚本入口 ─────────────────────────
zh_f = tmpfile(ZH_HUMAN)
try:
    rc, so, se = run_py("term_check.py", [zh_f])
    chk("term_check rc=0", rc == 0, f"rc={rc} {se[:80]}")
    rc, so, se = run_py("term_check.py", [zh_f, "--auto-fix"])
    chk("term_check --auto-fix rc=0", rc == 0, f"rc={rc}")
    rc, so, se = run_py("translation_smell_check.py", [zh_f, "--json"])
    ok = rc == 0
    if ok:
        try:
            json.loads(so)
        except Exception:
            ok = False
    chk("translation_smell --json 可解析", ok, f"rc={rc} out={so[:60]}")
    rc, so, se = run_py("quality_report.py", [zh_f, "--format", "json"])
    ok = rc == 0
    if ok:
        try:
            json.loads(so)
        except Exception:
            ok = False
    chk("quality_report --format json 可解析", ok, f"rc={rc}")
    rc, so, se = run_py("quality_report.py", [zh_f])
    chk("quality_report text 含 AI 痕迹行", rc == 0 and "AI痕迹" in so)
    rc, so, se = run_py("style_distance.py", [zh_f, "--json"])
    chk("style_distance --json rc=0", rc == 0, f"rc={rc} {se[:60]}")
    out_html = Path(tempfile.gettempdir()) / f"pp_smoke_{os.getpid()}.html"
    rc, so, se = run_py("paragraph_report.py", [zh_f, "--output", str(out_html)])
    chk("paragraph_report 产出 HTML", rc == 0 and out_html.exists() and out_html.stat().st_size > 500,
        f"rc={rc} exists={out_html.exists()}")
    out_html.unlink(missing_ok=True)
    rc, so, se = run_py("aigc_label_check.py", [zh_f])
    # rc 语义: 0=有合规标识; 1=无标识(检查结果,非错误); 2+=真错误
    chk("aigc_label_check 正常执行(rc∈{0,1})", rc in (0, 1), f"rc={rc} {se[:60]}")
    rc, so, se = run_py("deai_gate.py", [zh_f, "--json"])
    ok = rc == 0
    if ok:
        try:
            g = json.loads(so)
            ok = "composite_ai_risk" in g and "verdict" in g
        except Exception:
            ok = False
    chk("deai_gate --json 四层融合可解析", ok, f"rc={rc} out={so[:80]}")
    rc, so, se = run_py("pp_doctor.py", [])
    chk("pp_doctor 全量自检 GREEN", rc == 0 and "-> GREEN" in so, f"rc={rc}")
finally:
    Path(zh_f).unlink(missing_ok=True)

# ───────────────────────── D. CLI 纪律 ─────────────────────────
for script in ["ai_detector.py", "term_check.py", "quality_report.py", "style_distance.py",
               "translation_smell_check.py", "paragraph_report.py", "aigc_label_check.py", "pp_doctor.py"]:
    rc, so, se = run_py(script, ["--help"])
    chk(f"--help 正常 {script}", rc == 0 and ("usage" in (so + se).lower() or "用法" in (so + se)), f"rc={rc}")
rc, so, se = run_py("deai_gate.py", ["--help"])
chk("--help 正常 deai_gate.py(v3.5 守卫)", rc == 0 and "用法" in so, f"rc={rc}")
rc, so, se = run_py("deai_gate.py", [])
chk("deai_gate 无参数给用法(rc=2)", rc == 2 and "用法" in (so + se), f"rc={rc}")
rc, so, se = run_py("ai_detector.py", ["no_such_file.txt"])
chk("缺文件报错不抛栈", rc != 0 and "Traceback" not in se, f"rc={rc}")

# ───────────────────────── E. 打包白名单预检 ─────────────────────────
bad = []
for f in ROOT.rglob("*"):
    if f.is_file():
        rel = f.relative_to(ROOT).as_posix()
        if "__pycache__" in rel or ".bak" in rel or rel.startswith(".git/") or rel == ".gitignore":
            continue
        if not f.suffix:
            bad.append(f"无扩展名: {rel}")
        if f.name == "_meta.json":
            bad.append(f"_meta.json: {rel}")
        if f.suffix.lower() == ".gif":
            bad.append(f"gif: {rel}")
chk("SH 白名单预检(无扩展名/_meta.json/gif)", not bad, "; ".join(bad[:3]))

# ───────────────────────── F. 可编程接口（v4.5.0） ─────────────────────────
import shutil as _shutil_f
try:
    sys.path.insert(0, str(SCRIPTS))
    import pp_api as _API
    _d = _API.detect_text(ZH_HUMAN, lang="zh")
    chk("SDK import + detect_text 出分", isinstance(_d.get("overall_ai_score"), (int, float)),
        f"score={_d.get('overall_ai_score')}")
    # 与 CLI 位级同源（同一 detect 代码路径）
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _f:
        _f.write(ZH_HUMAN); _cli_f = _f.name
    _rc, _so, _se = run_py("ai_detector.py", [_cli_f, "--format", "json"])
    Path(_cli_f).unlink(missing_ok=True)
    _cli_score = json.loads(_so).get("overall_ai_score") if _rc == 0 else None
    chk("SDK detect_text 与 CLI 同分（同源校验）",
        _cli_score is not None and _cli_score == _d.get("overall_ai_score"),
        f"sdk={_d.get('overall_ai_score')} cli={_cli_score}")
    _g = _API.gate_text(ZH_HUMAN)
    chk("SDK gate_text 出复合分", isinstance(_g.get("composite_ai_risk"), (int, float))
        and _g.get("verdict") in ("pass", "review", "ai_suspect"),
        f"composite={_g.get('composite_ai_risk')}")
    _doc = _API.doctor_summary()
    chk("SDK doctor_summary 档位+版本", _doc.get("engine_mode") in ("full", "degraded")
        and isinstance(_doc.get("version"), str),
        f"mode={_doc.get('engine_mode')} v={_doc.get('version')}")
    # 终审 NO-GO 修复回归: doctor_summary 的 data_files_ok 在健康机器上必须 True
    chk("SDK doctor_summary data_files_ok", _doc.get("data_files_ok") is True,
        f"data_files_ok={_doc.get('data_files_ok')} missing={_doc.get('data_missing')}")
    # 终审 NO-GO 修复回归: smell_report 有命中时必须 JSON 可序列化
    import json as _json_f
    _hit_text = "这个问题的结果被进行了详细的分析和讨论。"
    _sr = _API.smell_report(_hit_text)
    _json_f.dumps(_sr)  # 不序列化即抛
    chk("SDK smell_report JSON 可序列化（含命中）", _sr.get("total_hits", 0) >= 1
        and isinstance(_sr["hits"][0], dict),
        f"total_hits={_sr.get('total_hits')}")
    # v4.6.0: 端到端 workflow
    _wf = _API.workflow(ZH_HUMAN, lang="zh")
    _json_f.dumps(_wf)
    _need = ("detect", "paragraphs", "gate", "terms", "smell", "style", "quality", "aigc_label")
    chk("SDK workflow 全键+JSON 可序列化", all(k in _wf for k in _need)
        and _wf["detect"].get("overall_ai_score") is not None
        and _wf["paragraphs"].get("total", 0) >= 1,
        f"keys={sorted(_wf)}")
    # 终审 NO-GO 修复回归: MD 报告质量报告节必须非空（键名错配曾致恒空）
    import pp_workflow as _PWf
    _md = _PWf.to_markdown(_wf)
    _sec6 = _md.split("## 6. 质量报告")[-1].split("##")[0].strip()
    chk("workflow MD 质量报告节非空", len(_sec6) > 20, f"sec6len={len(_sec6)}")
    # v4.7.0: 混写文档评估块（人写段夹 AI 段 → mixed_document.detected 必须 True）
    _hu = ("本研究采用前瞻性队列设计，共纳入2024年1月至2025年6月期间就诊的312例患儿。"
           "所有纳入对象均由两名副主任医师及以上职称者独立诊断，诊断符合率Kappa值为0.87。"
           "随访终点为首次复发，中位随访时间18.4个月，四分位距12.1至24.6。"
           "统计学分析使用Python完成，组间比较采用Mann-Whitney U检验，分类资料采用卡方检验。")
    _ai = ("值得注意的是，本研究具有重要的理论意义与实践价值。首先，我们系统性地梳理了相关领域的研究脉络，"
           "为后续研究奠定了坚实的基础。其次，本研究采用了多元化的研究方法，确保了结论的可靠性和普适性。"
           "总而言之，这项研究不仅填补了学术空白，更为实践应用提供了强有力的支撑和指导。")
    _wm = _API.workflow(_hu + "\n\n" + _ai + "\n\n" + _hu.replace("312", "286"), lang="zh")
    _json_f.dumps(_wm)
    chk("workflow 混写评估块（夹心文档 detected=True+校准字段在位）",
        _wm.get("mixed_document", {}).get("detected") is True
        and _wm["mixed_document"].get("measured", {}).get("paragraph_level_auroc") == 0.6883
        and _wm["mixed_document"].get("measured", {}).get("calibrated_high_threshold") is not None,
        f"detected={_wm.get('mixed_document', {}).get('detected')} "
        f"calibrated={_wm.get('mixed_document', {}).get('measured', {}).get('calibrated_high_threshold')}")
    # v4.7.0 求星合规铺设: MD 交付物页脚恰好一次（同一产物仅一次纪律）
    _foot = "觉得有用欢迎 Star / 收藏"
    chk("workflow MD 页脚恰好一次（求星合规）", _md.count(_foot) == 1,
        f"count={_md.count(_foot)}")
    # v4.8.0: journal+json 纯度（第三方测试 Bug#8 回归）与 risk_bands 透出（发现#4）
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _hf:
        _hf.write(ZH_HUMAN); _hu_file_hold = _hf.name
    _p = subprocess.run([sys.executable, str(SCRIPTS / "ai_detector.py"), _hu_file_hold,
                         "--profile", "journal", "--format", "json"],
                        capture_output=True, text=True, encoding="utf-8", timeout=180,
                        env={**os.environ, "PP_ORT_THREADS": "8"})
    try:
        _jd = json.loads(_p.stdout)
        _ok_j = _jd.get("journal_precheck") is not None and _jd.get("risk_bands") is not None
    except Exception:
        _ok_j = False
    chk("journal+json 纯度且 risk_bands 透出", _ok_j,
        f"rc={_p.returncode} parse={'ok' if _ok_j else 'FAIL'}")
    Path(_hu_file_hold).unlink(missing_ok=True)
    # v4.9.0: pp.py 统一入口路由
    _pp = subprocess.run([sys.executable, str(SCRIPTS / "pp.py")],
                         capture_output=True, text=True, encoding="utf-8", timeout=60)
    _pp_bad = subprocess.run([sys.executable, str(SCRIPTS / "pp.py"), "no-such-cmd"],
                             capture_output=True, text=True, encoding="utf-8", timeout=60)
    chk("pp.py 统一入口（列表+未知命令 rc=2）",
        _pp.returncode == 0 and "detect" in _pp.stdout and _pp_bad.returncode == 2,
        f"rc={_pp.returncode}/{_pp_bad.returncode}")
    # v5.9.0: 脚本头部不得有游离的旧式独立版本号（内部版本与包版本漂移=标注性瑕疵类，评监委点名）
    import re as _re_v
    _stray = [p_.name for p_ in sorted(SCRIPTS.glob("*.py"))
              if _re_v.search(r"paper-polisher( pro)? v\d+\.\d+",
                              chr(10).join(p_.read_text(encoding="utf-8", errors="replace").splitlines()[:6]))]
    chk("脚本头部无游离版本号", not _stray, f"{_stray}")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _rf:
        _rf.write(ZH_HUMAN); _route_f = _rf.name
    _pp_d = subprocess.run([sys.executable, str(SCRIPTS / "pp.py"), "detect", _route_f,
                            "--format", "json"], capture_output=True, text=True,
                           encoding="utf-8", timeout=180,
                           env={**os.environ, "PP_ORT_THREADS": "8"})
    Path(_route_f).unlink(missing_ok=True)
    try:
        _route_ok = _pp_d.returncode == 0 and isinstance(json.loads(_pp_d.stdout).get("overall_ai_score"), (int, float))
    except Exception:
        _route_ok = False
    chk("pp.py detect 路由可达引擎", _route_ok,
        f"rc={_pp_d.returncode}")
except Exception as _e:
    chk("SDK import + detect_text 出分", False, f"exception: {_e}")

# pp_setup: --check 与未知指纹拒绝
try:
    _p = subprocess.run([sys.executable, str(SCRIPTS / "pp_setup.py"), "--check"],
                        capture_output=True, text=True, encoding="utf-8", timeout=180,
                        env={**os.environ, "PP_ORT_THREADS": "8"})
    chk("pp_setup --check 可跑", _p.returncode in (0, 1), f"rc={_p.returncode}")
    _fake = Path(tempfile.mkdtemp()) / "fake.onnx"
    _fake.write_bytes(b"not a model")
    _p2 = subprocess.run([sys.executable, str(SCRIPTS / "pp_setup.py"), "--model", str(_fake)],
                         capture_output=True, text=True, encoding="utf-8", timeout=120)
    chk("pp_setup 未知指纹拒绝(exit 2)", _p2.returncode == 2, f"rc={_p2.returncode}")
    _shutil_f.rmtree(_fake.parent, ignore_errors=True)
except Exception as _e:
    chk("pp_setup --check 可跑", False, f"exception: {_e}")

# 零网络契约在新增接口上依然成立（SKILL.md 的 grep 零命中承诺）
import re as _re
_bad_net = []
for _n in ("pp_api.py", "pp_setup.py"):
    _src = (SCRIPTS / _n).read_text(encoding="utf-8")
    if _re.search(r"import\s+(socket|http|urllib|requests)|from\s+(socket|http|urllib|requests)", _src):
        _bad_net.append(_n)
chk("SDK/装模零网络导入", not _bad_net, "; ".join(_bad_net))

# ───────────────────────── G. 可信验证与改写建议（v5.0.0） ─────────────────────────
# G1. pp_verify 结构化零网络自证：正例（本包 scripts）干净
_rcv, _sov, _sev = run_py("pp_verify.py", ["--json"])
try:
    _vjson = json.loads(_sov)
except Exception:
    _vjson = {}
chk("pp_verify: 本包零网络(AST)", _rcv == 0 and _vjson.get("zero_network") is True
    and _vjson.get("files_scanned", 0) >= 20,
    f"rc={_rcv} zero_network={_vjson.get('zero_network')} files={_vjson.get('files_scanned')}")

# G2. pp_verify 负例：合成违规必须命中，URL 字符串必须放行
import shutil as _shutil_g
_tmpv = Path(tempfile.mkdtemp(prefix="smoke_v500_"))
try:
    (_tmpv / "bad.py").write_text("import urllib.request\nurllib.request.urlopen('http://x')\n",
                                  encoding="utf-8")
    _rcb, _sob, _ = run_py("pp_verify.py", ["--dir", str(_tmpv), "--json"])
    (_tmpv / "bad.py").unlink()
    (_tmpv / "ok.py").write_text('URL = "https://example.com/x"\nimport urllib.parse\n'
                                 "print(URL, urllib.parse.quote('论文'))\n", encoding="utf-8")
    _rco, _soo, _ = run_py("pp_verify.py", ["--dir", str(_tmpv), "--json"])
    chk("pp_verify: 违规命中 rc=1", _rcb == 1, f"rc={_rcb}")
    chk("pp_verify: URL字符串数据不误报 rc=0", _rco == 0, f"rc={_rco} out={_soo[:120]}")
finally:
    _shutil_g.rmtree(_tmpv, ignore_errors=True)

# G3. pp_fix_suggest：AI 感样例命中、人类感样例零命中、短文本拒绝、demo 可跑
_DEMO_AI = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。"
            "具体而言，AI 不仅能够提高诊断效率，而且可以优化治疗方案的制定。"
            "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。"
            "在一定程度上，数据安全问题的存在对行业发展产生了一定的制约。"
            "综上所述，本研究为该领域的进一步探索提供了一定的参考价值。"
            "此外，本研究仍存在一定局限性，未来需要进一步扩大样本量予以验证。")
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _f:
    _f.write(_DEMO_AI); _fx_ai = _f.name
_rcf1, _sof1, _ = run_py("pp_fix_suggest.py", [_fx_ai, "--json"])
Path(_fx_ai).unlink(missing_ok=True)
try:
    _fx = json.loads(_sof1)
except Exception:
    _fx = {}
_fs = (_fx.get("stats") or {})
chk("fix_suggest: AI样例命中", _rcf1 == 0 and _fs.get("flagged_sentences", 0) >= 3
    and "integrity_notice" in _fx,
    f"flagged={_fs.get('flagged_sentences')}/{_fs.get('total_sentences')}")
_HUMAN_DEMO = ZH_HUMAN
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _f:
    _f.write(_HUMAN_DEMO); _fx_hu = _f.name
_rcf2, _sof2, _ = run_py("pp_fix_suggest.py", [_fx_hu, "--json"])
Path(_fx_hu).unlink(missing_ok=True)
try:
    _fsh = json.loads(_sof2).get("stats") or {}
except Exception:
    _fsh = {}
chk("fix_suggest: 学术人类样例零命中", _rcf2 == 0 and _fsh.get("flagged_sentences") == 0,
    f"flagged={_fsh.get('flagged_sentences')}")
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _f:
    _f.write("太短。"); _fx_st = _f.name
_rcf3, _, _sef3 = run_py("pp_fix_suggest.py", [_fx_st])
Path(_fx_st).unlink(missing_ok=True)
chk("fix_suggest: 短文本拒绝(rc=2)", _rcf3 == 2 and "100" in _sef3, f"rc={_rcf3}")
_rcf4, _sof4, _ = run_py("pp_fix_suggest.py", ["--demo"])
chk("fix_suggest: --demo 双样例可跑", _rcf4 == 0 and "样例 A" in _sof4 and "样例 B" in _sof4,
    f"rc={_rcf4}")

# G4. workflow 的 fix_suggest 块 + MD 第 3 节
try:
    _wfr = _API.workflow(_DEMO_AI)
    _wfstats = ((_wfr.get("fix_suggest") or {}).get("stats") or {})
    chk("workflow: fix_suggest 块在位", bool(_wfstats), f"keys={bool(_wfstats)}")
except Exception as _e:
    chk("workflow: fix_suggest 块在位", False, f"exception: {_e}")

# G5. pp.py 路由：新子命令注册 + 未知命令 rc=2 + quickstart 三步
_ppe = subprocess.run([sys.executable, str(SCRIPTS / "pp.py")], capture_output=True,
                      text=True, encoding="utf-8")
chk("pp.py 入口: fix/verify/test/quickstart 已注册",
    _ppe.returncode == 0 and all(w in _ppe.stdout for w in ("fix", "verify", "test", "quickstart")))
_ppu = subprocess.run([sys.executable, str(SCRIPTS / "pp.py"), "no-such"], capture_output=True,
                      text=True, encoding="utf-8")
chk("pp.py 未知子命令 rc=2", _ppu.returncode == 2)

# G6. 语域感知 2.0：文学叙事提示、学术样本不受扰
_NARR = ("我翻开历史一查，这历史没有年代，歪歪斜斜的每页上都写着仁义道德几个字。"
         "我横竖睡不着，仔细看了半夜，才从字缝里看出字来，满本都写着两个字是吃人！"
         "那时候，大哥还在。母亲常对我说：你应当去。那天他忽然来了，"
         "我心里一沉，眼泪几乎要落下来。老爷说这没有什么可笑。"
         "第二天一早，他拎着包走了，我到现在还记得那天清晨的凉。")
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _f:
    _f.write(_NARR); _nr = _f.name
_rcn2, _son2, _ = run_py("ai_detector.py", [_nr, "--format", "json"])
Path(_nr).unlink(missing_ok=True)
try:
    _rn2 = json.loads(_son2)
except Exception:
    _rn2 = {}
chk("语域2.0: 文学叙事提示触发", _rcn2 == 0 and "文学叙事" in (_rn2.get("register_hint") or "")
    and "勿当作 AI 生成证据" in (_rn2.get("register_hint") or ""))
chk("语域2.0: 学术样本无叙事提示", "文学叙事" not in (r1.get("register_hint") or ""))

# G7. doctor 保鲜可见化 + requirements.txt 在位
_rcd2, _sod2, _ = run_py("pp_doctor.py", [])
chk("doctor: 最近评测记录行", _rcd2 == 0 and "最近留出集评测记录" in _sod2)
chk("requirements.txt 在位且声明可选依赖",
    (ROOT / "requirements.txt").exists()
    and "onnxruntime" in (ROOT / "requirements.txt").read_text(encoding="utf-8"))

# G8. CHANGELOG 节序锁（英/中两区均严格降序 + 顶部为当前版本）
import re as _re2
_tcl = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

def _vk(_s):
    _m = _re2.search(r"(\d+)\.(\d+)\.(\d+)", _s)
    return tuple(map(int, _m.groups())) if _m else (0, 0, 0)

def _order_ok(_body):
    _vs = [_vk(m.group(0)) for m in _re2.finditer(r"^## .+$", _body, _re2.M)]
    return len(_vs) >= 10 and all(_vs[i] > _vs[i + 1] for i in range(len(_vs) - 1)), _vs[:3]

_zh_i = _tcl.index("# 更新日志（中文）")
_en_ok, _en_top = _order_ok(_tcl[:_zh_i])
_zh_ok, _zh_top = _order_ok(_tcl[_zh_i:])
chk("CHANGELOG 双语节序严格降序", _en_ok and _zh_ok, f"EN top={_en_top} ZH top={_zh_top}")
_cur = _vk(json.load(open(ROOT / "skill.json", encoding="utf-8"))["version"])
chk("CHANGELOG 顶部为当前版本(EN/ZH)", _en_top[:1] == [_cur] and _zh_top[:1] == [_cur],
    f"EN={_en_top[:1]} ZH={_zh_top[:1]}")

# G9. 包内测试套件可发现且全绿（计数只看规模下限，避免脆弱绑定）
try:
    # v6.9.0 机制化：超时上限随套件规模自适应（420→900→公式），套件每增一个
    # 版本测试文件自动 +75s——不再每次撞墙手调。基线 420s + 每文件 75s。
    _ntestfiles = len(list((ROOT / "tests").glob("test_*.py")))
    _ut_timeout = 420 + 75 * _ntestfiles
    _ut_env = dict(os.environ, PP_IN_SMOKE="1")  # v7.0.0: 嵌套标记（防 smoke→单测→smoke 套娃）
    _ut = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests",
                          "-t", "."], capture_output=True, text=True, encoding="utf-8",
                         cwd=str(ROOT), timeout=_ut_timeout, env=_ut_env)
    _m = _re2.search(r"Ran (\d+) tests", _ut.stderr + _ut.stdout)
    _ntests = int(_m.group(1)) if _m else 0
    _failnames = _re.findall(r"^(?:FAIL|ERROR): .*$", (_ut.stderr or "") + (_ut.stdout or ""), _re.M)
    chk("包内单测全绿", _ut.returncode == 0 and _ntests >= 40,
        f"rc={_ut.returncode} ran={_ntests} names={_failnames[:3]}")
except Exception as _e:
    chk("包内单测全绿", False, f"exception: {_e}")

# ───────────────────────── H. 改写闭环与批量报告（v5.1.0） ─────────────────────────
# H1. rewrite_check：演示对（AI 稿→具体化重写稿，实测 98.1/high→30.4/low）应降分且风险带迁移；同稿对比零变化
try:
    import pp_rewrite_check as _rwc_mod
    _rwc = _API.rewrite_check(_rwc_mod._DEMO_ORIG, _rwc_mod._DEMO_REV)
    _rwd = _rwc["document"]
    chk("rewrite_check: 改稿降分+风险带迁移",
        _rwd["original_score"] > _rwd["revised_score"] and _rwd["risk_moved"] is True,
        f"{_rwd['original_score']}({_rwd['original_risk']}) → {_rwd['revised_score']}({_rwd['revised_risk']})")
    _rwc2 = _API.rewrite_check(ZH_HUMAN, ZH_HUMAN)
    chk("rewrite_check: 同稿对比零变化", _rwc2["document"]["delta"] == 0.0
        and _rwc2["document"]["risk_moved"] is False)
    chk("rewrite_check: 特征 delta 键齐全",
        all(all(k in x for k in ("type", "original", "revised", "change"))
            for x in _rwc["features"]["delta_by_type"]))
except Exception as _e:
    chk("rewrite_check: 改稿降分+风险带迁移", False, f"exception: {_e}")

# H2. rewrite_check CLI：--json 与短文本拒绝
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _f:
    _f.write(_DEMO_AI); _rw_o = _f.name
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _f:
    _f.write(ZH_HUMAN); _rw_r = _f.name
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _f:
    _f.write("短"); _rw_s = _f.name
_rwr1, _sow1, _ = run_py("pp_rewrite_check.py", [_rw_o, _rw_r, "--json"])
try:
    _rwj = json.loads(_sow1)
except Exception:
    _rwj = {}
chk("rewrite_check CLI: --json 契约", _rwr1 == 0 and "edit_extent" in _rwj
    and "integrity_notice" in _rwj, f"rc={_rwr1}")
_rwr2, _, _sew2 = run_py("pp_rewrite_check.py", [_rw_s, _rw_r])
Path(_rw_o).unlink(missing_ok=True); Path(_rw_r).unlink(missing_ok=True); Path(_rw_s).unlink(missing_ok=True)
chk("rewrite_check CLI: 短文本拒绝 rc=2", _rwr2 == 2 and "100" in _sew2, f"rc={_rwr2}")

# H3. batch_report：合成 CSV 直测渲染器（确定性，不依赖引擎给样例打的分数）
_tmpb = Path(tempfile.mkdtemp(prefix="smoke_v510_"))
try:
    with open(_tmpb / "scores.csv", "w", encoding="utf-8-sig", newline="") as _cf:
        import csv as _csv_h
        _w = _csv_h.writer(_cf)
        _w.writerow(["file", "ai_score", "risk", "language", "degraded_mode"])
        _w.writerow(["high_first.txt", "90.0", "high", "zh", ""])
        _w.writerow(["low_second.txt", "40.0", "medium", "zh", "true"])
        _w.writerow(["short_unknown.txt", "", "unknown", "", "insufficient text (<100 chars)"])
    _rbb, _sob2, _ = run_py("pp_batch_report.py", [str(_tmpb / "scores.csv"),
                                                   "-o", str(_tmpb / "r.html")])
    _hb = (_tmpb / "r.html").read_text(encoding="utf-8") if (_tmpb / "r.html").exists() else ""
    _ok_rows = all(m in _hb for m in ("high_first.txt", "low_second.txt", "short_unknown.txt",
                                      "unknown", "学术诚信", "分数分布"))
    _ok_order = _hb.index("high_first.txt") < _hb.index("low_second.txt") if _ok_rows else False
    _ok_degraded_note = "降级档" in _hb
    chk("batch_report: CSV→HTML 全 marker+降序+降级注记",
        _rbb == 0 and _ok_rows and _ok_order and _ok_degraded_note,
        f"rc={_rbb} rows={_ok_rows} order={_ok_order} deg={_ok_degraded_note}")
finally:
    _shutil_g.rmtree(_tmpb, ignore_errors=True)

# H4. pp.py 新子命令注册
chk("pp.py 入口: rewrite-check/batch-report 已注册",
    "rewrite-check" in _ppe.stdout and "batch-report" in _ppe.stdout)

# ───────────────────────── I. 学术规范自查（v5.2.0） ─────────────────────────
_NORM_BAD = ("本研究纳入了156例患者，其中五例随访脱落。所有患者均接受 5 mg 剂量治疗，"
             "另取 10mg 作为对照组。SLE 患者的 CRP 水平明显升高，CRP 与病情活动度相关。"
             "结果表明 SLE 组 50％ 达标，百分之三十部分缓解。"
             "计量资料采用ｔ检验，Ｐ<0.05 为差异有统计学意义。"
             "用量为 5 μg 与 2 µg 两组对比,结果如下。")
try:
    _snr = _API.style_norm(_NORM_BAD)
    _sn_checks = {f["check"] for f in _snr["findings"]}
    chk("style_norm: 富问题样本四查齐发",
        _snr["finding_count"] >= 5 and _sn_checks == {"fullwidth", "numbers", "abbrev", "units"},
        f"findings={_snr['finding_count']} checks={_sn_checks}")
    _snc = _API.style_norm("本研究纳入156例患者，其中5例随访脱落。患者接受5 mg剂量治疗。"
                           "炎症标志物（C反应蛋白，CRP）水平升高。结果显示62%达标。")
    chk("style_norm: 干净样本零全半角误报",
        not any(f["check"] == "fullwidth" for f in _snc["findings"]),
        f"findings={_snc['finding_count']}")
    chk("style_norm: 无判定类字段",
        all(k not in _snr for k in ("score", "risk", "verdict", "overall")))
except Exception as _e:
    chk("style_norm: 富问题样本四查齐发", False, f"exception: {_e}")

# I2. CLI + workflow §9 + --batch --report 直出
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _f:
    _f.write(_NORM_BAD); _sn_f = _f.name
_rcs, _sos, _ = run_py("pp_style_norm.py", [_sn_f, "--json"])
try:
    _snj = json.loads(_sos)
except Exception:
    _snj = {}
Path(_sn_f).unlink(missing_ok=True)
chk("style_norm CLI: --json 契约", _rcs == 0 and "findings" in _snj
    and "integrity_notice" in _snj, f"rc={_rcs}")
try:
    _snw = _API.workflow(_NORM_BAD)
    chk("workflow §9: style_norm 块在位", _snw.get("style_norm", {}).get("finding_count", 0) >= 5)
except Exception as _e:
    chk("workflow §9: style_norm 块在位", False, f"exception: {_e}")

_tmpn = Path(tempfile.mkdtemp(prefix="smoke_v520_"))
try:
    (_tmpn / "x.txt").write_text(ZH_HUMAN, encoding="utf-8")
    run_py("ai_detector.py", ["--batch", str(_tmpn), "--csv", str(_tmpn / "s.csv"),
                              "--report", str(_tmpn / "r.html")])
    _hr = (_tmpn / "r.html").read_text(encoding="utf-8") if (_tmpn / "r.html").exists() else ""
    chk("--batch --report: 直出 HTML", "逐文件明细" in _hr and "学术诚信" in _hr,
        f"html_size={len(_hr)}")
finally:
    _shutil_g.rmtree(_tmpn, ignore_errors=True)

# I3. 存档 README 解释化（评监委点名的 STALE 标记感知问题）
_arch_readme = ROOT / "eval" / "results" / "archive" / "README.md"
chk("评测存档: STALE 标记解释化 README 在位",
    _arch_readme.exists() and "STALE-cache-poisoned" in _arch_readme.read_text(encoding="utf-8"))

# ───────────────────────── J. Word 直读与自查包（v5.3.0） ─────────────────────────
def _smoke_make_docx(path, paras):
    import zipfile as _zip
    _W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    _body = "".join(f'<w:p xmlns:w="{_W}"><w:r><w:t xml:space="preserve">{x}</w:t></w:r></w:p>'
                    for x in paras)
    _doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<w:document xmlns:w="{_W}">{_body}</w:document>')
    with _zip.ZipFile(path, "w", _zip.ZIP_DEFLATED) as _z:
        _z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types/>')
        _z.writestr("word/document.xml", _doc)


# J1. docx 单文件检测
_tmpd = Path(tempfile.mkdtemp(prefix="smoke_v530_"))
try:
    _dx = _tmpd / "w.docx"
    _smoke_make_docx(_dx, [ZH_HUMAN])
    _rcd3, _sod3, _ = run_py("ai_detector.py", [str(_dx), "--format", "json"])
    try:
        _rj3 = json.loads(_sod3)
    except Exception:
        _rj3 = {}
    chk("docx 直读: 单文件检测出分", _rcd3 == 0 and isinstance(_rj3.get("overall_ai_score"), (int, float)),
        f"rc={_rcd3} score={_rj3.get('overall_ai_score')}")

    # J2. batch 收 docx
    (_tmpd / "n.txt").write_text(ZH_HUMAN, encoding="utf-8")
    run_py("ai_detector.py", ["--batch", str(_tmpd), "--csv", str(_tmpd / "s.csv")])
    _csvt = (_tmpd / "s.csv").read_text(encoding="utf-8-sig") if (_tmpd / "s.csv").exists() else ""
    chk("docx 直读: --batch 自动收集 *.docx", "w.docx" in _csvt and "n.txt" in _csvt)

    # J3. 投稿自查包（docx 输入）
    _rcb3, _sob3, _ = run_py("pp_report_bundle.py", [str(_dx), "--outdir", str(_tmpd)])
    _bundles = list(_tmpd.glob("selfcheck_*/README.md"))
    _bok = False
    if _bundles:
        _mt = _bundles[0].read_text(encoding="utf-8")
        _bok = ("阅读顺序" in _mt and "学术诚信" in _mt
                and (_bundles[0].parent / "workflow.md").exists()
                and (_bundles[0].parent / "paragraph_report.html").exists())
    chk("自查包: 一条命令产出全件+清单", _rcb3 == 0 and _bok, f"rc={_rcb3} ok={_bok}")

    # J4. 假 docx 拒绝
    (_tmpd / "fake.docx").write_text("not a zip")
    _rcf5, _, _sef5 = run_py("ai_detector.py", [str(_tmpd / "fake.docx")])
    chk("docx 直读: 假 docx 报错不抛栈", _rcf5 != 0 and "Traceback" not in _sef5, f"rc={_rcf5}")
finally:
    _shutil_g.rmtree(_tmpd, ignore_errors=True)

# J5. 文档面（评监委 10-12 双靶点）：子功能适用域矩阵 + FAQ 分组
_skill_md = (ROOT / "SKILL.md").read_text(encoding="utf-8")
_skill_zh = skill_zh  # v7.0.0: 复用双语自适应读取（CH 包缺 ZH 时为空串）
chk("文档: 子功能适用域矩阵在位" + ("(双语)" if HAS_ZH else f"［{FORM.upper()} 形态］"),
    (("Sub-tool scope matrix" in _skill_md) if not IS_SH
     else ("子功能适用域矩阵" in _skill_md))
    and (not HAS_ZH or "子功能适用域矩阵" in _skill_zh)
    and "translation_smell_check" in _skill_md)
# v6.3.0: 分组细节随 FAQ 迁 references/faq.md——断言改查 faq.md 分组与 SKILL 指针
_faq_ref = (ROOT / "references" / "faq.md").read_text(encoding="utf-8")
chk("文档: FAQ 分组编号(faq.md 完整版" + ("（双语）" if HAS_ZH else "［CH 英文包］"),
    "### Tools & workflow" in _faq_ref and "### Verdicts & boundaries" in _faq_ref
    and "### 工具与工作流" in _faq_ref and "### 判定与边界" in _faq_ref
    and "references/faq.md" in _skill_md
    and (not HAS_ZH or "references/faq.md" in _skill_zh))

# ───────────────────────── K. 期刊语境与保鲜状态（v5.4.0） ─────────────────────────
# K1. journal 2.0：学科自动识别 + 分学科语境 + --discipline 覆盖 + JSON 纯度
with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as _f:
    _f.write(ZH_HUMAN); _jp_f = _f.name
_rcj1, _soj1, _ = run_py("ai_detector.py", [_jp_f, "--profile", "journal", "--format", "json"])
try:
    _jp1 = json.loads(_soj1).get("journal_precheck", {})
except Exception:
    _jp1 = {}
chk("journal 2.0: 学科识别+语境字段", _rcj1 == 0 and _jp1.get("discipline") in
    ("medical", "engineering", "social", "general")
    and bool(_jp1.get("discipline_context"))
    and "不虚构" in (_jp1.get("reference_line_discipline_note") or ""),
    f"discipline={_jp1.get('discipline')}")
_rcj2, _soj2, _ = run_py("ai_detector.py", [_jp_f, "--profile", "journal", "--format", "json",
                                            "--discipline", "social"])
try:
    _jp2 = json.loads(_soj2).get("journal_precheck", {})
except Exception:
    _jp2 = {}
Path(_jp_f).unlink(missing_ok=True)
chk("journal 2.0: --discipline 覆盖生效", _rcj2 == 0 and _jp2.get("discipline") == "social",
    f"discipline={_jp2.get('discipline')}")

# K2. freshness --status：契约 + 基线零漂移
_rcf6, _sof6, _ = run_py("freshness_refresh.py", ["--status", "--json"])
try:
    _frj = json.loads(_sof6)
except Exception:
    _frj = {}
chk("freshness: 状态契约齐全", _rcf6 == 0 and
    all(k in _frj for k in ("last_refresh", "latest_eval_record", "baseline_drift",
                            "due_for_refresh", "baselines_expected"))
    and _frj.get("baselines_expected", {}).get("fused_oldgen") == 0.9998,
    f"rc={_rcf6}")
chk("freshness: 四基线零漂移", _frj.get("baseline_drift") == [], f"drift={_frj.get('baseline_drift')}")

# K3. 二进制输入护栏：PDF 干净拒绝+转存建议
with tempfile.NamedTemporaryFile("w", suffix=".pdf", delete=False) as _f:
    _f.write("%PDF-1.4 smoke fake")
    _pdf_f = _f.name
_rcp1, _, _sep1 = run_py("ai_detector.py", [_pdf_f])
Path(_pdf_f).unlink(missing_ok=True)
chk("二进制护栏: PDF 干净拒绝+转存指引", _rcp1 != 0 and "Traceback" not in _sep1
    and "PDF" in _sep1 and "docx" in _sep1, f"rc={_rcp1}")

# ───────────────────────── L. 卡片转化/文档模式（v5.5.0，模块 2+3） ─────────────────────────
_skill_zh2 = skill_zh  # v7.0.0: 双语自适应
_zh_desc_m = re.search(r"description: >-?\n((?:  .+\n)+)", _skill_zh2) if HAS_ZH else None
_zh_desc = " ".join(x.strip() for x in (_zh_desc_m.group(1).splitlines())) if _zh_desc_m else ""
# L1. desc 首行需求词（模块 2.1：头 120 字符逐字覆盖；品牌词不在首 60）——ZH 断言双语包自适应
if HAS_ZH:
    chk("desc 首行需求词在头 120 字符",
        "论文润色" in _zh_desc[:120] and "AI率" in _zh_desc[:120],
        f"head120={_zh_desc[:120]!r}")
    chk("desc 品牌词不在首 60 字符",
        "Paper Polisher Pro" not in _zh_desc[:60] and "polisher" not in _zh_desc[:60].lower())
else:
    chk("desc 需求词断言［CH 英文包：ZH 断言自适应跳过］", True)
# L2. Skip when 负触发器（模块 3.4，置换式在位）
chk("desc Skip-when 负触发器" + ("（双语）" if HAS_ZH else f"［{FORM.upper()} 形态］"),
    (("Not for:" in (re.search(r"description: >-?\n((?:  .+\n)+)",
     (ROOT / "SKILL.md").read_text(encoding="utf-8")).group(1))) if not IS_SH
     else ("不适用" in (re.search(r"description: >-?\n((?:  .+\n)+)",
     (ROOT / "SKILL.md").read_text(encoding="utf-8")).group(1))))
    and (not HAS_ZH or "不适用" in _zh_desc))
# L3. 反模式替代方案 + 重试纪律（模块 3.3，双语）
chk("反模式每条带替代方案" + ("（双语）" if HAS_ZH else f"［{FORM.upper()} 形态］"),
    (("✅ Instead" in _skill_md) if not IS_SH
     else ("✅ 替代" in _skill_md))
    and (not HAS_ZH or "✅ 替代" in _skill_zh2))
chk("重试纪律反模式在位" + ("（双语）" if HAS_ZH else f"［{FORM.upper()} 形态］"),
    (("repeat the same analysis" in _skill_md) if not IS_SH
     else ("重复同一分析" in _skill_md))
    and (not HAS_ZH or "重复同一分析" in _skill_zh2))
# L4. 30 秒任务路由 + 深文档指针（模块 3.2）
chk("30 秒任务路由表" + ("（双语）" if HAS_ZH else f"［{FORM.upper()} 形态］"),
    (("30-second task routing" in _skill_md) if FORM == "ch"
     else ("30 秒任务路由" in _skill_md))
    and (not HAS_ZH or "30 秒任务路由" in _skill_zh2))
chk("article-review-workflow.md 入口指针",
    "何时读我" in (ROOT / "references" / "article-review-workflow.md").read_text(encoding="utf-8"))
# L5. 子功能矩阵补全（boundary 自查发现）
chk("子功能矩阵含 quality_report/docx_text/batch 行" + ("（双语）" if HAS_ZH else f"［{FORM.upper()} 形态］"),
    "quality_report" in _skill_md and "docx_text" in _skill_md
    and (("5 MB skipped by design" in _skill_md) if FORM == "ch"
         else ("按设计跳过" in _skill_md)))
# L6. workflow findings ledger（模块 3.5）
try:
    _flw = _API.workflow(_DEMO_AI)
    _fli = (_flw.get("findings_ledger") or {}).get("items") or []
    _fstat = [x["status"] for x in _fli]
    chk("workflow: findings ledger 在位（answered/partially/unresolved）",
        len(_fli) >= 5 and all(s in ("answered", "partially", "unresolved") for s in _fstat),
        f"items={len(_fli)}")
except Exception as _e:
    chk("workflow: findings ledger 在位", False, f"exception: {_e}")
# L7. 术语一致性检查（v5.5.0 新查）
try:
    _snc2 = _API.style_norm("本研究纳入156例患者，病人均签署知情同意。患者随访12个月，病人无失访。")
    _sc_types = [f for f in _snc2["findings"] if f["check"] == "consistency"]
    chk("style_norm: 同概念异写混用检出（患者/病人）",
        len(_sc_types) >= 1 and "患者" in str(_sc_types[0]["examples"]),
        f"findings={len(_sc_types)}")
    _snc3 = _API.style_norm(ZH_HUMAN)
    chk("style_norm: 干净学术样本零一致性误报",
        not any(f["check"] == "consistency" for f in _snc3["findings"]))
except Exception as _e:
    chk("style_norm: 同概念异写混用检出", False, f"exception: {_e}")

# ───────────────────────── M. LLM 腔自查与负结果披露（v5.6.0） ─────────────────────────
try:
    _mj = _API.style_norm("免疫系统的某一个零件出厂即缺失，机会性病原最先破门。家族史是探针，把这条主线收拢。"
                          "先兜底再根治需要克制。六张面孔背后是同一机制，一网打尽并不现实。"
                          "风湿科是第一站，把治疗窗口前移至关重要。综上所述，检出要把另一面讲透。")
    _mj_l1 = [f for f in _mj["findings"] if f["check"] == "llm_jargon" and "L1" in f["advice"]]
    chk("style_norm 第7查: L1 隐喻滥用检出", len(_mj_l1) >= 1,
        f"findings={_mj['finding_count']}")
    _mjc = (ROOT / "references" / "style_guard_cases.json")
    chk("判例库随包（18 对原句→改句）",
        _mjc.exists() and len(json.load(open(_mjc, encoding="utf-8")).get("cases", [])) >= 18)
except Exception as _e:
    chk("style_norm 第7查: L1 隐喻滥用检出", False, f"exception: {_e}")

try:
    import ai_detector as _ad
    _mjrep = _ad.detect("免疫系统的某一个零件出厂即缺失，机会性病原最先破门。家族史是探针，把这条主线收拢。"
                        "先兜底再根治需要克制。六张面孔背后是同一机制，一网打尽并不现实。"
                        "风湿科是第一站，把治疗窗口前移至关重要。综上所述，检出要把另一面讲透，"
                        "免疫力失守就会塌方，车轮般的命运碾压而至，叙事至此收束。", lang="zh")
    chk("负结果披露: 检测器报命中不计分",
        bool(_mjrep.jargon_hits) and _mjrep.jargon_bonus == 0.0,
        f"hits={len(_mjrep.jargon_hits)} bonus={_mjrep.jargon_bonus}")
    chk("负结果工件随包",
        (ROOT / "eval" / "results" / "archive" / "meddocs_20261014.json").exists())
except Exception as _e:
    chk("负结果披露: 检测器报命中不计分", False, f"exception: {_e}")

# ───────────────────────── 汇总 ─────────────────────────
failed = [r for r in results if not r[1]]
print("────────────────────────────────")
print(f"[汇总] total={len(results)} pass={len(results)-len(failed)} fail={len(failed)} "
      f"-> {'GREEN' if not failed else 'RED'}")
sys.exit(0 if not failed else 1)
