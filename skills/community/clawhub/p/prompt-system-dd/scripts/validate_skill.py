#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""契约门禁校验脚本(v5.1 原子注册制+位序契约+规则求值)

校验维度:
  FM  前言区契约(version一致性)  RI  资源索引契约    LT  LITE骨架契约
  CR  核心原子契约(含位号)       DM  域原子契约       OU  输出原子契约
  MF  组合清单契约(双向登记)     AT  原子引用契约
  DP  深度适配契约(位序/规则求值/数量下限)
  RP  路由协议契约               EX  示例契约(R3/R4覆盖)
  TS  唯一真相源                 DH  目录卫生

扩展位设计:原子采用注册制——脚本动态扫描 atoms/{core,domains,outputs}/
目录,新增原子文件自动纳入校验,无需修改本脚本。唯一要求:新原子遵循
references/depth-adaptation.md 中的扩展指南(头部声明+段结构+质量清单),
并在 composition-manifest.md 判定表登记(MF011/MF013 强制)。

版本真相源:本脚本不维护独立版本常量,输出版本派生自 SKILL.md frontmatter。

用法:
  python scripts/validate_skill.py --skill-dir <dir> [--strict]
输出:stdout JSON,退出码 0=passed / 1=failed
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SUPPORTED_LEVELS = ["D1", "D2", "D3", "D4"]
# 组装顺序 = DEPTH 指纹位序(T14:example-shot 插入第 4 位,共 9 位)
CORE_ATOM_KEYS = [
    "role-anchor", "task-define", "context-inject", "example-shot",
    "format-spec", "think-chain", "constraints", "self-check", "iterate",
]
MIN_CORE = 9
MIN_DOMAINS = 9
MIN_OUTPUTS = 10
MIN_BENCH_CASES = 12
MIN_MODEL_ADAPTERS = 4
# R04 档位 token 基线(估算待标定);必须与 depth-adaptation.md 同表一致
TOKEN_BASELINE = {"D1": 200, "D2": 600, "D3": 1500, "D4": 3500}
# R03 回归基线
BENCHMARK_DIR = "references/benchmark"
# 顶层白名单:DH005 唯一消费点(T23,勿再另建硬编码集合)
WHITELIST_TOP = {"SKILL.md", "main.py", "scripts", "references",
                 "assets", ".coze"}
ALLOWED_HIDDEN = {".coze", ".git", ".gitignore"}
TMP_PATTERNS = ("__pycache__", ".DS_Store", "tmp*", ".cache", "*.pyc")


def read_text(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def check(condition, level, code, message, findings):
    if not condition:
        findings.append({"level": level, "code": code, "message": message})
    return condition


def fm_number(text, field):
    m = re.search(rf"^{field}:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def validate_frontmatter(skill_dir, findings, checked):
    sp = skill_dir / "SKILL.md"
    text = read_text(sp)
    checked.append("SKILL.md")
    if not check(text is not None, "error", "FM001",
                 "SKILL.md 不存在或不可读", findings):
        return
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not check(m is not None, "error", "FM002",
                 "缺少 YAML 前言区(--- 包裹)", findings):
        return
    fm = m.group(1)
    name = fm_number(fm, "name")
    desc = fm_number(fm, "description")
    ver = fm_number(fm, "version")
    check(name is not None and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name),
          "error", "FM003", f"name 缺失或不符合小写连字符规范: {name}", findings)
    check(desc is not None and 60 <= len(desc) <= 200 and "\n" not in desc,
          "error", "FM004",
          f"description 需为 60-200 字符单行,当前 {len(desc or '')} 字符", findings)
    check(name is None or name == skill_dir.name, "warning", "FM005",
          f"name({name}) 与目录名({skill_dir.name})不一致", findings)
    # T11: version 三处一致(frontmatter / SKILL.md 标题 / 目录名均派生主版本)
    fm_major = ver.split(".")[0] if ver else None
    title_m = re.search(r"v(\d+)\.\d+", text)
    title_major = title_m.group(1) if title_m else None
    check(ver is not None and fm_major == title_major, "error", "FM006",
          f"版本真相源冲突: frontmatter version={ver}(主版本 {fm_major}) "
          f"与标题 v{title_major} 不一致", findings)


def validate_resource_index(skill_dir, findings, checked):
    text = read_text(skill_dir / "SKILL.md")
    if text is None:
        return
    links = re.findall(r"\]\(([^)]+\.md|[^)]+\.py)\)", text)
    links = [l for l in links if not l.startswith("http")]
    check(len(links) >= 4, "error", "RI001",
          f"资源索引声明过少({len(links)} 条),应覆盖路由/清单/深度/示例等", findings)
    for rel in links:
        checked.append(rel)
        check((skill_dir / rel).exists(), "error", "RI002",
              f"资源索引声明的文件不存在: {rel}", findings)


def validate_lite_skeleton(skill_dir, findings):
    """T05:路由 A 仅引用 LITE-1;LITE-2/3/4 已退役,不再校验。"""
    text = read_text(skill_dir / "SKILL.md")
    if text is None:
        return
    check("LITE-1" in text, "error", "LT001",
          "SKILL.md 缺少 LITE 骨架锚点 LITE-1", findings)
    for dead in ("LITE-2", "LITE-3", "LITE-4"):
        check(dead not in text, "error", "LT005",
              f"SKILL.md 仍存在已退役的死代码锚点 {dead}", findings)


def _atom_header_ok(text):
    head = text[:400]
    return "唯一真相源" in head and ("自包含" in head or "深度语义锚" in head)


def _segment_lines(text):
    return len([l for l in text.splitlines() if l.strip()])


def validate_core_atoms(skill_dir, findings, checked, fingerprints):
    core_dir = skill_dir / "references" / "atoms" / "core"
    if not check(core_dir.is_dir(), "error", "CR000",
                 "缺少核心原子目录 references/atoms/core/", findings):
        return
    found = {p.stem for p in core_dir.glob("*.md")}
    for key in CORE_ATOM_KEYS:
        check(key in found, "error", "CR009",
              f"缺少必需核心原子: {key}.md", findings)
    check(len(found) >= MIN_CORE, "error", "DP013",
          f"核心原子数量({len(found)})低于下限 {MIN_CORE}", findings)
    for f in sorted(core_dir.glob("*.md")):
        rel = str(f.relative_to(skill_dir)).replace("\\", "/")
        checked.append(rel)
        text = read_text(f)
        if not check(text and text.strip(), "error", "CR001",
                     f"核心原子为空: {rel}", findings):
            continue
        check(_atom_header_ok(text), "error", "CR002",
              f"{rel} 头部缺少唯一真相源+自包含声明", findings)
        for lv in SUPPORTED_LEVELS:
            pat = re.compile(r"^#{2,3}\s*" + lv + r"\b.*$", re.MULTILINE)
            idx = None
            for m in re.finditer(pat, text):
                idx = m
                break
            check(idx is not None, "error", "CR003",
                  f"{rel} 缺少深度段 {lv}", findings)
            if idx is not None:
                seg_text = text[idx.end():]
                nxt = re.search(r"^#{2,3}\s*D[1-4]\b", seg_text, re.MULTILINE)
                seg_body = seg_text[:nxt.start()] if nxt else seg_text
                check(_segment_lines(seg_body) >= 3, "error", "CR004",
                      f"{rel} 深度段 {lv} 内容过少(<3 有效行)", findings)
        # T02: 质量清单位号必须等于该原子在 CORE_ATOM_KEYS 中的组装位序
        slot = CORE_ATOM_KEYS.index(f.stem) + 1 if f.stem in CORE_ATOM_KEYS else None
        slot_mentions = re.findall(r"指纹第\s*(\d+)\s*位", text)
        if slot is None:
            # T29: 位序外核心原子不得声明位号,避免与 None 比较产出坏消息
            check(not slot_mentions, "error", "CR011",
                  f"{rel} 为位序外核心原子,不得声明'指纹第N位'"
                  f"(需先在 CORE_ATOM_KEYS 登记位序)", findings)
        else:
            for mentioned in slot_mentions:
                check(int(mentioned) == slot, "error", "CR010",
                      f"{rel} 质量清单位号(第{mentioned}位)与组装序"
                      f"(第{slot}位)不一致,DEPTH 指纹错位", findings)
            if not slot_mentions:
                check(False, "warning", "CR008",
                      f"{rel} 缺少质量清单(含'指纹第{slot}位一致'条目)", findings)
        fingerprints[rel] = hashlib.md5(
            "\n".join(text.strip().splitlines()[:3]).encode()).hexdigest()


def validate_category_atoms(skill_dir, category, code_prefix,
                            findings, checked):
    cat_dir = skill_dir / "references" / "atoms" / category
    if not check(cat_dir.is_dir(), "error", code_prefix + "000",
                 f"缺少目录 references/atoms/{category}/", findings):
        return set()
    files = sorted(cat_dir.glob("*.md"))
    if not check(len(files) >= 1, "error", code_prefix + "001",
                 f"{category} 原子目录为空", findings):
        return set()
    min_n = MIN_DOMAINS if category == "domains" else MIN_OUTPUTS
    check(len(files) >= min_n, "error",
          "DP014" if category == "domains" else "DP015",
          f"{category} 原子数量({len(files)})低于下限 {min_n}", findings)
    stems = set()
    for f in files:
        stems.add(f.stem)
        rel = str(f.relative_to(skill_dir)).replace("\\", "/")
        checked.append(rel)
        text = read_text(f)
        if not check(text and text.strip(), "error", code_prefix + "002",
                     f"{category} 原子为空: {rel}", findings):
            continue
        check(_atom_header_ok(text), "error", code_prefix + "003",
              f"{rel} 头部缺少唯一真相源+自包含声明", findings)
        check(_segment_lines(text) >= 5, "error", code_prefix + "004",
              f"{rel} 内容过少(<5 有效行)", findings)
    return stems


def _parse_manifest_tables(text):
    """解析 manifest 域/输出判定表:返回 {表名: {原子名: 信号串}}。"""
    tables = {}
    current = None
    for line in text.splitlines():
        s = line.strip()
        # 任何二级标题都终止上一个表的收集,否则后续章节的表格会被误吞
        if s.startswith("##"):
            current = None
            if re.match(r"^##\s*域判定(信号)?表", s):
                current = "domains"
                tables[current] = {}
            elif re.match(r"^##\s*输出判定(信号)?表", s):
                current = "outputs"
                tables[current] = {}
            continue
        if current and s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if (len(cells) >= 2 and re.fullmatch(r"[a-z0-9-]+", cells[0])
                    and not re.fullmatch(r"-+", cells[0])):
                if cells[0] not in ("原子", "----", "---"):
                    tables[current][cells[0]] = cells[1]
    return tables


def validate_manifest(skill_dir, findings, checked, dir_stems, out_stems):
    p = skill_dir / "references" / "composition-manifest.md"
    text = read_text(p)
    checked.append("references/composition-manifest.md")
    if not check(text is not None, "error", "MF001",
                 "缺少 references/composition-manifest.md", findings):
        return
    atom_refs = set(re.findall(
        r"atoms/(?:core|domains|outputs)/[a-z0-9-]+\.md", text))
    for rel in sorted(atom_refs):
        checked.append("references/" + rel)
        check((skill_dir / "references" / rel).exists(), "error", "AT001",
              f"组合清单引用的原子不存在: {rel}", findings)
    check("组装流程" in text, "error", "MF002",
          "组合清单缺少'组装流程'章节", findings)
    check(("依赖规则" in text or "R1-R5" in text), "error", "MF003",
          "组合清单缺少对依赖规则(R1-R5)的引用声明"
          "(规则定义归 depth-adaptation.md)", findings)
    # T07: 基调映射须降级为速查并指向计分制唯一判定源
    check(re.search(r"速查|以.*计分制为准|以 routing-protocol", text),
          "error", "MF015",
          "组合清单的基调映射未标注为速查,须声明判定以"
          " routing-protocol.md 计分制为准", findings)
    # T03: 判定表与原子目录双向登记
    tables = _parse_manifest_tables(text)
    for cat, stems in (("domains", dir_stems), ("outputs", out_stems)):
        table = tables.get(cat, {})
        for atom, _sig in table.items():
            check(atom in stems, "error", "MF010" if cat == "domains" else "MF012",
                  f"manifest {cat} 判定表登记了 {atom},但原子文件不存在", findings)
        for stem in stems:
            check(stem in table, "error", "MF011" if cat == "domains" else "MF013",
                  f"{cat} 原子 {stem}.md 已存在,但未登记 manifest {cat} 判定表", findings)


def _eval_depth_pred(depths, atom, op, level):
    """求值单个深度断言:原子名在位序中取深度,按 =/≥/≤ 比较。"""
    if atom not in CORE_ATOM_KEYS:
        return False
    val = depths[CORE_ATOM_KEYS.index(atom)]
    return {"=": val == level, "≥": val >= level, "≤": val <= level}[op]


def validate_depth_adaptation(skill_dir, findings, checked):
    p = skill_dir / "references" / "depth-adaptation.md"
    text = read_text(p)
    checked.append("references/depth-adaptation.md")
    if not check(text is not None, "error", "DP001",
                 "缺少 references/depth-adaptation.md", findings):
        return
    for lv in SUPPORTED_LEVELS:
        check(re.search(r"\b" + lv + r"\b", text) is not None,
              "error", "DP002", f"深度适配协议缺少 {lv} 全局语义定义", findings)
    check(("扩展指南" in text) and ("新增原子" in text),
          "error", "DP003", "深度适配协议缺少'新增原子'扩展指南", findings)
    check(("触发信号" in text) and ("覆盖" in text),
          "error", "DP004", "深度适配协议缺少覆盖触发信号机制", findings)
    check("R1" in text or "依赖规则" in text, "error", "DP005",
          "深度适配协议缺少依赖规则说明", findings)
    dep_defs = set(re.findall(r"^\|\s*R(\d+)\s*\|", text, re.MULTILINE))
    check(len(dep_defs) >= 5, "error", "DP006",
          f"依赖规则 R1-R5 定义不足 5 条(检测到 {sorted(dep_defs)})", findings)
    # T01: 位序表必须与 CORE_ATOM_KEYS 逐位一致(组装序,非字母序)
    seq_m = re.search(r"位序固定为核心原子的组装顺序(.*?)指纹必须写入", text, re.DOTALL)
    if not check(seq_m is not None, "error", "DP007",
                 "深度适配协议缺少'位序固定为组装顺序'声明段", findings):
        return
    pairs = re.findall(r"(\d+)\.\s*([a-z][a-z-]+)", seq_m.group(1))
    seq = [name for _, name in sorted(((int(n), name) for n, name in pairs))]
    check(seq == CORE_ATOM_KEYS, "error", "DP007",
          f"DEPTH 位序表({seq})与脚本组装序({CORE_ATOM_KEYS})不一致,"
          f"指纹将全位错位", findings)
    # T15/T16: LITE-1 豁免声明存在
    check("LITE 骨架豁免" in text, "error", "DP016",
          "深度适配协议缺少 LITE 骨架豁免声明(T06)", findings)


def validate_dependency_rules(skill_dir, findings, checked):
    """T04: R1-R5 规则真实求值——对 complete-examples.md 中每个 DEPTH
    指纹逐规则求值,违反即 error;示例宣称的规则校验结论须与求值一致。"""
    da = read_text(skill_dir / "references" / "depth-adaptation.md")
    ex = read_text(skill_dir / "references" / "complete-examples.md")
    checked.append("references/complete-examples.md")
    if da is None or ex is None:
        return
    rules = re.findall(
        r"^\|\s*R(\d+)\s*\|\s*([a-z-]+)\s*(=|≥|≤)\s*D(\d)\s*\|"
        r"\s*([a-z-]+)\s*(=|≥|≤)\s*D(\d)\s*\|",
        da, re.MULTILINE)
    for num, pre_atom, pre_op, pre_lv, post_atom, post_op, post_lv in rules:
        if pre_atom not in CORE_ATOM_KEYS or post_atom not in CORE_ATOM_KEYS:
            check(False, "warning", "DP012",
                  f"依赖规则 R{num} 引用了位序外原子: "
                  f"{pre_atom}/{post_atom}(需先扩展位序)", findings)
    fingerprints = re.findall(r"DEPTH:\s*\[([\d,\s]+)\]", ex)
    for fp_text in fingerprints:
        vals = [int(x) for x in re.findall(r"\d", fp_text)]
        if len(vals) != len(CORE_ATOM_KEYS):
            check(False, "error", "DP017",
                  f"示例指纹位数({len(vals)})与位序"
                  f"({len(CORE_ATOM_KEYS)}位)不一致: {fp_text.strip()}", findings)
            continue
        for num, pre_atom, pre_op, pre_lv, post_atom, post_op, post_lv in rules:
            pre_true = _eval_depth_pred(vals, pre_atom, pre_op, int(pre_lv))
            if not pre_true:
                continue
            post_true = _eval_depth_pred(vals, post_atom, post_op, int(post_lv))
            check(post_true, "error", "DP011",
                  f"示例指纹 [{','.join(map(str, vals))}] 违反依赖规则 "
                  f"R{num}: 前提({pre_atom}{pre_op}D{pre_lv})成立但"
                  f"结论({post_atom}{post_op}D{post_lv})不成立", findings)
    # T18/T29 门禁化: 示例须覆盖 R3 与 R4 的校验结论(须出现在含校验语义的
    # 行内,防止文档任意位置顺带提及即通过 —— 存在性检查收紧)
    def _has_rule_conclusion(text, rule):
        return any(rule in ln and re.search(r"校验|验证|通过|违反|成立|拦截|满足",
                                            ln)
                   for ln in text.splitlines())
    check(_has_rule_conclusion(ex, "R3"), "warning", "EX004",
          "示例未包含依赖规则 R3 的校验结论", findings)
    check(_has_rule_conclusion(ex, "R4"), "warning", "EX005",
          "示例未包含依赖规则 R4 的校验结论", findings)


def validate_protocol_and_examples(skill_dir, findings, checked):
    rp = skill_dir / "references" / "routing-protocol.md"
    text = read_text(rp)
    checked.append("references/routing-protocol.md")
    if check(text is not None, "error", "RP001",
             "缺少 references/routing-protocol.md", findings):
        check(("第一步" in text and "第五步" in text) or "五步判定" in text,
              "error", "RP002", "路由协议缺少五步判定", findings)
        check("边界场景" in text, "error", "RP003",
              "路由协议缺少边界场景处理", findings)
        # T19: 假设标注统一前缀
        check("假设:" in text, "error", "RP004",
              "路由协议缺少统一的'假设:'标注前缀规范", findings)
    ex = skill_dir / "references" / "complete-examples.md"
    text = read_text(ex)
    if check(text is not None, "error", "EX001",
             "缺少 references/complete-examples.md", findings):
        check("DEPTH:" in text, "error", "EX002",
              "示例缺少 DEPTH 指纹展示", findings)
        check("调档" in text or "迭代" in text, "warning", "EX003",
              "示例未展示调档迭代过程", findings)


def validate_truth_source(skill_dir, fingerprints, findings):
    if not fingerprints:
        return
    probes = ["SKILL.md",
              "references/composition-manifest.md",
              "references/depth-adaptation.md",
              "references/routing-protocol.md",
              "references/complete-examples.md"]
    for probe in probes:
        text = read_text(skill_dir / probe)
        if text is None:
            continue
        hits = [rel for rel, fp in fingerprints.items() if fp in text]
        if hits:
            check(False, "error", "TS001",
                  f"{probe} 复制了原子内容(指纹命中 {hits}),违反唯一真相源",
                  findings)


def _parse_benchmark_yaml(text):
    """极简 YAML 解析:仅支持 cases.yaml 的固定结构,避免引入第三方依赖"""
    cases, cur, slots = [], None, None
    in_cases = False
    for ln in text.splitlines():
        stripped = ln.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = re.match(r"^fingerprint_slots:\s*(\d+)", stripped)
        if m:
            slots = int(m.group(1))
            continue
        if stripped.startswith("cases:"):
            in_cases = True
            continue
        if not in_cases:
            continue
        m = re.match(r"^-\s+id:\s*(\S+)", stripped)
        if m:
            if cur:
                cases.append(cur)
            cur = {"id": m.group(1)}
            continue
        if cur is None:
            continue
        m2 = re.match(r"^(level|domain|requirement|expected_fingerprint"
                      r"|confirmed|boundary_precheck):\s*(.+)$", stripped)
        if m2:
            cur[m2.group(1)] = m2.group(2).strip()
            continue
        m3 = re.match(r"^outputs:\s*\[(.+)\]", stripped)
        if m3:
            cur["outputs"] = [x.strip() for x in m3.group(1).split(",")]
    if cur:
        cases.append(cur)
    return cases, slots


def validate_regression_baseline(skill_dir, findings, checked):
    """R03 产出回归基线:cases.yaml 结构与快照确认状态"""
    yml = skill_dir / BENCHMARK_DIR / "cases.yaml"
    checked.append(str(yml.relative_to(skill_dir)).replace("\\", "/"))
    text = read_text(yml)
    if not check(text is not None, "error", "RB001",
                 "缺少产出回归基线需求集 references/benchmark/cases.yaml",
                 findings):
        return
    cases, slots = _parse_benchmark_yaml(text)
    check(len(cases) >= MIN_BENCH_CASES, "warning", "RB002",
          f"回归需求集用例不足 {MIN_BENCH_CASES} 条(当前 {len(cases)})",
          findings)
    check(slots == len(CORE_ATOM_KEYS), "error", "RB004",
          f"fingerprint_slots({slots}) 与核心原子数"
          f"({len(CORE_ATOM_KEYS)}) 不一致", findings)
    snap_dir = skill_dir / BENCHMARK_DIR / "snapshots"
    check(snap_dir.is_dir(), "warning", "RB005",
          "缺少快照目录 references/benchmark/snapshots/", findings)
    for c in cases:
        fp = c.get("expected_fingerprint", "")
        n = len(re.findall(r"\d+", fp))
        check(n == len(CORE_ATOM_KEYS), "error", "RB006",
              f"用例 {c.get('id')} 指纹位数 {n} 与原子数"
              f" {len(CORE_ATOM_KEYS)} 不一致", findings)
        has_snap = snap_dir.is_dir() and (
            snap_dir / (c.get("id", "") + ".md")).exists()
        # P1-5/R10: 每条用例必须登记第零步能力边界预判结论
        bp = c.get("boundary_precheck", "")
        check(bp in {"none", "C1→A"}, "error", "RB008",
              f"用例 {c.get('id')} boundary_precheck 字段缺失或非法"
              f"(允许: none / C1→A,当前: '{bp}')", findings)
        if c.get("confirmed", "").lower() == "true":
            # T26: 反向校验 —— confirmed:true 必须有对应快照文件
            check(has_snap, "error", "RB007",
                  f"用例 {c.get('id')} 标记 confirmed:true,但快照文件缺失"
                  f"(references/benchmark/snapshots/{c.get('id')}.md)",
                  findings)
        else:
            check(not has_snap, "warning", "RB003",
                  f"用例 {c.get('id')} 已有快照但未人工确认"
                  f"(confirmed 应为 true)", findings)


def validate_quality_metrics(skill_dir, findings, checked):
    """R01 自动可检验指标:阈值表与评分脚本常量的一致性"""
    import ast

    qm = skill_dir / "references" / "quality-metrics.md"
    checked.append("references/quality-metrics.md")
    qtext = read_text(qm)
    sp = skill_dir / "scripts" / "score_prompt.py"
    checked.append("scripts/score_prompt.py")
    stext = read_text(sp)
    if not check(qtext is not None, "error", "QL001",
                 "缺少 references/quality-metrics.md(R01 指标唯一真相源)",
                 findings):
        return
    if not check(stext is not None, "error", "QL002",
                 "缺少 scripts/score_prompt.py(R01 评分实现)", findings):
        return

    doc_codes = set(re.findall(r"^\|\s*(QL\d{3})\s*\|", qtext, re.MULTILINE))
    check(len(doc_codes) >= 8, "warning", "QL003",
          f"指标表条目不足 8 条(检测到 {sorted(doc_codes)})", findings)

    script_metrics = None
    try:
        for node in ast.walk(ast.parse(stext)):
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name) and tgt.id == "METRICS":
                        script_metrics = ast.literal_eval(node.value)
    except (SyntaxError, ValueError) as exc:
        check(False, "error", "QL004",
              f"score_prompt.py 的 METRICS 常量解析失败: {exc}", findings)
        return
    if not check(script_metrics is not None, "error", "QL005",
                 "score_prompt.py 缺少 METRICS 常量", findings):
        return

    only_doc = doc_codes - set(script_metrics)
    only_script = set(script_metrics) - doc_codes
    check(not only_doc, "error", "QL006",
          f"指标表独有的编码未同步到脚本: {sorted(only_doc)}", findings)
    check(not only_script, "error", "QL007",
          f"脚本独有的编码未登记到指标表: {sorted(only_script)}", findings)

    for code in sorted(doc_codes & set(script_metrics)):
        row = re.search(r"^\|\s*" + code + r"\s*\|(.+)$", qtext, re.MULTILINE)
        if not row:
            continue
        cells = [c.strip() for c in row.group(1).split("|")]
        nums = [c for c in cells if re.fullmatch(r"-|\d+(?:\.\d+)?", c)]
        doc_th = {}
        for i, c in enumerate(nums[-4:], start=1):
            if c != "-":
                doc_th[i] = float(c) if "." in c else int(c)
        scr_th = script_metrics[code].get("thresholds", {})
        check(doc_th == scr_th, "warning", "QL008",
              f"{code} 阈值两侧不一致: 文档 {doc_th} vs 脚本 {scr_th}",
              findings)


def validate_token_budget(skill_dir, findings, checked):
    """R04 档位 Token 基线:表结构完整性与常量一致性"""
    p = skill_dir / "references" / "depth-adaptation.md"
    text = read_text(p)
    checked.append("references/depth-adaptation.md")
    if not check(text is not None, "error", "TB001",
                 "缺少 references/depth-adaptation.md", findings):
        return
    check("档位 Token 基线" in text, "error", "TB002",
          "depth-adaptation.md 缺少'档位 Token 基线'章节(R04)", findings)
    rows = re.findall(r"^\|\s*D(\d)\s*\|\s*≈?(\d+)\s*\|", text,
                      re.MULTILINE)
    found = {int(a): int(b) for a, b in rows}
    check(len(found) >= len(SUPPORTED_LEVELS), "warning", "TB003",
          f"Token 基线表档位不足 {len(SUPPORTED_LEVELS)} 档"
          f"(检测到 {sorted(found)})", findings)
    expect = {i + 1: v for i, v in
              enumerate(TOKEN_BASELINE[f"D{i+1}"]
                        for i in range(len(SUPPORTED_LEVELS)))}
    check(found == expect, "warning", "TB004",
          f"Token 基线与脚本常量不一致: 文档 {found} vs 脚本 {expect}"
          f"(估算值待标定,仅提示)", findings)


def validate_model_adapters(skill_dir, findings, checked):
    """R02 模型适配层:适配器契约、注册表双向一致、@model 后缀合法性"""
    ad_dir = skill_dir / "references" / "model-adapters"
    if not check(ad_dir.is_dir(), "error", "MA001",
                 "缺少模型适配器目录 references/model-adapters/(R02)",
                 findings):
        return
    files = sorted(ad_dir.glob("*.md"))
    check(len(files) >= MIN_MODEL_ADAPTERS, "error", "MA002",
          f"模型适配器不足 {MIN_MODEL_ADAPTERS} 个(当前 {len(files)})",
          findings)

    ids = set()
    for f in files:
        rel = str(f.relative_to(skill_dir)).replace("\\", "/")
        checked.append(rel)
        text = read_text(f)
        if not check(text and text.strip(), "error", "MA003",
                     f"模型适配器为空: {rel}", findings):
            continue
        head = text[:500]
        check("MODEL-ADAPTER" in head, "error", "MA004",
              f"{rel} 头部缺少 MODEL-ADAPTER 契约块", findings)
        m = re.search(r"^id:\s*([a-z0-9-]+)\s*$", head, re.MULTILINE)
        if not check(m is not None, "error", "MA005",
                     f"{rel} 契约块缺少 id 字段", findings):
            continue
        aid = m.group(1)
        ids.add(aid)
        check(aid == f.stem, "error", "MA006",
              f"{rel} 契约块 id({aid}) 与文件名({f.stem})不一致", findings)
        suf = re.search(r"^fingerprint_suffix:\s*@model=([a-z0-9-]+)\s*$",
                        head, re.MULTILINE)
        check(suf is not None and suf.group(1) == aid, "error", "MA007",
              f"{rel} 的 fingerprint_suffix 缺失或与 id 不一致", findings)
        check("注入模块" in text, "warning", "MA008",
              f"{rel} 缺少'注入模块'章节(尾部追加片段)", findings)
        check("适用判定信号" in text, "warning", "MA009",
              f"{rel} 缺少'适用判定信号'章节", findings)

    mpath = skill_dir / "references" / "composition-manifest.md"
    mtext = read_text(mpath) or ""
    mdl = re.search(r"## 模型适配表.*?(?=\n## )", mtext, re.DOTALL)
    table_ids = set()
    if mdl:
        table_ids = set(re.findall(r"^\|\s*([a-z][a-z0-9-]*)\s*\|[^|]*\|"
                                   r"[^|]*\|[^|]*\|", mdl.group(0),
                                   re.MULTILINE))
    check(table_ids, "error", "MA010",
          "composition-manifest.md 缺少'模型适配表'或表体为空", findings)
    only_dir = ids - table_ids
    only_table = table_ids - ids
    check(not only_dir, "error", "MA011",
          f"模型适配表未登记的适配器: {sorted(only_dir)}", findings)
    check(not only_table, "error", "MA012",
          f"模型适配表登记了不存在的适配器: {sorted(only_table)}", findings)

    for probe in ("SKILL.md", "references/depth-adaptation.md",
                  "references/composition-manifest.md",
                  "references/complete-examples.md"):
        text = read_text(skill_dir / probe) or ""
        for used in set(re.findall(r"@model=([a-z0-9-]+)", text)):
            check(used in ids, "error", "MA013",
                  f"{probe} 使用了未注册的 @model={used}", findings)


def validate_capability_boundary(skill_dir, findings, checked):
    """R10 能力边界预判:类别齐全、决策树前置、场景4不重复定义"""
    rp = skill_dir / "references" / "routing-protocol.md"
    text = read_text(rp)
    checked.append("references/routing-protocol.md")
    if not check(text is not None, "error", "BN001",
                 "缺少 references/routing-protocol.md", findings):
        return
    m = re.search(r"## 能力边界预判.*?(?=\n## )", text, re.DOTALL)
    if not check(m is not None, "error", "BN002",
                 "routing-protocol.md 缺少'能力边界预判(R10)'章节", findings):
        return
    sec = m.group(0)
    for cid in ("C1", "C2", "C3", "C4", "C5"):
        check(re.search(r"^\|\s*" + cid + r"\s*\|", sec, re.MULTILINE)
              is not None, "error", "BN003",
              f"能力边界判定表缺少类别 {cid}", findings)
    # 精确定位决策树中的第零步标题(存在性检查会被别处提及蒙混过关)
    step0 = re.search(r"^### 第零步[:：].*$", text, re.MULTILINE)
    check(step0 is not None and "能力边界预判" in step0.group(0), "error",
          "BN004",
          "决策树缺少'第零步:能力边界预判'或其标题未标注能力边界,"
          "边界检查未前置到计分之前", findings)
    # 场景 4 必须指向 R10 节,避免两处重复定义同一规则
    s4 = re.search(r"### 场景 4:.*?(?=\n### )", text, re.DOTALL)
    check(s4 is not None and "能力边界预判" in s4.group(0), "error", "BN005",
          "边界场景 4 未指向'能力边界预判(R10)'节,"
          "存在重复定义风险(唯一真相源)", findings)
    check("处理模板" in sec and re.search(r"^A\.|A\. 降级", sec, re.MULTILINE)
          is not None, "error", "BN006",
          "能力边界预判节缺少'处理模板'或 A/B/C 路径", findings)
    # C4 与场景 3 易混淆,必须有显式区分说明
    check("C4 与边界场景 3" in sec or "场景 3" in sec, "warning", "BN007",
          "能力边界预判节未说明 C4 与边界场景 3 的区分,易重复处理", findings)


def validate_fingerprint(skill_dir, findings, checked):
    """R07 指纹 v2:工具存在性、位序一致、文档指纹可解析、后缀白名单"""
    import ast
    import subprocess

    fp = skill_dir / "scripts" / "fingerprint.py"
    checked.append("scripts/fingerprint.py")
    if not check(fp.exists(), "error", "FP001",
                 "缺少 scripts/fingerprint.py(R07 指纹工具)", findings):
        return
    stext = read_text(fp)
    script_keys = None
    try:
        for node in ast.walk(ast.parse(stext)):
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name) and tgt.id == "CORE_ATOM_KEYS":
                        script_keys = ast.literal_eval(node.value)
    except (SyntaxError, ValueError) as exc:
        check(False, "error", "FP002",
              f"fingerprint.py 的 CORE_ATOM_KEYS 解析失败: {exc}", findings)
        return
    check(script_keys == CORE_ATOM_KEYS, "error", "FP003",
          f"fingerprint.py 位序 {script_keys} 与门禁 CORE_ATOM_KEYS "
          f"{CORE_ATOM_KEYS} 不一致", findings)

    da = skill_dir / "references" / "depth-adaptation.md"
    dtext = read_text(da) or ""
    # 精确定位后缀语法声明行,避免文档别处提及即误判为已定义
    syn = re.search(r"^DEPTH:\s*\[d1[^\n]*$", dtext, re.MULTILINE)
    if not check(syn is not None, "error", "FP004",
                 "depth-adaptation.md 缺少指纹后缀语法声明行"
                 "(形如 DEPTH: [d1,...,d9] [@model=..] [@lang=..] [@tokens=..])",
                 findings):
        syn_line = ""
    else:
        syn_line = syn.group(0)
        for key in ("@model", "@lang", "@tokens"):
            check(key in syn_line, "error", "FP005",
                  f"指纹后缀语法声明行缺少 {key}(R07)", findings)
    check("FP-HASH" in dtext or "指纹哈希" in dtext, "error", "FP006",
          "depth-adaptation.md 缺少'指纹哈希'规范(R07)", findings)

    # T28: R1-R5 双真相源一致性 —— fingerprint.py 硬编码的 DEPENDENCY_RULES
    # 必须与 depth-adaptation.md 规则表逐条一致(注意两侧归一化为同型)
    script_rules = None
    try:
        for node in ast.walk(ast.parse(stext)):
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name) and tgt.id == "DEPENDENCY_RULES":
                        script_rules = ast.literal_eval(node.value)
    except (SyntaxError, ValueError) as exc:
        check(False, "error", "FP010",
              f"fingerprint.py 的 DEPENDENCY_RULES 解析失败: {exc}", findings)
        script_rules = None
    if script_rules is not None:
        norm_scr = sorted(tuple(r) for r in script_rules)
        doc_rules = re.findall(
            r"^\|\s*R(\d+)\s*\|\s*([a-z-]+)\s*(=|≥|≤)\s*D(\d)\s*\|"
            r"\s*([a-z-]+)\s*(=|≥|≤)\s*D(\d)\s*\|", dtext, re.MULTILINE)
        norm_doc = sorted((a, op, int(l), b, op2, int(l2))
                          for _, a, op, l, b, op2, l2 in doc_rules)
        check(norm_doc == norm_scr, "error", "FP010",
              f"fingerprint.py DEPENDENCY_RULES 与 depth-adaptation.md "
              f"规则表不一致,diff 的依赖违规提示将失真: "
              f"文档 {norm_doc} vs 脚本 {norm_scr}", findings)

    allowed = {"model", "lang", "tokens"}
    probes = ("SKILL.md", "references/depth-adaptation.md",
              "references/composition-manifest.md",
              "references/complete-examples.md")
    pat = re.compile(r"DEPTH:\s*\[[\d,\s]+\](?:\s+@[a-z]+=\S+)*")
    seen = 0
    for probe in probes:
        text = read_text(skill_dir / probe) or ""
        for used in set(re.findall(r"@([a-z]+)=", text)):
            if used in allowed:
                continue
            # 仅在 DEPTH 上下文中的 @key 才算后缀
            check(not re.search(r"DEPTH:[^\n]*@" + used + r"=", text),
                  "error", "FP007",
                  f"{probe} 使用了未支持的指纹后缀 @{used}="
                  f"(合法: {sorted(allowed)})", findings)
        for m in pat.finditer(text):
            raw = m.group(0)
            seen += 1
            r = subprocess.run(
                [sys.executable, str(fp), "parse", raw,
                 "--skill-dir", str(skill_dir)],
                capture_output=True, text=True, encoding="utf-8")
            check(r.returncode == 0, "error", "FP008",
                  f"{probe} 中的指纹无法解析: {raw}", findings)
    check(seen >= 1, "warning", "FP009",
          "未在文档中发现任何 DEPTH 指纹示例,FP007 校验未生效", findings)


def validate_prompt_ir(skill_dir, findings, checked):
    """R05 PromptIR v0:规范文档结构与多模型样本完备性"""
    p = skill_dir / "references" / "prompt-ir.md"
    checked.append("references/prompt-ir.md")
    text = read_text(p)
    if not check(text is not None, "error", "IR001",
                 "缺少 references/prompt-ir.md(PromptIR 规范)", findings):
        return
    check("五后端映射表" in text and "IR 字段表" in text, "error", "IR002",
          "prompt-ir.md 缺少'IR 字段表'或'五后端映射表'章节", findings)
    check("一致性不变量" in text, "error", "IR003",
          "prompt-ir.md 缺少'一致性不变量'章节(后端渲染校验清单)", findings)
    samples = sorted((skill_dir / "references" / "benchmark" /
                      "model-samples").glob("*.md")) if (
        skill_dir / "references" / "benchmark" / "model-samples").is_dir() else []
    check(len(samples) >= MIN_MODEL_ADAPTERS, "error", "IR004",
          f"多模型样本不足 {MIN_MODEL_ADAPTERS} 组(当前 {len(samples)}),"
          f"IR 抽象失去样本支撑", findings)
    for s in samples:
        rel = str(s.relative_to(skill_dir)).replace("\\", "/")
        checked.append(rel)
        stext = read_text(s) or ""
        check(re.search(r"^DEPTH:\s*\[[\d,\s]+\]\s+@model=", stext, re.MULTILINE)
              is not None, "error", "IR005",
              f"多模型样本 {rel} 缺少带 @model 后缀的 DEPTH 头部", findings)


def validate_prompt_package(skill_dir, findings, checked):
    """R06 提示词包协议 v0:协议文档结构完整性"""
    p = skill_dir / "references" / "prompt-package.md"
    checked.append("references/prompt-package.md")
    text = read_text(p)
    if not check(text is not None, "error", "PK001",
                 "缺少 references/prompt-package.md(提示词包协议)", findings):
        return
    check("包结构" in text and "交接协议" in text, "error", "PK002",
          "prompt-package.md 缺少'包结构'或'交接协议'章节", findings)
    check("task_id" in text and "status" in text and "depends_on" in text,
          "error", "PK003",
          "prompt-package.md 缺少交接字段(task_id/status)或 DAG 依赖"
          "(depends_on)定义", findings)
    check("package.yaml" in text, "error", "PK004",
          "prompt-package.md 缺少 package.yaml 包清单定义", findings)


def validate_atom_registry(skill_dir, findings, checked):
    """R08 原子注册中心:registry 与 atoms 目录双向一致"""
    p = skill_dir / "references" / "registry" / "atom-registry.yaml"
    checked.append("references/registry/atom-registry.yaml")
    text = read_text(p)
    if not check(text is not None, "error", "RG001",
                 "缺少 references/registry/atom-registry.yaml(原子注册中心)",
                 findings):
        return
    entries = {}
    cur = None
    for ln in text.splitlines():
        s = ln.strip()
        m = re.match(r"^-\s+id:\s*([a-z0-9-]+)", s)
        if m:
            cur = m.group(1)
            entries[cur] = {}
            continue
        m2 = re.match(r"^(type|source|version|description):\s*(.+)$", s)
        if m2 and cur:
            entries[cur][m2.group(1)] = m2.group(2).strip()
    dir_entries = {}
    for cat, ctype in (("core", "core"), ("domains", "domain"),
                       ("outputs", "output")):
        d = skill_dir / "references" / "atoms" / cat
        if d.is_dir():
            for f in d.glob("*.md"):
                dir_entries[f.stem] = ctype
    only_reg = set(entries) - set(dir_entries)
    only_dir = set(dir_entries) - set(entries)
    check(not only_reg, "error", "RG002",
          f"注册中心登记了不存在的原子: {sorted(only_reg)}", findings)
    check(not only_dir, "error", "RG003",
          f"目录存在但未登记注册中心的原子: {sorted(only_dir)}", findings)
    for aid, fields in sorted(entries.items()):
        wrong_type = ("type" in fields and aid in dir_entries
                      and fields["type"] != dir_entries[aid])
        check(not wrong_type, "error", "RG004",
              f"原子 {aid} 的 type({fields.get('type')}) 与目录归属"
              f"({dir_entries.get(aid)})不一致", findings)
        missing = [k for k in ("type", "source", "version")
                   if k not in fields]
        check(not missing, "warning", "RG005",
              f"原子 {aid} 注册条目缺少字段: {missing}", findings)
    # RG006(P2-3): deps 字段与 DEPENDENCY_RULES 反查一致 —— 激活 deps 死接口
    fp_src = read_text(skill_dir / "scripts" / "fingerprint.py")
    if check(fp_src is not None, "error", "RG006",
             "缺少 scripts/fingerprint.py,deps 反查失败", findings):
        try:
            fm = re.search(r"DEPENDENCY_RULES = \[(.*?)\]", fp_src, re.DOTALL)
            pairs = re.findall(
                r'\("([a-z0-9-]+)",\s*"[≥≤=]+",\s*\d+,\s*'
                r'"([a-z0-9-]+)",\s*"[≥≤=]+",\s*\d+\)', fm.group(1))
            expected = {}
            for i, (a, b) in enumerate(pairs, 1):
                expected.setdefault(a, set()).add(f"R{i}")
                expected.setdefault(b, set()).add(f"R{i}")
        except (AttributeError, ValueError):
            pairs = []
        if pairs:
            for aid in sorted(dir_entries):
                atom_file = (skill_dir / "references" / "atoms" /
                             ("core" if dir_entries[aid] == "core"
                              else "domains" if dir_entries[aid] == "domain"
                              else "outputs") / (aid + ".md"))
                atext = read_text(atom_file)
                am = re.search(r"^deps:\s*(\S+)\s*$", atext or "",
                               re.MULTILINE)
                declared = am.group(1) if am else ""
                want = (",".join(sorted(expected.get(aid, set())))
                        or "none")
                check(declared == want, "error", "RG006",
                      f"原子 {aid} deps 声明('{declared}')与依赖规则反查"
                      f"('{want}')不一致", findings)


def validate_dir_hygiene(skill_dir, findings):
    for item in sorted(skill_dir.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir() and not any(item.iterdir()):
            check(False, "warning", "DH002",
                  f"空目录: {item.name}", findings)
        if item.is_file() and item.name not in WHITELIST_TOP:
            check(False, "warning", "DH005",
                  f"存在资源索引声明之外的顶层文件: {item.name}", findings)
        # T30: 顶层目录同受白名单约束,堵住"新目录绕过 DH005"的盲区
        if item.is_dir() and item.name not in WHITELIST_TOP:
            check(False, "warning", "DH005",
                  f"存在资源索引声明之外的顶层目录: {item.name}", findings)
    for pat in TMP_PATTERNS:
        for f in skill_dir.rglob(pat):
            check(False, "warning", "DH003",
                  f"临时文件残留: {f.relative_to(skill_dir)}", findings)
    atoms_dir = skill_dir / "references" / "atoms"
    if atoms_dir.is_dir():
        for f in atoms_dir.rglob("*"):
            if f.is_file() and f.suffix != ".md":
                check(False, "warning", "DH006",
                      f"atoms 目录存在非 .md 文件: {f.name}", findings)
    coze = skill_dir / ".coze"
    if coze.exists():
        findings.append({"level": "info", "code": "DH004",
                         "message": "检测到 .coze 文件,按保护规则保留"})


def main():
    parser = argparse.ArgumentParser(description="Skill 契约门禁校验(v5.1)")
    parser.add_argument("--skill-dir", required=True)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--token-budget", type=int, default=None,
                        help="R04:给定 token 预算,输出推荐的最高可用档位")
    args = parser.parse_args()
    skill_dir = Path(args.skill_dir).resolve()

    findings, checked, fingerprints = [], [], {}
    validate_frontmatter(skill_dir, findings, checked)
    validate_resource_index(skill_dir, findings, checked)
    validate_lite_skeleton(skill_dir, findings)
    validate_core_atoms(skill_dir, findings, checked, fingerprints)
    dir_stems = validate_category_atoms(skill_dir, "domains", "DM",
                                        findings, checked)
    out_stems = validate_category_atoms(skill_dir, "outputs", "OU",
                                        findings, checked)
    validate_manifest(skill_dir, findings, checked, dir_stems, out_stems)
    validate_depth_adaptation(skill_dir, findings, checked)
    validate_dependency_rules(skill_dir, findings, checked)
    validate_protocol_and_examples(skill_dir, findings, checked)
    validate_truth_source(skill_dir, fingerprints, findings)
    validate_quality_metrics(skill_dir, findings, checked)
    validate_regression_baseline(skill_dir, findings, checked)
    validate_token_budget(skill_dir, findings, checked)
    validate_model_adapters(skill_dir, findings, checked)
    validate_capability_boundary(skill_dir, findings, checked)
    validate_fingerprint(skill_dir, findings, checked)
    validate_prompt_ir(skill_dir, findings, checked)
    validate_prompt_package(skill_dir, findings, checked)
    validate_atom_registry(skill_dir, findings, checked)
    validate_dir_hygiene(skill_dir, findings)

    advice = None
    if args.token_budget is not None:
        budget = args.token_budget
        fit = [lv for lv in SUPPORTED_LEVELS if TOKEN_BASELINE[lv] <= budget]
        advice = {
            "budget": budget,
            "max_level": fit[-1] if fit else None,
            "note": ("预算低于 D1 基线,建议走 LITE 骨架直出"
                     if not fit else
                     f"最高可用档位 {fit[-1]};若低于基调判定档位,"
                     f"降级后须重跑依赖规则 R1-R5"),
        }
        findings.append({"level": "info", "code": "TB010",
                         "message": f"token 预算 {budget} → "
                                    f"{advice['note']}"})

    errors = sum(1 for f in findings if f["level"] == "error")
    warnings = sum(1 for f in findings if f["level"] == "warning")
    status = "passed" if errors == 0 and (not args.strict or warnings == 0) else "failed"
    # 版本真相源:派生自 SKILL.md frontmatter(T11)
    sk = read_text(skill_dir / "SKILL.md") or ""
    fm_ver = fm_number(re.match(r"^---\s*\n(.*?)\n---\s*\n", sk, re.DOTALL).group(1)
                       if re.match(r"^---\s*\n(.*?)\n---\s*\n", sk, re.DOTALL) else "",
                       "version") or "unknown"
    result = {
        "skill_dir": str(skill_dir),
        "version": fm_ver + "-atomic-registry",
        "checked_files": sorted(set(checked)),
        "summary": {"passed": len(checked), "warnings": warnings,
                    "errors": errors},
        "findings": findings,
        "status": status,
    }
    if advice is not None:
        result["token_advice"] = advice
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if status == "passed" else 1)


if __name__ == "__main__":
    main()
