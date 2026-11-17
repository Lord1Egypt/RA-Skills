#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
on-demand-expert-team 团队设计文档门禁预检脚本
在 OD1-02 设计定稿前运行，检查设计稿是否满足本领域硬约束：
编排者纯编排声明 / 成员清单（含输出物列）/ SOP 阶段数 3~5 / 并行串行标注 / 门禁点 / 凭证安全。

用法:
    python scripts/validate_team_design.py <团队设计文档.md>

输出: 逐项 [PASS]/[FAIL]/[WARN] + 汇总；存在 FAIL 时退出码为 1，否则 0。
依赖: 仅 Python 3.8+ 标准库。
说明: 本脚本只做结构门禁预检，不判断设计内容的业务正确性。
"""
import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    (r"Bearer\s+[A-Za-z0-9\-_.]{25,}", "疑似硬编码 Bearer Token"),
    (r"sk-[A-Za-z0-9]{16,}", "疑似 API Key（sk- 前缀）"),
    (r"ghp_[A-Za-z0-9]{20,}", "疑似 GitHub Token"),
    (r"AKIA[0-9A-Z]{16}", "疑似 AWS Access Key"),
]

PHASE_RE = re.compile(r"(?i)phase\s*([0-9]+)|阶段\s*([0-9]+)|第\s*([一二三四五六七八九十])\s*阶段")

results = []


def add(level, name, detail=""):
    results.append((level, name, detail))


def split_row(line: str):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/validate_team_design.py <团队设计文档.md>")
        sys.exit(2)
    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"[FAIL] 设计文档不存在: {path}")
        sys.exit(2)
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[FAIL] 无法以 UTF-8 读取: {e}")
        sys.exit(2)

    # 1. 编排者纯编排声明
    if re.search(r"纯编排|不亲自|只做编排", text):
        add("PASS", "编排者纯编排声明", "包含纯编排/不亲自做专业分析表述")
    else:
        add("FAIL", "编排者纯编排声明", "未找到「纯编排/不亲自/只做编排」声明——编排者必须纯编排")

    # 2. 成员清单表（含输出物列）
    tables = []
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            header = split_row(lines[i])
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append(split_row(lines[j]))
                j += 1
            tables.append((header, rows))
            i = j
        else:
            i += 1
    member_tables = [t for t in tables if "输出物" in t[0]]
    if not member_tables:
        add("FAIL", "成员清单表", "未找到含「输出物」列的成员清单表（五列：角色/类型/职责/输出物/接口）")
    else:
        header, rows = member_tables[0]
        rows = [r for r in rows if any(r)]
        if len(rows) >= 1:
            add("PASS", "成员清单表", f"{len(rows)} 名成员，含输出物列")
            empty_out = [r[header.index("输出物")] for r in rows
                         if "输出物" in header and header.index("输出物") < len(r)
                         and not r[header.index("输出物")]]
            if empty_out:
                add("FAIL", "成员输出物", f"{len(empty_out)} 名成员输出物为空——每个成员必须有明确输出物")
            else:
                add("PASS", "成员输出物", "全部成员输出物已定义")
        else:
            add("FAIL", "成员清单表", "成员清单表无数据行")

    # 3. SOP 阶段数 3~5
    phase_tokens = set()
    for m in PHASE_RE.finditer(text):
        num = next((g for g in m.groups() if g), "")
        cn = {"一": "1", "二": "2", "三": "3", "四": "4", "五": "5",
              "六": "6", "七": "7", "八": "8", "九": "9", "十": "10"}
        phase_tokens.add(cn.get(num, num))
    if 3 <= len(phase_tokens) <= 5:
        add("PASS", "SOP 阶段数", f"{len(phase_tokens)} 个阶段（3~5 达标，基元数≤5）")
    elif len(phase_tokens) > 5:
        add("FAIL", "SOP 阶段数", f"{len(phase_tokens)} 个阶段，超过 5——须回 OD0-01 重新拆解（基元数≤5）")
    else:
        add("FAIL", "SOP 阶段数", f"仅识别到 {len(phase_tokens)} 个阶段，至少需要 3 个")

    # 4. 并行/串行标注
    if re.search(r"并行|串行|‖|⇉", text):
        add("PASS", "并行/串行标注", "存在执行方式标注")
    else:
        add("FAIL", "并行/串行标注", "未找到并行/串行标注——每阶段必须标注执行方式")

    # 5. 门禁点
    if "门禁" in text:
        add("PASS", "门禁校准点", "存在门禁点定义")
    else:
        add("FAIL", "门禁校准点", "未找到门禁点——每阶段必须定义覆盖性/一致性/可汇编性核对内容")

    # 6. 凭证安全
    scanned = re.sub(r"\{\{[A-Za-z0-9_]+\}\}", "PLACEHOLDER", text)
    scanned = re.sub(r"\$\{[A-Za-z0-9_]+\}", "PLACEHOLDER", scanned)
    sec_hits = [label for pattern, label in SECRET_PATTERNS if re.search(pattern, scanned)]
    if sec_hits:
        add("FAIL", "凭证安全", "；".join(set(sec_hits)) + "，请改为 ${VAR} 占位符")
    else:
        add("PASS", "凭证安全", "未发现硬编码凭证")

    n_fail = sum(1 for lv, _, _ in results if lv == "FAIL")
    n_pass = sum(1 for lv, _, _ in results if lv == "PASS")
    print(f"\n===== 团队设计门禁预检: {path.name} =====")
    for lv, name, detail in results:
        mark = "✅" if lv == "PASS" else "❌"
        line = f"{mark} [{lv}] {name}"
        if detail:
            line += f" — {detail}"
        print(line)
    print(f"----- 汇总: PASS={n_pass}  FAIL={n_fail} -----")
    if n_fail:
        print("结论: 未通过（FAIL 项修正后复检，全部通过再进入拉起运行）")
        sys.exit(1)
    print("结论: 通过（进入 OD2 团队实例化）")
    sys.exit(0)


if __name__ == "__main__":
    main()
