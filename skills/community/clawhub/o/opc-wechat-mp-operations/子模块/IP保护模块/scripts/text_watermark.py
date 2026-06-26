#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字水印脚本 - 为公众号文章添加开头/结尾水印

使用方法:
    python text_watermark.py --input article.md --output article_marked.md
    python text_watermark.py --input article.md --output article_marked.md --intro "自定义开头" --outro "自定义结尾"
"""

import argparse
import os
import re


# 默认配置
DEFAULT_CONFIG = {
    "wechat_name": "老胡说",
    "intro": "📌 本文首发于【老胡说】，专注技术成果转化与政策解读",
    "outro": "💡 原创文章，未经授权禁止转载 | 老胡说",
    "intro_style": "blockquote",  # simple/blockquote
    "outro_style": "simple",
}


def create_intro_block(intro_text, style="blockquote"):
    """创建开头水印块"""
    if style == "blockquote":
        return f'''
<div style="border-left: 4px solid #2D7D9A; padding: 12px 16px; background: #f8f9fa; margin: 20px 0;">
  <p style="margin: 0; color: #333;">
    {intro_text}
  </p>
</div>
'''
    else:
        return f'''
<div style="text-align: center; padding: 16px; margin: 20px 0; color: #666; font-size: 14px;">
  <p style="margin: 0;">{intro_text}</p>
</div>
'''


def create_outro_block(outro_text, style="simple"):
    """创建结尾水印块"""
    if style == "blockquote":
        return f'''
<hr style="border: none; border-top: 1px dashed #ddd; margin: 30px 0;"/>
<div style="border-left: 4px solid #2D7D9A; padding: 12px 16px; background: #f8f9fa; margin: 20px 0; text-align: center;">
  <p style="margin: 0; color: #333; text-align: center;">{outro_text}</p>
</div>
'''
    else:
        return f'''
<hr style="border: none; border-top: 1px dashed #ddd; margin: 30px 0;"/>
<div style="text-align: center; color: #666; font-size: 14px; padding: 20px;">
  <p style="margin: 0;">{outro_text}</p>
</div>
'''


def create_author_card(name="老胡", style="simple"):
    """创建作者背景卡片"""
    if style == "detailed":
        return f'''
<hr style="border: none; border-top: 1px dashed #ddd; margin: 30px 0;"/>
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px; border-radius: 12px; color: white;">
  <p style="margin: 0 0 12px 0; font-size: 18px;"><strong>👤 关于{name}</strong></p>
  <p style="margin: 0; font-size: 14px; line-height: 1.8;">
    技术成果转化咨询师，曾任央企投资公司常务副总、产权交易机构负责人。
    <br/>专注领域：技术成果转化、知识产权交易、投资咨询、政策解读。
    <br/>十余年实战经验，陪伴数百个项目完成转化落地。
  </p>
  <p style="margin: 12px 0 0 0; font-size: 13px; opacity: 0.9;">
    📧 深度交流，后台私信 | 🔄 转发请注明出处
  </p>
</div>
'''
    else:
        return f'''
<hr style="border: none; border-top: 1px dashed #ddd; margin: 30px 0;"/>
<div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
  <p style="margin: 0 0 10px 0;"><strong>关于{name}</strong></p>
  <p style="margin: 0; color: #666; font-size: 14px; line-height: 1.8;">
    {name}，技术成果转化咨询师，曾任央企投资公司常务副总、产权交易机构负责人，
    专注技术成果转化和知识产权交易十余年。
  </p>
</div>
'''


def add_text_watermark(content, config=None):
    """
    为文章添加文字水印
    
    Args:
        content: 文章内容
        config: 配置字典，包含 wechat_name, intro, outro, intro_style, outro_style
    
    Returns:
        添加水印后的文章内容
    """
    if config is None:
        config = DEFAULT_CONFIG
    
    # 构建开头水印
    intro = config.get("intro", DEFAULT_CONFIG["intro"])
    intro_style = config.get("intro_style", DEFAULT_CONFIG["intro_style"])
    intro_block = create_intro_block(intro, intro_style)
    
    # 构建结尾水印
    outro = config.get("outro", DEFAULT_CONFIG["outro"])
    outro_style = config.get("outro_style", DEFAULT_CONFIG["outro_style"])
    outro_block = create_outro_block(outro, outro_style)
    
    # 判断是否已添加过水印（避免重复添加）
    if "本文首发于【" in content and config.get("wechat_name", "") in content:
        # 已添加过，尝试更新
        content = re.sub(
            r'<div style="[^"]*border-left:[^"]*#2D7D9A[^"]*>.*?</div>\s*',
            intro_block,
            content,
            flags=re.DOTALL
        )
    else:
        # 添加开头水印（在正文开始处）
        # 查找第一个段落或标题
        first_content_match = re.search(r'(<h[1-6][^>]*>|[\u4e00-\u9fa5]{2,}<br/?>)', content)
        if first_content_match:
            insert_pos = first_content_match.start()
            content = content[:insert_pos] + intro_block + content[insert_pos:]
        else:
            content = intro_block + content
    
    # 添加结尾水印
    if "未经授权禁止转载" not in content:
        content = content + "\n" + outro_block
    
    return content


def process_file(input_path, output_path, config=None):
    """处理单个文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    marked_content = add_text_watermark(content, config)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(marked_content)
    
    print(f"✅ 已处理: {input_path} → {output_path}")


def batch_process(input_dir, output_dir, config=None):
    """批量处理目录下的所有markdown文件"""
    os.makedirs(output_dir, exist_ok=True)
    
    count = 0
    for filename in os.listdir(input_dir):
        if filename.endswith(('.md', '.txt', '.html')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            process_file(input_path, output_path, config)
            count += 1
    
    print(f"\n处理完成：{count} 个文件")


def main():
    parser = argparse.ArgumentParser(description='为公众号文章添加文字水印')
    parser.add_argument('--input', '-i', required=True, help='输入文件或目录路径')
    parser.add_argument('--output', '-o', help='输出文件或目录路径')
    parser.add_argument('--intro', help='自定义开头水印文本')
    parser.add_argument('--outro', help='自定义结尾水印文本')
    parser.add_argument('--name', default='老胡说', help='公众号名称')
    
    args = parser.parse_args()
    
    # 构建配置
    config = DEFAULT_CONFIG.copy()
    if args.name:
        config["wechat_name"] = args.name
        config["intro"] = f"📌 本文首发于【{args.name}】，专注技术成果转化与政策解读"
        config["outro"] = f"💡 原创文章，未经授权禁止转载 | {args.name}"
    
    if args.intro:
        config["intro"] = args.intro
    
    if args.outro:
        config["outro"] = args.outro
    
    # 判断输入是文件还是目录
    if os.path.isfile(args.input):
        output_path = args.output or args.input.replace('.', '_marked.')
        process_file(args.input, output_path, config)
    elif os.path.isdir(args.input):
        output_dir = args.output or args.input + '_marked'
        batch_process(args.input, output_dir, config)
    else:
        print(f"❌ 错误：找不到文件或目录 {args.input}")


if __name__ == '__main__':
    main()
