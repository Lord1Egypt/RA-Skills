#!/usr/bin/env python3
"""
md2wechat — Markdown 转微信公众号草稿箱一键工具

用法:
    # 仅转换为微信兼容 HTML（不需要微信密钥）
    python md2wechat.py article.md --convert-only --output ./preview.html

    # 转换并上传到微信草稿箱
    python md2wechat.py article.md --draft

    # 指定封面图和自定义标题
    python md2wechat.py article.md --draft --title "我的文章" --cover ./cover.png

    # 使用指定的 .env 文件
    python md2wechat.py article.md --draft --env-file /path/to/.env
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 确保 scripts 目录在搜索路径中，以便导入同目录下的模块
SCRIPT_DIR = Path(__file__).parent.resolve()
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from md_converter import MarkdownConverter


def load_env(env_file: str = None):
    """加载 .env 环境变量文件"""
    if env_file and os.path.exists(env_file):
        try:
            from dotenv import load_dotenv
            load_dotenv(env_file)
            print(f"[INFO] 已加载配置文件: {env_file}")
        except ImportError:
            # 手动解析简单 .env 文件
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, _, value = line.partition('=')
                        os.environ[key.strip()] = value.strip()
            print(f"[INFO] 已加载配置文件: {env_file}")


def main():
    parser = argparse.ArgumentParser(
        description='md2wechat — 将 Markdown 文件转换为微信公众号兼容格式并上传到草稿箱',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s article.md --convert-only                    # 仅转换，输出到 stdout
  %(prog)s article.md --convert-only --output out.html  # 仅转换，保存到文件
  %(prog)s article.md --draft                           # 转换并上传到微信草稿箱
  %(prog)s article.md --draft --cover ./cover.png       # 带封面图上传
  %(prog)s article.md --draft --env-file .env           # 指定配置文件
        """
    )

    parser.add_argument('md_file', help='Markdown 文件路径')

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument('--convert-only', action='store_true',
                            help='仅转换为微信兼容 HTML（不上传）')
    mode_group.add_argument('--draft', action='store_true', default=True,
                            help='转换并上传到微信草稿箱（默认模式）')

    parser.add_argument('--title', help='自定义文章标题（不传则自动从 Markdown 提取）')
    parser.add_argument('--author', help='文章作者（不传则从 Front Matter 提取）')
    parser.add_argument('--cover', help='封面图片路径')
    parser.add_argument('--output', help='HTML 输出路径（用于 --convert-only 模式）或本地预览保存目录')
    parser.add_argument('--env-file', help='.env 环境变量配置文件路径')

    args = parser.parse_args()

    # 验证输入文件
    md_path = Path(args.md_file).resolve()
    if not md_path.exists():
        print(f"[ERROR] 文件不存在: {md_path}")
        sys.exit(1)
    if md_path.suffix.lower() != '.md':
        print(f"[WARN] 警告: 文件不是 .md 格式: {md_path.suffix}")

    # 加载环境变量
    if args.env_file:
        load_env(args.env_file)

    print(f"\n[FILE] 正在处理: {md_path.name}")
    print("=" * 50)

    # ── convert-only 模式 ──
    if args.convert_only:
        result = MarkdownConverter.convert_file(str(md_path))
        if not result:
            print("[ERROR] 转换失败")
            sys.exit(1)

        # 覆盖标题和作者
        if args.title:
            result['title'] = args.title
        if args.author:
            result['author'] = args.author

        if args.output:
            # 保存到文件
            output_path = Path(args.output).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)

            preview_html = (
                f"<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n"
                f"<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
                f"<title>{result['title']} - 本地预览</title>\n"
                f"<style>body {{ max-width: 677px; margin: 20px auto; padding: 20px; "
                f"font-family: -apple-system, system-ui, sans-serif; background: #f7f7f7; }} "
                f"#wechat-article {{ background: #fff; padding: 30px; border-radius: 8px; "
                f"box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}</style>\n"
                f"</head>\n<body>\n<div id='wechat-article'>\n"
                f"<h1 style='font-size: 22px; margin-bottom: 20px;'>{result['title']}</h1>\n"
                f"{result['content']}\n"
                f"</div>\n</body>\n</html>"
            )
            output_path.write_text(preview_html, encoding='utf-8')
            print(f"\n[OK] 转换成功！已保存到: {output_path}")
        else:
            # 输出到 stdout
            print(f"\n[OK] 转换成功！")
            print(f"[TITLE] 标题: {result['title']}")
            print(f"[DRAFT] 摘要: {result['summary']}")
            print(f"[LENGTH] 内容长度: {len(result['content'])} 字符")
            print(f"\n{'─' * 50}")
            print(result['content'])

        # 输出结构化 JSON（便于其他程序或 AI Agent 读取）
        meta_json = {
            'title': result['title'],
            'author': result.get('author', ''),
            'summary': result.get('summary', ''),
            'content_length': len(result['content']),
            'publish_mode': result.get('publish_mode', 'draft'),
        }
        print(f"\n[INFO] 元数据 (JSON):")
        print(json.dumps(meta_json, ensure_ascii=False, indent=2))
        sys.exit(0)

    # ── draft 模式 ──
    # 检查微信密钥
    appid = os.environ.get('WECHAT_APPID')
    secret = os.environ.get('WECHAT_SECRET')

    if not appid or not secret:
        print("[ERROR] 缺少微信公众号配置！")
        print("   请通过以下方式之一设置：")
        print("   1. 设置环境变量 WECHAT_APPID 和 WECHAT_SECRET")
        print("   2. 使用 --env-file 参数指定 .env 配置文件")
        print(f"\n   配置模板参见: {SCRIPT_DIR.parent / 'resources' / 'env_template.txt'}")
        sys.exit(1)

    # 导入微信客户端（延迟导入，仅在 draft 模式下需要）
    from wechat_client import WeChatSkillClient

    try:
        client = WeChatSkillClient(appid=appid, secret=secret)
    except Exception as e:
        print(f"[ERROR] 初始化微信客户端失败: {e}")
        sys.exit(1)

    # 转换 Markdown（同时传入 publisher 以处理正文内嵌图片）
    result = MarkdownConverter.convert_file(str(md_path), publisher=client)
    if not result:
        print("[ERROR] 转换失败")
        sys.exit(1)

    if args.title:
        result['title'] = args.title
    if args.author:
        result['author'] = args.author

    print(f"\n[TITLE] 标题: {result['title']}")
    print(f"[DRAFT] 摘要: {result['summary']}")
    print(f"[LENGTH] 内容长度: {len(result['content'])} 字符")

    # 上传封面图（如果指定）
    cover_media_id = None
    if args.cover:
        cover_path = Path(args.cover).resolve()
        if cover_path.exists():
            print(f"\n[IMAGE]  正在上传封面图: {cover_path.name}")
            cover_media_id = client.upload_image(str(cover_path))
        else:
            print(f"[WARN] 封面图文件不存在: {args.cover}")

    # 创建草稿
    print(f"\n[UPLOAD] 正在上传到微信草稿箱...")
    draft_media_id = client.create_draft(result, cover_media_id=cover_media_id)

    if draft_media_id:
        print(f"\n[SUCCESS] 发布完成！")
        print(f"   草稿 media_id: {draft_media_id}")
        print(f"   请登录微信公众平台查看草稿箱")
    else:
        print(f"\n[ERROR] 上传到草稿箱失败")
        sys.exit(1)

    # 保存预览（如果指定了输出路径）
    if args.output:
        output_dir = Path(args.output).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        preview_file = output_dir / f"{md_path.stem}_preview.html"

        preview_html = (
            f"<!DOCTYPE html>\n<html>\n<head>\n<meta charset='utf-8'>\n"
            f"<title>{result['title']} - 预览</title>\n"
            f"<style>body {{ max-width: 677px; margin: 20px auto; padding: 20px; "
            f"font-family: -apple-system, system-ui, sans-serif; background: #f7f7f7; }} "
            f"#wechat-article {{ background: #fff; padding: 30px; border-radius: 8px; "
            f"box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}</style>\n"
            f"</head>\n<body>\n<div id='wechat-article'>\n"
            f"<h1 style='font-size: 22px; margin-bottom: 20px;'>{result['title']}</h1>\n"
            f"{result['content']}\n</div>\n</body>\n</html>"
        )
        preview_file.write_text(preview_html, encoding='utf-8')
        print(f"💾 本地预览已保存: {preview_file}")


if __name__ == '__main__':
    main()
