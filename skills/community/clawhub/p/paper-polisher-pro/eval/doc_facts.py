#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""doc_facts.py — 文档事实契约检查器（v7.8.0 新增；零依赖）

定位：安装完整性自证(v7.6.0) → 输出契约(v7.7.0) → 文档事实(v7.8.0)。
让文档也成为可机器验证的工件：引用不死链、数字不漂移、入口不虚标、
指标可溯源、版本不脱节。文档与实现/数据漂移在打包前当场暴露。

五闸:
  A 文件引用   .md 中 eval/results/… 引用必须实存；实存 archive/ 的文件必须带
               archive/ 前缀引用（历史口径文件严禁伪装成顶层结果）
  C 数字对账   SKILL.md 与 SKILL_ZH.md 数值集合一致（双语平行文档不得各说各话；
               白名单逐条注明理由）
  D 入口对账   文档化 `pp.py <cmd>` ↔ pp.py 注册表（COMMANDS+BUILTIN）双向一致；
               隐藏命令（api）白名单豁免
  E 指标锚     文档关键指标必须在所引 eval JSON 中可复现（指纹绑定时代数字；
               逐锚注明字段与口径）
  F 版本一致   skill.json == CHANGELOG 顶条目 == SKILL.md/SKILL_ZH.md 变更史顶条目
               == schemas/*.schema.json $id 契约主版本

用法:
  python3 eval/doc_facts.py              # 全闸（退出码 0=全绿 / 1=任一 FAIL）
  python3 eval/doc_facts.py --root DIR   # 指定包根（测试用包副本隔离，正本只读）
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parent

# ── 闸 A：文件引用 ────────────────────────────────────────────────
_DOC_GLOBS = ("SKILL.md", "SKILL_ZH.md", "README.md")
_REF_RE = re.compile(r"eval/results/[A-Za-z0-9_./\*-]+")
# 输出路径引用白名单：这些通配指向"流水线将生成的文件"，首跑前不存在=设计内
# （逐条注明生成者，防止白名单变成逃逸口）。
REF_OUTPUT_GLOBS = {
    "eval/results/freshness_*.json":
        "月度保鲜流水线输出（freshness_refresh.py 首跑前不存在=设计内）",
}

# ── 闸 C：数字对账 ────────────────────────────────────────────────
_NUM_RES = (
    (re.compile(r"\d+\.\d{2,4}"), "dec"),            # 0.9998 / 52.1
    (re.compile(r"\d+(?:\.\d+)?%"), "pct"),          # 2.3% / 59%
    (re.compile(r"n=\d[\d,]*"), "n"),                # n=1,304
    (re.compile(r"\b[0-9a-f]{12}\b"), "md5"),        # 2631df3d388b
)
# 白名单：(token, 类别, 理由)。加入前必须人工确认两侧差异是有意为之。
NUM_WHITELIST = {
    # （首版为空——闸 C 首跑即全绿说明双语数字本就同步；后续如有意不对称，
    #   在此登记 token+理由，登记即承诺该差异被审阅过）
}

# ── 闸 D：入口对账 ────────────────────────────────────────────────
_HIDDEN_CMDS = {"api"}  # pp.py help 有意隐藏（`pp.py api` 仅打印 SDK 指引一行）

# ── 闸 E：指标锚 ──────────────────────────────────────────────────
# 每锚: (文档数字, eval JSON 相对路径, 字段, 口径)。口径:
#   dec4=round(json,4) 相等 | int=整数相等 | str=字符串相等
#   percent=round(json*100,1) 相等 | int_commas=文档带千分位剥逗号后相等
ANCHORS = (
    ("0.9998", "eval/results/v35ctl_oldgen.json", "auroc", "dec4"),
    ("0.9400", "eval/results/v35ctl_gen2026.json", "auroc", "dec4"),
    ("0.8985", "eval/results/archive/v480_rules_oldgen.json", "auroc", "dec4"),
    ("0.7149", "eval/results/archive/v480_rules_gen2026.json", "auroc", "dec4"),
    ("2631df3d388b", "eval/results/v35ctl_oldgen.json", "model_fp", "str"),
    ("2.3", "eval/results/v35ctl_oldgen.json", "human_fpr@med", "percent"),
    ("443", "eval/results/v35ctl_gen2026.json", "n_base", "int"),
    ("927", "eval/results/v35ctl_oldgen.json", "n_base", "int"),
    ("1,304", "eval/results/v35ctl_oldgen.json", "n", "int_commas"),
    ("5,251", "eval/results/archive/v3_final_test.json", "n", "int_commas"),
)

# ── 闸 F：版本一致 ────────────────────────────────────────────────
_VER_RE = re.compile(r"\d+\.\d+\.\d+")
_CHANGELOG_TOP = re.compile(r"^## What's new in v(\d+\.\d+\.\d+)", re.M)
_SKILL_HISTORY_TOP = re.compile(r"^- \*\*v(\d+\.\d+\.\d+)", re.M)


def _docs(root):
    out = []
    for pat in _DOC_GLOBS:
        p = root / pat
        if p.is_file():
            out.append(p)
    for p in sorted((root / "references").glob("*.md")):
        out.append(p)
    return out


def gate_a(root):
    """文件引用：.md 中 eval/results 引用必须实存；archive 内文件必须带前缀。"""
    results = root / "eval" / "results"
    fails = []
    for doc in _docs(root):
        text = doc.read_text(encoding="utf-8")
        for m in _REF_RE.finditer(text):
            ref = m.group(0).rstrip(".,;:)）」")
            rel = ref[len("eval/results/"):]
            if ref in REF_OUTPUT_GLOBS:
                continue  # 输出路径引用（首跑前不存在=设计内，白名单已注明生成者）
            if rel.startswith("archive/"):
                if not list(results.glob(rel)):
                    fails.append(f"{doc.name}: 引用不存在 {ref}")
                continue
            if list(results.glob(rel)):
                continue
            if list(results.glob("archive/" + rel)):
                fails.append(f"{doc.name}: {ref} 实存 archive/，引用需带 archive/ 前缀"
                             "（历史口径文件不得伪装成顶层结果）")
            else:
                fails.append(f"{doc.name}: 引用不存在 {ref}")
    return fails


def _numbers(text):
    from collections import Counter
    c = Counter()
    for rx, tag in _NUM_RES:
        for m in rx.finditer(text):
            c[(m.group(0), tag)] += 1
    return c


def gate_c(root):
    """数字对账：SKILL.md 与 SKILL_ZH.md 数值集合一致（ZH 缺席=CH 打包形态，无对偶可查）。"""
    if not (root / "SKILL_ZH.md").is_file():
        return []  # 形态自适应：打包副本无中文正本（_docs SkipTest 同语义）
    en = (root / "SKILL.md").read_text(encoding="utf-8")
    zh = (root / "SKILL_ZH.md").read_text(encoding="utf-8")
    ce, cz = _numbers(en), _numbers(zh)
    fails = []
    for key in sorted(set(ce) | set(cz)):
        if key[0] in NUM_WHITELIST:
            continue
        if ce.get(key, 0) != cz.get(key, 0):
            side = "仅英文" if ce.get(key, 0) > cz.get(key, 0) else "仅中文"
            fails.append(f"数字不对称 {key[0]}（{key[1]}）×英文{ce.get(key, 0)}/中文{cz.get(key, 0)}"
                         f"——{side}；要么补齐，要么进 NUM_WHITELIST 并注明理由")
    return fails


def _registry(root):
    """pp.py 注册表真值：COMMANDS dict 键 + BUILTIN 元组。"""
    src = (root / "scripts" / "pp.py").read_text(encoding="utf-8")
    m = re.search(r"^BUILTIN = \(([^)]*)\)", src, re.M | re.S)
    builtin = set(re.findall(r'"([a-z][a-z0-9-]*)"', m.group(1))) if m else set()
    m = re.search(r"^COMMANDS = \{(.*?)^\}", src, re.M | re.S)
    commands = set(re.findall(r'^    "([a-z][a-z0-9-]*)":', m.group(1), re.M)) if m else set()
    return builtin | commands


def gate_d(root):
    """入口对账：文档化命令 ↔ 注册表双向。"""
    registry = _registry(root)
    doc_cmds = set()
    for doc in _docs(root):
        doc_cmds |= set(re.findall(r"\bpp\.py ([a-z][a-z0-9-]*)",
                                   doc.read_text(encoding="utf-8")))
    fails = []
    for c in sorted(doc_cmds - registry - _HIDDEN_CMDS):
        fails.append(f"文档引用 pp.py {c} 未注册进统一入口"
                     "（孤儿引用——补 COMMANDS/BUILTIN 或改文档）")
    for c in sorted(registry - doc_cmds - _HIDDEN_CMDS):
        fails.append(f"统一入口命令 pp.py {c} 无任何文档提及"
                     "（虚注册——补文档或从注册表移除）")
    return fails


def gate_e(root):
    """指标锚：文档数字 ↔ eval JSON 字段逐锚复现。"""
    doc_text = "\n".join(d.read_text(encoding="utf-8") for d in _docs(root))
    fails = []
    for num, rel, field, mode in ANCHORS:
        jp = root / rel
        if not jp.is_file():
            fails.append(f"锚 {num}: JSON 缺失 {rel}")
            continue
        val = json.loads(jp.read_text(encoding="utf-8")).get(field)
        if val is None:
            fails.append(f"锚 {num}: {rel} 无字段 {field}")
            continue
        cited = num in doc_text or num.replace(",", "") in doc_text
        if not cited:
            fails.append(f"锚 {num}: 文档未引用该指标（锚失去意义——补引用或删锚）")
        if mode == "dec4":
            if round(float(val), 4) != float(num):
                fails.append(f"锚 {num}: {rel}:{field}={val} 与文档不符")
        elif mode == "int":
            if int(val) != int(num):
                fails.append(f"锚 {num}: {rel}:{field}={val} 与文档不符")
        elif mode == "int_commas":
            if int(val) != int(num.replace(",", "")):
                fails.append(f"锚 {num}: {rel}:{field}={val} 与文档不符")
        elif mode == "str":
            if str(val) != num:
                fails.append(f"锚 {num}: {rel}:{field}={val} 与文档不符")
        elif mode == "percent":
            if round(float(val) * 100, 1) != float(num):
                fails.append(f"锚 {num}: {rel}:{field}={val} ×100 与文档 {num}% 不符")
    return fails


def gate_f(root):
    """版本一致：skill.json == CHANGELOG 顶 == 双语变更史顶 == schema $id 主版本。"""
    ver = _VER_RE.search(
        json.loads((root / "skill.json").read_text(encoding="utf-8")).get("version", "")
    ).group(0)
    fails = []
    ch = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    m = _CHANGELOG_TOP.search(ch)
    if not m or m.group(1) != ver:
        fails.append(f"CHANGELOG 顶条目 {m.group(1) if m else '缺失'} != skill.json {ver}")
    for name in ("SKILL.md", "SKILL_ZH.md"):
        _p = root / name
        if not _p.is_file():
            continue  # 形态自适应：打包副本无 SKILL_ZH.md（SH 包 SKILL.md 即中文）
        m = _SKILL_HISTORY_TOP.search(_p.read_text(encoding="utf-8"))
        if not m or m.group(1) != ver:
            fails.append(f"{name} 变更史顶条目 {m.group(1) if m else '缺失'} != skill.json {ver}")
    for sp in sorted((root / "schemas").glob("*.schema.json")):
        sid = json.loads(sp.read_text(encoding="utf-8")).get("$id", "")
        m = re.search(r"@(\d+)", sid)
        if m and m.group(1) != ver.split(".")[0]:
            fails.append(f"{sp.name} $id 契约主版本 @{m.group(1)} != skill.json 主版本 "
                         f"{ver.split('.')[0]}（契约升级须同步 $id）")
    return fails


def main():
    args = sys.argv[1:]
    root = DEFAULT_ROOT
    if "--root" in args:
        root = Path(args[args.index("--root") + 1]).resolve()
    gates = (("A 文件引用", gate_a), ("C 数字对账", gate_c), ("D 入口对账", gate_d),
             ("E 指标锚", gate_e), ("F 版本一致", gate_f))
    failed = False
    print(f"文档事实契约 doc_facts（根={root}）")
    for name, fn in gates:
        fails = fn(root)
        if fails:
            failed = True
            print(f"[FAIL] 闸{name}: {len(fails)} 处")
            for f in fails:
                print(f"  - {f}")
        else:
            print(f"[PASS] 闸{name}")
    if failed:
        print("文档事实契约 FAIL——文档也是工件，漂移在打包前死亡", file=sys.stderr)
        return 1
    print("文档事实契约 PASS（5/5 闸）")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
