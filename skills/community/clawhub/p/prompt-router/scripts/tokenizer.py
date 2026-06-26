"""
Prompt-Router Tokenizer

分词器：支持中英文混合输入
- 英文：按空格/标点分词
- 中文：按字符/词语分词（简化版基于字符）
- 支持关键词标准化（小写、去除标点）
"""

import re
from typing import Set, List


class Tokenizer:
    """中英文混合分词器"""
    
    def __init__(self):
        # 中文标点符号
        self.chinese_punctuation = '，。！？；：""''、（）《》【】…—～·'
        # 英文标点符号
        self.english_punctuation = ',.!?;:"\'()[]{}<>…—~`@#$%^&*+=|\\/`'
        # 所有标点
        self.all_punctuation = self.chinese_punctuation + self.english_punctuation
        
        # 分词正则
        self.token_pattern = re.compile(r'[\w\u4e00-\u9fff]+')
    
    def tokenize(self, text: str) -> Set[str]:
        """
        将文本分词（混合策略：英文按词，中文按字符）
        
        Args:
            text: 输入文本
            
        Returns:
            分词集合（去重、小写）
        """
        # 转换为小写
        text = text.lower()
        
        tokens = set()
        
        # Step 1: 提取英文单词和数字
        english_tokens = self.token_pattern.findall(text)
        for token in english_tokens:
            # 如果是纯英文（包含字母），保留
            if any('a' <= c <= 'z' for c in token):
                if not token.isdigit():  # 去除纯数字
                    tokens.add(token)
        
        # Step 2: 提取中文字符（按字符分词）
        chinese_chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
        
        # Step 3: 提取中文词组（2-4 个连续汉字）
        chinese_text = ''.join(chinese_chars)
        for i in range(len(chinese_text)):
            # 2 字词
            if i + 2 <= len(chinese_text):
                tokens.add(chinese_text[i:i+2])
            # 3 字词
            if i + 3 <= len(chinese_text):
                tokens.add(chinese_text[i:i+3])
            # 4 字词
            if i + 4 <= len(chinese_text):
                tokens.add(chinese_text[i:i+4])
        
        # 去除纯数字 token
        tokens = {t for t in tokens if not t.isdigit()}
        
        return tokens
    
    def tokenize_preserve_order(self, text: str) -> List[str]:
        """
        分词并保留顺序
        
        Args:
            text: 输入文本
            
        Returns:
            分词列表（保留顺序）
        """
        text = text.lower()
        tokens = self.token_pattern.findall(text)
        tokens = [t for t in tokens if not t.isdigit()]
        return tokens
    
    def extract_keywords(self, text: str, min_length: int = 2) -> Set[str]:
        """
        提取关键词（过滤短词）
        
        Args:
            text: 输入文本
            min_length: 最小词长度
            
        Returns:
            关键词集合
        """
        tokens = self.tokenize(text)
        return {t for t in tokens if len(t) >= min_length}
    
    def is_chinese(self, text: str) -> bool:
        """
        判断文本是否主要为中文
        
        Args:
            text: 输入文本
            
        Returns:
            True 如果中文字符占比 > 50%
        """
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        total_chars = len(text.replace(' ', ''))
        if total_chars == 0:
            return False
        return chinese_chars / total_chars > 0.5
    
    def is_mixed(self, text: str) -> bool:
        """
        判断文本是否为中英文混合
        
        Args:
            text: 输入文本
            
        Returns:
            True 如果包含中英文
        """
        has_chinese = any('\u4e00' <= c <= '\u9fff' for c in text)
        has_english = any('a' <= c.lower() <= 'z' for c in text)
        return has_chinese and has_english


# 示例用法
if __name__ == '__main__':
    tokenizer = Tokenizer()
    
    # 测试英文
    text_en = "Read the config.json file"
    print(f"英文：{text_en}")
    print(f"分词：{tokenizer.tokenize(text_en)}")
    print()
    
    # 测试中文
    text_zh = "读取配置文件"
    print(f"中文：{text_zh}")
    print(f"分词：{tokenizer.tokenize(text_zh)}")
    print()
    
    # 测试混合
    text_mixed = "搜索 Python 教程"
    print(f"混合：{text_mixed}")
    print(f"分词：{tokenizer.tokenize(text_mixed)}")
    print()
    
    # 测试关键词提取
    text_long = "帮我搜索一下北京今天的天气怎么样"
    print(f"长文本：{text_long}")
    print(f"关键词：{tokenizer.extract_keywords(text_long)}")
