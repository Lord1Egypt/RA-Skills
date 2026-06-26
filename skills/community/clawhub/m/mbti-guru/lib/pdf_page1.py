#!/usr/bin/env python3
"""
MBTI PDF Report Generator - Page 1 (Original v1.0.3 Layout)
保持原有版式不变
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import os

plt.rcParams['font.family'] = 'Noto Sans CJK JP'
plt.rcParams['axes.unicode_minus'] = False

def create_pdf_page1(type_code: str, scores: dict, clarity_levels: dict, output_path: str = "mbti_page1.pdf"):
    from lib.mbti_types import get_type
    
    type_data = get_type(type_code)
    name_en = type_data.get("name_en", "")
    name_cn = type_data.get("name_cn", "")
    summary = type_data.get("summary", "")
    summary_cn = type_data.get("summary_cn", "")
    strengths = type_data.get("strengths", [])
    weaknesses = type_data.get("weaknesses", [])
    careers = type_data.get("careers", [])
    relationships = type_data.get("relationships", {})
    
    total_clarity = sum(c[0] for c in clarity_levels.values()) / len(clarity_levels)
    
    PRIMARY = '#4A90D9'
    SECONDARY = '#2C3E50'
    ACCENT = '#E74C3C'
    LIGHT_BG = '#F8F9FA'
    GREEN = '#27AE60'
    PURPLE = '#8E44AD'
    
    fig, ax = plt.subplots(1, 1, figsize=(8.27, 11.69))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    
    y = 0.98
    left = 0.08
    right = 0.92
    content_width = right - left
    
    # Header
    ax.text(0.5, y, 'MBTI PERSONALITY REPORT', fontsize=18, fontweight='bold', color=PRIMARY, ha='center', va='top')
    y -= 0.026
    
    ax.plot([left, right], [y, y], color=PRIMARY, linewidth=2)
    y -= 0.022
    
    # Type Badge - LARGER
    badge_w = 0.26
    badge_h = 0.08
    ax.add_patch(FancyBboxPatch(((1-badge_w)/2, y-badge_h), badge_w, badge_h,
                                  boxstyle="round,pad=0.012,rounding_size=0.02", 
                                  facecolor=PRIMARY, edgecolor='none'))
    ax.text(0.5, y-badge_h/2, f'{type_code}', fontsize=46, fontweight='bold', color='white', ha='center', va='center')
    y -= (badge_h + 0.02)
    
    # Type names
    ax.text(0.5, y, f'{name_en}  |  {name_cn}', fontsize=18, fontweight='bold', color=SECONDARY, ha='center', va='top')
    y -= 0.038
    
    # Clarity box - LARGER
    ax.add_patch(FancyBboxPatch((0.28, y-0.028), 0.44, 0.028,
                                  boxstyle="round,pad=0.005,rounding_size=0.006", 
                                  facecolor=LIGHT_BG, edgecolor=PRIMARY, linewidth=2))
    ax.text(0.5, y-0.014, f'综合清晰度 / Overall Clarity: {total_clarity:.0f}%',
            fontsize=13, fontweight='bold', color=PRIMARY, ha='center', va='center')
    y -= 0.05
    
    # Dimension Scores
    ax.text(left, y, '维度得分 / Dimension Scores', fontsize=12, fontweight='bold', color=PRIMARY, va='top')
    y -= 0.024
    
    dim_cn_labels = {"EI": "能量 Energy", "SN": "信息 Info", "TF": "决策 Decisions", "JP": "结构 Structure"}
    
    bar_height = 0.024
    bar_x = left + 0.08
    bar_width = 0.48
    right_label_x = bar_x + bar_width + 0.015
    
    for dim, score in scores.items():
        pref = dim[0] if score > 50 else dim[1]
        
        ax.add_patch(FancyBboxPatch((bar_x, y-bar_height), bar_width, bar_height,
                                    boxstyle="round,pad=0.002,rounding_size=0.005",
                                    facecolor='#E8E8E8', edgecolor='none'))
        
        fill_width = bar_width * score / 100
        if fill_width > 0.005:
            ax.add_patch(FancyBboxPatch((bar_x, y-bar_height), fill_width, bar_height,
                                        boxstyle="round,pad=0.002,rounding_size=0.005",
                                        facecolor=PRIMARY, edgecolor='none', alpha=0.85))
        
        ax.text(bar_x + 0.012, y-bar_height/2, f'{dim}',
                fontsize=13, fontweight='bold', color='black', va='center')
        
        ax.text(bar_x + bar_width - 0.012, y-bar_height/2, f'{score:.0f}% {pref}',
                fontsize=13, fontweight='bold', color=PRIMARY, va='center', ha='right')
        
        ax.text(right_label_x, y-bar_height/2, dim_cn_labels.get(dim, ""),
                fontsize=10, fontweight='bold', color='#555', va='center', ha='left')
        
        y -= (bar_height + 0.018)
    
    y -= 0.004
    
    # Summary
    ax.text(left, y, '简介 / Summary', fontsize=12, fontweight='bold', color=PRIMARY, va='top')
    y -= 0.024
    ax.text(left+0.01, y, summary[:65], fontsize=12, color=SECONDARY, va='top', style='italic')
    y -= 0.02
    ax.text(left+0.01, y, summary_cn, fontsize=12, color=SECONDARY, va='top')
    y -= 0.04
    
    # Two columns - Strengths & Weaknesses
    col_width = (content_width - 0.06) / 2
    
    ax.text(left, y, '优势 Strengths', fontsize=12, fontweight='bold', color=GREEN, va='top')
    temp_y = y - 0.024
    for i, s in enumerate(strengths[:4], 1):
        en = s.split("/")[0].strip()
        cn = s.split("/")[1].strip() if "/" in s else ""
        ax.text(left+0.01, temp_y, f'{i}. {en}', fontsize=12, fontweight='bold', color=SECONDARY, va='top')
        temp_y -= 0.02
        ax.text(left+0.04, temp_y, cn, fontsize=11, color='#555', va='top')
        temp_y -= 0.024
    
    ax.text(left+col_width+0.02, y, '劣势 Weaknesses', fontsize=12, fontweight='bold', color=ACCENT, va='top')
    temp_y2 = y - 0.024
    for i, w in enumerate(weaknesses[:4], 1):
        en = w.split("/")[0].strip()
        cn = w.split("/")[1].strip() if "/" in w else ""
        ax.text(left+col_width+0.03, temp_y2, f'{i}. {en}', fontsize=12, fontweight='bold', color=SECONDARY, va='top')
        temp_y2 -= 0.02
        ax.text(left+col_width+0.06, temp_y2, cn, fontsize=11, color='#555', va='top')
        temp_y2 -= 0.024
    
    y = min(temp_y, temp_y2) - 0.028
    
    ax.text(left, y, '适合职业 / Careers', fontsize=12, fontweight='bold', color=PURPLE, va='top')
    y -= 0.024
    
    careers_en = [c.split("/")[0].strip() for c in careers[:4]]
    careers_cn = [c.split("/")[1].strip() if "/" in c else "" for c in careers[:4]]
    
    for i in range(4):
        ax.text(left+0.01, y, f'{i+1}. {careers_en[i]}  {careers_cn[i]}',
                fontsize=12, fontweight='bold', color=SECONDARY, va='top')
        y -= 0.024
    
    y -= 0.008
    
    ax.text(left, y, '人际关系 / Relationships', fontsize=12, fontweight='bold', color=PRIMARY, va='top')
    y -= 0.024
    
    best = relationships.get("best", [])
    challenging = relationships.get("challenging", [])
    
    ax.text(left+0.01, y, f'最佳匹配 Best Match:  {", ".join(best)}',
            fontsize=12, fontweight='bold', color=SECONDARY, va='top')
    y -= 0.022
    
    ax.text(left+0.01, y, f'挑战类型 Challenging:  {", ".join(challenging)}',
            fontsize=12, fontweight='bold', color=SECONDARY, va='top')
    
    # Footer
    ax.plot([left, right], [0.045, 0.045], color='#CCC', linewidth=0.8)
    ax.text(0.5, 0.03, 'Generated by MBTI Guru', fontsize=8, color='#AAA', ha='center', va='top')
    
    plt.tight_layout()
    fig.savefig(output_path, format='pdf', dpi=150, facecolor='white')
    plt.close()
    
    return output_path
