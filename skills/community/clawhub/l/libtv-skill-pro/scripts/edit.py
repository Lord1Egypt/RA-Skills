#!/usr/bin/env python3
"""LibTV 节点修饰器（风格 / 标记 / 聚焦 / 运镜 / 角色库）"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import create_session, build_project_url, record_project, safe_run


MODIFIERS = {
    "style": {
        "scope": "图片/视频",
        "label": "风格",
        "template": (
            "请在当前内容上应用指定风格（对应 LibTV 节点的「风格」修饰器）。\n"
            "目标素材：{target}\n"
            "风格描述：{topic}\n"
            "要求：保持主体内容不变，仅替换视觉风格。"
        ),
    },
    "mark": {
        "scope": "图片/视频",
        "label": "标记",
        "template": (
            "请对当前内容中的指定区域做标记/局部约束（对应 LibTV 节点的「标记」修饰器）。\n"
            "目标素材：{target}\n"
            "标记区域与意图：{topic}"
        ),
    },
    "focus": {
        "scope": "图片",
        "label": "聚焦",
        "template": (
            "请对当前图片做聚焦/局部强调（对应 LibTV 图片节点的「聚焦」修饰器）。\n"
            "目标素材：{target}\n"
            "聚焦区域：{topic}\n"
            "要求：保持画面其余部分不变，仅调整聚焦区域。"
        ),
    },
    "camera": {
        "scope": "视频",
        "label": "运镜",
        "template": (
            "请对视频生成应用指定运镜方式（对应 LibTV 视频节点的「运镜」修饰器）。\n"
            "目标素材：{target}\n"
            "运镜描述：{topic}\n"
            "示例：环绕、推、拉、跟、移、希区柯克变焦、第一人称视角等。"
        ),
    },
    "character_lib": {
        "scope": "视频",
        "label": "角色库",
        "template": (
            "请使用角色库中的角色生成视频（对应 LibTV 视频节点的「角色库」修饰器）。\n"
            "角色名/参考：{topic}\n"
            "场景描述：{target}\n"
            "要求：保持角色外观一致性。"
        ),
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="LibTV 节点修饰器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "环境变量:\n  LIBTV_ACCESS_KEY  必填\n\n"
            "可用修饰器：\n  "
            + "\n  ".join(f"{k:<18}[{v['scope']}] {v['label']}" for k, v in MODIFIERS.items())
            + "\n\n示例:\n"
            "  # 给上一会话的视频应用风格\n"
            "  python3 edit.py style \"宫崎骏吉卜力\" --target https://example.com/v.mp4 --session-id SID\n"
            "  # 在当前生成里强制运镜\n"
            "  python3 edit.py camera \"无人机环绕镜头\" --target \"待生成的场景\" --session-id SID\n"
        ),
    )
    parser.add_argument("modifier", choices=list(MODIFIERS.keys()), help="修饰器名称")
    parser.add_argument("topic", help="修饰器的具体描述（风格名、运镜名、聚焦区域等）")
    parser.add_argument("--target", default="", help="目标素材（URL 或描述）。不传时使用「当前内容/上一条结果」")
    parser.add_argument("--session-id", default="", help="已有会话 ID（推荐传入，以便对同一会话内容做修饰）")
    parser.add_argument("--dry-run", action="store_true", help="只打印将发送的 prompt，不调真实 API（不消耗积分）")

    args = parser.parse_args()
    spec = MODIFIERS[args.modifier]

    target = args.target or "（当前会话的上一条生成结果）"
    message = spec["template"].format(topic=args.topic, target=target)

    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "modifier": args.modifier,
            "label": spec["label"],
            "scope": spec["scope"],
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
        record_project(project_uuid, set_current=True, desc=f"修饰器:{spec['label']}")

    out = {
        "modifier": args.modifier,
        "label": spec["label"],
        "scope": spec["scope"],
        "projectUuid": project_uuid,
        "sessionId": session_id,
        "projectUrl": build_project_url(project_uuid),
        "message_sent": message,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    safe_run(main)
