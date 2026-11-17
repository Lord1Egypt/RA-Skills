# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

"""
知识规则提取脚本
从 Markdown 文档中提取结构化知识规则

规则类型:
- frequency: 巡查/检测频率
- threshold: 技术阈值
- grade: 等级分类
- formula: 计算公式
- period: 周期要求
- material: 材料规格
- specification: 尺寸/规格要求
"""

import re
import sys
import os
import json
from datetime import datetime

# 规则模式定义
PATTERNS = {
    'frequency': [
        # 每日/每周/每月/每年
        r'(每[日月年天周季]|每隔?\d+[日月天年周季]|[一二三四五六七八九十\d]+[日月天年周季](?:一?次|巡查|检测|检验|检查|清扫|保洁))',
        r'(?:巡查|检测|检验|检查|清扫|保洁)[的]?(?:频次|频率|周期)[是为]?(\d+[日月天年周季]?一?次?)',
        r'(?:道路|桥梁|设施)(?:养护|维修|检测)[的]?周期[是为]?(\d+)',
    ],
    'threshold': [
        # 阈值表达式
        r'(?:≤|小于等于|不超过|不超过|不大于|> ?|≥|大于等于|不低于|不少于|不低于|不小于)[=]?\s*(\d+(?:\.\d+)?)\s*(?:mm|cm|m|kg|kN|Mpa|%|°C|米|厘米|毫米|千克|千牛|兆帕|度)?',
        r'(\d+(?:\.\d+)?)\s*(?:mm|cm|m|kg|kN|Mpa|%|°C|米|厘米|毫米|千克|千牛|兆帕|度)\s*(?:以上|以下|以下|以上)',
        r'平整度[为]?\s*[≤>=]\s*(\d+)\s*(?:mm|厘米)?',
        r'宽度[为]?\s*(\d+(?:\.\d+)?)\s*(?:m|米|厘米|cm)?',
        r'厚度[为]?\s*(\d+(?:\.\d+)?)\s*(?:cm|mm|m|米|厘米)?',
    ],
    'grade': [
        # 等级分类
        r'(?:等级|类别|分级)[为]?:?\s*([甲乙丙丁A-Za-z一二三四优良合格])',
        r'([优|良|合格|不合格|差|优秀|良好|中等|及格|不及格])(?:级|等)?[/、]([优|良|合格|不合格|差|优秀|良好|中等|及格|不及格])?',
        r'(A|B|C|D|a|b|c|d|Ⅰ|Ⅱ|Ⅲ|Ⅳ|1级|2级|3级|4级|一级|二级|三级|四级)(?:等|级)',
    ],
    'formula': [
        # 公式表达式
        r'([A-Z_]+)\s*=\s*[^=]{1,200}?(?:公式|计算)',
        r'计算公式[为]?:?\s*(.+)',
        r'养护费用[为]?\s*(\d+(?:\.\d+)?)\s*(?:元|万元)?',
    ],
    'period': [
        # 周期/养护期
        r'养护期[为]?:?\s*(≥|大于|不少于|不低于)?\s*(\d+)\s*(?:天|日|月|年)',
        r'(?:养护|保养|维护|存放)[期时][为]?:?\s*(\d+)\s*(?:天|日|月|年)',
        r'使用寿[命期][为]?:?\s*(\d+)\s*(?:年|月)',
    ],
    'material': [
        # 材料规格
        r'(?:水泥|混凝土|沥青|钢材)[为]?:?\s*(?:标号|强度)?\s*(?:C|c|[A-Z])(\d{2,4})',
        r'(?:沥青|水泥|钢材)[型号]?[为]?:?\s*([A-Z0-9]{2,10})',
        r'(?:水泥|混凝土)[强度]?[等]?级[为]?:?\s*(C\d{2,4})',
    ],
    'specification': [
        # 尺寸规格
        r'直径[为]?:?\s*(\d+(?:\.\d+)?)\s*(?:mm|cm|m|米|厘米)?',
        r'高度[为]?:?\s*(\d+(?:\.\d+)?)\s*(?:mm|cm|m|米|厘米)?',
        r'长度[为]?:?\s*(\d+(?:\.\d+)?)\s*(?:mm|cm|m|米|厘米)?',
        r'间距[为]?:?\s*(\d+(?:\.\d+)?)\s*(?:mm|cm|m|米|厘米)?',
    ]
}

# 中文数字转阿拉伯数字
CN_NUM = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}

def normalize_number(text):
    """标准化数字表达"""
    # 转换中文数字
    for cn, ar in CN_NUM.items():
        text = text.replace(cn, str(ar))
    return text

def extract_rules(text):
    """从文本中提取所有规则"""
    rules = {
        'frequency': [],
        'threshold': [],
        'grade': [],
        'formula': [],
        'period': [],
        'material': [],
        'specification': []
    }
    
    # 提取上下文（句子级别）
    sentences = re.split(r'[。；\n]', text)
    
    for rtype, patterns in PATTERNS.items():
        for sent in sentences:
            for pat in patterns:
                matches = re.finditer(pat, sent, re.IGNORECASE)
                for m in matches:
                    context = sent.strip()
                    if len(context) > 10 and len(context) < 300:
                        rule = {
                            'type': rtype,
                            'text': context,
                            'value': m.group(0) if m.lastindex is None else m.group(1),
                            'match': m.group(0)
                        }
                        # 去重
                        if rule not in rules[rtype]:
                            rules[rtype].append(rule)
    
    return rules

def rules_to_markdown(rules, title, standard_id):
    """将规则转为Markdown格式"""
    md = f'''# 知识规则提取报告

- 文档: {title}
- 标准号: {standard_id}
- 提取时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

'''
    
    type_names = {
        'frequency': '频率要求',
        'threshold': '技术阈值',
        'grade': '等级分类',
        'formula': '计算公式',
        'period': '周期要求',
        'material': '材料规格',
        'specification': '尺寸规格'
    }
    
    total = 0
    for rtype, rlist in rules.items():
        if rlist:
            md += f'## {type_names[rtype]}\n\n'
            for i, rule in enumerate(rlist, 1):
                md += f'{i}. **{rule["value"]}**\n   - 原文: {rule["text"][:150]}...\n'
            md += '\n'
            total += len(rlist)
    
    md += f'\n---\n共提取 {total} 条规则。\n'
    return md

def main():
    if len(sys.argv) < 2:
        print("用法: python extract_rules.py <md_file> [--output output.json]")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output = None
    
    for i, arg in enumerate(sys.argv):
        if arg == '--output' and i+1 < len(sys.argv):
            output = sys.argv[i+1]
    
    if not os.path.exists(md_file):
        print(f"[ERROR] File not found: {md_file}")
        sys.exit(1)
    
    # 读取
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取YAML front matter
    title = "未知文档"
    standard_id = "未知"
    
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', fm_text)
        if title_match:
            title = title_match.group(1).strip()
        sid_match = re.search(r'standard_id:\s*["\']?([^"\'\n]+)["\']?', fm_text)
        if sid_match:
            standard_id = sid_match.group(1).strip()
        # 去掉front matter
        content = content[fm_match.end():]
    
    # 提取正文（去掉标题行）
    lines = content.split('\n')
    body_lines = [l for l in lines if not l.startswith('#')]
    body = '\n'.join(body_lines)
    
    print(f"[EXTRACT] {title} ({standard_id})")
    
    rules = extract_rules(body)
    
    # 统计
    total = sum(len(v) for v in rules.values())
    print(f"[OK] Extracted {total} rules:")
    for rtype, rlist in rules.items():
        if rlist:
            print(f"  - {rtype}: {len(rlist)}")
    
    # 输出
    if output:
        result = {
            'title': title,
            'standard_id': standard_id,
            'rules': rules,
            'timestamp': datetime.now().isoformat()
        }
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[OK] Saved to {output}")
    else:
        md = rules_to_markdown(rules, title, standard_id)
        print()
        print(md)

if __name__ == '__main__':
    main()
