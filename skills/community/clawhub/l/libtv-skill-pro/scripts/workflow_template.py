#!/usr/bin/env python3
"""
工作流模板脚本 - 预设的常用工作流
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import create_session, build_project_url, safe_run


# 预设工作流模板
WORKFLOW_TEMPLATES = {
    "storyboard": {
        "name": "分镜生成",
        "description": "生成故事分镜",
        "prompt": "请帮我生成一个故事的完整分镜，包含场景描述、镜头角度、画面内容。主题是：{topic}",
    },
    "character_design": {
        "name": "角色设计",
        "description": "设计角色形象",
        "prompt": "请帮我设计一个角色，包含正面、侧面、背面三视图，以及角色的服装、发型、特征描述。角色设定：{topic}",
    },
    "video_generation": {
        "name": "视频生成",
        "description": "生成 AI 视频",
        "prompt": "请帮我生成一个视频：{topic}",
    },
    "image_generation": {
        "name": "图片生成",
        "description": "生成 AI 图片",
        "prompt": "请帮我生成一张图片：{topic}",
    },
    "style_transfer": {
        "name": "风格迁移",
        "description": "转换图片/视频风格",
        "prompt": "请将参考内容转换为 {topic} 风格",
    },
    "short_drama": {
        "name": "短剧生成",
        "description": "生成完整短剧",
        "prompt": """请帮我制作一个短剧：{topic}

请按以下步骤完成：
1. 编写剧本
2. 设计角色形象
3. 生成分镜
4. 制作视频片段
5. 合成完整短剧
""",
    },
    "music_video": {
        "name": "音乐 MV",
        "description": "根据音乐生成 MV",
        "prompt": "请根据音乐生成一个 MV：{topic}",
    },
    "product_showcase": {
        "name": "产品展示",
        "description": "生成产品展示视频",
        "prompt": "请帮我制作一个产品展示视频：{topic}",
    },
}


def list_templates():
    """列出所有模板"""
    print("可用工作流模板:")
    print("-" * 60)
    print(f"{'ID':20} {'名称':15} {'描述'}")
    print("-" * 60)
    for key, template in WORKFLOW_TEMPLATES.items():
        print(f"{key:20} {template['name']:15} {template['description']}")


def run_template(template_id: str, topic: str, session_id: str = ""):
    """运行指定模板"""
    if template_id not in WORKFLOW_TEMPLATES:
        print(f"错误：未知模板 '{template_id}'", file=sys.stderr)
        print("使用 --list 查看可用模板")
        sys.exit(1)
    
    template = WORKFLOW_TEMPLATES[template_id]
    prompt = template["prompt"].format(topic=topic)
    
    print(f"[*] 使用模板: {template['name']}")
    print(f"[*] 描述: {template['description']}")
    print("-" * 60)
    print(f"[*] 生成提示词:")
    print(prompt)
    print("-" * 60)
    
    # 创建会话
    print(f"[*] 创建会话并发送请求...")
    
    result = create_session(session_id=session_id, message=prompt)
    result["projectUrl"] = build_project_url(result.get("projectUuid", ""))
    
    print(f"[*] 会话创建成功!")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="工作流模板工具 - 使用预设模板快速创建任务",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
环境变量:
  LIBTV_ACCESS_KEY  必填，Bearer 鉴权

示例:
  # 列出所有模板
  python3 workflow_template.py --list

  # 使用分镜模板
  python3 workflow_template.py storyboard "一个科幻城市的故事"

  # 使用角色设计模板
  python3 workflow_template.py character_design "一个勇敢的骑士"

  # 使用短剧模板
  python3 workflow_template.py short_drama "一个关于友情的故事"

  # 使用已有会话
  python3 workflow_template.py video_generation "夕阳下的海滩" --session-id <id>

可用模板:
  storyboard       - 分镜生成
  character_design - 角色设计
  video_generation - 视频生成
  image_generation - 图片生成
  style_transfer   - 风格迁移
  short_drama      - 短剧生成
  music_video      - 音乐 MV
  product_showcase - 产品展示
        """,
    )
    parser.add_argument("template", nargs="?", help="模板 ID")
    parser.add_argument("topic", nargs="?", help="主题/描述")
    parser.add_argument("--list", action="store_true", help="列出所有模板")
    parser.add_argument("--session-id", help="使用已有会话 ID")
    
    args = parser.parse_args()
    
    if args.list:
        list_templates()
        return
    
    if not args.template or not args.topic:
        parser.print_help()
        sys.exit(1)
    
    run_template(args.template, args.topic, args.session_id)


if __name__ == "__main__":
    safe_run(main)
