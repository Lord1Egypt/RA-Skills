#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小绿书一键生成器 v1.0
输入主题 → 自动输出全套卡片（HTML + PNG + TXT）

使用方法:
    python3 generate_xiaolvshu.py --topic "主题" --type [psychology|history|business|selfhelp]
    
示例:
    python3 generate_xiaolvshu.py --topic "达克效应" --type psychology
    python3 generate_xiaolvshu.py --topic "曾国藩的成事心法" --type history
"""

import argparse
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 配置路径
WORKSPACE = Path("/root/.openclaw/workspace")
TEMPLATE_DIR = WORKSPACE / "template-xiaolvshu"
OUTPUT_DIR = WORKSPACE / "reports"
SKILL_DIR = WORKSPACE / "skills" / "knowledge-card-designer"

class XiaolvshuGenerator:
    def __init__(self, topic, content_type):
        self.topic = topic
        self.content_type = content_type
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_folder = OUTPUT_DIR / f"xiaogreenbook_{self._slugify(topic)}_{self.timestamp}"
        
        # 加载系统配置
        self.content_system = self._load_content_system()
        self.visual_system = self._load_visual_system()
        
    def _slugify(self, text):
        """将中文主题转换为文件夹名"""
        return text.replace(" ", "_").replace("/", "_")[:30]
    
    def _load_content_system(self):
        """加载内容系统配置"""
        # 简化的内容模板
        return {
            "psychology": {
                "theme": "冷静灰",
                "colors": {"primary": "#2d3436", "accent": "#ff6b6b", "accent2": "#00b894"},
                "structure": ["概念定义", "生活案例", "心理机制", "应对方法"],
                "hooks": ["你不知道的", "为什么你总是", "心理学家发现"]
            },
            "history": {
                "theme": "暖金棕", 
                "colors": {"primary": "#3d2914", "accent": "#e9c46a", "accent2": "#d4af37"},
                "structure": ["历史背景", "人物故事", "关键决策", "现代启示"],
                "hooks": ["1940年", "在动荡年代", "鲜为人知的是"]
            },
            "business": {
                "theme": "专业蓝",
                "colors": {"primary": "#1a1a2e", "accent": "#e9c46a", "accent2": "#e76f51"},
                "structure": ["问题现象", "底层逻辑", "实战案例", "行动清单"],
                "hooks": ["顶级高手", "年薪百万的人", "公司不想让你知道的"]
            },
            "selfhelp": {
                "theme": "活力多彩",
                "colors": {"primary": "#1a1a2e", "accent": "#e76f51", "accent2": "#2a9d8f"},
                "structure": ["痛点场景", "认知升级", "方法论", "行动指南"],
                "hooks": ["30岁才懂的", "如果早点知道", "改变我一生的"]
            }
        }
    
    def _load_visual_system(self):
        """加载视觉系统配置"""
        return {
            "card_width": 1080,
            "card_height": 1350,
            "padding": 60,
            "fonts": {
                "number": "28px",
                "title": "64px",
                "subtitle": "24px",
                "quote": "32px",
                "body": "26px"
            }
        }
    
    def generate(self):
        """主生成流程"""
        print(f"🚀 开始生成：{self.topic}")
        print(f"📁 输出目录：{self.output_folder}")
        
        # 创建输出目录
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # 1. 生成文案
        content = self._generate_content()
        self._save_txt(content)
        
        # 2. 生成封面HTML
        cover_html = self._generate_cover_html()
        self._save_html("cover.html", cover_html)
        self._save_html("cover_card.html", self._generate_cover_card_html())
        
        # 3. 生成内容卡片HTML
        for i, card_content in enumerate(content["cards"], 1):
            card_html = self._generate_card_html(i, card_content)
            self._save_html(f"card{i}.html", card_html)
        
        # 4. 生成预览索引
        preview_html = self._generate_preview_html()
        self._save_html("preview.html", preview_html)
        
        print(f"✅ 生成完成！")
        print(f"📂 文件位置：{self.output_folder}")
        print(f"\n下一步：")
        print(f"  1. 查看 preview.html 预览效果")
        print(f"  2. 修改各card.html内容")
        print(f"  3. 运行截图脚本生成PNG")
        
        return self.output_folder
    
    def _generate_content(self):
        """生成文案结构（框架，需人工填充）"""
        config = self.content_system.get(self.content_type, self.content_system["selfhelp"])
        
        # 选择钩子
        import random
        hook = random.choice(config["hooks"])
        
        content = {
            "title": self.topic,
            "hook": hook,
            "subtitle": f"{hook}{self.topic}的3个关键洞察",
            "tags": ["#认知升级", "#人间清醒", f"#{self.content_type}"],
            "cards": []
        }
        
        # 生成卡片框架
        for i, section in enumerate(config["structure"][:4], 1):
            content["cards"].append({
                "number": i,
                "title": f"{section}：待填写",
                "subtitle": "待填写副标题",
                "quote": "待填写金句",
                "case_label": "💬 场景",
                "case_text": "待填写案例内容...",
                "insight_label": "💡 洞察",
                "insight_text": "待填写洞察内容..."
            })
        
        return content
    
    def _generate_cover_html(self):
        """生成横版封面HTML"""
        config = self.content_system.get(self.content_type, self.content_system["selfhelp"])
        colors = config["colors"]
        
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif; }}
.cover {{
    width: 900px;
    height: 383px;
    background: linear-gradient(135deg, {colors['primary']} 0%, {colors['accent']} 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 40px;
    position: relative;
}}
.cover-title {{ font-size: 44px; font-weight: 800; color: #fff; text-align: center; margin-bottom: 16px; }}
.cover-subtitle {{ font-size: 20px; color: rgba(255,255,255,0.8); text-align: center; }}
</style>
</head>
<body>
<div class="cover">
    <div class="cover-title">{self.topic}</div>
    <div class="cover-subtitle">点击编辑副标题</div>
</div>
</body>
</html>"""
    
    def _generate_cover_card_html(self):
        """生成卡片尺寸封面HTML"""
        config = self.content_system.get(self.content_type, self.content_system["selfhelp"])
        colors = config["colors"]
        
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif; }}
.cover {{
    width: 1080px;
    height: 1350px;
    background: linear-gradient(135deg, {colors['primary']} 0%, {colors['accent']} 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 80px;
    position: relative;
}}
.cover-title {{ font-size: 72px; font-weight: 800; color: #fff; text-align: center; margin-bottom: 40px; line-height: 1.3; }}
.cover-subtitle {{ font-size: 36px; color: rgba(255,255,255,0.8); text-align: center; }}
</style>
</head>
<body>
<div class="cover">
    <div class="cover-title">{self.topic}</div>
    <div class="cover-subtitle">点击编辑副标题</div>
</div>
</body>
</html>"""
    
    def _generate_card_html(self, number, card_content):
        """生成单张卡片HTML"""
        config = self.content_system.get(self.content_type, self.content_system["selfhelp"])
        colors = config["colors"]
        
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", sans-serif; }}
.card {{
    width: 1080px;
    height: 1350px;
    background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    position: relative;
    overflow: hidden;
    padding: 60px;
}}
.card-number {{
    display: inline-block;
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent2']} 100%);
    border-radius: 50%;
    text-align: center;
    line-height: 56px;
    color: white;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 24px;
}}
.card-title {{ font-size: 56px; font-weight: 800; color: #1a1a2e; margin-bottom: 12px; }}
.card-subtitle {{ font-size: 24px; color: #636e72; margin-bottom: 36px; }}
.card-quote {{
    background: linear-gradient(135deg, {colors['accent']} 0%, {colors['accent2']} 100%);
    padding: 32px 40px;
    border-radius: 16px;
    margin-bottom: 36px;
}}
.card-quote-text {{ font-size: 32px; color: white; font-weight: 600; line-height: 1.5; }}
.card-case {{
    background: white;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    border-left: 5px solid {colors['accent']};
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}}
.card-case-label {{ font-size: 17px; color: {colors['accent']}; font-weight: 700; margin-bottom: 12px; }}
.card-case-text {{ font-size: 26px; color: #2d3436; line-height: 1.7; }}
.card-footer {{
    position: absolute;
    bottom: 50px;
    left: 60px;
    right: 60px;
    display: flex;
    justify-content: space-between;
    padding-top: 24px;
    border-top: 1px solid #dee2e6;
}}
.card-footer-brand {{ font-size: 22px; color: #636e72; font-weight: 600; }}
.card-footer-page {{ font-size: 20px; color: #adb5bd; }}
</style>
</head>
<body>
<div class="card">
    <div class="card-number">{number}</div>
    <div class="card-title">{card_content['title']}</div>
    <div class="card-subtitle">{card_content['subtitle']}</div>
    
    <div class="card-quote">
        <div class="card-quote-text">{card_content['quote']}</div>
    </div>
    
    <div class="card-case">
        <div class="card-case-label">{card_content['case_label']}</div>
        <div class="card-case-text">{card_content['case_text']}</div>
    </div>
    
    <div class="card-footer">
        <div class="card-footer-brand">{self.topic}</div>
        <div class="card-footer-page">{number}/4</div>
    </div>
</div>
</body>
</html>"""
    
    def _generate_preview_html(self):
        """生成预览页面HTML"""
        return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{self.topic} - 预览</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; padding: 40px; background: #f0f0f0; }}
.preview-container {{ max-width: 1200px; margin: 0 auto; }}
.preview-item {{ margin-bottom: 40px; background: white; padding: 20px; border-radius: 12px; }}
.preview-item h3 {{ margin-bottom: 16px; color: #333; }}
.preview-item img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
</style>
</head>
<body>
<div class="preview-container">
    <h1>{self.topic}</h1>
    <p>类型：{self.content_type} | 生成时间：{self.timestamp}</p>
    <hr>
    <div class="preview-item">
        <h3>封面（横版）</h3>
        <iframe src="cover.html" width="900" height="400" style="border:none;"></iframe>
    </div>
    <div class="preview-item">
        <h3>封面（卡片）</h3>
        <iframe src="cover_card.html" width="1080" height="1350" style="border:none; transform: scale(0.5); transform-origin: top left;"></iframe>
    </div>
    <div class="preview-item">
        <h3>卡片1</h3>
        <iframe src="card1.html" width="1080" height="1350" style="border:none; transform: scale(0.5); transform-origin: top left;"></iframe>
    </div>
</div>
</body>
</html>"""
    
    def _save_txt(self, content):
        """保存文案文本"""
        txt_content = f"""【{content['title']}】

{content['hook']}{content['subtitle']}

"""
        for card in content["cards"]:
            txt_content += f"""
━━━

{card['number']}. {card['title']}

{card['quote']}

{card['case_label']}：
{card['case_text']}

{card['insight_label']}：
{card['insight_text']}
"""
        
        txt_content += f"""

━━━

{' '.join(content['tags'])}
"""
        
        with open(self.output_folder / "content.txt", "w", encoding="utf-8") as f:
            f.write(txt_content)
    
    def _save_html(self, filename, html_content):
        """保存HTML文件"""
        with open(self.output_folder / filename, "w", encoding="utf-8") as f:
            f.write(html_content)

def main():
    parser = argparse.ArgumentParser(description="小绿书一键生成器")
    parser.add_argument("--topic", "-t", required=True, help="主题名称")
    parser.add_argument("--type", "-p", choices=["psychology", "history", "business", "selfhelp"],
                       default="selfhelp", help="内容类型")
    
    args = parser.parse_args()
    
    generator = XiaolvshuGenerator(args.topic, args.type)
    generator.generate()

if __name__ == "__main__":
    main()
