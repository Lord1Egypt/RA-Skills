#!/usr/bin/env python3
"""LibTV 预设流程入口（对应 LibTV 画布首页的 4 个预设流程）"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import create_session, build_project_url, record_project, safe_run


PRESETS = {
    "story_script": {
        "label": "故事脚本生成",
        "template": (
            "请生成完整的故事脚本（对应 LibTV 画布的「故事脚本生成」流程）。\n"
            "主题/设定：{topic}\n"
            "要求：包含多场景结构、镜头描述、对白、节奏建议，输出可直接用于后续分镜的脚本。"
        ),
        "needs_ref": False,
    },
    "character_views": {
        "label": "角色三视图",
        "template": (
            "请生成角色三视图（对应 LibTV 画布的「角色三视图」流程）。\n"
            "角色描述：{topic}\n"
            "要求：保持角色一致性，输出正面、3/4 侧面、背面三张图，纯背景，便于作为后续角色资产。"
        ),
        "needs_ref": False,
    },
    "keyframe_to_video": {
        "label": "首帧图生视频",
        "template": (
            "请以参考图作为视频首帧生成视频（对应 LibTV 画布的「首帧图生视频」流程）。\n"
            "首帧参考图：{ref}\n"
            "动作/场景描述：{topic}\n"
            "要求：从该图自然开场，按描述演绎动作。"
        ),
        "needs_ref": True,
        "ref_kind": "image",
    },
    "audio_to_video": {
        "label": "音频生视频",
        "template": (
            "请基于音频生成对应视频画面（对应 LibTV 画布的「音频生视频」流程）。\n"
            "音频文件：{ref}\n"
            "画面风格/概念：{topic}\n"
            "要求：画面节奏与音乐情绪匹配，按描述风格生成。"
        ),
        "needs_ref": True,
        "ref_kind": "audio",
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="LibTV 预设流程入口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "环境变量:\n  LIBTV_ACCESS_KEY  必填\n\n"
            "可用预设：\n  "
            + "\n  ".join(f"{k:<22}{v['label']}" + (f"  [需 --ref {v.get('ref_kind','')}]" if v.get('needs_ref') else "") for k, v in PRESETS.items())
            + "\n\n示例:\n"
            "  python3 flow.py story_script \"机器人来到唐朝\"\n"
            "  python3 flow.py character_views \"穿汉服的赛博朋克少女，银发\"\n"
            "  python3 flow.py keyframe_to_video \"角色拔剑出鞘\" --ref https://example.com/start.png\n"
            "  python3 flow.py audio_to_video \"暗黑风格 MV\" --ref https://example.com/song.mp3"
        ),
    )
    parser.add_argument("preset", choices=list(PRESETS.keys()), help="预设流程名称")
    parser.add_argument("topic", help="主题/描述")
    parser.add_argument("--ref", default="", help="参考图或音频 URL（部分预设需要，配合 upload_file.py 拿到的 OSS 地址）")
    parser.add_argument("--session-id", default="", help="已有会话 ID，不传则新建会话")
    parser.add_argument("--dry-run", action="store_true", help="只打印将发送的 prompt，不调真实 API（不消耗积分）")

    args = parser.parse_args()
    preset = PRESETS[args.preset]
    if preset.get("needs_ref") and not args.ref:
        print(f"错误：{args.preset} 需要 --ref ({preset.get('ref_kind','')}) 参数", file=sys.stderr)
        sys.exit(1)

    message = preset["template"].format(topic=args.topic, ref=args.ref)

    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "preset": args.preset,
            "label": preset["label"],
            "session_id": args.session_id or "(new)",
            "would_send": message,
        }, ensure_ascii=False, indent=2))
        return

    data = create_session(session_id=args.session_id or "", message=message)

    project_uuid = data.get("projectUuid", "")
    session_id = data.get("sessionId", "")
    if not session_id:
        print("错误：未返回 sessionId", file=sys.stderr)
        sys.exit(1)

    if project_uuid:
        record_project(project_uuid, set_current=True, desc=preset["label"])

    out = {
        "preset": args.preset,
        "label": preset["label"],
        "projectUuid": project_uuid,
        "sessionId": session_id,
        "projectUrl": build_project_url(project_uuid),
        "message_sent": message,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    safe_run(main)
