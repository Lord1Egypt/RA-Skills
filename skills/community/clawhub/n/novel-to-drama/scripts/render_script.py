#!/usr/bin/env python3
"""Validate and render a screenplay already written by the current AI agent."""
import argparse
import json
import sys
from pathlib import Path


def _text(value, path):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{path} 必须是非空文本")


def _text_list(value, path):
    if not isinstance(value, list):
        raise ValueError(f"{path} 必须是数组")
    for index, item in enumerate(value):
        _text(item, f"{path}[{index}]")


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("剧本必须是 JSON 对象")
    if data.get("status") == "scaffold":
        raise ValueError("占位示例不能作为完整剧本输出，请先完成改编")
    _text(data.get("title"), "title")
    if isinstance(data.get("episode"), bool) or not isinstance(data.get("episode"), int) or data["episode"] < 1:
        raise ValueError("episode 必须是大于 0 的整数")
    _text_list(data.get("gaps"), "gaps")
    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("scenes 必须包含至少一个场次")
    seen = set()
    for index, scene in enumerate(scenes):
        path = f"scenes[{index}]"
        if not isinstance(scene, dict):
            raise ValueError(f"{path} 必须是对象")
        for field in ("scene_id", "slugline", "goal", "turn", "ending_hook"):
            _text(scene.get(field), f"{path}.{field}")
        if scene["scene_id"] in seen:
            raise ValueError(f"{path}.scene_id 重复")
        seen.add(scene["scene_id"])
        for field in ("characters", "actions", "props"):
            _text_list(scene.get(field), f"{path}.{field}")
        if not isinstance(scene.get("dialogue"), list):
            raise ValueError(f"{path}.dialogue 必须是数组")
        for line_index, line in enumerate(scene["dialogue"]):
            if not isinstance(line, dict):
                raise ValueError(f"{path}.dialogue[{line_index}] 必须是对象")
            for field in ("speaker", "line"):
                _text(line.get(field), f"{path}.dialogue[{line_index}].{field}")
        if not scene["actions"] and not scene["dialogue"]:
            raise ValueError(f"{path} 至少需要动作或对白")
        if "beats" in scene:
            if not isinstance(scene["beats"], list) or not scene["beats"]:
                raise ValueError(f"{path}.beats 必须是非空数组")
            beat_actions, beat_dialogue = [], []
            for beat_index, beat in enumerate(scene["beats"]):
                beat_path = f"{path}.beats[{beat_index}]"
                if not isinstance(beat, dict) or beat.get("type") not in ("action", "dialogue"):
                    raise ValueError(f"{beat_path}.type 必须是 action 或 dialogue")
                if beat["type"] == "action":
                    _text(beat.get("text"), f"{beat_path}.text")
                    beat_actions.append(beat["text"])
                else:
                    _text(beat.get("speaker"), f"{beat_path}.speaker")
                    _text(beat.get("line"), f"{beat_path}.line")
                    beat_dialogue.append({"speaker": beat["speaker"], "line": beat["line"]})
            dialogue_pairs = [{"speaker": line["speaker"], "line": line["line"]} for line in scene["dialogue"]]
            if beat_actions != scene["actions"] or beat_dialogue != dialogue_pairs:
                raise ValueError(f"{path}.beats 必须与 actions 和 dialogue 的内容及顺序一致")
        conflict = scene.get("conflict")
        if not isinstance(conflict, dict):
            raise ValueError(f"{path}.conflict 必须是对象")
        for field in ("obstacle", "escalation", "result"):
            _text(conflict.get(field), f"{path}.conflict.{field}")
        if "camera_notes" in scene:
            _text_list(scene["camera_notes"], f"{path}.camera_notes")
    return data


def markdown(data):
    lines = [f"# {data['title']}", "", f"第 {data['episode']} 集"]
    for scene in data["scenes"]:
        lines += ["", f"## {scene['scene_id']} · {scene['slugline']}", "", f"场次目标：{scene['goal']}"]
        if scene["characters"]:
            lines += ["", "人物：" + "、".join(scene["characters"])]
        if scene.get("camera_notes"):
            lines += ["", "### 拍摄建议"] + [f"- {item}" for item in scene["camera_notes"]]
        if "beats" in scene:
            lines += ["", "### 场景"]
            for beat in scene["beats"]:
                lines.append(f"- {beat['text']}" if beat["type"] == "action" else f"**{beat['speaker']}**：{beat['line']}")
        else:
            if scene["actions"]:
                lines += ["", "### 动作"] + [f"- {item}" for item in scene["actions"]]
            if scene["dialogue"]:
                lines += ["", "### 对白"] + [f"**{line['speaker']}**：{line['line']}" for line in scene["dialogue"]]
        conflict = scene["conflict"]
        lines += ["", "### 冲突与转折", f"- 阻力：{conflict['obstacle']}", f"- 升级：{conflict['escalation']}", f"- 结果：{conflict['result']}", f"- 转折：{scene['turn']}"]
        if scene["props"]:
            lines += ["", "道具：" + "、".join(scene["props"])]
        lines += ["", f"结尾钩子：{scene['ending_hook']}"]
    if data["gaps"]:
        lines += ["", "## 待用户确认"] + [f"- {gap}" for gap in data["gaps"]]
    return "\n".join(lines) + "\n"


def render(data, output):
    validate(data)
    output = Path(output)
    targets = [output / "drama-script.json", output / "drama-script.md"]
    if any(target.exists() for target in targets):
        raise ValueError("输出文件已存在，请选择新目录")
    output.mkdir(parents=True, exist_ok=True)
    written = []
    try:
        for target, content in zip(targets, (json.dumps(data, ensure_ascii=False, indent=2) + "\n", markdown(data))):
            with target.open("x", encoding="utf-8") as handle:
                written.append(target)
                handle.write(content)
    except (OSError, ValueError):
        for target in written:
            target.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser(description="检查并输出已由 AI 或用户写好的剧本；本程序不生成剧情。")
    parser.add_argument("--input", required=True, help="已完成的剧本 JSON")
    parser.add_argument("--output", required=True, help="输出目录，不能覆盖已有剧本")
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        render(data, args.output)
    except (OSError, ValueError) as error:
        print(f"剧本未输出：{error}", file=sys.stderr)
        return 1
    print("已输出 drama-script.md 和 drama-script.json；请核对原文和创作质量。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
