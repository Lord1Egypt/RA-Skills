#!/usr/bin/env python3
"""Validate and render an AI-authored storyboard; never adapts source text."""
import argparse
import json
import math
import sys
from decimal import Decimal
from pathlib import Path

STATUSES = {"complete", "needs_review", "needs_more_source"}


def reject_nonfinite(value: str):
    raise ValueError(f"invalid_json: 不允许 NaN 或 Infinity（{value}）")


def parse_finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        reject_nonfinite(value)
    return parsed


def require_text(value, field: str):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"invalid_storyboard: {field} 必须是非空字符串")


def require_text_list(value, field: str, allow_empty=True):
    if not isinstance(value, list) or (not allow_empty and not value) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"invalid_storyboard: {field} 必须是非空字符串数组" if not allow_empty else f"invalid_storyboard: {field} 必须是字符串数组")


def require_positive_number(value, field: str):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0 or (isinstance(value, float) and not math.isfinite(value)):
        raise ValueError(f"invalid_storyboard: {field} 必须是正的有限数值")


def validate_storyboard(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("invalid_storyboard: 顶层必须是 JSON 对象")
    status = data.get("status")
    if status not in STATUSES:
        raise ValueError("invalid_storyboard: status 必须是 complete、needs_review 或 needs_more_source")
    if status == "needs_more_source":
        require_text(data.get("message"), "message")
        return data

    for key in ("title", "source_type"):
        require_text(data.get(key), key)
    require_positive_number(data.get("duration_seconds"), "duration_seconds")
    require_text_list(data.get("gaps"), "gaps")
    characters = data.get("characters")
    scenes = data.get("scenes")
    if not isinstance(characters, list) or not isinstance(scenes, list) or not scenes:
        raise ValueError("invalid_storyboard: characters 和 scenes 必须是数组，且 scenes 不能为空")
    for index, person in enumerate(characters, 1):
        field = f"characters[{index - 1}]"
        if not isinstance(person, dict):
            raise ValueError(f"invalid_storyboard: {field} 必须是对象")
        for key in ("name", "role", "goal", "conflict", "relationship", "source_anchor"):
            require_text(person.get(key), f"{field}.{key}")
        require_text_list(person.get("facts"), f"{field}.facts", allow_empty=False)

    total_duration = Decimal(0)
    scene_ids = set()
    shot_ids = set()
    for scene_index, scene in enumerate(scenes):
        field = f"scenes[{scene_index}]"
        if not isinstance(scene, dict):
            raise ValueError(f"invalid_storyboard: {field} 必须是对象")
        for key in ("scene_id", "location", "time", "purpose", "source_anchor"):
            require_text(scene.get(key), f"{field}.{key}")
        if scene["scene_id"] in scene_ids:
            raise ValueError(f"invalid_storyboard: 重复 scene_id：{scene['scene_id']}")
        scene_ids.add(scene["scene_id"])
        require_text_list(scene.get("characters"), f"{field}.characters")
        require_text_list(scene.get("actions"), f"{field}.actions", allow_empty=False)
        require_text_list(scene.get("gaps", []), f"{field}.gaps")
        dialogue = scene.get("dialogue")
        shots = scene.get("shots")
        if not isinstance(dialogue, list) or not isinstance(shots, list) or not shots:
            raise ValueError(f"invalid_storyboard: {field}.dialogue 和 shots 必须是数组，且 shots 不能为空")
        for dialogue_index, line in enumerate(dialogue):
            line_field = f"{field}.dialogue[{dialogue_index}]"
            if not isinstance(line, dict):
                raise ValueError(f"invalid_storyboard: {line_field} 必须是对象")
            require_text(line.get("speaker"), f"{line_field}.speaker")
            require_text(line.get("line"), f"{line_field}.line")
        for shot_index, shot in enumerate(shots):
            shot_field = f"{field}.shots[{shot_index}]"
            if not isinstance(shot, dict):
                raise ValueError(f"invalid_storyboard: {shot_field} 必须是对象")
            for key in ("shot_id", "framing", "camera", "visual", "action", "sound", "source_anchor"):
                require_text(shot.get(key), f"{shot_field}.{key}")
            if shot["shot_id"] in shot_ids:
                raise ValueError(f"invalid_storyboard: 重复 shot_id：{shot['shot_id']}")
            shot_ids.add(shot["shot_id"])
            for key in ("dialogue_or_voiceover", "creative_note"):
                if key not in shot or not isinstance(shot[key], str):
                    raise ValueError(f"invalid_storyboard: {shot_field}.{key} 必须是字符串")
            require_positive_number(shot.get("duration_seconds"), f"{shot_field}.duration_seconds")
            total_duration += Decimal(str(shot["duration_seconds"]))
    if abs(Decimal(str(data["duration_seconds"])) - total_duration) > Decimal("0.01"):
        raise ValueError("invalid_storyboard: duration_seconds 必须等于所有镜头时长之和")
    if status == "complete" and (data["gaps"] or any(scene.get("gaps") for scene in scenes)):
        raise ValueError("invalid_storyboard: 存在未解决 gaps 时不能标记 complete")
    return data


def render_markdown(data: dict) -> str:
    if data["status"] == "needs_more_source":
        return f"# 小说剧本转分镜\n\n状态：needs_more_source\n\n{data['message']}\n"
    lines = [f"# {data['title']}", "", f"状态：{data['status']}", f"总时长：{data['duration_seconds']} 秒", "", "## 人物卡", ""]
    if not data["characters"]:
        lines.append("- （原文未能确认人物信息）")
    for person in data["characters"]:
        lines += [f"- **{person['name']}**：{person['role']}", f"  - 目标：{person['goal']}", f"  - 阻力：{person['conflict']}", f"  - 关系：{person['relationship']}", f"  - 原文事实：{'；'.join(person['facts'])}"]
    def md_text(value):
        return str(value).replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>\n  ")

    for scene in data["scenes"]:
        lines += ["", f"## 场景 {scene['scene_id']}", "", f"- 地点/时间：{scene['location']} / {scene['time']}", f"- 场景目的：{scene['purpose']}", f"- 动作：{'；'.join(scene['actions'])}", "", "### 对白", ""]
        lines += [f"- {line['speaker']}：{line['line']}" for line in scene["dialogue"]] or ["- （原文未识别对白）"]
        lines += ["", "### 分镜", ""]
        for shot in scene["shots"]:
            lines += [
                f"#### 镜头 {md_text(shot['shot_id'])}",
                "",
                f"- 时长：{md_text(shot['duration_seconds'])} 秒",
                f"- 景别：{md_text(shot['framing'])}",
                f"- 运镜：{md_text(shot['camera'])}",
                f"- 画面：{md_text(shot['visual'])}",
                f"- 动作：{md_text(shot['action'])}",
                f"- 对白/旁白：{md_text(shot['dialogue_or_voiceover']) or '无'}",
                f"- 声音：{md_text(shot['sound'])}",
                f"- 原文锚点：{md_text(shot['source_anchor'])}",
                f"- 创作补充：{md_text(shot['creative_note']) or '无'}",
                "",
            ]
        if scene.get("gaps"):
            lines += ["", "待确认："] + [f"- {gap}" for gap in scene["gaps"]]
    if data["gaps"]:
        lines += ["", "## 待确认", ""] + [f"- {gap}" for gap in data["gaps"]]
    lines += ["", "> 结构校验不证明原文引用、事实对应或创作质量；这些由当前 AI 对照原文负责。"]
    return "\n".join(lines) + "\n"


def write_outputs(data: dict, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    payloads = {
        out / "storyboard.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        out / "storyboard.md": render_markdown(data),
    }
    created = []
    try:
        for path, contents in payloads.items():
            with path.open("x", encoding="utf-8") as stream:
                created.append(path)
                stream.write(contents)
    except FileExistsError as exc:
        for path in created:
            path.unlink(missing_ok=True)
        raise ValueError("output_exists: 输出目录已有 storyboard.json 或 storyboard.md；请换新目录") from exc
    except OSError:
        for path in created:
            path.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description="校验并排版 AI 已完成的分镜 JSON；本脚本不分析或改编原文。")
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
        data = validate_storyboard(json.loads(Path(args.input).read_text(encoding="utf-8"), parse_constant=reject_nonfinite, parse_float=parse_finite_float))
        write_outputs(data, Path(args.output))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(f"已校验并排版 AI 分镜：storyboard.md 和 storyboard.json → {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
