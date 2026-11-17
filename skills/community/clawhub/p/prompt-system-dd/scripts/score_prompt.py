#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提示词产出质量评分脚本(R01 自动可检验指标)

对组装产出的提示词做静态可检验指标评分,把七维质量表中"能算的部分"
从人工核对转为机械判定。阈值唯一真相源:references/quality-metrics.md,
本文件 METRICS 常量必须与之逐格一致(门禁 QL001-QL008 校验)。

用法:
  python scripts/score_prompt.py --prompt-file out.md --depth 3,3,3,3,3,3,3,3,3
  python scripts/score_prompt.py --prompt-file out.md --depth-json '{"role-anchor":3,...}'
  cat out.md | python scripts/score_prompt.py --depth 3,3,3,3,3,3,3,3,3

输出:stdout JSON,退出码 0=全部通过 / 1=存在 fail / 2=参数或解析错误
注意:阈值当前为草案未标定,fail 仅提示,不代替人做返工判断。
"""
import argparse
import json
import re
import sys
from pathlib import Path

# 与 references/quality-metrics.md 阈值表逐格对应,修改需同步两侧
METRICS = {
    "QL001": {"dim": "清晰度与明确性", "kind": "max",
              "thresholds": {1: 3, 2: 2, 3: 0, 4: 0}},
    "QL002": {"dim": "结构化组织", "kind": "min",
              "thresholds": {2: 5, 3: 5, 4: 5}},
    "QL003": {"dim": "上下文与示例", "kind": "min_ratio",
              "thresholds": {3: 1.0, 4: 1.0}},
    "QL004": {"dim": "约束与成功标准", "kind": "min",
              "thresholds": {1: 3, 2: 5, 3: 8, 4: 12}},
    "QL005": {"dim": "约束对称性", "kind": "max_ratio",
              "thresholds": {2: 4.0, 3: 3.0, 4: 3.0}},
    "QL006": {"dim": "深度推理引导", "kind": "min",
              "thresholds": {3: 3, 4: 3}},
    "QL007": {"dim": "自校正机制", "kind": "min",
              "thresholds": {2: 3, 3: 5, 4: 5}},
    "QL008": {"dim": "迭代机制", "kind": "min",
              "thresholds": {2: 2, 3: 3, 4: 3}},
}

VAGUE_WORDS = [
    "大概", "大约", "差不多", "可能", "也许", "或许", "一些", "某些",
    "若干", "相关的", "适当的", "合适的", "尽快", "尽量", "等等",
    "诸如此类", "视情况", "酌情", "根据需要", "一定程度上",
]

SECTION_PATTERNS = {
    "角色": r"(专业身份|角色|你是|你已被|作为.{0,10}专家)",
    "任务": r"(任务|核心目标|你要完成|本次目标)",
    "上下文": r"(上下文|背景|已知信息|已知事实|参考资料)",
    "格式": r"(输出格式|输出契约|输出[:：]|格式要求|结构框架)",
    "思考": r"(思考步骤|思维链|思考指令|三阶段|分析层|推理)",
}

SOURCE_MARKERS = [r"来源[:：]", r"[（(]来源", r"据\s*\S{2,10}", r"\[\d+\]",
                  r"引自", r"数据来源[:：]"]

POSITIVE_CUES = ["必须", "应该", "需要", "要求", "确保", "包含"]
NEGATIVE_CUES = ["禁止", "不得", "不要", "避免", "不可", "不允许", "排除"]

STAGE_PATTERNS = [r"分析层", r"构建层", r"压力层",
                  r"第[一二三1-3]阶段", r"步骤\s*[一二三1-3]"]

GENERIC_TRIGGERS = {"内容", "结构", "风格", "规模", "长度", "语气", "格式"}


def read_prompt(path):
    if path:
        p = Path(path)
        if not p.exists():
            return None
        return p.read_text(encoding="utf-8")
    return sys.stdin.read()


def parse_depth(depth_str, depth_json, keys):
    """返回 {atom_key: level};失败返回 None"""
    if depth_json:
        try:
            obj = json.loads(depth_json)
        except json.JSONDecodeError:
            return None
        if not isinstance(obj, dict):
            return None
        out = {}
        for k, v in obj.items():
            try:
                out[k] = int(v)
            except (TypeError, ValueError):
                return None
        return out or None
    if not depth_str:
        return None
    nums = re.findall(r"\d+", depth_str)
    if len(nums) != len(keys):
        return None
    return dict(zip(keys, [int(n) for n in nums]))


def base_level(depths):
    """全局基调:取众数,平票取最高"""
    if not depths:
        return 3
    vals = list(depths.values())
    if not vals:
        return 3
    counts = {}
    for v in vals:
        counts[v] = counts.get(v, 0) + 1
    top = max(counts.values())
    return max(v for v, c in counts.items() if c == top)


def count_vague(text):
    return sum(len(re.findall(re.escape(w), text)) for w in VAGUE_WORDS)


def count_sections(text):
    return sum(1 for pat in SECTION_PATTERNS.values()
               if re.search(pat, text))


DATA_HINT = (r"(\d+(\.\d+)?\s*%)"          # 百分比
             r"|(\d{3,})"                   # 四位数以上统计量
             r"|(同比|环比|占比|增长率|渗透率|万元|亿元)")


def source_ratio(text):
    """(有来源标记的数据行数, 数据行总数)

    仅把具备统计语义的行计为数据项。纯年份(如"2026年...报告"标题)
    不计入 —— 标定 case:任务行含 2026 但无统计语义,曾误判为未标注来源。
    """
    data_lines = []
    for ln in text.splitlines():
        if len(ln.strip()) <= 4:
            continue
        # 先剥离年份再判定,避免"2026年...报告"这类标题被计入数据项
        no_year = re.sub(r"(19|20)\d{2}\s*年?", "", ln)
        if re.search(DATA_HINT, no_year):
            data_lines.append(ln)
    if not data_lines:
        return None
    marked = [ln for ln in data_lines
              if any(re.search(m, ln) for m in SOURCE_MARKERS)]
    return len(marked), len(data_lines)


def _constraint_block(text):
    """提取约束段:含约束类标题或首句的行,到下一个同级标题为止"""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.search(r"^#{1,4}\s*.*(约束|边界|必须|禁止)", ln) or \
           re.search(r"^(约束|边界条件)[:：]", ln.strip()):
            start = i
            break
    if start is None:
        return []
    block = []
    for ln in lines[start + 1:]:
        if re.match(r"^#{1,4}\s", ln) and not re.search(r"(约束|边界)", ln):
            break
        block.append(ln)
    return block


def count_constraints(text):
    block = _constraint_block(text)
    if not block:
        return 0
    return len([ln for ln in block
                if re.match(r"^\s*([-*+•]|\d+[.、)])\s*\S", ln)])


def symmetry_ratio(text):
    block = _constraint_block(text)
    if not block:
        return None
    pos = neg = 0
    for ln in block:
        if not re.match(r"^\s*([-*+•]|\d+[.、)])\s*\S", ln):
            continue
        if any(c in ln for c in NEGATIVE_CUES):
            neg += 1
        elif any(c in ln for c in POSITIVE_CUES):
            pos += 1
    if neg == 0:
        return None
    return pos, neg


def count_stages(text):
    hits = set()
    for pat in STAGE_PATTERNS:
        for m in re.finditer(pat, text):
            hits.add(m.group(0))
    # 三阶段按"分析/构建/压力"三个语义族分别计数
    fam = 0
    for group in (r"分析层|第一阶段|阶段\s*1|理解需求|分析",
                  r"构建层|第二阶段|阶段\s*2|逐步执行|构建",
                  r"压力层|第三阶段|阶段\s*3|自查|压力"):
        if re.search(group, text):
            fam += 1
    return max(len(hits), fam)


def count_selfcheck(text):
    boxes = len(re.findall(r"^\s*[-*+]\s*\[[ xX]\]", text, re.MULTILINE))
    if boxes:
        return boxes
    m = re.search(r"(自检|自我检查|检查清单|验收)[:：]?\s*\n((?:\s*[-*+]\s*\S.*\n?)+)",
                  text)
    if m:
        return len(re.findall(r"^\s*[-*+]\s*\S", m.group(2), re.MULTILINE))
    return 0


def count_contextual_triggers(text):
    """提取"调整/补充/修改/简化 XX"结构中的 XX,统计非通用词数量"""
    cands = set()
    for m in re.finditer(r"(?:调整|补充|修改|简化|扩展|强化)\s*[「\[]?\s*"
                         r"([\u4e00-\u9fa5A-Za-z0-9]{1,8})", text):
        w = m.group(1).strip()
        if w and w not in GENERIC_TRIGGERS:
            cands.add(w)
    return len(cands)


def evaluate(text, level):
    """逐维判定,返回 findings 列表"""
    results = []

    def add(code, value, note=""):
        spec = METRICS[code]
        th = spec["thresholds"].get(level)
        if th is None:
            results.append({"code": code, "dim": spec["dim"], "value": value,
                            "threshold": None, "result": "skip", "note": note})
            return
        if value is None:
            # 无法计算(如无数据行/无约束段)统一降级 skip,不参与计分(T21)
            results.append({"code": code, "dim": spec["dim"], "value": None,
                            "threshold": th, "result": "skip", "note": note})
            return
        kind = spec["kind"]
        if kind == "max":
            ok = value <= th
        elif kind == "min":
            ok = value >= th
        elif kind == "min_ratio":
            ok = value >= th
        elif kind == "max_ratio":
            ok = value <= th
        else:
            ok = True
        results.append({"code": code, "dim": spec["dim"], "value": value,
                        "threshold": th, "result": "pass" if ok else "fail",
                        "note": note})

    add("QL001", count_vague(text))
    add("QL002", count_sections(text))

    sr = source_ratio(text)
    if sr is None:
        add("QL003", None, "未识别到数据行,降级不参与计分")
    else:
        add("QL003", round(sr[0] / sr[1], 3), "标记 %d / 数据行 %d" % sr)

    add("QL004", count_constraints(text))

    sym = symmetry_ratio(text)
    if sym is None:
        add("QL005", None, "无负面条目或约束段,不参与计分")
    else:
        add("QL005", round(sym[0] / sym[1], 2), "正 %d : 负 %d" % sym)

    add("QL006", count_stages(text))
    add("QL007", count_selfcheck(text))
    add("QL008", count_contextual_triggers(text))
    return results


def main():
    ap = argparse.ArgumentParser(description="提示词产出质量评分(R01)")
    ap.add_argument("--prompt-file", help="产出提示词文件路径,省略则读 stdin")
    ap.add_argument("--depth", help="DEPTH 指纹,如 3,3,3,3,3,3,3,3,3")
    ap.add_argument("--depth-json", help='指纹的 JSON 形式 {"role-anchor":3,...}')
    ap.add_argument("--atoms", help="核心原子位序逗号分隔,缺省读 validate_skill.CORE_ATOM_KEYS(单一真相源,P0-1)")
    args = ap.parse_args()

    if args.atoms:
        keys = args.atoms.split(",")
    else:
        import validate_skill  # 同目录,位序唯一真相源;FP003 家族已守护该常量
        keys = validate_skill.CORE_ATOM_KEYS

    text = read_prompt(args.prompt_file)
    if text is None or not text.strip():
        print(json.dumps({"error": "提示词为空或文件不存在"},
                         ensure_ascii=False, indent=2))
        sys.exit(2)

    depths = parse_depth(args.depth, args.depth_json, keys)
    if depths is None:
        print(json.dumps({"error": "DEPTH 指纹解析失败,位数需与原子数一致(%d)"
                          % len(keys)}, ensure_ascii=False, indent=2))
        sys.exit(2)

    level = base_level(depths)
    results = evaluate(text, level)
    scored = [r for r in results if r["result"] != "skip"]
    passed = [r for r in scored if r["result"] == "pass"]

    out = {
        "version": "R01-draft",
        "base_level": "D%d" % level,
        "depths": depths,
        "thresholds_calibrated": False,
        "metrics": results,
        "summary": {
            "total": len(scored),
            "passed": len(passed),
            "failed": len(scored) - len(passed),
            "skipped": len(results) - len(scored),
            "pass_rate": round(len(passed) / len(scored), 3) if scored else None,
        },
        "manual_checklist": [
            "专业性:术语符合行业标准,无外行表述",
            "场景适配性:针对具体场景定制,域原子已真正落地",
            "语气一致性:风格定义在全文贯彻,无前后断裂",
        ],
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["summary"]["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
