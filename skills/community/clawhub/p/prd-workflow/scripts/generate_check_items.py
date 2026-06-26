#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRD 质量检查项生成器

从 docs/checker.md 生成 workflows/check_items.py
用于 Python 脚本中直接导入检查项数据

使用方法:
    python scripts/generate_check_items.py
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime


class CheckItemsGenerator:
    """检查项生成器"""
    
    def __init__(self, base_path):
        """
        初始化生成器
        
        Args:
            base_path: 技能根目录路径
        """
        self.base_path = Path(base_path)
        self.checker_md_path = self.base_path / 'docs' / 'checker.md'
        self.output_py_path = self.base_path / 'workflows' / 'check_items.py'
    
    def parse_checker_md(self):
        """
        解析 checker.md 文件
        
        Returns:
            list: 检查项列表
        """
        if not self.checker_md_path.exists():
            raise FileNotFoundError(f"检查项文档不存在：{self.checker_md_path}")
        
        with open(self.checker_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        items = []
        lines = content.split('\n')
        
        current_item = None
        current_category = None
        in_checkpoints = False
        in_questions = False
        in_criteria = False
        
        for line in lines:
            trimmed_line = line.strip()
            
            # 检测分类标题
            category_match = re.match(
                r'^##\s+[🔴🟡🟢]?\s*([^(]+)\s*\((CORE|COMPLETE|OPTIMIZE)\)',
                trimmed_line
            )
            if category_match:
                current_category = {
                    'name': category_match.group(1).strip(),
                    'code': category_match.group(2)
                }
                continue
            
            # 检测检查项标题
            item_match = re.match(
                r'^###\s+(CORE|COMPLETE|OPTIMIZE)-(\d+):\s*(.+)',
                trimmed_line
            )
            if item_match:
                if current_item and current_category:
                    items.append(current_item)
                
                current_item = {
                    'id': f"{item_match.group(1)}-{item_match.group(2)}",
                    'code': item_match.group(1),
                    'number': int(item_match.group(2)),
                    'name': item_match.group(3).strip(),
                    'category': current_category['code'] if current_category else 'UNKNOWN',
                    'checkpoints': [],
                    'questions': [],
                    'criteria': {}
                }
                in_checkpoints = False
                in_questions = False
                in_criteria = False
                continue
            
            # 检测检查点部分
            if trimmed_line == '**检查点**:':
                in_checkpoints = True
                in_questions = False
                in_criteria = False
                continue
            
            # 检测检查问题部分
            if trimmed_line == '**检查问题**:':
                in_checkpoints = False
                in_questions = True
                in_criteria = False
                continue
            
            # 检测验收标准部分
            if trimmed_line == '**验收标准**:':
                in_checkpoints = False
                in_questions = False
                in_criteria = True
                continue
            
            # 解析检查点列表
            if in_checkpoints and trimmed_line.startswith('- [ ]'):
                checkpoint = trimmed_line.replace('- [ ]', '').strip()
                if current_item:
                    current_item['checkpoints'].append(checkpoint)
            
            # 解析检查问题列表
            if in_questions and re.match(r'^\d+\.', trimmed_line):
                question = re.sub(r'^\d+\.\s*', '', trimmed_line).rstrip('?')
                if current_item:
                    current_item['questions'].append(question)
            
            # 解析验收标准
            if in_criteria and trimmed_line.startswith('- '):
                criteria_text = trimmed_line.replace('- ', '').strip()
                criteria_match = re.match(r'^(.+?):\s*(.+)', criteria_text)
                if criteria_match and current_item:
                    current_item['criteria'][criteria_match.group(1).strip()] = criteria_match.group(2).strip()
        
        # 添加最后一个检查项
        if current_item:
            items.append(current_item)
        
        return items
    
    def generate_python_file(self, items):
        """
        生成 Python 文件
        
        Args:
            items: 检查项列表
        """
        header = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRD 质量检查项数据

自动生成文件 - 请勿手动编辑
源文件：docs/checker.md
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
生成脚本：scripts/generate_check_items.py
"""

# 检查项数据
CHECK_ITEMS = {json.dumps(items, ensure_ascii=False, indent=2)}


def get_all_items():
    """获取所有检查项"""
    return CHECK_ITEMS


def get_items_by_category(category_code):
    """
    按类别获取检查项
    
    Args:
        category_code: 类别代码 (CORE, COMPLETE, OPTIMIZE)
    
    Returns:
        list: 检查项列表
    """
    return [item for item in CHECK_ITEMS if item['code'] == category_code]


def get_item_by_id(item_id):
    """
    按 ID 获取检查项
    
    Args:
        item_id: 检查项 ID (如：CORE-1)
    
    Returns:
        dict: 检查项详情，不存在则返回 None
    """
    for item in CHECK_ITEMS:
        if item['id'] == item_id:
            return item
    return None


def get_items_for_stage(stage):
    """
    按阶段获取检查项
    
    Args:
        stage: 阶段名称 (decomposition, prd_generation, quality_check, optimization)
    
    Returns:
        list: 检查项列表
    """
    stage_mapping = {{
        'decomposition': ['CORE'],
        'prd_generation': ['CORE', 'COMPLETE'],
        'quality_check': ['CORE', 'COMPLETE', 'OPTIMIZE'],
        'optimization': ['OPTIMIZE']
    }}
    
    allowed_codes = stage_mapping.get(stage, ['CORE', 'COMPLETE', 'OPTIMIZE'])
    return [item for item in CHECK_ITEMS if item['code'] in allowed_codes]


def generate_prompt(stage):
    """
    生成阶段提示词
    
    Args:
        stage: 阶段名称
    
    Returns:
        str: 提示词字符串
    """
    items = get_items_for_stage(stage)
    
    if not items:
        return ''
    
    stage_names = {{
        'decomposition': '需求分解阶段',
        'prd_generation': 'PRD 生成阶段',
        'quality_check': '质量检查阶段',
        'optimization': '优化建议阶段'
    }}
    
    prompt = f"## {{stage_names.get(stage, stage)}} - 质量检查项指导\\n\\n"
    prompt += f"请在{{stage_names.get(stage, stage)}}中，重点关注以下检查项：\\n\\n"
    
    # 按类别分组
    grouped = {{}}
    for item in items:
        code = item['code']
        if code not in grouped:
            grouped[code] = []
        grouped[code].append(item)
    
    category_names = {{
        'CORE': '🔴 核心检查项（必须满足）',
        'COMPLETE': '🟡 完善检查项（建议满足）',
        'OPTIMIZE': '🟢 优化检查项（可选满足）'
    }}
    
    for code in ['CORE', 'COMPLETE', 'OPTIMIZE']:
        if code not in grouped:
            continue
        
        prompt += f"### {{category_names.get(code, code)}}\\n\\n"
        
        for item in grouped[code]:
            prompt += f"#### {{item['id']}}: {{item['name']}}\\n\\n"
            
            if item['checkpoints']:
                prompt += '**检查点**:\\n'
                for cp in item['checkpoints']:
                    prompt += f"- {{cp}}\\n"
                prompt += '\\n'
            
            if item['questions']:
                prompt += '**关键问题**:\\n'
                for idx, q in enumerate(item['questions'], 1):
                    prompt += f"{{idx}}. {{q}}\\n"
                prompt += '\\n'
            
            if item['criteria']:
                prompt += '**验收标准**:\\n'
                for key, value in item['criteria'].items():
                    prompt += f"- {{key}}: {{value}}\\n"
                prompt += '\\n'
    
    prompt += "---\\n\\n"
    prompt += "**使用说明**:\\n"
    prompt += "- 核心检查项（CORE）必须 100% 满足，否则 PRD 质量不达标\\n"
    prompt += "- 完善检查项（COMPLETE）建议满足 80% 以上\\n"
    prompt += "- 优化检查项（OPTIMIZE）根据项目实际情况选择性满足\\n"
    
    return prompt


def get_stats():
    """
    获取检查项统计信息
    
    Returns:
        dict: 统计信息
    """
    stats = {{
        'total': len(CHECK_ITEMS),
        'by_category': {{}},
        'total_checkpoints': 0,
        'total_questions': 0
    }}
    
    for item in CHECK_ITEMS:
        code = item['code']
        if code not in stats['by_category']:
            stats['by_category'][code] = 0
        stats['by_category'][code] += 1
        stats['total_checkpoints'] += len(item['checkpoints'])
        stats['total_questions'] += len(item['questions'])
    
    return stats


if __name__ == '__main__':
    # 测试代码
    print("PRD 质量检查项数据")
    print("=" * 50)
    
    stats = get_stats()
    print(f"总检查项数：{{stats['total']}}")
    print(f"按类别统计：{{stats['by_category']}}")
    print(f"总检查点数：{{stats['total_checkpoints']}}")
    print(f"总问题数：{{stats['total_questions']}}")
    
    print("\\n示例：CORE-1 详情")
    item = get_item_by_id('CORE-1')
    if item:
        print(f"名称：{{item['name']}}")
        print(f"检查点数：{{len(item['checkpoints'])}}")
        print(f"问题数：{{len(item['questions'])}}")
'''
        
        # 确保输出目录存在
        self.output_py_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 写入文件
        with open(self.output_py_path, 'w', encoding='utf-8') as f:
            f.write(header)
        
        print(f"✓ 已生成：{self.output_py_path}")
    
    def run(self):
        """执行生成流程"""
        print(f"开始生成检查项数据...")
        print(f"源文件：{self.checker_md_path}")
        print(f"目标文件：{self.output_py_path}")
        print()
        
        # 解析 checker.md
        items = self.parse_checker_md()
        print(f"✓ 解析完成：共 {len(items)} 个检查项")
        
        # 生成 Python 文件
        self.generate_python_file(items)
        
        # 验证生成结果
        stats = {
            'total': len(items),
            'by_category': {},
            'total_checkpoints': 0,
            'total_questions': 0
        }
        
        for item in items:
            code = item['code']
            if code not in stats['by_category']:
                stats['by_category'][code] = 0
            stats['by_category'][code] += 1
            stats['total_checkpoints'] += len(item['checkpoints'])
            stats['total_questions'] += len(item['questions'])
        
        print()
        print("生成统计:")
        print(f"  总检查项数：{stats['total']}")
        print(f"  按类别统计：{stats['by_category']}")
        print(f"  总检查点数：{stats['total_checkpoints']}")
        print(f"  总问题数：{stats['total_questions']}")
        print()
        print("✓ 生成完成!")


def main():
    """主函数"""
    # 确定基路径
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent  # 返回技能根目录
    
    generator = CheckItemsGenerator(base_path)
    generator.run()


if __name__ == '__main__':
    main()
