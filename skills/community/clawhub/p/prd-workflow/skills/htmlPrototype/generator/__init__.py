#!/usr/bin/env python3
"""HTML 生成器"""

from .templates import get_template

def generate_html(page_type: str, keywords: list = None) -> str:
    """
    生成 HTML 原型
    
    Args:
        page_type: 页面类型 (list/form/dashboard/detail/login)
        keywords: 关键词列表
    
    Returns:
        HTML 字符串
    """
    template = get_template(page_type)
    
    # 根据关键词定制内容
    if keywords:
        html = template
        
        # 替换标题
        if '产品' in keywords:
            html = html.replace('管理系统', '产品管理系统')
            html = html.replace('列表', '产品列表')
        elif '用户' in keywords:
            html = html.replace('管理系统', '用户管理系统')
            html = html.replace('列表', '用户列表')
        elif '订单' in keywords:
            html = html.replace('管理系统', '订单管理系统')
            html = html.replace('列表', '订单列表')
        elif '电商' in keywords:
            html = html.replace('管理系统', '电商管理')
        
        return html
    
    return template
