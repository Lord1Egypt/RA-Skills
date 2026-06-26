#!/usr/bin/env python3
"""
单个单词卡片生成脚本
功能：根据单词信息生成视觉化学习卡片
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

class VocabularyCard:
    """单词卡片生成器"""
    
    def __init__(self, word, style="artistic"):
        self.word = word.lower()
        self.style = style
        self.card_data = {}
        
    def fetch_word_info(self):
        """
        获取单词信息（音标、释义、例句）
        注：实际使用时需要调用词典API或数据库
        """
        # 模拟数据结构
        self.card_data = {
            "word": self.word,
            "phonetic": "",  # 待填充
            "part_of_speech": "",  # 待填充
            "chinese_meaning": "",  # 待填充
            "example_sentence": "",  # 待填充
            "root_analysis": {},  # 待填充
            "image_style": self.style,
            "created_at": datetime.now().isoformat()
        }
        return self.card_data
    
    def analyze_roots(self):
        """
        分析词根词缀
        注：需要配合词根词缀数据库使用
        """
        # 常见词根词缀库（示例）
        common_roots = {
            "un-": {"meaning": "not", "type": "prefix"},
            "re-": {"meaning": "again", "type": "prefix"},
            "-tion": {"meaning": "action/process", "type": "suffix"},
            "-able": {"meaning": "can be", "type": "suffix"},
            "spect": {"meaning": "look/see", "type": "root"},
            "port": {"meaning": "carry", "type": "root"},
        }
        
        # 简单匹配逻辑（实际应使用更复杂的词根分析算法）
        analysis = []
        for root, info in common_roots.items():
            if root in self.word:
                analysis.append({
                    "part": root,
                    "meaning": info["meaning"],
                    "type": info["type"]
                })
        
        self.card_data["root_analysis"] = analysis
        return analysis
    
    def generate_card_markdown(self):
        """生成Markdown格式的卡片"""
        md_content = f"""# 📚 {self.word.upper()}

## 🎨 Visual Memory
[图片区域 - 使用 search_images 或 image_generate 工具生成配图]
风格：{self.style}

## 📖 Word Information

**音标**: `{self.card_data.get('phonetic', '待获取')}`

**词性**: {self.card_data.get('part_of_speech', '待获取')}

**中文释义**: {self.card_data.get('chinese_meaning', '待获取')}

## 🔍 Root Analysis
"""
        
        roots = self.card_data.get('root_analysis', [])
        if roots:
            for root in roots:
                md_content += f"- **{root['part']}** ({root['type']}): {root['meaning']}\n"
        else:
            md_content += "_该单词无明显词根词缀分解_\n"
        
        md_content += f"""
## 💬 Example Sentence
{self.card_data.get('example_sentence', '待获取')}

---
*创建时间: {self.card_data['created_at']}*
"""
        return md_content
    
    def save_card(self, output_dir="./cards"):
        """保存卡片到文件"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存Markdown
        md_content = self.generate_card_markdown()
        md_file = output_path / f"{self.word}_card.md"
        md_file.write_text(md_content, encoding='utf-8')
        
        # 保存JSON数据
        json_file = output_path / f"{self.word}_data.json"
        json_file.write_text(json.dumps(self.card_data, ensure_ascii=False, indent=2), encoding='utf-8')
        
        print(f"✅ 卡片已生成：{md_file}")
        return str(md_file)


def main():
    parser = argparse.ArgumentParser(description='生成单词学习卡片')
    parser.add_argument('--word', required=True, help='要学习的单词')
    parser.add_argument('--style', default='artistic', 
                       choices=['cartoon', 'realistic', 'artistic', 'minimalist'],
                       help='图片风格')
    parser.add_argument('--output', default='./cards', help='输出目录')
    
    args = parser.parse_args()
    
    # 创建卡片
    card = VocabularyCard(args.word, args.style)
    card.fetch_word_info()
    card.analyze_roots()
    card.save_card(args.output)


if __name__ == "__main__":
    main()
