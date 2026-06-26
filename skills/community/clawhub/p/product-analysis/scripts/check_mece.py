#!/usr/bin/env python3
"""
check_mece.py - MECE 原则检查工具

用法:
    python3 check_mece.py <markdown_file>

功能:
    对产品分析文档中的功能清单进行 MECE 原则检查：
    1. 互斥性检查：识别功能描述中的潜在重叠
    2. 完整性检查：识别需求中可能未被覆盖的关键词
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Set
from collections import Counter


def extract_feature_list(content: str) -> List[str]:
    """从文档中提取功能清单。"""
    features = []
    
    # 方法1: 查找"功能清单"章节后的列表项
    feature_section = re.search(
        r"#+\s*.*功能清单.*?\n(.*?)(?=\n#+|\Z)", 
        content, 
        re.DOTALL | re.IGNORECASE
    )
    
    if feature_section:
        section_text = feature_section.group(1)
        # 提取有序列表和无序列表
        items = re.findall(r"^\s*[\d\-\*]+\.?\s+\*?\*?(.+?)\*?\*?$", section_text, re.MULTILINE)
        features.extend([item.strip() for item in items if item.strip()])
    
    # 方法2: 查找表格中的功能名称列
    table_matches = re.finditer(
        r"\|\s*功能(?:ID|名称|点)?\s*\|.*?\n\|.*?\n((?:\|.*?\n)+)",
        content,
        re.IGNORECASE
    )
    
    for match in table_matches:
        rows = match.group(1).strip().split('\n')
        for row in rows:
            cells = [c.strip() for c in row.split('|') if c.strip()]
            if len(cells) >= 2 and not cells[0].startswith('-'):
                # 第二列通常是功能名称
                feature_name = cells[1] if len(cells) > 1 else cells[0]
                if feature_name and not re.match(r'^[P\d\-]+$', feature_name):
                    features.append(feature_name)
    
    return list(set(features))  # 去重


def extract_requirements(content: str) -> str:
    """提取需求背景和业务目标文本。"""
    req_text = ""
    
    # 提取需求背景
    background = re.search(
        r"#+\s*需求(?:背景|概述).*?\n(.*?)(?=\n#+|\Z)",
        content,
        re.DOTALL | re.IGNORECASE
    )
    if background:
        req_text += background.group(1) + "\n"
    
    # 提取业务目标
    goals = re.search(
        r"#+\s*业务目标.*?\n(.*?)(?=\n#+|\Z)",
        content,
        re.DOTALL | re.IGNORECASE
    )
    if goals:
        req_text += goals.group(1) + "\n"
    
    return req_text


def check_mutual_exclusivity(features: List[str], threshold: float = 0.4) -> List[Tuple[str, str, float]]:
    """检查功能清单的互斥性（基于简单的词汇重叠）。"""
    overlaps = []
    
    def tokenize(text: str) -> Set[str]:
        """简单分词（基于空格和标点）。"""
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        # 提取中文字符和英文单词
        chinese_chars = set(re.findall(r'[\u4e00-\u9fa5]', text))
        english_words = set(re.findall(r'[a-z]+', text))
        return chinese_chars | english_words
    
    def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
        """计算 Jaccard 相似度。"""
        if not set1 or not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    # 两两比较
    for i in range(len(features)):
        for j in range(i + 1, len(features)):
            tokens1 = tokenize(features[i])
            tokens2 = tokenize(features[j])
            similarity = jaccard_similarity(tokens1, tokens2)
            
            if similarity >= threshold:
                overlaps.append((features[i], features[j], similarity))
    
    return sorted(overlaps, key=lambda x: x[2], reverse=True)


def check_collective_exhaustiveness(requirements: str, features: List[str]) -> List[str]:
    """检查功能清单的完整性（基于关键词覆盖）。"""
    # 提取需求中的关键动词和名词（中文）
    req_keywords = set()
    
    # 常见的业务动词
    action_verbs = [
        '查看', '查询', '添加', '删除', '修改', '编辑', '创建', '取消',
        '提交', '审核', '发布', '导出', '导入', '搜索', '筛选', '排序',
        '通知', '提醒', '统计', '分析', '管理', '配置', '设置', '同步'
    ]
    
    # 从需求中提取这些动词
    for verb in action_verbs:
        if verb in requirements:
            req_keywords.add(verb)
    
    # 提取需求中的关键名词（2-4个字的词组）
    noun_patterns = re.findall(r'[\u4e00-\u9fa5]{2,4}', requirements)
    common_nouns = [word for word, count in Counter(noun_patterns).items() if count >= 2]
    req_keywords.update(common_nouns[:10])  # 取前10个高频词
    
    # 检查哪些关键词未在功能清单中出现
    features_text = ' '.join(features).lower()
    missing_keywords = []
    
    for keyword in req_keywords:
        if keyword not in features_text:
            missing_keywords.append(keyword)
    
    return missing_keywords


def main():
    if len(sys.argv) != 2:
        print("用法: python3 check_mece.py <markdown_file>")
        sys.exit(1)
    
    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"错误: 文件不存在 - {filepath}")
        sys.exit(1)
    
    print(f"正在检查文件: {filepath.name}")
    print("=" * 50)
    
    try:
        content = filepath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            content = filepath.read_text(encoding="gbk")
            print(f"⚠️  检测到非 UTF-8 编码，已使用 GBK 编码读取。\n")
        except Exception as e:
            print(f"错误: 无法读取文件 - {e}")
            sys.exit(1)
    
    # 提取功能清单和需求
    features = extract_feature_list(content)
    requirements = extract_requirements(content)
    
    if not features:
        print("⚠️  未能从文档中提取到功能清单。")
        print("提示: 请确保文档中包含'功能清单'章节或功能表格。")
        sys.exit(1)
    
    print(f"✅ 已提取 {len(features)} 个功能项\n")
    
    # 互斥性检查
    print("【互斥性检查 (Mutually Exclusive)】")
    overlaps = check_mutual_exclusivity(features)
    
    if overlaps:
        print(f"⚠️  发现 {len(overlaps)} 组潜在重叠:\n")
        for f1, f2, sim in overlaps:
            print(f"  • \"{f1}\" ↔ \"{f2}\"")
            print(f"    相似度: {sim:.2f}")
            print(f"    建议: 检查是否可以合并或明确区分职责\n")
    else:
        print("✅ 未发现明显的功能重叠\n")
    
    # 完整性检查
    print("【完整性检查 (Collectively Exhaustive)】")
    
    if not requirements:
        print("⚠️  未能提取到需求背景或业务目标，跳过完整性检查。")
        print("提示: 请确保文档中包含'需求背景'或'业务目标'章节。\n")
    else:
        missing = check_collective_exhaustiveness(requirements, features)
        
        if missing:
            print(f"⚠️  需求中的以下关键词可能未被功能清单覆盖:\n")
            for keyword in missing[:10]:  # 只显示前10个
                print(f"  • \"{keyword}\"")
            print(f"\n  建议: 检查这些关键词是否对应遗漏的功能点\n")
        else:
            print("✅ 需求中的主要关键词均已被覆盖\n")
    
    # 总结
    print("=" * 50)
    print("【检查总结】")
    print(f"  • 功能项总数: {len(features)}")
    print(f"  • 潜在重叠: {len(overlaps)} 组")
    print(f"  • 可能遗漏: {len(missing) if requirements else 'N/A'} 个关键词")
    print("\n💡 提示: MECE 检查基于启发式算法，建议人工复核所有标记的问题。")
    
    # 返回状态码
    if overlaps or (requirements and missing):
        sys.exit(1)  # 发现潜在问题
    else:
        sys.exit(0)  # 未发现问题


if __name__ == "__main__":
    main()
