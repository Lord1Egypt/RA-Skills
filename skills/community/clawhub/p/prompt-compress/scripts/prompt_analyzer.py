#!/usr/bin/env python3
"""
Prompt Analyzer - 分析和统计提示词 Token 使用情况

功能:
- 计算原始提示词的 Token 数量
- 提取关键词
- 分析冗余内容
- 提供压缩建议
"""

import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    """分析结果"""
    original_text: str
    original_tokens: int
    keywords: List[str]
    redundant_phrases: List[str]
    structure: Dict[str, str]
    compression_suggestions: List[str]


# 简化的 Token 估算（中英文混合）
# 英文约 4 字符 = 1 token，中文约 1.5 字符 = 1 token
def estimate_tokens(text: str) -> int:
    """估算文本的 Token 数量"""
    # 分离中英文
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    other_chars = len(text) - chinese_chars - english_chars
    
    # 估算 token
    chinese_tokens = chinese_chars / 1.5
    english_tokens = english_chars / 4
    other_tokens = other_chars / 3
    
    return int(chinese_tokens + english_tokens + other_tokens)


def extract_keywords(text: str) -> List[str]:
    """提取关键词"""
    # 常见停用词
    stopwords = {
        '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
        '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
        '自己', '这', '那', '他', '她', '它', '们', '这个', '那个', '什么', '怎么',
        'please', 'help', 'need', 'want', 'would', 'could', 'should', 'can', 'will',
        'thank', 'thanks', 'hello', 'hi', 'hey', 'dear', 'sorry', 'maybe'
    }
    
    # 提取中英文词汇
    chinese_words = re.findall(r'[\u4e00-\u9fff]{2,}', text)
    english_words = re.findall(r'[a-zA-Z]{3,}', text.lower())
    
    # 过滤停用词并去重
    keywords = []
    for word in chinese_words + english_words:
        if word.lower() not in stopwords and word not in stopwords:
            keywords.append(word)
    
    # 保持顺序去重
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw.lower() not in seen:
            seen.add(kw.lower())
            unique_keywords.append(kw)
    
    return unique_keywords[:20]  # 最多返回 20 个关键词


def find_redundant_phrases(text: str) -> List[str]:
    """识别冗余短语"""
    redundant_patterns = [
        r'请[你您]?帮我[做写看分析]?一下',
        r'谢谢[您你]?',
        r'你好[,，]?我是',
        r'我[需要想]要你[帮请]我',
        r'如果可以的?话',
        r'麻烦你',
        r'非常感谢',
        r'详细地?',
        r'仔细地?',
        r'尽可能',
        r'帮帮忙',
    ]
    
    found = []
    for pattern in redundant_patterns:
        matches = re.findall(pattern, text)
        found.extend(matches)
    
    return found


def analyze_structure(text: str) -> Dict[str, str]:
    """分析提示词结构"""
    structure = {}
    
    # 识别任务类型
    task_patterns = [
        (r'写|创作|生成|编写', 'create'),
        (r'分析|研究|解读', 'analyze'),
        (r'总结|概括|提炼', 'summarize'),
        (r'解释|说明|讲解', 'explain'),
        (r'翻译|转换', 'transform'),
        (r'修复|解决|debug', 'fix'),
        (r'优化|改进|提升', 'optimize'),
    ]
    
    for pattern, task_type in task_patterns:
        if re.search(pattern, text):
            structure['task'] = task_type
            break
    
    # 识别约束条件
    constraints = []
    if re.search(r'\d+字', text):
        word_count = re.search(r'(\d+)字', text)
        if word_count:
            constraints.append(f"字数:{word_count.group(1)}")
    
    if re.search(r'步骤|第一|第二', text):
        structure['format'] = 'steps'
    
    if constraints:
        structure['constraints'] = ', '.join(constraints)
    
    return structure


def generate_compression_suggestions(text: str, keywords: List[str], redundant: List[str]) -> List[str]:
    """生成压缩建议"""
    suggestions = []
    
    if redundant:
        suggestions.append(f"删除冗余用语: {', '.join(redundant[:5])}")
    
    if len(text) > 200:
        suggestions.append("使用结构化格式（列表/表格）替代长段落")
    
    if len(keywords) > 10:
        suggestions.append("用关键词标签替代描述性文本")
    
    suggestions.append("用符号替代常用词：优点→+，缺点→-，问题→Q:")
    suggestions.append("删除重复修饰词和语气词")
    
    return suggestions


def analyze_prompt(text: str) -> AnalysisResult:
    """分析提示词"""
    original_tokens = estimate_tokens(text)
    keywords = extract_keywords(text)
    redundant = find_redundant_phrases(text)
    structure = analyze_structure(text)
    suggestions = generate_compression_suggestions(text, keywords, redundant)
    
    return AnalysisResult(
        original_text=text,
        original_tokens=original_tokens,
        keywords=keywords,
        redundant_phrases=redundant,
        structure=structure,
        compression_suggestions=suggestions
    )


def format_result(result: AnalysisResult) -> str:
    """格式化输出结果"""
    output = []
    output.append("=" * 50)
    output.append("[ANALYSIS] 提示词分析结果")
    output.append("=" * 50)
    output.append(f"\n[TOKENS] 原始 Token 数: {result.original_tokens}")
    
    if result.keywords:
        output.append(f"\n[KEYWORDS] 关键词 ({len(result.keywords)}个):")
        output.append(f"   {', '.join(result.keywords)}")
    
    if result.redundant_phrases:
        output.append(f"\n[REDUNDANT] 冗余内容 ({len(result.redundant_phrases)}处):")
        for phrase in result.redundant_phrases[:5]:
            output.append(f'   - "{phrase}"')
    
    if result.structure:
        output.append(f"\n[STRUCTURE] 结构分析:")
        for key, value in result.structure.items():
            output.append(f"   {key}: {value}")
    
    if result.compression_suggestions:
        output.append(f"\n[SUGGESTIONS] 压缩建议:")
        for i, suggestion in enumerate(result.compression_suggestions, 1):
            output.append(f"   {i}. {suggestion}")
    
    output.append("\n" + "=" * 50)
    
    return "\n".join(output)


def main():
    """主函数"""
    import sys
    import io
    
    # 设置 UTF-8 输出
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    if len(sys.argv) > 1:
        # 从命令行参数读取
        text = " ".join(sys.argv[1:])
    else:
        # 从标准输入读取
        print("请输入提示词（Ctrl+D 结束）:")
        text = sys.stdin.read()
    
    if not text.strip():
        print("错误: 未输入文本")
        sys.exit(1)
    
    result = analyze_prompt(text)
    print(format_result(result))


if __name__ == "__main__":
    main()