#!/usr/bin/env python3
"""
批量单词卡片生成脚本
功能：批量处理单词列表，生成学习卡片集
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
import concurrent.futures

class BatchCardGenerator:
    """批量卡片生成器"""
    
    def __init__(self, words_list, style="artistic", output_dir="./cards"):
        self.words = [w.strip().lower() for w in words_list]
        self.style = style
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def process_word(self, word):
        """处理单个单词"""
        # 导入单个卡片生成器
        from generate_card import VocabularyCard
        
        card = VocabularyCard(word, self.style)
        card.fetch_word_info()
        card.analyze_roots()
        return card.save_card(str(self.output_dir))
    
    def generate_all(self, parallel=True):
        """批量生成卡片"""
        results = []
        
        if parallel:
            # 并行处理（提高效率）
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(self.process_word, word): word 
                          for word in self.words}
                
                for future in concurrent.futures.as_completed(futures):
                    word = futures[future]
                    try:
                        result = future.result()
                        results.append(result)
                        print(f"✅ {word} 处理完成")
                    except Exception as e:
                        print(f"❌ {word} 处理失败: {e}")
        else:
            # 顺序处理
            for word in self.words:
                try:
                    result = self.process_word(word)
                    results.append(result)
                    print(f"✅ {word} 处理完成")
                except Exception as e:
                    print(f"❌ {word} 处理失败: {e}")
        
        return results
    
    def generate_summary(self):
        """生成学习总结文档"""
        summary_file = self.output_dir / "learning_summary.md"
        
        content = f"""# 📚 学习卡片集总结

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**单词数量**: {len(self.words)}

**图片风格**: {self.style}

## 📋 单词列表

"""
        for i, word in enumerate(self.words, 1):
            content += f"{i}. {word}\n"
        
        content += """
## 📂 文件结构

"""
        content += f"""
```
{self.output_dir}/
├── learning_summary.md (本文件)
"""
        for word in self.words:
            content += f"├── {word}_card.md\n"
            content += f"├── {word}_data.json\n"
        
        content += "```\n"
        
        summary_file.write_text(content, encoding='utf-8')
        print(f"\n✅ 总结文档已生成：{summary_file}")
        
        return str(summary_file)


def main():
    parser = argparse.ArgumentParser(description='批量生成单词学习卡片')
    parser.add_argument('--words', required=True, help='单词列表（逗号分隔）')
    parser.add_argument('--style', default='artistic', 
                       choices=['cartoon', 'realistic', 'artistic', 'minimalist'],
                       help='图片风格')
    parser.add_argument('--output', default='./cards', help='输出目录')
    parser.add_argument('--parallel', action='store_true', default=True,
                       help='并行处理（默认开启）')
    
    args = parser.parse_args()
    
    # 解析单词列表
    words_list = [w.strip() for w in args.words.split(',')]
    
    # 批量生成
    generator = BatchCardGenerator(words_list, args.style, args.output)
    generator.generate_all(parallel=args.parallel)
    generator.generate_summary()


if __name__ == "__main__":
    main()
