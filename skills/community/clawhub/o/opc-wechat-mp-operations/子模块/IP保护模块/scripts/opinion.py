#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
观点模块脚本 - 为文章添加观点IP模块

使用方法:
    python opinion.py --input article.md --output article_ip.md --type comment --content "我的观点内容"
"""

import argparse
import os
import re


# 观点类型定义
OPINION_TYPES = {
    "comment": {
        "name": "老胡评论",
        "emoji": "💬",
        "color": "#2D7D9A",
        "bg_color": "#f0f7fa",
    },
    "viewpoint": {
        "name": "老胡观点",
        "emoji": "🎯",
        "color": "#E67E22",
        "bg_color": "#fef9f3",
    },
    "reminder": {
        "name": "老胡提醒",
        "emoji": "⚠️",
        "color": "#27AE60",
        "bg_color": "#f0faf4",
    },
}


def create_opinion_block(opinion_type, content):
    """创建观点模块HTML"""
    config = OPINION_TYPES.get(opinion_type, OPINION_TYPES["comment"])
    
    return f'''
<div style="border-left: 4px solid {config['color']}; padding: 12px 16px; margin: 16px 0; background: {config['bg_color']}; border-radius: 0 8px 8px 0;">
  <p style="margin: 0;"><strong>{config['emoji']} {config['name']}</strong></p>
  <p style="margin: 8px 0 0 0; color: #333; line-height: 1.6;">{content}</p>
</div>
'''


def create_author_card(name="老胡", style="simple"):
    """创建作者背景卡片"""
    if style == "detailed":
        return '''
<hr style="border: none; border-top: 1px dashed #ddd; margin: 30px 0;"/>
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 24px; border-radius: 12px; color: white;">
  <p style="margin: 0 0 12px 0; font-size: 18px;"><strong>👤 关于老胡</strong></p>
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
        return '''
<hr style="border: none; border-top: 1px dashed #ddd; margin: 30px 0;"/>
<div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
  <p style="margin: 0 0 10px 0;"><strong>关于老胡</strong></p>
  <p style="margin: 0; color: #666; font-size: 14px; line-height: 1.8;">
    老胡，技术成果转化咨询师，曾任央企投资公司常务副总、产权交易机构负责人，
    专注技术成果转化和知识产权交易十余年。
  </p>
</div>
'''


def insert_opinion(content, opinion_type, opinion_content):
    """在文章中插入观点"""
    opinion_block = create_opinion_block(opinion_type, opinion_content)
    
    # 在第一个 </h2> 或 </h3> 后插入（假设第一个小标题之后是第一个论点位置）
    match = re.search(r'(</h[2-3][^>]*>)', content)
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + '\n' + opinion_block + content[insert_pos:]
    else:
        # 如果没有找到标题，在文章中间位置插入
        mid = len(content) // 2
        content = content[:mid] + '\n' + opinion_block + content[mid:]
    
    return content


def insert_author_card(content, name="老胡", style="simple"):
    """在文章末尾插入作者卡片"""
    card = create_author_card(name, style)
    content = content + '\n' + card
    return content


def add_opinions_to_article(content, opinions):
    """
    为文章批量添加观点
    
    Args:
        content: 文章内容
        opinions: 观点列表，每个元素为 dict: {"type": "comment", "content": "..."}
    
    Returns:
        添加观点后的文章
    """
    for opinion in opinions:
        opinion_type = opinion.get("type", "comment")
        opinion_content = opinion.get("content", "")
        if opinion_content:
            content = insert_opinion(content, opinion_type, opinion_content)
    
    return content


class AuthorCard:
    """作者卡片生成器"""
    
    @staticmethod
    def generate(style="simple", name="老胡"):
        """生成作者卡片"""
        return create_author_card(name, style)
    
    @staticmethod
    def generate_detailed():
        """生成详细版作者卡片"""
        return create_author_card("老胡", "detailed")
    
    @staticmethod
    def generate_compact():
        """生成简洁版作者卡片"""
        return create_author_card("老胡", "simple")


def process_file(input_path, output_path, opinions=None, add_card=True):
    """处理单个文件"""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加观点
    if opinions:
        content = add_opinions_to_article(content, opinions)
    
    # 添加作者卡片
    if add_card:
        content = insert_author_card(content)
    
    # 保存
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已处理: {input_path} → {output_path}")


def main():
    parser = argparse.ArgumentParser(description='为公众号文章添加观点模块')
    parser.add_argument('--input', '-i', required=True, help='输入文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--type', '-t', default='comment', 
                        choices=['comment', 'viewpoint', 'reminder'],
                        help='观点类型')
    parser.add_argument('--content', '-c', help='观点内容')
    parser.add_argument('--no-card', action='store_true', help='不添加作者卡片')
    
    args = parser.parse_args()
    
    output_path = args.output or args.input.replace('.', '_ip.')
    
    # 构建观点列表
    opinions = []
    if args.content:
        opinions.append({"type": args.type, "content": args.content})
    
    process_file(args.input, output_path, opinions, not args.no_card)


if __name__ == '__main__':
    main()
