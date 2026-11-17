#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Humanizer 检查脚本 —— 《奉天1928》去 AI 痕迹自检工具
规范依据：STYLE-GUIDE.md §12 去 AI 痕迹（Humanizer 规范）

用法（脚本存于技能仓库 scripts/，须在子项目根目录执行）：
    python "../GitHub Novel Serialization Skill/scripts/humanizer_check.py" chapters/          # 全量扫描
    python "../GitHub Novel Serialization Skill/scripts/humanizer_check.py" "chapters/第一卷 备战"  # 目录
    python "../GitHub Novel Serialization Skill/scripts/humanizer_check.py" "chapters/第一卷 备战/第一幕 皇姑屯之变/第001章 滦州惊雷.md"
    python "../GitHub Novel Serialization Skill/scripts/humanizer_check.py" chapters/ --out 报告.md  # 输出 Markdown 报告

判定：
    FAIL —— 命中禁用词（结构套话／抽象评价）或章末升华句，必须改写
    WARN —— 限用项超标（模糊副词／情绪标签／套路句式／标点密度／段长过匀）
    PASS —— 全部达标

说明：脚本只负责挑出可疑处，最终以主编人工复核为准（STYLE-GUIDE §12.5）。
"""

import sys
import os
import re
import argparse
from pathlib import Path

# ---- 词表（STYLE-GUIDE §12.2）----
BANNED_STRUCT = ["首先", "其次", "与此同时", "值得一提的是", "总的来说", "不难看出",
                 "由此可见", "综上所述", "换言之", "换句话说", "总的来说"]
BANNED_ABSTRACT = ["意味深长", "耐人寻味", "五味杂陈", "百感交集", "心潮澎湃", "若有所思",
                   "不言而喻", "扑朔迷离", "错综复杂", "息息相关", "至关重要", "潜移默化",
                   "前所未有", "焕然一新", "堪称", "尤为关键", "不禁让人", "仿佛预示"]
LIMIT_VAGUE = ["微微", "轻轻", "稍稍", "缓缓", "淡淡", "似乎", "仿佛", "莫名",
               "某种", "一丝", "一抹", "几分", "隐约"]
LIMIT_EMOTION = ["心中一紧", "心头一沉", "心里一沉", "眼眶一热", "鼻子一酸", "浑身一震"]
IDIOMS = ["一丝不苟", "井井有条", "一如既往", "不动声色", "不约而同", "从容不迫",
          "若无其事", "心事重重", "若隐若现", "恍然大悟", "豁然开朗", "戛然而止",
          "鸦雀无声", "面面相觑", "小心翼翼", "义无反顾", "斩钉截铁", "胸有成竹",
          "目不转睛", "屏息凝神", "意味深长", "不可思议", "出人意料", "恰恰相反"]

# 设定术语白名单：大纲/世界观中的固定对举口径，不算套路句式（STYLE-GUIDE §12.3 注）
TERM_PAIRS = ["既合作又警惕", "既利用又防备", "既忌惮又依赖", "既警惕又利用",
              "既合作又防备", "既合作又戒备", "既拉又打", "既防范又借重"]

# ---- 阈值（STYLE-GUIDE §12.3 / §12.5）----
MAX_VAGUE = 5        # 模糊副词/章
MAX_EMOTION = 1      # 情绪标签/章
MAX_PATTERN = 1      # 套路句式/章
MAX_DASH_PER_K = 5   # 破折号/千字
MAX_ELLIPSIS_PER_K = 2
MAX_EXCL_PER_K = 2   # 叙述中感叹号（对话内已剔除）
AI_DENSITY = 1.0     # AI 腔词/千字上限


def count_cn(text):
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def strip_dialogue(text):
    """剔除引号内对话后的叙述文本"""
    return re.sub(r'“[^”]*”', '', text)


def check_file(path):
    raw = Path(path).read_text(encoding='utf-8')
    # 叙事正文（chapters/）按“章”计阈值；大纲/设定类文档按“4000 字等价章数”折算
    is_prose = 'chapters' in str(Path(path)).replace('\\', '/')
    equiv = max(1, round(count_cn(raw) / 4000.0)) if not is_prose else 1
    lines = raw.split('\n')
    # 去掉文件头元数据（> 开头）与标题行
    body_lines = [ln for ln in lines if not ln.startswith('>')]
    text = '\n'.join(body_lines)
    narr = strip_dialogue(text)
    cn = count_cn(text) or 1
    k = cn / 1000.0

    issues = []   # (级别, 类别, 说明, 行号样例)
    def hit(words, label, level, limit=None):
        found = []
        for i, ln in enumerate(body_lines, 1):
            for w in words:
                if w in ln:
                    found.append((i, w))
        if found:
            if limit is None:
                issues.append((level, label, len(found), found[:5]))
            elif len(found) > limit:
                issues.append((level, label, len(found), found[:5]))
        return len(found)

    n_struct = hit(BANNED_STRUCT, "结构套话（禁用）", "FAIL")
    n_abstract = hit(BANNED_ABSTRACT, "抽象评价（禁用）", "FAIL")
    n_vague = hit(LIMIT_VAGUE, f"模糊副词（限 {MAX_VAGUE * equiv}）", "WARN", MAX_VAGUE * equiv)
    n_emotion = hit(LIMIT_EMOTION, f"情绪标签（限 {MAX_EMOTION * equiv}）", "WARN", MAX_EMOTION * equiv)

    # 套路句式
    pats = [r'不是[^。！？]{1,15}而是', r'不仅仅?[^。！？]{0,12}更是',
            r'与其说[^。！？]{1,15}不如说', r'既[^。！？]{1,10}又[^。！？]{1,10}']
    pat_hits = []
    for i, ln in enumerate(body_lines, 1):
        s = ln.strip()
        # 结构条目（表格行/列表项/标题）不参与套路句式判定——设定文档的对举属术语
        if s.startswith('|') or s.startswith('- ') or s.startswith('#'):
            continue
        probe = ln
        for term in TERM_PAIRS:      # 设定术语对举不计
            probe = probe.replace(term, '〇')
        for p in pats:
            if re.search(p, probe):
                pat_hits.append((i, re.search(p, probe).group(0)[:12]))
    if len(pat_hits) > MAX_PATTERN * equiv:
        issues.append(("WARN", f"套路句式（限 {MAX_PATTERN * equiv}）", len(pat_hits), pat_hits[:5]))

    # 章末升华
    tail = '\n'.join([ln for ln in body_lines if ln.strip()][-2:])
    climax_pat = r'(明白了?|意识到|才知道|从此|只是一个开始|一切都不同|仿佛预示|这一刻，他)'
    if re.search(climax_pat, tail):
        issues.append(("FAIL", "章末升华句（禁用）", 1, [(len(body_lines), tail.strip()[:40])]))

    # 成语连用
    idiom_hits = []
    for i, ln in enumerate(body_lines, 1):
        found = [w for w in IDIOMS if w in ln]
        if len(found) >= 2:
            idiom_hits.append((i, '/'.join(found[:3])))
    if idiom_hits:
        issues.append(("WARN", "成语连用（限 2）", len(idiom_hits), idiom_hits[:3]))

    # 标点密度
    dash = narr.count('——') / k
    ell = narr.count('……') / k
    excl = narr.count('！') / k
    if dash > MAX_DASH_PER_K:
        issues.append(("WARN", f"破折号 {dash:.1f}/千字（限 {MAX_DASH_PER_K}）", int(narr.count('——')), []))
    if ell > MAX_ELLIPSIS_PER_K:
        issues.append(("WARN", f"省略号 {ell:.1f}/千字（限 {MAX_ELLIPSIS_PER_K}）", int(narr.count('……')), []))
    if excl > MAX_EXCL_PER_K:
        issues.append(("WARN", f"感叹号 {excl:.1f}/千字（限 {MAX_EXCL_PER_K}）", int(narr.count('！')), []))

    # 段长均匀度（变异系数）
    paras = [len(p) for p in text.split('\n') if p.strip() and not p.startswith(('#', '>'))]
    cv = 0
    if is_prose and len(paras) >= 8:
        mean = sum(paras) / len(paras)
        var = sum((x - mean) ** 2 for x in paras) / len(paras)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.45:
            issues.append(("WARN", f"段长过于均匀 CV={cv:.2f}（应 ≥ 0.45）", len(paras), []))

    # AI 腔密度
    ai_total = n_struct + n_abstract
    density = ai_total / k

    level = "PASS"
    if any(i[0] == "FAIL" for i in issues):
        level = "FAIL"
    elif any(i[0] == "WARN" for i in issues):
        level = "WARN"

    return {
        "file": str(path),
        "cn": cn,
        "level": level,
        "density": density,
        "issues": issues,
        "stats": {"vague": n_vague, "emotion": n_emotion, "dash": dash, "cv": cv},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", default="chapters/")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    t = Path(args.target)
    files = [t] if t.is_file() else sorted(t.rglob("*.md"))
    files = [f for f in files if f.name != "_幕导语.md"]
    if not files:
        print("未找到 md 文件：", args.target)
        return

    results = [check_file(f) for f in files]
    lines = ["# Humanizer 去 AI 痕迹检查报告", "",
             "> 依据 STYLE-GUIDE §12；FAIL 必须改写，WARN 需人工复核", "",
             f"- 扫描文件：{len(results)}",
             f"- PASS {sum(1 for r in results if r['level']=='PASS')} ｜ "
             f"WARN {sum(1 for r in results if r['level']=='WARN')} ｜ "
             f"FAIL {sum(1 for r in results if r['level']=='FAIL')}",
             "", "| 文件 | 字数 | 判定 | AI腔/千字 | 主要问题 |", "|---|---|---|---|---|"]
    for r in results:
        main_issue = "；".join(f"{i[1]}({i[2]})" for i in r["issues"][:3]) or "—"
        lines.append(f"| `{Path(r['file']).name}` | {r['cn']} | **{r['level']}** | {r['density']:.2f} | {main_issue} |")

    lines += ["", "## 问题明细", ""]
    for r in results:
        if not r["issues"]:
            continue
        lines.append(f"### {Path(r['file']).name}（{r['level']}）")
        for lv, label, cnt, samples in r["issues"]:
            loc = "、".join(f"L{i}:{w}" for i, w in samples[:3])
            lines.append(f"- [{lv}] {label} × {cnt}" + (f" —— {loc}" if loc else ""))
        lines.append("")

    out = "\n".join(lines)
    if args.out:
        Path(args.out).write_text(out, encoding='utf-8')
        print(f"报告已写入：{args.out}")
    print(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding='utf-8')
    main()
