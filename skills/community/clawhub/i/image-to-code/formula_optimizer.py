#!/usr/bin/env python3
"""
公式格式优化器
将 OCR 识别的公式转换为标准 LaTeX 格式
"""

import re

def optimize_formula(text):
    """
    优化公式格式
    
    Args:
        text: OCR 识别的原始公式
        
    Returns:
        优化后的 LaTeX 公式
    """
    formula = text
    
    # 1. 下标优化：p1 → p_1, t2 → t_2
    # 匹配字母 + 数字的模式
    formula = re.sub(r'([a-zA-Z])([0-9]+)', r'\1_\2', formula)
    
    # 2. 乘号优化：在括号前添加 \times
    # F,NP → F_t \times N_p
    formula = re.sub(r'F,([A-Z])', r'F_t\\times\1', formula)
    
    # 3. △p → △p（保持原样，不转 LaTeX）
    # 如果需要 LaTeX 格式，可以改为 \Delta p
    
    # 4. 括号转义
    formula = formula.replace('(', '\\(')
    formula = formula.replace(')', '\\)')
    
    return formula

# 测试
test_cases = [
    "Σ△p1=(△p1+△P2)F,NP",
    "u=A3600×994×0.0311=0.74m/s",
    "∑△p1=(2780+820)×1.4×2=10080Pa",
]

print("公式优化测试:")
print("=" * 60)
for test in test_cases:
    optimized = optimize_formula(test)
    print(f"原始：{test}")
    print(f"优化：{optimized}")
    print()
