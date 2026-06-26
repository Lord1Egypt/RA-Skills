#!/usr/bin/env python3
"""LibTV 节点能力封装：文本节点 / 图片节点 / 视频节点的细分动作"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import create_session, build_project_url, record_project, safe_run


NODE_ACTIONS = {
    # ---------- 文本节点 ----------
    "text_to_video_prompt": {
        "node": "文本",
        "label": "文生视频提示词",
        "template": (
            "请把以下故事/场景描述转写为高质量的文生视频提示词（对应 LibTV 文本节点 → 文生视频）。\n"
            "原始描述：{topic}\n"
            "要求：补充镜头、运镜、光线、节奏、情绪关键词；输出可直接喂给视频模型的 prompt。"
        ),
        "ref_label": None,
    },
    "image_caption": {
        "node": "文本",
        "label": "图片反推提示词",
        "template": (
            "请反推下面这张图片的生成提示词（对应 LibTV 文本节点 → 图片反推提示词）。\n"
            "图片：{ref}\n"
            "{topic_line}"
            "要求：尽可能精准描述主体、风格、构图、光影、相机参数。"
        ),
        "ref_label": "图片 URL",
        "topic_optional": True,
    },
    "text_to_music": {
        "node": "文本",
        "label": "文字生音乐",
        "template": (
            "请生成与下列描述匹配的音乐（对应 LibTV 文本节点 → 文字生音乐）。\n"
            "音乐描述：{topic}\n"
            "要求：明确风格/情绪/乐器/节奏；如需对应画面，请保持时长合理。"
        ),
        "ref_label": None,
    },

    # ---------- 图片节点 ----------
    "image_to_image": {
        "node": "图片",
        "label": "图生图",
        "template": (
            "请基于参考图执行图生图（对应 LibTV 图片节点 → 图生图）。\n"
            "参考图：{ref}\n"
            "目标描述：{topic}\n"
            "要求：保留参考图主体结构/构图，按目标描述改变内容。"
        ),
        "ref_label": "原图 URL",
    },
    "image_upscale": {
        "node": "图片",
        "label": "图片高清",
        "template": (
            "请对下列图片做高清化（对应 LibTV 图片节点 → 图片高清）。\n"
            "图片：{ref}\n"
            "{topic_line}"
            "要求：保持原图内容不变，提升分辨率与清晰度。"
        ),
        "ref_label": "图片 URL",
        "topic_optional": True,
    },

    # ---------- 视频节点 ----------
    "first_last_frame": {
        "node": "视频",
        "label": "首尾帧生成视频",
        "template": (
            "请以首帧 + 尾帧生成中间过程视频（对应 LibTV 视频节点 → 首尾帧生成视频）。\n"
            "首帧：{ref}\n"
            "尾帧：{ref2}\n"
            "中间过程描述：{topic}"
        ),
        "ref_label": "首帧图 URL",
        "needs_ref2": True,
        "ref2_label": "尾帧图 URL",
    },
    "reference_video": {
        "node": "视频",
        "label": "图片参考 / 全能参考生成视频",
        "template": (
            "请以参考素材生成视频（对应 LibTV 视频节点 → 图片参考 / 全能参考）。\n"
            "参考素材：{ref}\n"
            "目标场景描述：{topic}\n"
            "要求：尽量保留参考素材中的主体特征/风格，按目标场景描述演绎。"
        ),
        "ref_label": "参考图或视频 URL",
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="LibTV 节点能力封装",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "环境变量:\n  LIBTV_ACCESS_KEY  必填\n\n"
            "可用动作（按节点分类）：\n  "
            + "\n  ".join(
                f"{k:<24}[{v['node']}] {v['label']}"
                + (f"  [需 --ref]" if v.get("ref_label") else "")
                + (f"  [需 --ref2]" if v.get("needs_ref2") else "")
                for k, v in NODE_ACTIONS.items()
            )
            + "\n\n示例:\n"
            "  python3 node.py text_to_video_prompt \"一只猫在屋顶看月亮\"\n"
            "  python3 node.py image_caption --ref https://example.com/a.png\n"
            "  python3 node.py image_to_image \"换成赛博朋克风\" --ref https://example.com/a.png\n"
            "  python3 node.py first_last_frame \"角色拔剑的过程\" --ref start.png --ref2 end.png\n"
        ),
    )
    parser.add_argument("action", choices=list(NODE_ACTIONS.keys()), help="动作名称")
    parser.add_argument("topic", nargs="?", default="", help="主题/目标描述（部分动作可省略）")
    parser.add_argument("--ref", default="", help="参考素材 URL")
    parser.add_argument("--ref2", default="", help="第二个参考素材 URL（首尾帧的尾帧）")
    parser.add_argument("--session-id", default="", help="已有会话 ID，不传则新建")
    parser.add_argument("--dry-run", action="store_true", help="只打印将发送的 prompt，不调真实 API（不消耗积分）")

    args = parser.parse_args()
    spec = NODE_ACTIONS[args.action]

    if spec.get("ref_label") and not args.ref:
        print(f"错误：{args.action} 需要 --ref ({spec['ref_label']})", file=sys.stderr)
        sys.exit(1)
    if spec.get("needs_ref2") and not args.ref2:
        print(f"错误：{args.action} 需要 --ref2 ({spec.get('ref2_label','')})", file=sys.stderr)
        sys.exit(1)
    if not args.topic and not spec.get("topic_optional"):
        print(f"错误：{args.action} 需要 topic 描述", file=sys.stderr)
        sys.exit(1)

    topic_line = (f"额外要求：{args.topic}\n" if args.topic else "")
    message = spec["template"].format(
        topic=args.topic,
        topic_line=topic_line,
        ref=args.ref,
        ref2=args.ref2,
    )

    if args.dry_run:
        print(json.dumps({
            "dry_run": True,
            "action": args.action,
            "node": spec["node"],
            "label": spec["label"],
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
        record_project(project_uuid, set_current=True, desc=f"{spec['node']}:{spec['label']}")

    out = {
        "action": args.action,
        "node": spec["node"],
        "label": spec["label"],
        "projectUuid": project_uuid,
        "sessionId": session_id,
        "projectUrl": build_project_url(project_uuid),
        "message_sent": message,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    safe_run(main)
