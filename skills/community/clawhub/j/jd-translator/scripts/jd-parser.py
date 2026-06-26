#!/usr/bin/env python3
"""
JD 文本解析脚本
提取 JD 中的关键词、协作对象、能力要求等关键信息

用法：
    python jd-parser.py < jd.txt
    python jd-parser.py "JD 文本内容"
"""

import sys
import re
from typing import List, Dict


def extract_sections(text: str) -> Dict[str, str]:
    """提取 JD 的各个部分（岗位职责、任职要求等）"""
    sections = {}
    
    # 常见 section 标题
    patterns = [
        (r'【岗位职责】(.+?)(?=【任职要求】|【|$])', 'responsibilities'),
        (r'【任职要求】(.+?)(?=【|岗位 | 职责 |$])', 'requirements'),
        (r'【岗位职责】(.+?)(?=任职 | 要求 |$])', 'responsibilities'),
        (r'【任职要求】(.+?)(?=职责 | 岗位 |$])', 'requirements'),
    ]
    
    for pattern, section_name in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match and section_name not in sections:
            sections[section_name] = match.group(1).strip()
    
    return sections


def extract_keywords(text: str) -> List[str]:
    """提取关键词（0-1、千万级、从雏形到上线等）"""
    keywords = []
    
    patterns = [
        r'0[-到 -]1',
        r'千万级',
        r'亿级',
        r'从雏形到上线',
        r'全流程',
        r'主导',
        r'驱动',
        r'协同',
        r'带领团队',
        r'管理',
        r'规划',
        r'迭代',
        r'优化',
        r'AI',
        r'大数据',
    ]
    
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            keywords.append(pattern)
    
    return keywords


def extract_collaboration(text: str) -> List[str]:
    """提取协作对象（协同 XX 团队、与 XX 协作等）"""
    collaborations = []
    
    patterns = [
        r'协同 (.+?) 团队',
        r'与 (.+?) 协作',
        r'和 (.+?) 配合',
        r'对接 (.+?) 部门',
        r'汇报给',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        collaborations.extend(matches)
    
    return list(set(collaborations))


def extract_capabilities(text: str) -> List[str]:
    """提取能力要求（每条任职要求）"""
    capabilities = []
    
    # 按序号或换行分割
    lines = re.split(r'\n|\d+[、.．]', text)
    
    for line in lines:
        line = line.strip()
        if len(line) > 10:  # 过滤太短的行
            capabilities.append(line)
    
    return capabilities[:15]  # 最多返回 15 条


def analyze_job_type(responsibilities: str) -> str:
    """分析岗位类型（新设岗/迭代岗/替换岗/管理岗）"""
    if re.search(r'0[-到 -]1|从雏形到上线 | 新设 | 搭建', responsibilities, re.IGNORECASE):
        return '新设岗（开拓型）'
    elif re.search(r'迭代 | 优化 | 持续改善 | 维护', responsibilities, re.IGNORECASE):
        return '迭代岗（优化型）'
    elif re.search(r'带领 | 管理 | 团队 | 负责', responsibilities, re.IGNORECASE):
        return '管理岗'
    else:
        return '替换岗（待确认）'


def format_output(sections: Dict, keywords: List, collaborations: List, 
                  capabilities: List, job_type: str) -> str:
    """格式化输出"""
    output = []
    output.append("=" * 60)
    output.append("JD 解析结果")
    output.append("=" * 60)
    output.append("")
    
    output.append("【岗位类型】")
    output.append(f"  {job_type}")
    output.append("")
    
    output.append("【关键词】")
    for kw in keywords:
        output.append(f"  • {kw}")
    output.append("")
    
    output.append("【协作对象】")
    if collaborations:
        for collab in collaborations:
            output.append(f"  • {collab}")
    else:
        output.append("  （未明确提及）")
    output.append("")
    
    output.append("【能力要求】")
    for i, cap in enumerate(capabilities[:10], 1):
        output.append(f"  {i}. {cap}")
    output.append("")
    
    if 'responsibilities' in sections:
        output.append("【岗位职责摘要】")
        resp = sections['responsibilities'][:300]
        output.append(f"  {resp}...")
        output.append("")
    
    output.append("=" * 60)
    output.append("提示：将以上信息输入 @jd-translator 进行深度分析")
    output.append("=" * 60)
    
    return '\n'.join(output)


def main():
    if len(sys.argv) > 1:
        # 从命令行参数获取 JD
        jd_text = ' '.join(sys.argv[1:])
    else:
        # 从标准输入获取 JD
        jd_text = sys.stdin.read()
    
    if not jd_text.strip():
        print("错误：请提供 JD 文本")
        print("用法：python jd-parser.py < jd.txt")
        print("      python jd-parser.py \"JD 文本内容\"")
        sys.exit(1)
    
    # 解析 JD
    sections = extract_sections(jd_text)
    keywords = extract_keywords(jd_text)
    collaborations = extract_collaboration(jd_text)
    capabilities = []
    
    if 'requirements' in sections:
        capabilities = extract_capabilities(sections['requirements'])
    
    job_type = '未知'
    if 'responsibilities' in sections:
        job_type = analyze_job_type(sections['responsibilities'])
    
    # 输出结果
    output = format_output(sections, keywords, collaborations, capabilities, job_type)
    print(output)


if __name__ == '__main__':
    main()
