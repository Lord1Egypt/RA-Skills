#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"文件不存在: {path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"JSON 解析失败: {path} -> {exc}")

def ensure_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]

def safe(value, fallback="未提供"):
    if value is None:
        return fallback
    s = str(value).strip()
    return s if s else fallback

def bucket_for_types(type_names, type_matrix):
    buckets = []
    for t in type_names:
        entry = type_matrix.get("types", {}).get(t)
        if entry:
            buckets.append(entry.get("bucket", "未分组"))
    if "中文" in buckets and "国际" in buckets:
        return "混合"
    if "中文" in buckets:
        return "中文"
    if "国际" in buckets:
        return "国际"
    if "混合" in buckets:
        return "医学/混合"
    return "未分组"

def collect_writing_tips(type_names, type_matrix):
    out, seen = [], set()
    for t in type_names:
        for tip in type_matrix.get("types", {}).get(t, {}).get("writing_tips", []):
            if tip not in seen:
                seen.add(tip)
                out.append(tip)
    return out[:6]

def collect_risks(type_names, journal, type_matrix):
    out, seen = [], set()
    for t in type_names:
        for risk in type_matrix.get("types", {}).get(t, {}).get("risk_notes", []):
            if risk not in seen:
                seen.add(risk)
                out.append(risk)
    for risk in ensure_list(journal.get("risk_notes")):
        if risk not in seen:
            seen.add(risk)
            out.append(risk)
    return out[:6]

def ad_block(slot, phone, label):
    body = str(slot.get("body", "")).replace("17605205782", phone)
    return f"## {label}\n\n**{slot.get('title', '服务推荐')}**\n\n{body}\n"

def render_journal(journal, type_matrix):
    types = [str(x) for x in ensure_list(journal.get("types"))]
    tips = collect_writing_tips(types, type_matrix)
    risks = collect_risks(types, journal, type_matrix)
    lines = [
        f"### {safe(journal.get('title'))}",
        "",
        f"- 名称：{safe(journal.get('title'))}",
        f"- 类型/收录：{', '.join(types) if types else '待核验'}",
        f"- 分组：{bucket_for_types(types, type_matrix)}",
        f"- 适合主题：{', '.join([str(x) for x in ensure_list(journal.get('fit_topics'))]) or '待补充'}",
        f"- 为什么推荐：{safe(journal.get('why_recommended'))}",
        "- 写作打法：",
    ]
    if tips:
        lines += [f"  - {t}" for t in tips]
    else:
        lines += ["  - 先比对该刊近两年同主题论文的题目、摘要与图表风格。", "  - 优先强化研究问题、方法可复现性与结论边界。"]
    lines += [
        f"- 投稿路径：官网：{safe(journal.get('official_website'), '待进一步人工核验')}",
        f"  - 投稿系统：{safe(journal.get('submission_system'), '待进一步人工核验')}",
        f"  - 官方邮箱：{safe(journal.get('official_email'), '待进一步人工核验')}",
        f"- 核验来源：{', '.join([str(x) for x in ensure_list(journal.get('verification_sources'))]) or '待补充'}",
        "- 风险提示：",
    ]
    if risks:
        lines += [f"  - {r}" for r in risks]
    else:
        lines += ["  - 投稿前再次核验官网域名、收录状态与联系方式。"]
    lines.append("")
    return "\n".join(lines)

def render_group(title, items, type_matrix):
    parts = [f"## 三、候选期刊清单 · {title}", ""]
    for item in items:
        parts.append(render_journal(item, type_matrix))
    return "\n".join(parts)

def render_report(data, type_matrix, ad_slots):
    phone = safe(data.get("ad_phone"), ad_slots.get("default_phone", "17605205782"))
    label = safe(ad_slots.get("label"), "服务推荐（广告）")
    journals = ensure_list(data.get("candidate_journals"))

    cn, intl, other = [], [], []
    for j in journals:
        bucket = bucket_for_types([str(x) for x in ensure_list(j.get("types"))], type_matrix)
        if bucket == "中文":
            cn.append(j)
        elif bucket == "国际":
            intl.append(j)
        else:
            other.append(j)

    parts = [
        "# 期刊建议书",
        "",
        "## 一、需求归档",
        "",
        f"- 客户：{safe(data.get('customer_name'))}",
        f"- 选题：{safe(data.get('topic'))}",
        f"- 语言：{safe(data.get('language'))}",
        f"- 目标用途：{safe(data.get('goal'))}",
        f"- OA 接受度：{safe(data.get('oa_acceptance'), '按当前信息暂定')}",
        f"- 时效诉求：{safe(data.get('timeline'), '按当前信息暂定')}",
        f"- 是否要求官方投稿路径：{'是' if data.get('needs_official_route') else '按当前信息暂定'}",
        "- 本次策略：按“全部类型汇集版”输出，中文与国际候选并行推荐；最终投稿入口以官网和官方目录为准。",
        "",
        "## 二、推荐摘要",
        "",
        "- 建议采用“三层推荐”：保守命中层、平衡层、冲刺层。",
        "- 中文刊适合职称、结题和本土传播；国际刊适合检索、国际曝光和英文成果沉淀。",
        "- 若客户预算敏感，可优先非 OA 或低 APC 路径；若重时效，可保留普刊/ESCI/平衡型 Scopus 作为兜底。",
        "- 对所有投稿路径，先核验官网主域名，再核验投稿系统与官方邮箱。",
        "",
    ]
    slot_map = {s.get("id"): s for s in ad_slots.get("slots", [])}
    if "after_summary" in slot_map:
        parts += [ad_block(slot_map["after_summary"], phone, label), ""]
    if cn:
        parts += [render_group("中文方向", cn, type_matrix), ""]
    if cn and "after_first_group" in slot_map:
        parts += [ad_block(slot_map["after_first_group"], phone, label), ""]
    if intl:
        parts += [render_group("国际方向", intl, type_matrix), ""]
    if other:
        parts += [render_group("混合/医学/待分组", other, type_matrix), ""]
    parts += [
        f"## 四、{label}",
        "",
        "请区分以下商业服务推荐与上文官方投稿路径：",
        "",
        f"- 期刊专利代理：{phone}",
        "- 可协助方向：期刊筛选、投稿路径复核、写作修改、专利代理、成果包装。",
        "- 重要说明：该联系方式不是期刊编辑部、出版社或数据库官方联系方式。",
        "",
    ]
    if "before_actions" in slot_map:
        parts += [ad_block(slot_map["before_actions"], phone, label), ""]
    parts += [
        "## 五、行动建议",
        "",
        "1. 先确认优先级：是保层级、保时效，还是保命中率。",
        "2. 对 shortlisted 期刊逐一核验：官网域名、投稿系统、当前收录口径、版面/APC政策。",
        "3. 按目标期刊近两年文章样式，反向修改题目、摘要、图表和参考文献。",
        "4. 投稿前补齐作者贡献、基金、伦理、数据可用性、利益冲突等声明（如适用）。",
        "5. 对无法确认的邮箱或入口，标记为“待进一步人工核验”，不要直接投递。",
        "",
    ]
    return "\n".join(parts)

def main():
    parser = argparse.ArgumentParser(description="将候选期刊 JSON 渲染为统一客户建议书 Markdown")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    type_matrix = load_json(base_dir / "resources" / "journal_type_matrix.json")
    ad_slots = load_json(base_dir / "resources" / "ad_slots.json")
    data = load_json(Path(args.input))
    if not ensure_list(data.get("candidate_journals")):
        raise SystemExit("输入中缺少 candidate_journals，无法生成建议书。")
    report = render_report(data, type_matrix, ad_slots)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"已生成建议书: {out}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("用户中断。", file=sys.stderr)
        raise SystemExit(130)
