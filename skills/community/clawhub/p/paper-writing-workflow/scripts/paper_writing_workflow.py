#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paper Writing Workflow - 标准化论文写作工作流
"""

import os
import sys
import io
import json
from datetime import datetime

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TEMPLATES = {
    'scientific_data': {
        'journal': 'Scientific Data (Nature)',
        'word_limit': 3000,
        'figures': '5+',
        'tables': '2+'
    },
    'nature_communications': {
        'journal': 'Nature Communications',
        'word_limit': 5000,
        'figures': '6+',
        'tables': '2+'
    },
    'ieee_conference': {
        'journal': 'IEEE Conference',
        'word_limit': 4000,
        'pages': '6-8',
        'figures': '4+'
    },
    'pnas': {
        'journal': 'PNAS',
        'word_limit': 5000,
        'figures': '5+'
    }
}

STAGES = [
    {'name': '选题与假设', 'duration': '10-20 分钟'},
    {'name': '文献搜索与综述', 'duration': '30-60 分钟'},
    {'name': '论文大纲设计', 'duration': '15-30 分钟'},
    {'name': '初稿写作', 'duration': '60-120 分钟'},
    {'name': '图表生成', 'duration': '30-60 分钟'},
    {'name': '润色与格式检查', 'duration': '30-60 分钟'}
]

def print_stage(stage_num, stage_info):
    """打印阶段信息"""
    print(f"\n阶段 {stage_num}: {stage_info['name']} ({stage_info['duration']})")

def generate_outline(topic, template):
    """生成论文大纲"""
    outline = []
    outline.append(f"# {topic}")
    outline.append("")
    outline.append("## Abstract")
    outline.append("- 背景（1-2 句）")
    outline.append("- 方法（1-2 句）")
    outline.append("- 结果（2-3 句）")
    outline.append("- 结论（1 句）")
    outline.append("")
    outline.append("## Introduction")
    outline.append("- 研究背景")
    outline.append("- 文献综述")
    outline.append("- 研究空白")
    outline.append("- 研究问题")
    outline.append("- 研究假设")
    outline.append("")
    outline.append("## Methods")
    outline.append("- 研究设计")
    outline.append("- 参与者")
    outline.append("- 材料")
    outline.append("- 程序")
    outline.append("- 数据分析")
    outline.append("")
    outline.append("## Results")
    outline.append("- 描述统计")
    outline.append("- 推断统计")
    outline.append("- 图表展示")
    outline.append("")
    outline.append("## Discussion")
    outline.append("- 主要发现")
    outline.append("- 与现有研究对比")
    outline.append("- 理论贡献")
    outline.append("- 实践意义")
    outline.append("- 局限性")
    outline.append("- 未来方向")
    outline.append("")
    outline.append("## Conclusion")
    outline.append("- 总结")
    outline.append("- 建议")
    outline.append("")
    outline.append("## References")
    outline.append("- 参考文献列表（30-50 篇）")
    
    return "\n".join(outline)

def paper_writing_workflow(topic, template='scientific_data', action='generate'):
    """论文写作工作流"""
    print(f"📝 开始论文写作：{topic}")
    print(f"模板：{template}")
    print(f"期刊：{TEMPLATES.get(template, {}).get('journal', 'Unknown')}")
    
    # 显示 6 个阶段
    print("\n" + "="*60)
    print("论文写作工作流 - 6 个阶段")
    print("="*60)
    for i, stage in enumerate(STAGES, 1):
        print_stage(i, stage)
    
    # 总时间估算
    total_time = "3-6 小时"
    print(f"\n预计总时间：{total_time}")
    print("="*60)
    
    if action == 'outline':
        # 生成大纲
        print("\n阶段 3: 生成论文大纲...")
        outline = generate_outline(topic, template)
        
        # 保存大纲
        filename = f"paper_outline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(outline)
        
        print(f"\n✅ 论文大纲已生成！")
        print(f"📁 文件已保存：{filename}")
        
        return outline
    
    elif action == 'polish':
        # 润色模式
        print("\n阶段 6: 润色与格式检查...")
        print("请使用 academic-writing 技能进行润色")
        print("命令：python academic_writing.py --action polish --input draft.md")
        
    else:
        # 完整工作流
        print("\n建议执行步骤：")
        print("1. 阶段 1-2: 使用 literature-search-workflow 搜索文献")
        print("2. 阶段 3: 使用 --action outline 生成大纲")
        print("3. 阶段 4: 使用 research-paper-writer 生成初稿")
        print("4. 阶段 5: 使用 scientific-schematics 生成图表")
        print("5. 阶段 6: 使用 academic-writing 润色")
    
    return None

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "AI 心理学研究"
    template = sys.argv[2] if len(sys.argv) > 2 else "scientific_data"
    action = sys.argv[3] if len(sys.argv) > 3 else "generate"
    
    paper_writing_workflow(topic, template, action)
