import sys
import re

def count_words(text):
    """统计字数，包含符号"""
    # 移除首尾空白
    text = text.strip()
    # 统计所有非空白字符（包含标点）
    chars = len(re.findall(r'\S', text))
    return chars

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python wordcount.py <文件路径>")
        print("示例: python wordcount.py chapter-001.md")
        sys.exit(1)
    
    filepath = sys.argv[1]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        count = count_words(content)
        print(f"字数统计: {count} 字")
    except FileNotFoundError:
        print(f"错误: 文件不存在 - {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
