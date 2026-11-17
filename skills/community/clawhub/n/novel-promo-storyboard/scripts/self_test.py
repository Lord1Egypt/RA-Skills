#!/usr/bin/env python3
"""Validate and render an AI-authored novel promotion package."""
import argparse
import json
import math
import sys
from decimal import Decimal
from pathlib import Path

STATUSES = {"complete", "needs_review", "needs_more_source"}
ORIGINS = {"source", "creative", "cta_requested", "cta_suggested"}
CTA_STATUSES = {"none", "user_requested", "agent_suggestion"}


def reject_nonfinite(value: str):
    raise ValueError(f"invalid_json: 不允许 NaN 或 Infinity（{value}）")


def parse_finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        reject_nonfinite(value)
    return parsed


def text(value, field: str, allow_empty=False):
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        qualifier = "字符串" if allow_empty else "非空字符串"
        raise ValueError(f"invalid_package: {field} 必须是{qualifier}")


def string_array(value, field: str, allow_empty=True):
    if not isinstance(value, list) or (not allow_empty and not value) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"invalid_package: {field} 必须是字符串数组")


def number(value, field: str, minimum=None, nullable=False):
    if nullable and value is None:
        return
    if not isinstance(value, (int, float)) or isinstance(value, bool) or (isinstance(value, float) and not math.isfinite(value)):
        raise ValueError(f"invalid_package: {field} 必须是有限数值" + ("或 null" if nullable else ""))
    if minimum is not None and value < minimum:
        raise ValueError(f"invalid_package: {field} 不能小于 {minimum}")


def require_attribution(anchor: str, note: str, field: str):
    if not anchor and not note:
        raise ValueError(f"invalid_package: {field} 缺少原文锚点与创作补充说明")


def timeline(items, field, id_key, text_keys):
    if not isinstance(items, list):
        raise ValueError(f"invalid_package: {field} 必须是数组")
    seen = set()
    previous_end = Decimal(0)
    for index, item in enumerate(items):
        item_field = f"{field}[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"invalid_package: {item_field} 必须是对象")
        text(item.get(id_key), f"{item_field}.{id_key}")
        if item[id_key] in seen:
            raise ValueError(f"invalid_package: 重复 {id_key}：{item[id_key]}")
        seen.add(item[id_key])
        for key in ("start", "end"):
            number(item.get(key), f"{item_field}.{key}", minimum=0)
        if item["end"] <= item["start"]:
            raise ValueError(f"invalid_package: {item_field}.end 必须大于 start")
        if Decimal(str(item["start"])) < previous_end:
            raise ValueError(f"invalid_package: {field} 时间段不能重叠或倒序")
        previous_end = Decimal(str(item["end"]))
        for key in text_keys:
            text(item.get(key), f"{item_field}.{key}", allow_empty=key in {"source_anchor", "creative_note"})
    return seen


def validate_package(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("invalid_package: 顶层必须是 JSON 对象")
    status = data.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        raise ValueError("invalid_package: status 必须是 complete、needs_review 或 needs_more_source")
    if status == "needs_more_source":
        text(data.get("message"), "message")
        return data

    intent = data.get("user_intent")
    if not isinstance(intent, dict):
        raise ValueError("invalid_package: user_intent 必须是对象")
    for key in ("platform", "audience", "objective", "cta_preference"):
        value = intent.get(key)
        if value is not None:
            text(value, f"user_intent.{key}")
    number(intent.get("target_duration_seconds"), "user_intent.target_duration_seconds", minimum=0.01, nullable=True)
    string_array(intent.get("not_provided"), "user_intent.not_provided")
    number(data.get("duration_seconds"), "duration_seconds", minimum=0.01)

    options = data.get("title_options")
    if not isinstance(options, list) or len(options) != 3:
        raise ValueError("invalid_package: title_options 必须包含三个候选标题")
    title_ids = set()
    for index, option in enumerate(options):
        field = f"title_options[{index}]"
        if not isinstance(option, dict):
            raise ValueError(f"invalid_package: {field} 必须是对象")
        text(option.get("text"), f"{field}.text")
        if len(option["text"]) > 30:
            raise ValueError(f"invalid_package: {field}.text 不能超过 30 个字符")
        if option["text"] in title_ids:
            raise ValueError("invalid_package: 三个候选标题不能重复")
        title_ids.add(option["text"])
        text(option.get("angle"), f"{field}.angle")
        text(option.get("source_anchor"), f"{field}.source_anchor", allow_empty=True)
        text(option.get("creative_note"), f"{field}.creative_note", allow_empty=True)
        require_attribution(option["source_anchor"], option["creative_note"], field)
    text(data.get("selected_hook"), "selected_hook")
    text(data.get("hook_source_anchor"), "hook_source_anchor", allow_empty=True)
    text(data.get("hook_creative_note"), "hook_creative_note", allow_empty=True)
    if not data["hook_source_anchor"] and not data["hook_creative_note"]:
        raise ValueError("invalid_package: 钩子没有原文锚点时必须说明创作补充")

    characters = data.get("characters")
    scenes = data.get("scenes")
    if not isinstance(characters, list) or not isinstance(scenes, list) or not scenes:
        raise ValueError("invalid_package: characters 和 scenes 必须是数组，且 scenes 不能为空")
    for index, character in enumerate(characters):
        field = f"characters[{index}]"
        if not isinstance(character, dict):
            raise ValueError(f"invalid_package: {field} 必须是对象")
        for key in ("name", "role", "goal", "conflict", "relationship", "visual_traits"):
            text(character.get(key), f"{field}.{key}")
        string_array(character.get("facts"), f"{field}.facts")
        text(character.get("source_anchor"), f"{field}.source_anchor", allow_empty=True)
        text(character.get("creative_note"), f"{field}.creative_note", allow_empty=True)
        require_attribution(character["source_anchor"], character["creative_note"], field)

    scene_ids = set()
    for index, scene in enumerate(scenes):
        field = f"scenes[{index}]"
        if not isinstance(scene, dict):
            raise ValueError(f"invalid_package: {field} 必须是对象")
        for key in ("scene_id", "location", "time", "goal", "conflict", "visual_focus", "conflict_turn"):
            text(scene.get(key), f"{field}.{key}")
        if scene["scene_id"] in scene_ids:
            raise ValueError(f"invalid_package: 重复 scene_id：{scene['scene_id']}")
        scene_ids.add(scene["scene_id"])
        string_array(scene.get("actions"), f"{field}.actions", allow_empty=False)
        text(scene.get("source_anchor"), f"{field}.source_anchor", allow_empty=True)
        text(scene.get("creative_note"), f"{field}.creative_note", allow_empty=True)
        require_attribution(scene["source_anchor"], scene["creative_note"], field)
        dialogue = scene.get("dialogue")
        if not isinstance(dialogue, list):
            raise ValueError(f"invalid_package: {field}.dialogue 必须是数组")
        for dindex, line in enumerate(dialogue):
            dfield = f"{field}.dialogue[{dindex}]"
            if not isinstance(line, dict):
                raise ValueError(f"invalid_package: {dfield} 必须是对象")
            for key in ("speaker", "line"):
                text(line.get(key), f"{dfield}.{key}")
            text(line.get("source_anchor"), f"{dfield}.source_anchor", allow_empty=True)
            text(line.get("creative_note"), f"{dfield}.creative_note", allow_empty=True)
            require_attribution(line["source_anchor"], line["creative_note"], dfield)

    voiceover_ids = timeline(data.get("voiceover"), "voiceover", "segment_id", ("text", "source_anchor", "creative_note"))
    for index, segment in enumerate(data["voiceover"]):
        origin = segment.get("origin")
        if not isinstance(origin, str) or origin not in ORIGINS:
            raise ValueError(f"invalid_package: voiceover[{index}].origin 必须标明 source、creative 或 CTA 来源")
        if not segment["source_anchor"] and not segment["creative_note"]:
            raise ValueError(f"invalid_package: voiceover[{index}] 无原文锚点时必须说明创作补充")
        if origin == "source" and not segment["source_anchor"]:
            raise ValueError(f"invalid_package: voiceover[{index}] source 来源必须提供原文锚点")
        if origin == "creative" and not segment["creative_note"]:
            raise ValueError(f"invalid_package: voiceover[{index}] creative 来源必须说明创作补充")
    shots = data.get("shots")
    if not isinstance(shots, list) or not shots:
        raise ValueError("invalid_package: 推广分镜至少需要一个镜头")
    timeline(shots, "shots", "shot_id", ("visual", "caption", "sound", "source_anchor", "creative_note"))
    voiceover_by_id = {item["segment_id"]: item for item in data["voiceover"]}
    for index, shot in enumerate(shots):
        field = f"shots[{index}]"
        number(shot.get("duration_seconds"), f"{field}.duration_seconds", minimum=0.01)
        if abs(Decimal(str(shot["end"])) - Decimal(str(shot["start"])) - Decimal(str(shot["duration_seconds"]))) > Decimal("0.01"):
            raise ValueError(f"invalid_package: {field} duration_seconds 必须等于 end-start")
        ref = shot.get("voiceover_ref")
        if ref is not None and (not isinstance(ref, str) or ref not in voiceover_ids):
            raise ValueError(f"invalid_package: {field}.voiceover_ref 必须引用现有口播 segment_id 或为 null")
        if ref is not None:
            segment = voiceover_by_id[ref]
            if shot["start"] >= segment["end"] or shot["end"] <= segment["start"]:
                raise ValueError(f"invalid_package: {field} 时间段与对应口播 {ref} 不重叠")
        if not shot["source_anchor"] and not shot["creative_note"]:
            raise ValueError(f"invalid_package: {field} 无原文锚点时必须说明创作补充")
    ending = data.get("ending_action")
    if not isinstance(ending, dict) or not isinstance(ending.get("status"), str) or ending["status"] not in CTA_STATUSES:
        raise ValueError("invalid_package: ending_action.status 必须是 none、user_requested 或 agent_suggestion")
    text(ending.get("text"), "ending_action.text", allow_empty=True)
    text(ending.get("note"), "ending_action.note", allow_empty=True)
    if ending["status"] == "none" and ending["text"]:
        raise ValueError("invalid_package: ending_action 为 none 时 text 必须为空")
    if ending["status"] != "none" and not ending["text"]:
        raise ValueError("invalid_package: CTA 有来源时必须提供 text")
    cta_segments = [item for item in data["voiceover"] if item["origin"] in {"cta_requested", "cta_suggested"}]
    if ending["status"] == "none" and cta_segments:
        raise ValueError("invalid_package: ending_action 为 none 时不应包含 CTA 口播段")
    if ending["status"] != "none":
        expected_origin = "cta_requested" if ending["status"] == "user_requested" else "cta_suggested"
        if ending["status"] == "user_requested" and intent.get("cta_preference") is None:
            raise ValueError("invalid_package: 用户要求 CTA 时需在 user_intent.cta_preference 记录要求")
        if ending["status"] == "agent_suggestion" and not ending["note"].strip():
            raise ValueError("invalid_package: AI 建议 CTA 必须说明其为建议")
        if not any(item["origin"] == expected_origin and item["text"] == ending["text"] for item in data["voiceover"]):
            raise ValueError("invalid_package: CTA 文案须在对应来源类型的口播时间线中出现")

    source_notes = data.get("source_notes")
    if not isinstance(source_notes, dict):
        raise ValueError("invalid_package: source_notes 必须是对象")
    for key in ("source_scope", "source_version"):
        value = source_notes.get(key)
        if value is not None:
            text(value, f"source_notes.{key}")
    text(source_notes.get("source_scope"), "source_notes.source_scope")
    string_array(source_notes.get("gaps"), "source_notes.gaps")
    timeline_end = max([0] + [item["end"] for item in data["voiceover"]] + [item["end"] for item in shots])
    if abs(Decimal(str(data["duration_seconds"])) - Decimal(str(timeline_end))) > Decimal("0.01"):
        raise ValueError("invalid_package: duration_seconds 必须等于口播/镜头时间线的最晚结束时间")
    if status == "complete" and source_notes["gaps"]:
        raise ValueError("invalid_package: 存在待确认 gaps 时不能标记 complete")
    return data


def md(value):
    return str(value).replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>\n  ")


def render_markdown(data: dict) -> str:
    if data["status"] == "needs_more_source":
        return f"# 小说推文方案\n\n状态：needs_more_source\n\n{md(data['message'])}\n"
    intent = data["user_intent"]
    lines = [f"# 小说推文方案：{data['status']}", "", f"总时长：{data['duration_seconds']} 秒", "", "## 用户意图", ""]
    for label, key in (("平台", "platform"), ("受众", "audience"), ("目标", "objective"), ("目标时长（秒）", "target_duration_seconds"), ("CTA 偏好", "cta_preference")):
        value = intent.get(key)
        lines.append(f"- {label}：{md(value) if value is not None else '未提供'}")
    if intent["not_provided"]:
        lines += ["- 用户未提供：" + "；".join(md(x) for x in intent["not_provided"])]
    lines += ["", "## 标题候选", ""]
    for option in data["title_options"]:
        lines += [f"### {md(option['text'])}", "", f"角度：{md(option['angle'])}", f"原文锚点：{md(option['source_anchor']) or '无'}", f"创作补充：{md(option['creative_note']) or '无'}", ""]
    lines += ["## 开头钩子", "", md(data["selected_hook"]), "", f"原文锚点：{md(data['hook_source_anchor']) or '无'}", f"创作补充：{md(data['hook_creative_note']) or '无'}", "", "## 人物卡", ""]
    for person in data["characters"]:
        lines += [f"### {md(person['name'])}", "", f"- 身份/作用：{md(person['role'])}", f"- 目标：{md(person['goal'])}", f"- 阻力：{md(person['conflict'])}", f"- 关系：{md(person['relationship'])}", f"- 视觉特征：{md(person['visual_traits'])}", f"- 原文事实：{'；'.join(md(x) for x in person['facts']) or '无'}", f"- 原文锚点：{md(person['source_anchor']) or '无'}", f"- 创作补充：{md(person['creative_note']) or '无'}", ""]
    lines += ["## 场景卡", ""]
    for scene in data["scenes"]:
        lines += [f"### {md(scene['scene_id'])}：{md(scene['location'])} / {md(scene['time'])}", "", f"- 目标：{md(scene['goal'])}", f"- 冲突：{md(scene['conflict'])}", f"- 动作：{'；'.join(md(x) for x in scene['actions'])}", f"- 视觉焦点：{md(scene['visual_focus'])}", f"- 局面变化：{md(scene['conflict_turn'])}", f"- 原文锚点：{md(scene['source_anchor']) or '无'}", f"- 创作补充：{md(scene['creative_note']) or '无'}", ""]
        if scene["dialogue"]:
            lines += ["对白："]
            for item in scene["dialogue"]:
                lines += [f"- {md(item['speaker'])}：{md(item['line'])}", f"  - 原文锚点：{md(item['source_anchor']) or '无'}", f"  - 创作补充：{md(item['creative_note']) or '无'}"]
            lines.append("")
    lines += ["## 口播时间线", ""]
    for segment in data["voiceover"]:
        lines += [f"### {md(segment['segment_id'])}｜{segment['start']}–{segment['end']} 秒", "", md(segment["text"]), f"- 来源类型：{md(segment['origin'])}", f"- 原文锚点：{md(segment['source_anchor']) or '无'}", f"- 创作补充：{md(segment['creative_note']) or '无'}", ""]
    lines += ["## 画面与声音时间线", ""]
    for shot in data["shots"]:
        lines += [f"### 镜头 {md(shot['shot_id'])}｜{shot['start']}–{shot['end']} 秒", "", f"- 画面：{md(shot['visual'])}", f"- 字幕：{md(shot['caption'])}", f"- 对应口播：{md(shot['voiceover_ref']) if shot['voiceover_ref'] else '无'}", f"- 声音：{md(shot['sound'])}", f"- 原文锚点：{md(shot['source_anchor']) or '无'}", f"- 创作补充：{md(shot['creative_note']) or '无'}", ""]
    ending = data["ending_action"]
    label = {"none": "未添加", "user_requested": "用户要求", "agent_suggestion": "AI 建议（非用户要求）"}[ending["status"]]
    lines += ["## 结尾行动引导", "", f"- 状态：{label}", f"- 文案：{md(ending['text']) or '无'}", f"- 说明：{md(ending['note']) or '无'}"]
    gaps = data["source_notes"]["gaps"]
    lines += ["", "## 待确认", ""] + ([f"- {md(gap)}" for gap in gaps] or ["- 无"])
    lines += ["", "> 结构校验不证明原文引用真实性、改编完整性或发布效果；这些由当前 AI 对照原文和用户意图负责。"]
    return "\n".join(lines) + "\n"


def write_outputs(data: dict, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    payloads = {out / "promo-package.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n", out / "promo-package.md": render_markdown(data)}
    created = []
    try:
        for path, contents in payloads.items():
            with path.open("x", encoding="utf-8") as stream:
                created.append(path)
                stream.write(contents)
    except FileExistsError as exc:
        for path in created:
            path.unlink(missing_ok=True)
        raise ValueError("output_exists: 输出目录已有 promo-package.json 或 promo-package.md；请换新目录") from exc
    except OSError:
        for path in created:
            path.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description="校验并排版 AI 已完成的小说推广方案；本脚本不分析或改编原文。")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("self-test")
    render = sub.add_parser("render")
    render.add_argument("--input", required=True)
    render.add_argument("--output", required=True)
    args = parser.parse_args()
    if args.command == "self-test":
        import unittest
        suite = unittest.defaultTestLoader.discover(str(Path(__file__).parents[1] / "tests"))
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        return 0 if result.wasSuccessful() else 1
    try:
        source = Path(args.input)
        data = json.loads(source.read_text(encoding="utf-8"), parse_constant=reject_nonfinite, parse_float=parse_finite_float)
        write_outputs(validate_package(data), Path(args.output))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(f"已校验并排版 AI 推广方案：promo-package.md 和 promo-package.json → {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
