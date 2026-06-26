#!/usr/bin/env python3
"""LibTV 模型路由：列出已知模型，或显式指定模型生成"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import create_session, build_project_url, record_project, safe_run


# 已知模型清单。来自 LibTV 平台公开信息与 SKILL.md 描述。
# 实际可用模型以服务端为准；这里给 Agent 一个推荐表。
MODELS = {
    # ---------- LLM / 文本 ----------
    "gvlm-3.1": {
        "kind": "llm",
        "suits": ["剧本", "广告词", "品牌文案", "提示词改写"],
        "note": "LibTV 默认文本模型",
    },
    # ---------- 图像 ----------
    "lib-nano-pro": {
        "kind": "image",
        "suits": ["快速生图", "图生图", "图片高清"],
        "note": "LibTV 自研 Nano 模型 Pro 版",
    },
    "nano-banana": {
        "kind": "image",
        "suits": ["平面海报", "插画"],
        "note": "Google Gemini 系小巧模型",
    },
    "midjourney": {
        "kind": "image",
        "suits": ["美学风", "插画", "海报"],
        "note": "经典美学",
    },
    "seedream-5.0": {
        "kind": "image",
        "suits": ["写实", "电影感"],
        "note": "字节豆包系图像模型",
    },
    # ---------- 视频 ----------
    "seedance-2.0-vip": {
        "kind": "video",
        "suits": ["文生视频", "图生视频", "短片"],
        "note": "字节豆包 Seedance 2.0 VIP 版，LibTV 默认视频模型",
    },
    "kling-3.0": {
        "kind": "video",
        "suits": ["写实人像", "动作连贯", "长视频"],
        "note": "快手可灵 3.0",
    },
    "kling-o3": {
        "kind": "video",
        "suits": ["高质量长视频"],
        "note": "可灵 O3 升级版",
    },
    "wan-2.6": {
        "kind": "video",
        "suits": ["文生视频", "多镜头长视频"],
        "note": "阿里通义万相 2.6",
    },
}


def cmd_list(kind_filter: str = ""):
    items = [
        (name, info)
        for name, info in MODELS.items()
        if not kind_filter or info["kind"] == kind_filter
    ]
    if not items:
        print(f"未找到模型（kind={kind_filter or 'any'}）")
        return
    print(f"{'模型名':<20} {'类型':<6} {'适用场景':<32} 备注")
    print("-" * 100)
    for name, info in items:
        suits = "/".join(info["suits"])[:30]
        print(f"{name:<20} {info['kind']:<6} {suits:<32} {info['note']}")


def cmd_with_model(model: str, message: str, params: dict, session_id: str = "", dry_run: bool = False):
    """显式指定模型 + 参数生成。所有指令以自然语言放在 prompt 顶端，
    后端 Agent 接收后会按指令路由（具体执行程度取决于服务端实现）。"""
    if model not in MODELS:
        # 不阻塞陌生模型，但提醒
        print(f"提醒：{model} 不在已知模型清单中，仍会原样转发给后端。", file=sys.stderr)

    instr_lines = [f"指定模型：{model}"]
    for k, v in params.items():
        if v:
            instr_lines.append(f"{k}：{v}")
    instr = "[模型/参数指令]\n" + "\n".join(instr_lines)

    full_message = f"{instr}\n\n[生成需求]\n{message}"

    if dry_run:
        print(json.dumps({
            "dry_run": True,
            "model": model,
            "params": {k: v for k, v in params.items() if v},
            "session_id": session_id or "(new)",
            "would_send": full_message,
        }, ensure_ascii=False, indent=2))
        return

    data = create_session(session_id=session_id or "", message=full_message)
    project_uuid = data.get("projectUuid", "")
    sid = data.get("sessionId", "")
    if not sid:
        print("错误：未返回 sessionId", file=sys.stderr)
        sys.exit(1)
    if project_uuid:
        record_project(project_uuid, set_current=True, desc=f"with-model:{model}")

    out = {
        "model": model,
        "params": params,
        "projectUuid": project_uuid,
        "sessionId": sid,
        "projectUrl": build_project_url(project_uuid),
        "message_sent": full_message,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="LibTV 模型路由",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "环境变量:\n  LIBTV_ACCESS_KEY  必填\n\n"
            "示例:\n"
            "  # 列出所有已知模型\n"
            "  python3 model.py list\n"
            "  # 仅列视频模型\n"
            "  python3 model.py list --kind video\n"
            "  # 指定 Seedance 2.0 VIP 生成 5 秒 720P 16:9 视频\n"
            "  python3 model.py with seedance-2.0-vip \"黄昏草原一只白马奔跑\" "
            "--ratio 16:9 --duration 5s --resolution 720P\n"
            "  # 指定 Lib Nano Pro 生成 16:9 2K 图片\n"
            "  python3 model.py with lib-nano-pro \"赛博朋克少女肖像\" --ratio 16:9 --resolution 2K\n"
            "\n说明：参数以自然语言形式拼到 prompt 前，后端 Agent 会按指令路由。\n"
            "       服务端最终是否严格执行指令，依赖 LibTV IM 后端实现。\n"
        ),
    )
    sub = parser.add_subparsers(dest="command")

    p_list = sub.add_parser("list", help="列出已知模型")
    p_list.add_argument("--kind", choices=["llm", "image", "video"], default="", help="按类型过滤")

    p_with = sub.add_parser("with", help="显式指定模型生成")
    p_with.add_argument("model", help="模型名（见 list）")
    p_with.add_argument("message", help="生成需求 prompt")
    p_with.add_argument("--ratio", default="", help="比例，如 16:9 / 1:1 / 9:16")
    p_with.add_argument("--resolution", default="", help="分辨率，如 2K / 720P / 1080P")
    p_with.add_argument("--duration", default="", help="时长（仅视频），如 5s / 10s")
    p_with.add_argument("--count", default="", help="生成数量，如 1张 / 4张")
    p_with.add_argument("--extra", default="", help="其他自由形式参数指令")
    p_with.add_argument("--session-id", default="", help="已有会话 ID")
    p_with.add_argument("--dry-run", action="store_true", help="只打印将发送的 prompt，不调真实 API（不消耗积分）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "list":
        cmd_list(kind_filter=args.kind)
    elif args.command == "with":
        params = {
            "比例": args.ratio,
            "分辨率": args.resolution,
            "时长": args.duration,
            "数量": args.count,
            "其他": args.extra,
        }
        cmd_with_model(
            model=args.model,
            message=args.message,
            params=params,
            session_id=args.session_id,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    safe_run(main)
