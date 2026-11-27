#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""知识循环定位策略师 — 产物确定性校验

校验七类产物文件的结构契约（章节齐全、字段顺序、枚举合法、占位符替换、声明非空）。

覆盖边界声明（按 requirements D 节纪律自应用）：
  覆盖：七类产物的结构契约——章节齐全与顺序、表头字段与顺序、枚举取值合法、
        占位符已替换、覆盖边界/默会核心声明非空。
  不覆盖：内容真值（由领域验证器与领域共同体裁决）、判据实例化质量、
          三态语义正确性（由 KLS0-03 人工抽查兜底）、新知识内容本身的裁决。

用法:
    python KLS_validate_position.py 【产物文件】 --type diagnosis|roadmap|verifier|question|experiment|valuecriteria|historyledger
退出码: 0=全部 PASS, 1=存在 FAIL, 2=用法错误
依赖: 仅 Python 3 标准库

原子结构（依赖序）:
  ① 枚举原子：THREE_STATES/CLOCK_STAGES/LADDER（零依赖合法值词表）
  ② 契约原子：REQUIRED_SECTIONS（七类型章节契约，按域管线序）＋ QUESTION_HEADER/HISTORY_HEADER（表头契约）
  ③ 读取原子：read_text（唯一 I/O 原语）
  ④ 检查原子：通用三检（章节/占位符/枚举）在前，类型专检按管线序在后，互不调用
  ⑤ 编排：validate 按类型分发，main 按 CLI 串联
"""

import argparse
import io
import os
import re
import sys

# ── 原子层①：枚举原子（零依赖合法值词表，被④枚举检查与类型专检引用）──
# 三态枚举（与 requirements 全局约定 G 一致）
THREE_STATES = ("已裁决", "已校验", "待裁决")
# 阶段枚举（与 requirements 全局约定 D 一致）
CLOCK_STAGES = ("已普及", "普及中", "稀缺")
# 五层阶梯枚举
LADDER = ("执行层", "设计层", "验证层", "问题层", "品味层")

# ── 原子层②：契约原子（各类型产物的结构契约，④检查原子的判据来源；类型按域管线序排列）──
# 各类型产物的必需章节关键词（按出现顺序）
# mode=heading：关键词只匹配 H2 及以下标题行（排除文档 H1 大标题）
# mode=table：关键词匹配全文（表格契约类）
REQUIRED_SECTIONS = {
    "diagnosis": {"mode": "heading", "sections": ["环节定位", "分层判定", "分档判定", "普及时钟评估", "资产盘点", "结论与建议", "白话结论"]},
    "roadmap": {"mode": "heading", "sections": ["目标匹配", "等价转化", "路线", "死路排除", "里程碑", "退路", "白话结论"]},
    "verifier": {"mode": "heading", "sections": ["直觉图景", "裁决点", "覆盖边界", "闭环运行方案"]},
    "question": {"mode": "table", "sections": ["来源模式", "问题表述", "核心问题", "四维评估", "去重状态"]},
    "experiment": {"mode": "table", "sections": ["需实验裁决点", "观测指标", "三态预期", "前置条件"]},
    "valuecriteria": {"mode": "table", "sections": ["判据编号", "判据内容", "适用轨道", "适用分层", "默会核心声明"]},
    "historyledger": {"mode": "table", "sections": ["取舍结论", "所用判据版本", "事后校验状态", "履历小结"]},
}

# question 类产物的表头字段契约（顺序敏感）
QUESTION_HEADER = [
    "序号", "日期", "来源模式", "问题表述", "核心问题",
    "四维评估", "可对话理论传统", "预期非平庸结论", "去重状态",
]

# historyledger 类产物的表头字段契约（顺序敏感，九列与价值终审协议同构）
HISTORY_HEADER = [
    "时间", "判断对象", "取舍结论", "所用判据版本", "依据",
    "事后校验状态", "证据来源", "共同体公认记录", "更新日期",
]


# ── 原子层③：读取原子（唯一 I/O 原语，被④全部检查原子依赖）──
def read_text(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return f.read()


# ── 原子层④：检查原子（每个只查一件事、互不调用；通用三检在前，类型专检按管线序 diagnosis→verifier→question→valuecriteria→historyledger）──
def check_sections(text, sections, results, mode="heading"):
    if mode == "heading":
        # 只取 H2 及以下标题行（排除文档 H1 大标题），按行序校验章节顺序
        headings = []
        for i, ln in enumerate(text.splitlines()):
            m = re.match(r"^#{2,6}\s*(.*)$", ln)
            if m:
                headings.append((i, m.group(1)))
        pos = -1
        for sec in sections:
            hit = next((h for h in headings if sec in h[1]), None)
            if hit is None:
                results.append(("FAIL", "缺少必需章节标题: %s" % sec))
            elif hit[0] < pos:
                results.append(("FAIL", "章节顺序错误: %s 出现在前序章节之前" % sec))
            else:
                pos = hit[0]
                results.append(("PASS", "章节存在且顺序正确: %s" % sec))
    else:
        pos = -1
        for sec in sections:
            idx = text.find(sec)
            if idx < 0:
                results.append(("FAIL", "缺少必需关键词: %s" % sec))
            elif idx < pos:
                results.append(("FAIL", "关键词顺序错误: %s" % sec))
            else:
                pos = idx
                results.append(("PASS", "关键词存在且顺序正确: %s" % sec))


def check_placeholders(text, results):
    leftovers = re.findall(r"\{\{[^}]*\}\}", text)
    if leftovers:
        results.append(("FAIL", "存在未替换占位符 %d 处，示例: %s" % (len(leftovers), leftovers[0])))
    else:
        results.append(("PASS", "占位符已全部替换"))


def check_enums(text, results):
    """按标签独立校验枚举取值。边界判定：取值后随分隔符（——/；/。/，/）/行尾/表格竖线）才算枚举用法，
    后随其他正文字符视为散文句式，跳过——避免把正文叙述误判为枚举违规。"""
    enum_map = {
        "状态": THREE_STATES,
        "阶段": CLOCK_STAGES,
        "档位": ("自主档", "协作档", "人类主导档"),
        "层级": LADDER,
        "层": LADDER,
        "轨道": ("学术轨", "商业轨", "生活轨", "多轨"),
    }
    separators = "——；。，）|\n"
    total_bad = 0
    for label, legal in enum_map.items():
        illegal = []
        for m in re.finditer(label + r"[:：]\s*([^\s|，。；——）]{1,12})", text):
            val = m.group(1).strip()
            nxt = text[m.end()] if m.end() < len(text) else "\n"
            if val and (nxt in separators or m.end() == len(text)) and not any(v in val for v in legal):
                illegal.append(val)
        if illegal:
            total_bad += len(illegal)
            results.append(("FAIL", "%s 存在非法枚举值: %s（合法值: %s）" % (label, "、".join(illegal[:5]), "/".join(legal))))
    if total_bad == 0:
        results.append(("PASS", "枚举值合法（状态/阶段/档位/层级，散文句式已豁免）"))


def check_clock_evidence(text, results):
    """diagnosis 类：时间区间旁必须有依据或"待验证"。"""
    if "时间区间" not in text and "时间估计" not in text:
        results.append(("PASS", "未含时间估计，无需依据检查"))
        return
    window = text[max(0, text.find("时间区间") if "时间区间" in text else text.find("时间估计")):]
    seg = window[:400]
    if ("依据" in seg) or ("待验证" in seg):
        results.append(("PASS", "时间估计附依据或标注待验证"))
    else:
        results.append(("FAIL", "时间估计缺少依据且未标注待验证"))


def check_verifier_states(text, results):
    """verifier 类：三态标注必须出现，且状态列只允许三态取值。"""
    if not any(s in text for s in THREE_STATES):
        results.append(("FAIL", "缺少三态标注（已裁决/已校验/待裁决）"))
        return
    results.append(("PASS", "三态标注存在"))
    rows = [ln for ln in text.splitlines() if ln.strip().startswith("|") and re.search(r"已裁决|已校验|待裁决", ln)]
    bad = [ln.strip()[:40] for ln in rows if not re.search(r"\|\s*(已裁决|已校验|待裁决)\s*\|", ln)]
    if bad:
        results.append(("FAIL", "状态列存在非法取值的行 %d 条，示例: %s" % (len(bad), bad[0])))
    else:
        results.append(("PASS", "状态列取值全部合法"))


def check_question_header(text, results):
    header_rows = [ln for ln in text.splitlines() if ln.strip().startswith("|")]
    if not header_rows:
        results.append(("FAIL", "未找到 Markdown 表格（问题资产卡需表格契约）"))
        return
    header_line = header_rows[0]
    cells = [c.strip() for c in header_line.strip("|").split("|")]
    missing = [h for h in QUESTION_HEADER if h not in cells]
    if missing:
        results.append(("FAIL", "表头缺少契约字段: %s" % "、".join(missing)))
    elif cells[: len(QUESTION_HEADER)] != QUESTION_HEADER:
        results.append(("FAIL", "表头字段顺序与契约不一致"))
    else:
        results.append(("PASS", "表头字段与顺序符合契约"))


def check_valuecriteria_declaration(text, results):
    """valuecriteria 类：默会核心声明必须存在且非空（硬边界二自应用）。"""
    idx = text.find("默会核心声明")
    if idx < 0:
        results.append(("FAIL", "缺少默会核心声明（品味层核心判断不可编码，必须显式声明）"))
        return
    seg = text[idx: idx + 300].strip()
    after = re.sub(r"^#\s*默会核心声明.*$", "", seg, flags=re.M).strip()
    after = re.sub(r"^##\s*.*$", "", after, flags=re.M).strip()
    body = after[len("默会核心声明"):].strip("：: \n")
    if len(body) < 10 and "{{" not in body:
        results.append(("FAIL", "默会核心声明为空或过短（不得为空）"))
    else:
        results.append(("PASS", "默会核心声明非空"))


def check_history_header(text, results):
    """historyledger 类：九列表头契约（顺序敏感，与价值终审协议同构）。"""
    header_rows = [ln for ln in text.splitlines() if ln.strip().startswith("|")]
    if not header_rows:
        results.append(("FAIL", "未找到 Markdown 表格（判断履历台账需表格契约）"))
        return
    header_line = header_rows[0]
    cells = [c.strip() for c in header_line.strip("|").split("|")]
    missing = [h for h in HISTORY_HEADER if h not in cells]
    if missing:
        results.append(("FAIL", "表头缺少契约字段: %s" % "、".join(missing)))
    elif cells[: len(HISTORY_HEADER)] != HISTORY_HEADER:
        results.append(("FAIL", "表头字段顺序与契约不一致"))
    else:
        results.append(("PASS", "表头九列与顺序符合契约"))


# ── 原子层⑤：编排（validate 按类型分发——依赖④；main 按 CLI 串联——依赖⑤）──
def validate(path, ptype):
    results = []
    if not os.path.isfile(path):
        results.append(("FAIL", "文件不存在: %s" % path))
        return results
    try:
        text = read_text(path)
    except UnicodeDecodeError:
        results.append(("FAIL", "编码错误：文件须为 UTF-8"))
        return results
    if not text.strip():
        results.append(("FAIL", "文件为空"))
        return results

    spec = REQUIRED_SECTIONS[ptype]
    check_sections(text, spec["sections"], results, mode=spec["mode"])
    check_placeholders(text, results)

    if ptype == "diagnosis":
        check_enums(text, results)
        check_clock_evidence(text, results)
    elif ptype == "roadmap":
        check_enums(text, results)
    elif ptype == "verifier":
        check_verifier_states(text, results)
        check_enums(text, results)
        idx = text.find("覆盖边界")
        if idx >= 0:
            seg = text[idx: idx + 300]
            after = re.sub(r"^#\s*覆盖边界.*$", "", seg, flags=re.M).strip()
            after = re.sub(r"^##\s*.*$", "", after, flags=re.M).strip()
            if len(after) < 10 and "{{" not in after:
                results.append(("FAIL", "覆盖边界声明为空（不得为空）"))
            else:
                results.append(("PASS", "覆盖边界声明非空"))
        else:
            results.append(("FAIL", "缺少覆盖边界声明"))
    elif ptype == "question":
        check_question_header(text, results)
    elif ptype == "experiment":
        pass  # 结构契约由 check_sections 覆盖（关键词存在与顺序）
    elif ptype == "valuecriteria":
        check_valuecriteria_declaration(text, results)
    elif ptype == "historyledger":
        check_history_header(text, results)
    return results


def main():
    parser = argparse.ArgumentParser(description="KLS 产物确定性校验")
    parser.add_argument("file", help="产物文件路径")
    parser.add_argument("--type", required=True,
                        choices=["diagnosis", "roadmap", "verifier", "question", "experiment", "valuecriteria", "historyledger"],
                        help="产物类型")
    args = parser.parse_args()

    results = validate(args.file, args.type)
    print("=" * 56)
    print("KLS 产物校验报告  类型: %s  文件: %s" % (args.type, os.path.basename(args.file)))
    print("=" * 56)
    fail = 0
    for status, msg in results:
        print("  [%s] %s" % (status, msg))
        if status == "FAIL":
            fail += 1
    total = len(results)
    print("-" * 56)
    print("  合计: %d 项, PASS %d, FAIL %d" % (total, total - fail, fail))
    print("  结论: %s" % ("全部通过" if fail == 0 else "存在 FAIL，修正后复检"))
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
