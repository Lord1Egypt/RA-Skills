#!/usr/bin/env python3
"""
MBTI PDF Report Generator - Page 2 (Deep Analysis)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import os

plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

def create_pdf_page2(type_code: str, output_path: str = "mbti_page2.pdf"):
    from lib.mbti_types import get_type
    from lib.cognitive import get_cognitive_functions
    from lib.relationships import get_relationship_data
    
    type_data = get_type(type_code)
    name_en = type_data.get("name_en", "")
    name_cn = type_data.get("name_cn", "")
    
    cognitive = get_cognitive_functions(type_code)
    rel_data = get_relationship_data(type_code)
    
    PRIMARY = '#4A90D9'
    SECONDARY = '#2C3E50'
    ACCENT = '#E74C3C'
    LIGHT_BG = '#F8F9FA'
    GREEN = '#27AE60'
    PURPLE = '#8E44AD'
    ORANGE = '#E67E22'
    
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 11.69))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    
    y = 0.97
    left = 0.08
    right = 0.92
    content_width = right - left
    footer_y = 0.045
    
    # Header
    ax.text(0.5, y, f'{name_en}  |  {name_cn}', fontsize=22, fontweight='bold', color=PRIMARY, ha='center', va='top')
    y -= 0.034
    
    ax.text(0.5, y, 'Deep Analysis / 深度分析报告', fontsize=17, fontweight='bold', color=SECONDARY, ha='center', va='top')
    y -= 0.032
    
    ax.plot([left, right], [y, y], color=PRIMARY, linewidth=2)
    y -= 0.018
    
    # 认知功能
    ax.text(left, y, 'Cognitive Functions / 认知功能', fontsize=16, fontweight='bold', color=PRIMARY, va='top')
    y -= 0.036
    
    if cognitive:
        funcs = cognitive.get("functions", {})
        
        func_data = [
            ("dominant", "Dominant / 主功能", GREEN),
            ("auxiliary", "Auxiliary / 辅助功能", PRIMARY),
            ("tertiary", "Tertiary / 第三功能", ORANGE),
            ("inferior", "Inferior / 劣势功能", ACCENT),
        ]
        
        box_width = (content_width - 0.04) / 2
        box_height = 0.085
        
        # Row 1
        row1_y = y
        for i, (key, label, color) in enumerate(func_data[:2]):
            func = funcs.get(key, {})
            name = func.get("name", "")
            desc = func.get("description", "")
            
            box_x = left + i * (box_width + 0.04)
            box_y = row1_y - box_height
            
            ax.add_patch(FancyBboxPatch((box_x, box_y), box_width, box_height,
                                          boxstyle="round,pad=0.005,rounding_size=0.01",
                                          facecolor=LIGHT_BG, edgecolor=color, linewidth=2))
            
            ax.text(box_x + 0.015, box_y + box_height - 0.015, f'{label}', 
                    fontsize=16, fontweight='bold', color=color, va='top')
            ax.text(box_x + 0.015, box_y + box_height - 0.04, f'{name}', 
                    fontsize=15, fontweight='bold', color=SECONDARY, va='top')
            ax.text(box_x + 0.015, box_y + box_height - 0.062, desc, 
                    fontsize=13, color='#555', va='top')
        
        # Row 2
        row2_y = row1_y - box_height - 0.018
        for i, (key, label, color) in enumerate(func_data[2:]):
            func = funcs.get(key, {})
            name = func.get("name", "")
            desc = func.get("description", "")
            
            box_x = left + i * (box_width + 0.04)
            box_y = row2_y - box_height
            
            ax.add_patch(FancyBboxPatch((box_x, box_y), box_width, box_height,
                                          boxstyle="round,pad=0.005,rounding_size=0.01",
                                          facecolor=LIGHT_BG, edgecolor=color, linewidth=2))
            
            ax.text(box_x + 0.015, box_y + box_height - 0.015, f'{label}', 
                    fontsize=16, fontweight='bold', color=color, va='top')
            ax.text(box_x + 0.015, box_y + box_height - 0.04, f'{name}', 
                    fontsize=15, fontweight='bold', color=SECONDARY, va='top')
            ax.text(box_x + 0.015, box_y + box_height - 0.062, desc, 
                    fontsize=13, color='#555', va='top')
        
        y = row2_y - box_height - 0.028
    
    # 成长建议 - 内容13pt
    ax.text(left, y, 'Growth Suggestions / 成长建议', fontsize=16, fontweight='bold', color=PRIMARY, va='top')
    y -= 0.032
    
    if cognitive and cognitive.get("growth"):
        for i, tip in enumerate(cognitive["growth"], 1):
            ax.text(left + 0.015, y, f'{i}. {tip}', fontsize=13, color=SECONDARY, va='top')
            y -= 0.026
        y -= 0.015
    
    # 职场 - 内容13pt（与成长建议一致）
    ax.text(left, y, 'Workplace / 职场', fontsize=16, fontweight='bold', color=GREEN, va='top')
    y -= 0.032
    
    workplace = rel_data.get("workplace", {})
    if workplace:
        best_env = workplace.get("best_environment", "")
        team_role = workplace.get("team_role", "")
        tips = workplace.get("collaboration_tips", [])
        
        ax.text(left + 0.015, y, f'Best Environment / 最佳环境:', fontsize=13, fontweight='bold', color=SECONDARY, va='top')
        y -= 0.022
        ax.text(left + 0.015, y, best_env, fontsize=13, color='#555', va='top')
        y -= 0.024
        
        ax.text(left + 0.015, y, f'Team Role / 团队角色:', fontsize=13, fontweight='bold', color=SECONDARY, va='top')
        y -= 0.022
        ax.text(left + 0.015, y, team_role, fontsize=13, color='#555', va='top')
        y -= 0.026
        
        if tips:
            ax.text(left + 0.015, y, f'Collaboration / 协作建议:', fontsize=13, fontweight='bold', color=SECONDARY, va='top')
            y -= 0.022
            for tip in tips[:2]:
                ax.text(left + 0.03, y, f'- {tip}', fontsize=13, color='#666', va='top')
                y -= 0.02
        y -= 0.015
    
    # 情感 - 内容13pt（与成长建议一致）
    ax.text(left, y, 'Romantic / 情感', fontsize=16, fontweight='bold', color=PURPLE, va='top')
    y -= 0.032
    
    romantic = rel_data.get("romantic", {})
    if romantic:
        best_matches = romantic.get("best_match", [])
        challenging = romantic.get("challenging", [])
        rel_tips = romantic.get("relationship_tips", [])
        
        ax.text(left + 0.015, y, f'Best Match / 最佳匹配:', fontsize=13, fontweight='bold', color=SECONDARY, va='top')
        y -= 0.022
        ax.text(left + 0.015, y, ', '.join(best_matches), fontsize=13, color='#555', va='top')
        y -= 0.026
        
        ax.text(left + 0.015, y, f'Challenging / 挑战类型:', fontsize=13, fontweight='bold', color=SECONDARY, va='top')
        y -= 0.022
        ax.text(left + 0.015, y, ', '.join(challenging), fontsize=13, color='#555', va='top')
        y -= 0.026
        
        if rel_tips:
            ax.text(left + 0.015, y, f'Reationship Tips / 关系建议:', fontsize=13, fontweight='bold', color=SECONDARY, va='top')
            y -= 0.022
            for tip in rel_tips[:2]:
                ax.text(left + 0.03, y, f'- {tip}', fontsize=13, color='#666', va='top')
                y -= 0.02
    
    # Footer
    ax.plot([left, right], [footer_y, footer_y], color='#CCC', linewidth=0.8)
    ax.text(0.5, footer_y - 0.015, 'Generated by MBTI Guru', fontsize=8, color='#AAA', ha='center', va='top')
    
    plt.tight_layout()
    fig.savefig(output_path, format='pdf', dpi=150, facecolor='white')
    plt.close()
    
    return output_path
