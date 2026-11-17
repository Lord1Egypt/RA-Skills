#!/usr/bin/env python3
"""
自动化营销版面审核入口：
  1. 长图分段
  2. 百度 OCR 识别文字和原图坐标
  3. 规则引擎生成候选 risks.json
  4. 本地兜底或宿主 Agent JSON 复核
  5. 生成长图批注版和 Markdown 报告
"""

import argparse
import copy
import json
import os
import sys
import tempfile
from pathlib import Path


def reexec_with_skill_venv():
    local_python = Path(__file__).resolve().parent.parent / ".venv" / "bin" / "python"
    if os.environ.get("MARKETING_REVIEW_VENV_REEXEC") == "1" or not local_python.exists():
        return
    if Path(sys.executable) == local_python:
        return
    env = os.environ.copy()
    env["MARKETING_REVIEW_VENV_REEXEC"] = "1"
    env.pop("__PYVENV_LAUNCHER__", None)
    os.execve(str(local_python), [str(local_python), str(Path(__file__).resolve()), *sys.argv[1:]], env)


reexec_with_skill_venv()

from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from annotate_image import annotate_image  # noqa: E402
from agent_review import KNOWN_PROVIDERS, run_agent_review  # noqa: E402
from agents.base import normalize_agent_output  # noqa: E402
from build_agent_payload import build_payload  # noqa: E402
from ocr_localize import ocr_with_baiduocr  # noqa: E402


DEFAULT_RULES_PATH = SCRIPT_DIR.parent / "references" / "risk-rules.json"
DEFAULT_AGENT_PROMPT_TEMPLATE = SCRIPT_DIR.parent / "template" / "agent-review-prompt.md"
REVIEW_MODES = ("strict", "balanced", "presentation")
LEVEL_WEIGHT = {"high": 3, "medium": 2, "low": 1}


def split_image(image_path, output_dir, slice_height, slice_overlap=120):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    slices = []
    step = max(slice_height - slice_overlap, 1)
    top = 0
    index = 1
    while top < height:
        bottom = min(top + slice_height, height)
        crop = image.crop((0, top, width, bottom))
        slice_path = output_dir / f"slice_{index:02d}_{top}_{bottom}.jpg"
        crop.save(slice_path, quality=92)
        slices.append((slice_path, top, bottom))
        if bottom >= height:
            break
        top += step
        index += 1
    return image.size, slices


def bbox_iou(a, b):
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    inter_w = max(0, min(ax2, bx2) - max(ax1, bx1))
    inter_h = max(0, min(ay2, by2) - max(ay1, by1))
    inter = inter_w * inter_h
    if inter == 0:
        return 0.0
    area_a = max(0, ax2 - ax1) * max(0, ay2 - ay1)
    area_b = max(0, bx2 - bx1) * max(0, by2 - by1)
    return inter / max(area_a + area_b - inter, 1)


def dedupe_ocr_regions(regions):
    kept = []
    for region in sorted(regions, key=lambda item: item.get("confidence", 0), reverse=True):
        text = region.get("text", "").strip()
        bbox = region.get("bbox")
        if not text or not bbox:
            continue
        duplicate = False
        for existing in kept:
            if existing.get("text", "").strip() == text and bbox_iou(existing["bbox"], bbox) >= 0.55:
                duplicate = True
                break
        if not duplicate:
            kept.append(region)
    return sorted(kept, key=lambda item: (item["bbox"][1], item["bbox"][0]))


def run_ocr(image_path, slice_height, slice_overlap=120):
    image = Image.open(image_path)
    width, height = image.size
    if height <= slice_height:
        regions, source = ocr_with_baiduocr(str(image_path))
        for region in regions:
            region["bbox"] = [region["x1"], region["y1"], region["x2"], region["y2"]]
            region["slice"] = None
        return (width, height), regions, source

    all_regions = []
    source = None
    with tempfile.TemporaryDirectory(prefix="layout_review_ocr_") as tmp:
        _, slices = split_image(image_path, Path(tmp), slice_height, slice_overlap)
        for slice_path, y_offset, _ in slices:
            regions, source = ocr_with_baiduocr(str(slice_path))
            for region in regions:
                region["y1"] += y_offset
                region["y2"] += y_offset
                region["bbox"] = [region["x1"], region["y1"], region["x2"], region["y2"]]
                if region.get("vertices"):
                    for point in region["vertices"]:
                        point["y"] += y_offset
                region["slice"] = slice_path.name
                all_regions.append(region)
    return (width, height), dedupe_ocr_regions(all_regions), source


def normalize_ocr_region(region):
    bbox = region.get("bbox")
    if not bbox and all(key in region for key in ("x1", "y1", "x2", "y2")):
        bbox = [region["x1"], region["y1"], region["x2"], region["y2"]]
    if not bbox:
        return None
    region["bbox"] = [int(v) for v in bbox]
    region.setdefault("x1", region["bbox"][0])
    region.setdefault("y1", region["bbox"][1])
    region.setdefault("x2", region["bbox"][2])
    region.setdefault("y2", region["bbox"][3])
    return region


def load_ocr_json(ocr_json_path):
    data = json.loads(Path(ocr_json_path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("regions") or data.get("words_result") or []
    regions = []
    for item in data:
        region = normalize_ocr_region(dict(item))
        if region:
            regions.append(region)
    return regions


def load_rules(rules_path, review_mode):
    data = json.loads(Path(rules_path).read_text(encoding="utf-8"))
    rules = data.get("rules", data if isinstance(data, list) else [])
    selected = []
    for rule in rules:
        profiles = rule.get("profiles") or ["strict", "balanced", "presentation"]
        if review_mode in profiles:
            selected.append(rule)
    return data, selected


def sort_risks_for_output(risks):
    risks.sort(key=lambda risk: min(bbox_min_y(box) for box in risk.get("bboxes", [risk.get("bbox", [0, 0, 0, 0])])))
    for index, risk in enumerate(risks, 1):
        risk["id"] = index
    return risks


def select_key_risks(risks, max_key_risks=14):
    candidates = [
        risk for risk in risks
        if risk.get("key") or risk.get("level") == "high"
    ]
    if not candidates:
        candidates = list(risks)
    candidates.sort(key=lambda risk: (
        -LEVEL_WEIGHT.get(risk.get("level"), 0),
        -int(risk.get("priority", 0)),
        min(bbox_min_y(box) for box in risk.get("bboxes", [risk.get("bbox", [0, 0, 0, 0])])),
    ))

    selected = []
    covered_rules = set()
    for risk in sorted(candidates, key=lambda item: (
        -int(item.get("priority", 0)),
        min(bbox_min_y(box) for box in item.get("bboxes", [item.get("bbox", [0, 0, 0, 0])])),
    )):
        rule_id = risk.get("rule_id")
        if rule_id and rule_id not in covered_rules:
            selected.append(risk)
            covered_rules.add(rule_id)
            if len(selected) >= max_key_risks:
                break

    selected_ids = {id(risk) for risk in selected}
    for risk in candidates:
        if id(risk) in selected_ids:
            continue
        selected.append(risk)
        if len(selected) >= max_key_risks:
            break

    return sort_risks_for_output(copy.deepcopy(selected))


def text_matches(text, keyword):
    return keyword.lower() in text.lower()


def should_skip_match(rule, region):
    text = region.get("text", "").strip()
    if rule["id"] == "human_study_effect" and text.startswith(("(", "（")):
        return True
    return False


def annotation_bbox(region):
    vertices = region.get("vertices")
    if vertices:
        return [[int(p["x"]), int(p["y"])] for p in vertices]
    return [int(v) for v in region["bbox"]]


def bbox_min_y(box):
    if len(box) == 4 and all(isinstance(v, (int, float)) for v in box):
        return box[1]
    return min(point[1] for point in box)


def group_hits(hits, max_vertical_gap=260):
    if not hits:
        return []
    hits = sorted(hits, key=lambda item: (item["bbox"][1], item["bbox"][0]))
    clusters = [[hits[0]]]
    for hit in hits[1:]:
        previous = clusters[-1][-1]
        if hit["bbox"][1] - previous["bbox"][3] <= max_vertical_gap:
            clusters[-1].append(hit)
        else:
            clusters.append([hit])
    return clusters


def build_risks(ocr_regions, rules, max_regions_per_risk=4):
    risks = []
    risk_id = 1
    used_regions = set()

    for rule in rules:
        hits = []
        for region_index, region in enumerate(ocr_regions):
            if region_index in used_regions:
                continue
            text = region.get("text", "")
            if should_skip_match(rule, region):
                continue
            if any(text_matches(text, keyword) for keyword in rule["any"]):
                hits.append((region_index, region))

        if not hits:
            continue

        indexed_hits = sorted(hits, key=lambda item: (item[1]["bbox"][1], item[1]["bbox"][0]))
        for cluster in group_hits([item[1] | {"_region_index": item[0]} for item in indexed_hits]):
            selected = cluster[:max_regions_per_risk]
            sample_words = []
            for hit in selected:
                text = hit.get("text", "")
                if text and text not in sample_words:
                    sample_words.append(text)

            risks.append({
                "id": risk_id,
                "word": " / ".join(sample_words[:3]) or rule["title"],
                "title": rule["title"],
                "bboxes": [annotation_bbox(hit) for hit in selected],
                "level": rule["level"],
                "basis": rule["basis"],
                "reason": rule["reason"],
                "suggestion": rule["suggestion"],
                "matched_texts": [hit.get("text", "") for hit in selected],
                "rule_id": rule.get("id"),
                "priority": rule.get("priority", 0),
                "key": bool(rule.get("key")),
            })
            used_regions.update(hit["_region_index"] for hit in selected)
            risk_id += 1

    return sort_risks_for_output(risks)


def write_report(
    report_path,
    image_path,
    image_size,
    ocr_regions,
    risks,
    annotated_path,
    risks_path,
    review_mode,
    key_annotated_path=None,
    key_risks_path=None,
    rule_risks_path=None,
    agent_payload_path=None,
    agent_risks_path=None,
    agent_runtime=None,
):
    high = sum(1 for risk in risks if risk["level"] == "high")
    medium = sum(1 for risk in risks if risk["level"] == "medium")
    low = sum(1 for risk in risks if risk["level"] == "low")
    level_label = {"high": "🔴 高风险", "medium": "🟡 中风险", "low": "🟢 低风险"}

    lines = [
        "# 版面自动审核报告",
        "",
        "## 审核对象",
        f"- 图片：`{image_path}`",
        f"- 尺寸：{image_size[0]} x {image_size[1]}",
        f"- 审核模式：`{review_mode}`",
        f"- Agent复核：`{agent_runtime or 'disabled'}`",
        f"- OCR文字区域：{len(ocr_regions)}",
        f"- 批注图：`{annotated_path}`",
        f"- 风险JSON：`{risks_path}`",
    ]
    if rule_risks_path:
        lines.append(f"- 规则候选JSON：`{rule_risks_path}`")
    if key_annotated_path and key_risks_path:
        lines.extend([
            f"- 重点批注图：`{key_annotated_path}`",
            f"- 重点风险JSON：`{key_risks_path}`",
        ])
    if agent_payload_path and agent_risks_path:
        lines.extend([
            f"- Agent输入：`{agent_payload_path}`",
            f"- Agent输出：`{agent_risks_path}`",
        ])
    lines.extend([
        "",
        "## 风险等级分布",
        "",
        "| 等级 | 数量 |",
        "|---|---:|",
        f"| 🔴 高风险 | {high} |",
        f"| 🟡 中风险 | {medium} |",
        f"| 🟢 低风险 | {low} |",
        "",
        "## 风险详情",
        "",
    ])

    for risk in risks:
        lines.extend([
            f"### {risk['id']}. {level_label.get(risk['level'], risk['level'])}：{risk.get('title') or risk.get('word')}",
            f"- 原文：{'；'.join(risk.get('matched_texts') or [risk.get('word', '')])}",
            f"- 依据：{risk.get('basis', '')}",
            f"- 判定：{risk.get('reason', '')}",
            f"- 建议：{risk.get('suggestion', '')}",
            "",
        ])

    if not risks:
        lines.extend(["未自动识别到明确风险点。建议人工复核 OCR 原文和行业专项规则。", ""])

    lines.extend([
        "## 说明",
        "",
        "本报告由规则引擎初筛并经 Agent 复核协议整理，用于初筛和标注。涉及上线结论时，仍建议法务按产品属性、检测报告、授权材料和最新版法规复核。",
        "",
    ])
    report_path.write_text("\n".join(lines), encoding="utf-8")


def write_agent_prompt(prompt_path, payload_path, agent_risks_path, review_mode, max_key_risks):
    template = DEFAULT_AGENT_PROMPT_TEMPLATE.read_text(encoding="utf-8")
    lines = [
        template.rstrip(),
        "",
        "## 本次审核任务",
        "",
        f"- 读取 Agent 输入：`{payload_path}`",
        f"- 写出 Agent 输出：`{agent_risks_path}`",
        f"- 审核模式：`{review_mode}`",
        f"- 重点版最多风险数：`{max_key_risks}`",
        "",
        "## 强制要求",
        "",
        "1. 不要只整理 `rule_risks`。必须全文扫描 `ocr_text` 和 `ocr`，新增规则漏检风险。",
        "2. 对每个新增风险，优先从 `ocr` 中找到对应文字区域并写入 `bboxes`。",
        "3. 如果无法确定精确坐标，允许写 `bbox_missing: true`，但必须说明需要人工定位。",
        "4. `presentation` 模式也不能只保留 1-2 条，除非已逐项检查所有强制维度并在 `notes` 中解释为什么其他维度不构成风险。",
        "5. 输出必须是 JSON 对象，可直接被 `scripts/run_review.py --agent-risks-json` 读取。",
        "",
        "## 建议执行顺序",
        "",
        "1. 读取 payload JSON。",
        "2. 先处理 `rule_risks`：keep / adjust / merge / exclude。",
        "3. 再按 `agent_task.mandatory_review_dimensions` 全文扫描 `ocr_text`，对漏检项执行 add。",
        "4. 写出 `agent_risks.json` 后，复跑渲染命令。",
        "",
        "复跑命令示例：",
        "",
        "```bash",
        "python3 scripts/run_review.py <原图路径> --output-dir <输出目录> --ocr-json <ocr.json> --agent-risks-json <agent_risks.json>",
        "```",
        "",
    ]
    prompt_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="自动审核营销素材并生成批注图")
    parser.add_argument("image_path", help="输入图片路径")
    parser.add_argument("--output-dir", default=None, help="输出目录，默认与图片同目录")
    parser.add_argument("--slice-height", type=int, default=3200, help="长图 OCR 切片高度")
    parser.add_argument("--slice-overlap", type=int, default=120, help="长图 OCR 切片重叠高度，降低边缘漏识别")
    parser.add_argument("--max-regions-per-risk", type=int, default=4, help="每类风险最多标注几个文字区域")
    parser.add_argument("--ocr-json", default=None, help="复用已有 OCR JSON，跳过百度 OCR，用于调试或节省额度")
    parser.add_argument("--rules", default=str(DEFAULT_RULES_PATH), help="风险规则 JSON 路径")
    parser.add_argument("--review-mode", choices=REVIEW_MODES, default="balanced",
                        help="审核模式：strict=全量初筛，balanced=日常审核，presentation=交付重点")
    parser.add_argument("--max-key-risks", type=int, default=14, help="重点版最多保留的风险点数量")
    parser.add_argument("--no-key-output", action="store_true", help="不额外生成重点版批注图")
    parser.add_argument("--agent-mode", choices=KNOWN_PROVIDERS, default=None,
                        help="本地兜底模式，仅 manual；OpenClaw/MiniMax 等宿主 Agent 结果请用 --agent-risks-json。")
    parser.add_argument("--agent-provider", choices=KNOWN_PROVIDERS, default=None,
                        help=argparse.SUPPRESS)
    parser.add_argument("--agent-risks-json", default=None,
                        help="使用宿主 Agent 已生成的 agent_risks.json，跳过本地兜底复核")
    parser.add_argument("--no-agent", action="store_true", help="跳过 Agent 复核协议，直接使用规则风险")
    parser.add_argument("--prepare-agent-review", action="store_true",
                        help="只生成 OCR、规则候选、agent_payload 和 agent_prompt，交给宿主 Agent 扩展审核")
    args = parser.parse_args()
    agent_mode = args.agent_mode or args.agent_provider or "manual"

    image_path = Path(args.image_path)
    if not image_path.exists():
        print(f"错误: 图片不存在 {image_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else image_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = image_path.stem
    if args.slice_overlap >= args.slice_height:
        print("错误: --slice-overlap 必须小于 --slice-height", file=sys.stderr)
        sys.exit(1)
    rules_path = Path(args.rules)
    if not rules_path.exists():
        print(f"错误: 规则文件不存在 {rules_path}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.ocr_json:
            image_size = Image.open(image_path).size
            ocr_regions = load_ocr_json(args.ocr_json)
            ocr_source = f"cached:{args.ocr_json}"
        else:
            image_size, ocr_regions, ocr_source = run_ocr(image_path, args.slice_height, args.slice_overlap)
    except Exception as exc:
        print(f"错误: OCR 失败：{exc}", file=sys.stderr)
        print("请确认 BAIDU_API_KEY/BAIDU_SECRET_KEY 已配置，且网络可访问 aip.baidubce.com。", file=sys.stderr)
        print("如已生成过 OCR，可使用 --ocr-json 复用已有结果继续生成风险和批注图。", file=sys.stderr)
        sys.exit(2)
    rules_data, rules = load_rules(rules_path, args.review_mode)
    rule_risks = build_risks(ocr_regions, rules, args.max_regions_per_risk)
    risks = rule_risks
    agent_payload = None
    agent_result = None
    agent_payload_path = output_dir / f"{stem}_agent_payload.json"
    agent_risks_path = output_dir / f"{stem}_agent_risks.json"
    agent_prompt_path = output_dir / f"{stem}_agent_prompt.md"
    agent_payload = build_payload(
        image_path,
        ocr_regions,
        rule_risks,
        rules_data,
        args.review_mode,
        SCRIPT_DIR.parent / "references",
    )
    agent_payload_path.write_text(json.dumps(agent_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_agent_prompt(agent_prompt_path, agent_payload_path, agent_risks_path, args.review_mode, args.max_key_risks)

    if args.prepare_agent_review:
        ocr_path = output_dir / f"{stem}_ocr.json"
        rule_risks_path = output_dir / f"{stem}_rule_risks.json"
        ocr_path.write_text(json.dumps(ocr_regions, ensure_ascii=False, indent=2), encoding="utf-8")
        rule_risks_path.write_text(json.dumps(rule_risks, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"OCR: {ocr_source}, {len(ocr_regions)} regions -> {ocr_path}")
        print(f"Rules: {len(rules)} active ({args.review_mode}) from {rules_path}")
        print(f"Rule risks: {len(rule_risks)} -> {rule_risks_path}")
        print(f"Agent payload: {agent_payload_path}")
        print(f"Agent prompt: {agent_prompt_path}")
        print(f"Expected agent risks: {agent_risks_path}")
        print("Prepared only: 宿主 Agent 必须读取 agent_prompt.md 并写出 agent_risks.json 后再复跑渲染。")
        return

    if not args.no_agent:
        try:
            if args.agent_risks_json:
                agent_result = normalize_agent_output(
                    json.loads(Path(args.agent_risks_json).read_text(encoding="utf-8"))
                )
            else:
                agent_result = run_agent_review(agent_payload, agent_mode)
            risks = agent_result.get("risks", [])
        except Exception as exc:
            print(f"错误: Agent 复核失败：{exc}", file=sys.stderr)
            print("如需只用规则结果，请加 --no-agent；如使用宿主 Agent，请先写出 agent_risks.json 再传 --agent-risks-json。", file=sys.stderr)
            sys.exit(3)
    if args.review_mode == "presentation":
        risks = select_key_risks(risks, args.max_key_risks)
    key_risks = select_key_risks(risks, args.max_key_risks)

    ocr_path = output_dir / f"{stem}_ocr.json"
    risks_path = output_dir / f"{stem}_risks.json"
    annotated_path = output_dir / f"{stem}_annotated.png"
    report_path = output_dir / f"{stem}_review.md"
    key_risks_path = output_dir / f"{stem}_risks_key.json"
    key_annotated_path = output_dir / f"{stem}_annotated_key.png"

    ocr_path.write_text(json.dumps(ocr_regions, ensure_ascii=False, indent=2), encoding="utf-8")
    rule_risks_path = output_dir / f"{stem}_rule_risks.json"
    rule_risks_path.write_text(json.dumps(rule_risks, ensure_ascii=False, indent=2), encoding="utf-8")
    if agent_result is not None:
        agent_risks_path.write_text(json.dumps(agent_result, ensure_ascii=False, indent=2), encoding="utf-8")
    risks_path.write_text(json.dumps(risks, ensure_ascii=False, indent=2), encoding="utf-8")
    annotate_image(str(image_path), copy.deepcopy(risks), str(annotated_path), bbox_space="original")
    if not args.no_key_output:
        key_risks_path.write_text(json.dumps(key_risks, ensure_ascii=False, indent=2), encoding="utf-8")
        annotate_image(str(image_path), copy.deepcopy(key_risks), str(key_annotated_path), bbox_space="original")
    else:
        key_risks_path = None
        key_annotated_path = None
    write_report(
        report_path,
        image_path,
        image_size,
        ocr_regions,
        risks,
        annotated_path,
        risks_path,
        args.review_mode,
        key_annotated_path,
        key_risks_path,
        rule_risks_path,
        agent_payload_path if agent_payload is not None else None,
        agent_risks_path if agent_result is not None else None,
        (agent_result.get("agent_runtime") or agent_result.get("provider")) if agent_result else None,
    )

    print(f"OCR: {ocr_source}, {len(ocr_regions)} regions -> {ocr_path}")
    print(f"Rules: {len(rules)} active ({args.review_mode}) from {rules_path}")
    print(f"Rule risks: {len(rule_risks)} -> {rule_risks_path}")
    print(f"Agent payload: {agent_payload_path}")
    print(f"Agent prompt: {agent_prompt_path}")
    if agent_result is not None:
        print(f"Agent runtime: {agent_result.get('agent_runtime') or agent_result.get('provider')} -> {agent_risks_path}")
        if agent_result.get("agent_runtime") == "manual-rule-pass-through":
            print("Warning: manual-rule-pass-through 只是规则直通，不是完整宿主 Agent 扩展审核。")
    print(f"Risks: {len(risks)} -> {risks_path}")
    print(f"Annotated: {annotated_path}")
    if key_annotated_path:
        print(f"Key risks: {len(key_risks)} -> {key_risks_path}")
        print(f"Key annotated: {key_annotated_path}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
