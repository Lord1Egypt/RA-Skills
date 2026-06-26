#!/usr/bin/env python3
"""
HTML 模板库 v2.0

支持：
- 8 种页面模板
- 完整设计系统注入
- 效果系统、无障碍、反模式检查
"""

import re


# ============================================================
# 设计系统应用函数
# ============================================================

def apply_design_tokens(html: str, tokens: dict) -> str:
    """
    将完整设计系统 tokens 注入到 HTML 模板中

    Args:
        html: 原始 HTML 模板
        tokens: 设计系统字典，包含 colors, typography, spacing, effects 等

    Returns:
        应用设计系统后的 HTML
    """
    if not tokens:
        return html

    # 1. 应用颜色系统
    html = apply_colors(html, tokens.get('colors', {}))

    # 2. 应用字体系统
    html = apply_typography(html, tokens.get('typography', {}))

    # 3. 应用间距系统
    html = apply_spacing(html, tokens.get('spacing', {}))

    # 4. 应用效果系统
    html = apply_effects(html, tokens.get('effects', {}))

    # 5. 应用圆角系统
    html = apply_border_radius(html, tokens.get('borderRadius', {}))

    # 6. 应用阴影系统
    html = apply_shadows(html, tokens.get('shadows', {}))

    # 7. 移除反模式
    html = remove_anti_patterns(html, tokens.get('antiPatterns', []))

    # 8. 添加无障碍支持
    html = ensure_accessibility(html, tokens)

    return html


def apply_colors(html: str, colors: dict) -> str:
    """应用完整颜色系统"""
    primary = colors.get('primary', '#667eea')
    secondary = colors.get('secondary', '#764ba2')
    cta = colors.get('cta', '#F97316')
    background = colors.get('background', '#FFFFFF')
    text = colors.get('text', '#1E293B')
    success = colors.get('success', '#52C41A')
    warning = colors.get('warning', '#FAAD14')
    error = colors.get('error', '#F5222D')
    muted = colors.get('muted', '#6B7280')
    border = colors.get('border', '#E5E7EB')

    # 替换主色和辅助色
    html = html.replace('#667eea', primary.lower() if primary.startswith('#') else primary)
    html = html.replace('#667EEA', primary.upper() if primary.startswith('#') else primary)
    html = html.replace('#764ba2', secondary.lower() if secondary.startswith('#') else secondary)
    html = html.replace('#764BA2', secondary.upper() if secondary.startswith('#') else secondary)

    # 替换渐变
    html = html.replace(
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        f'linear-gradient(135deg, {primary} 0%, {secondary} 100%)'
    )
    html = html.replace(
        'linear-gradient(135deg, #667EEA 0%, #764BA2 100%)',
        f'linear-gradient(135deg, {primary} 0%, {secondary} 100%)'
    )

    # 替换背景色
    html = html.replace('background: #f5f5f5', f'background: {background}')
    html = html.replace('background: #F5F5F5', f'background: {background}')

    # 替换文字颜色
    html = html.replace('color: #333', f'color: {text}')
    html = html.replace('color: #666', f'color: {muted}')

    # 替换状态色
    html = html.replace('#52C41A', success)
    html = html.replace('#28a745', success)
    html = html.replace('#FAAD14', warning)
    html = html.replace('#ffc107', warning)
    html = html.replace('#F5222D', error)
    html = html.replace('#dc3545', error)

    # 替换边框色
    html = html.replace('border: 1px solid #ddd', f'border: 1px solid {border}')
    html = html.replace('border: 1px solid #eee', f'border: 1px solid {border}')

    return html


def apply_typography(html: str, typography: dict) -> str:
    """应用字体系统"""
    font_family = typography.get('fontFamily', 'system-ui, -apple-system, sans-serif')
    font_size = typography.get('fontSize', 14)

    # 替换字体
    default_fonts = [
        '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        'system-ui, -apple-system, sans-serif',
    ]
    for default_font in default_fonts:
        html = html.replace(default_font, font_family)

    return html


def apply_spacing(html: str, spacing: dict) -> str:
    """应用间距系统"""
    unit = spacing.get('unit', 8)

    # 可以根据需要添加更多间距替换逻辑
    return html


def apply_effects(html: str, effects: dict) -> str:
    """应用效果系统"""
    transition = effects.get('transition', 'all 200ms ease')

    # 确保 transition 存在
    if 'transition:' not in html and 'transition-' not in html:
        # 在 </style> 前添加全局 transition
        html = html.replace('</style>', f'''
    /* 效果系统 */
    * {{ transition: {transition}; }}
    .btn:hover {{ transform: translateY(-1px); }}
    .card:hover {{ transform: translateY(-2px); }}
</style>''')

    return html


def apply_border_radius(html: str, borderRadius: dict) -> str:
    """应用圆角系统"""
    # 可以根据需要添加圆角替换逻辑
    return html


def apply_shadows(html: str, shadows: dict) -> str:
    """应用阴影系统"""
    # 可以根据需要添加阴影替换逻辑
    return html


def remove_anti_patterns(html: str, anti_patterns: list) -> str:
    """
    移除反模式

    反模式包括：
    - no-emoji-icons: 禁止用 emoji 做图标
    - cursor-pointer-required: 所有可点击元素必须 cursor: pointer
    """
    if 'no-emoji-icons' in anti_patterns:
        # 将 emoji 替换为 SVG 图标占位符
        # 这里只是标记，实际需要更复杂的处理
        pass

    if 'cursor-pointer-required' in anti_patterns:
        # 确保所有 .btn 和 .action-link 有 cursor: pointer
        if '.btn {' in html and 'cursor: pointer' not in html.split('.btn {')[1].split('}')[0]:
            html = html.replace('.btn {', '.btn {\n        cursor: pointer;')

        if '.action-link {' in html and 'cursor: pointer' not in html.split('.action-link {')[1].split('}')[0]:
            html = html.replace('.action-link {', '.action-link {\n        cursor: pointer;')

    return html


def ensure_accessibility(html: str, tokens: dict) -> str:
    """确保无障碍支持"""
    colors = tokens.get('colors', {})
    primary = colors.get('primary', '#667eea')

    # 添加 focus 状态
    focus_style = f'''
    /* 无障碍：焦点状态 */
    :focus {{
        outline: 2px solid {primary};
        outline-offset: 2px;
    }}
    .btn:focus, .filter-input:focus, .form-input:focus {{
        outline: 2px solid {primary};
        outline-offset: 2px;
    }}
    @media (prefers-reduced-motion: reduce) {{
        * {{
            transition: none !important;
            animation: none !important;
        }}
    }}
'''

    if ':focus {' not in html:
        html = html.replace('</style>', focus_style + '</style>')

    return html


# ============================================================
# 页面模板
# ============================================================

# 列表页模板
LIST_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>产品管理系统 - 产品列表</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; color: #333; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; height: 60px; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .header-logo { font-size: 20px; font-weight: 600; }
        .header-user { display: flex; align-items: center; gap: 8px; font-size: 14px; cursor: pointer; }
        .container { display: flex; min-height: calc(100vh - 60px); }
        .sidebar { width: 220px; background: white; box-shadow: 1px 0 8px rgba(0,0,0,0.05); padding: 20px 0; }
        .menu-item { display: flex; align-items: center; gap: 12px; padding: 14px 24px; color: #333; text-decoration: none; border-left: 3px solid transparent; transition: all 200ms ease; cursor: pointer; }
        .menu-item:hover { background: #f5f5f5; }
        .menu-item.active { background: #f0f4ff; border-left-color: #667eea; color: #667eea; }
        .main { flex: 1; padding: 24px; }
        .page-title { font-size: 24px; font-weight: 600; color: #333; margin-bottom: 24px; }
        .filter-section { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
        .filter-row { display: flex; gap: 16px; margin-bottom: 16px; flex-wrap: wrap; }
        .filter-item { display: flex; flex-direction: column; gap: 6px; }
        .filter-label { font-size: 13px; color: #666; }
        .filter-input { padding: 10px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; width: 200px; cursor: pointer; }
        .filter-input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.15); }
        .btn { padding: 10px 20px; border-radius: 6px; font-size: 14px; cursor: pointer; border: none; transition: all 200ms ease; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }
        .btn-secondary { background: white; color: #666; border: 1px solid #ddd; }
        .btn-secondary:hover { background: #f5f5f5; }
        .btn-cta { background: #F97316; color: white; }
        .btn-cta:hover { background: #EA580C; }
        .action-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 12px; }
        .table-container { background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
        .table-responsive { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; min-width: 600px; }
        thead { background: #f8f9fa; }
        th { padding: 14px 16px; text-align: left; font-size: 13px; font-weight: 600; color: #666; border-bottom: 1px solid #eee; white-space: nowrap; }
        td { padding: 14px 16px; font-size: 14px; color: #333; border-bottom: 1px solid #eee; }
        tbody tr:hover { background: #f8f9fa; }
        .status-badge { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 500; }
        .status-success { background: #d4edda; color: #155724; }
        .status-warning { background: #fff3cd; color: #856404; }
        .status-danger { background: #f8d7da; color: #721c24; }
        .action-link { color: #667eea; text-decoration: none; margin-right: 12px; cursor: pointer; transition: color 150ms; }
        .action-link:hover { text-decoration: underline; color: #5a67d8; }
        .action-link.delete { color: #dc3545; }
        .action-link.delete:hover { color: #c82333; }
        .pagination { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; background: white; border-top: 1px solid #eee; flex-wrap: wrap; gap: 12px; }
        .pagination-info { color: #666; font-size: 14px; }
        .pagination-btns { display: flex; gap: 8px; flex-wrap: wrap; }
        .page-btn { padding: 6px 12px; border: 1px solid #ddd; background: white; border-radius: 4px; cursor: pointer; font-size: 14px; transition: all 150ms; }
        .page-btn.active { background: #667eea; color: white; border-color: #667eea; }
        .page-btn:hover:not(.active) { background: #f5f5f5; border-color: #667eea; }
        @media (max-width: 768px) {
            .sidebar { display: none; }
            .filter-input { width: 100%; }
            .filter-row { flex-direction: column; }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-logo">产品管理系统</div>
        <div class="header-user"><span>管理员</span><span>▼</span></div>
    </header>
    <div class="container">
        <aside class="sidebar">
            <a href="#" class="menu-item active"><span>产品列表</span></a>
            <a href="#" class="menu-item"><span>订单管理</span></a>
            <a href="#" class="menu-item"><span>用户管理</span></a>
            <a href="#" class="menu-item"><span>数据统计</span></a>
            <a href="#" class="menu-item"><span>系统设置</span></a>
        </aside>
        <main class="main">
            <h1 class="page-title">产品列表</h1>
            <div class="filter-section">
                <div class="filter-row">
                    <div class="filter-item"><label class="filter-label">产品名称</label><input type="text" class="filter-input" placeholder="请输入产品名称"></div>
                    <div class="filter-item"><label class="filter-label">产品状态</label><select class="filter-input"><option>全部状态</option><option>上架中</option><option>已下架</option></select></div>
                    <div class="filter-item"><label class="filter-label">创建时间</label><input type="date" class="filter-input"></div>
                </div>
                <div class="filter-row"><button class="btn btn-primary">查询</button><button class="btn btn-secondary">重置</button></div>
            </div>
            <div class="action-bar">
                <div><button class="btn btn-primary">+ 新建产品</button><button class="btn btn-secondary">导出</button><button class="btn btn-secondary">批量删除</button></div>
            </div>
            <div class="table-container">
                <div class="table-responsive">
                    <table>
                        <thead><tr><th width="40"><input type="checkbox"></th><th>产品名称</th><th>价格</th><th>库存</th><th>状态</th><th>创建时间</th><th>操作</th></tr></thead>
                        <tbody>
                            <tr><td><input type="checkbox"></td><td>无线蓝牙耳机 Pro</td><td>¥299.00</td><td>1,234</td><td><span class="status-badge status-success">上架中</span></td><td>2026-02-20</td><td><a class="action-link">编辑</a><a class="action-link delete">删除</a></td></tr>
                            <tr><td><input type="checkbox"></td><td>智能手环运动版</td><td>¥199.00</td><td>856</td><td><span class="status-badge status-success">上架中</span></td><td>2026-02-19</td><td><a class="action-link">编辑</a><a class="action-link delete">删除</a></td></tr>
                            <tr><td><input type="checkbox"></td><td>便携式充电宝</td><td>¥149.00</td><td>2,341</td><td><span class="status-badge status-success">上架中</span></td><td>2026-02-18</td><td><a class="action-link">编辑</a><a class="action-link delete">删除</a></td></tr>
                            <tr><td><input type="checkbox"></td><td>机械键盘 RGB</td><td>¥399.00</td><td>0</td><td><span class="status-badge status-danger">售罄</span></td><td>2026-02-17</td><td><a class="action-link">编辑</a><a class="action-link delete">删除</a></td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="pagination">
                    <div class="pagination-info">共 156 条记录</div>
                    <div class="pagination-btns"><button class="page-btn">&lt;</button><button class="page-btn active">1</button><button class="page-btn">2</button><button class="page-btn">3</button><button class="page-btn">&gt;</button></div>
                </div>
            </div>
        </main>
    </div>
</body>
</html>'''

# 表单页模板
FORM_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>表单页</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; height: 60px; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .header-logo { font-size: 20px; font-weight: 600; cursor: pointer; }
        .container { display: flex; min-height: calc(100vh - 60px); }
        .sidebar { width: 220px; background: white; box-shadow: 1px 0 8px rgba(0,0,0,0.05); padding: 20px 0; }
        .menu-item { display: flex; align-items: center; gap: 12px; padding: 14px 24px; color: #333; text-decoration: none; border-left: 3px solid transparent; cursor: pointer; transition: all 200ms; }
        .menu-item.active { background: #f0f4ff; border-left-color: #667eea; color: #667eea; }
        .main { flex: 1; padding: 24px; }
        .page-title { font-size: 24px; font-weight: 600; color: #333; margin-bottom: 24px; }
        .form-section { background: white; padding: 32px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); max-width: 800px; }
        .form-group { margin-bottom: 24px; }
        .form-label { display: block; margin-bottom: 8px; font-size: 14px; color: #333; font-weight: 500; }
        .form-label .required { color: #dc3545; margin-left: 4px; }
        .form-input { width: 100%; padding: 12px 16px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; transition: border-color 200ms, box-shadow 200ms; }
        .form-input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.15); }
        .form-textarea { min-height: 120px; resize: vertical; }
        .form-help { font-size: 12px; color: #666; margin-top: 6px; }
        .form-row { display: flex; gap: 16px; }
        .form-row .form-group { flex: 1; }
        .form-actions { display: flex; gap: 12px; margin-top: 32px; padding-top: 24px; border-top: 1px solid #eee; }
        .btn { padding: 12px 24px; border-radius: 6px; font-size: 14px; cursor: pointer; border: none; transition: all 200ms; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }
        .btn-secondary { background: white; color: #666; border: 1px solid #ddd; }
        .btn-secondary:hover { background: #f5f5f5; }
        @media (max-width: 768px) {
            .sidebar { display: none; }
            .form-row { flex-direction: column; }
        }
    </style>
</head>
<body>
    <header class="header"><div class="header-logo">管理系统</div></header>
    <div class="container">
        <aside class="sidebar">
            <a href="#" class="menu-item"><span>列表</span></a>
            <a href="#" class="menu-item active"><span>新建</span></a>
            <a href="#" class="menu-item"><span>设置</span></a>
        </aside>
        <main class="main">
            <h1 class="page-title">新建项目</h1>
            <div class="form-section">
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">名称 <span class="required">*</span></label>
                        <input type="text" class="form-input" placeholder="请输入名称" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">编码 <span class="required">*</span></label>
                        <input type="text" class="form-input" placeholder="请输入编码" required>
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">类型</label>
                    <select class="form-input">
                        <option>请选择类型</option>
                        <option>类型A</option>
                        <option>类型B</option>
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">数值</label>
                    <input type="number" class="form-input" placeholder="0">
                </div>
                <div class="form-group">
                    <label class="form-label">描述</label>
                    <textarea class="form-input form-textarea" placeholder="请输入描述..."></textarea>
                    <p class="form-help">最多 500 字</p>
                </div>
                <div class="form-actions">
                    <button class="btn btn-primary">保存</button>
                    <button class="btn btn-secondary">取消</button>
                </div>
            </div>
        </main>
    </div>
</body>
</html>'''

# 仪表盘模板
DASHBOARD_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据仪表盘</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; height: 60px; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        .header-logo { font-size: 20px; font-weight: 600; }
        .container { display: flex; min-height: calc(100vh - 60px); }
        .sidebar { width: 220px; background: white; box-shadow: 1px 0 8px rgba(0,0,0,0.05); padding: 20px 0; }
        .menu-item { display: flex; align-items: center; gap: 12px; padding: 14px 24px; color: #333; text-decoration: none; border-left: 3px solid transparent; cursor: pointer; transition: all 200ms; }
        .menu-item.active { background: #f0f4ff; border-left-color: #667eea; color: #667eea; }
        .main { flex: 1; padding: 24px; }
        .page-title { font-size: 24px; font-weight: 600; color: #333; margin-bottom: 24px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 24px; }
        .stat-card { background: white; padding: 24px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); transition: transform 200ms; cursor: pointer; }
        .stat-card:hover { transform: translateY(-2px); }
        .stat-label { font-size: 13px; color: #666; margin-bottom: 8px; }
        .stat-value { font-size: 32px; font-weight: 700; color: #333; margin-bottom: 8px; }
        .stat-change { font-size: 12px; font-weight: 500; }
        .stat-change.up { color: #52C41A; }
        .stat-change.down { color: #F5222D; }
        .charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 24px; }
        .chart-card { background: white; padding: 24px; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); min-height: 300px; }
        .chart-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; }
        .chart-placeholder { background: #f8f9fa; border-radius: 4px; height: 240px; display: flex; align-items: center; justify-content: center; color: #999; font-size: 14px; }
        .table-card { background: white; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); overflow: hidden; }
        .table-header { padding: 16px 20px; border-bottom: 1px solid #eee; }
        .table-title { font-size: 16px; font-weight: 600; }
        table { width: 100%; border-collapse: collapse; }
        thead { background: #f8f9fa; }
        th { padding: 12px 16px; text-align: left; font-size: 13px; font-weight: 600; color: #666; }
        td { padding: 12px 16px; font-size: 14px; color: #333; border-bottom: 1px solid #eee; }
        @media (max-width: 768px) { .sidebar { display: none; } }
    </style>
</head>
<body>
    <header class="header"><div class="header-logo">数据仪表盘</div></header>
    <div class="container">
        <aside class="sidebar">
            <a href="#" class="menu-item active"><span>仪表盘</span></a>
            <a href="#" class="menu-item"><span>数据分析</span></a>
            <a href="#" class="menu-item"><span>报表</span></a>
            <a href="#" class="menu-item"><span>设置</span></a>
        </aside>
        <main class="main">
            <h1 class="page-title">数据概览</h1>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">总销售额</div>
                    <div class="stat-value">¥1,234,567</div>
                    <div class="stat-change up">↑ 较上月 +15%</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">订单数量</div>
                    <div class="stat-value">8,234</div>
                    <div class="stat-change up">↑ 较上月 +8%</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">用户数量</div>
                    <div class="stat-value">12,456</div>
                    <div class="stat-change up">↑ 较上月 +12%</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">转化率</div>
                    <div class="stat-value">3.2%</div>
                    <div class="stat-change down">↓ 较上月 -0.5%</div>
                </div>
            </div>
            <div class="charts-grid">
                <div class="chart-card">
                    <div class="chart-title">销售趋势</div>
                    <div class="chart-placeholder">图表区域（可集成 ECharts）</div>
                </div>
                <div class="chart-card">
                    <div class="chart-title">用户分布</div>
                    <div class="chart-placeholder">图表区域</div>
                </div>
            </div>
            <div class="table-card">
                <div class="table-header"><div class="table-title">最近订单</div></div>
                <table>
                    <thead><tr><th>订单号</th><th>客户</th><th>金额</th><th>状态</th><th>时间</th></tr></thead>
                    <tbody>
                        <tr><td>ORD-2026-001</td><td>张三</td><td>¥299.00</td><td>已完成</td><td>2026-04-04</td></tr>
                        <tr><td>ORD-2026-002</td><td>李四</td><td>¥199.00</td><td>处理中</td><td>2026-04-04</td></tr>
                        <tr><td>ORD-2026-003</td><td>王五</td><td>¥599.00</td><td>已完成</td><td>2026-04-03</td></tr>
                    </tbody>
                </table>
            </div>
        </main>
    </div>
</body>
</html>'''

# 登录页模板
LOGIN_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 20px; }
        .login-card { background: white; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); padding: 48px; width: 100%; max-width: 400px; }
        .login-header { text-align: center; margin-bottom: 32px; }
        .login-logo { font-size: 32px; font-weight: 700; color: #333; margin-bottom: 8px; }
        .login-subtitle { color: #666; font-size: 14px; }
        .form-group { margin-bottom: 20px; }
        .form-label { display: block; margin-bottom: 8px; font-size: 14px; color: #333; font-weight: 500; }
        .form-input { width: 100%; padding: 12px 16px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; transition: border-color 200ms, box-shadow 200ms; }
        .form-input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.15); }
        .form-options { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; font-size: 14px; }
        .remember-me { display: flex; align-items: center; gap: 8px; cursor: pointer; }
        .remember-me input { cursor: pointer; }
        .forgot-password { color: #667eea; text-decoration: none; }
        .forgot-password:hover { text-decoration: underline; }
        .btn { width: 100%; padding: 14px; border-radius: 6px; font-size: 16px; cursor: pointer; border: none; transition: all 200ms; font-weight: 600; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }
        .login-footer { text-align: center; margin-top: 24px; color: #666; font-size: 14px; }
        .login-footer a { color: #667eea; text-decoration: none; }
        .login-footer a:hover { text-decoration: underline; }
        .divider { display: flex; align-items: center; margin: 24px 0; color: #999; font-size: 14px; }
        .divider::before, .divider::after { content: ''; flex: 1; height: 1px; background: #eee; }
        .divider::before { margin-right: 16px; }
        .divider::after { margin-left: 16px; }
        .social-login { display: flex; gap: 12px; }
        .btn-social { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 6px; background: white; cursor: pointer; transition: background 200ms; font-size: 14px; }
        .btn-social:hover { background: #f5f5f5; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="login-header">
            <div class="login-logo">登录</div>
            <div class="login-subtitle">欢迎回来</div>
        </div>
        <form>
            <div class="form-group">
                <label class="form-label">邮箱 / 手机号</label>
                <input type="text" class="form-input" placeholder="请输入邮箱或手机号" required>
            </div>
            <div class="form-group">
                <label class="form-label">密码</label>
                <input type="password" class="form-input" placeholder="请输入密码" required>
            </div>
            <div class="form-options">
                <label class="remember-me"><input type="checkbox"> 记住我</label>
                <a href="#" class="forgot-password">忘记密码？</a>
            </div>
            <button type="submit" class="btn btn-primary">登录</button>
        </form>
        <div class="divider">或</div>
        <div class="social-login">
            <button class="btn-social">微信</button>
            <button class="btn-social">钉钉</button>
        </div>
        <div class="login-footer">
            还没有账号？<a href="#">立即注册</a>
        </div>
    </div>
</body>
</html>'''

# 落地页模板
LANDING_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>产品落地页</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #fff; color: #333; }
        .navbar { position: fixed; top: 16px; left: 16px; right: 16px; background: white; border-radius: 12px; padding: 16px 32px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 20px rgba(0,0,0,0.1); z-index: 1000; }
        .navbar-logo { font-size: 20px; font-weight: 700; color: #333; }
        .navbar-links { display: flex; gap: 32px; }
        .navbar-links a { color: #666; text-decoration: none; font-size: 14px; transition: color 200ms; cursor: pointer; }
        .navbar-links a:hover { color: #667eea; }
        .btn { padding: 12px 24px; border-radius: 6px; font-size: 14px; cursor: pointer; border: none; transition: all 200ms; font-weight: 500; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }
        .btn-cta { background: #F97316; color: white; }
        .btn-cta:hover { background: #EA580C; transform: translateY(-1px); }
        .hero { padding: 140px 32px 80px; text-align: center; background: linear-gradient(180deg, #f8f9ff 0%, #fff 100%); }
        .hero h1 { font-size: 48px; font-weight: 700; margin-bottom: 24px; line-height: 1.2; }
        .hero p { font-size: 18px; color: #666; max-width: 600px; margin: 0 auto 32px; line-height: 1.6; }
        .hero-buttons { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
        .features { padding: 80px 32px; background: #f8f9fa; }
        .section-title { text-align: center; font-size: 32px; font-weight: 700; margin-bottom: 48px; }
        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 32px; max-width: 1200px; margin: 0 auto; }
        .feature-card { background: white; padding: 32px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: transform 200ms, box-shadow 200ms; }
        .feature-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
        .feature-icon { width: 48px; height: 48px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; margin-bottom: 16px; }
        .feature-title { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
        .feature-desc { color: #666; font-size: 14px; line-height: 1.6; }
        .pricing { padding: 80px 32px; }
        .pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; max-width: 1000px; margin: 0 auto; }
        .pricing-card { background: white; border: 1px solid #eee; border-radius: 12px; padding: 32px; text-align: center; transition: transform 200ms; }
        .pricing-card:hover { transform: translateY(-4px); }
        .pricing-card.featured { border: 2px solid #667eea; position: relative; }
        .pricing-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: #667eea; color: white; padding: 4px 16px; border-radius: 12px; font-size: 12px; font-weight: 600; }
        .pricing-name { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
        .pricing-price { font-size: 36px; font-weight: 700; margin-bottom: 16px; }
        .pricing-price span { font-size: 14px; font-weight: 400; color: #666; }
        .pricing-features { list-style: none; margin-bottom: 24px; }
        .pricing-features li { padding: 8px 0; color: #666; font-size: 14px; border-bottom: 1px solid #f0f0f0; }
        .cta-section { padding: 80px 32px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); text-align: center; color: white; }
        .cta-section h2 { font-size: 32px; margin-bottom: 16px; }
        .cta-section p { font-size: 18px; opacity: 0.9; margin-bottom: 32px; }
        .btn-white { background: white; color: #667eea; }
        .btn-white:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
        footer { padding: 32px; text-align: center; color: #666; font-size: 14px; }
        @media (max-width: 768px) {
            .navbar-links { display: none; }
            .hero h1 { font-size: 32px; }
            .hero p { font-size: 16px; }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-logo">产品名</div>
        <div class="navbar-links">
            <a href="#features">功能</a>
            <a href="#pricing">价格</a>
            <a href="#">文档</a>
            <button class="btn btn-primary">开始使用</button>
        </div>
    </nav>

    <section class="hero">
        <h1>让工作更高效的智能解决方案</h1>
        <p>简单、快速、安全。一站式解决您的业务需求，提升团队协作效率。</p>
        <div class="hero-buttons">
            <button class="btn btn-cta">免费试用</button>
            <button class="btn btn-secondary" style="background: white; border: 1px solid #ddd;">了解更多</button>
        </div>
    </section>

    <section class="features" id="features">
        <h2 class="section-title">核心功能</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">1</div>
                <h3 class="feature-title">智能分析</h3>
                <p class="feature-desc">基于 AI 的智能数据分析，帮助您快速洞察业务趋势。</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">2</div>
                <h3 class="feature-title">团队协作</h3>
                <p class="feature-desc">实时同步，多人协作，让团队沟通更高效。</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">3</div>
                <h3 class="feature-title">安全可靠</h3>
                <p class="feature-desc">企业级安全防护，数据加密存储，保障信息安全。</p>
            </div>
        </div>
    </section>

    <section class="pricing" id="pricing">
        <h2 class="section-title">价格方案</h2>
        <div class="pricing-grid">
            <div class="pricing-card">
                <div class="pricing-name">基础版</div>
                <div class="pricing-price">免费</div>
                <ul class="pricing-features">
                    <li>5 个项目</li>
                    <li>基础功能</li>
                    <li>社区支持</li>
                </ul>
                <button class="btn btn-secondary" style="width: 100%;">开始使用</button>
            </div>
            <div class="pricing-card featured">
                <div class="pricing-badge">推荐</div>
                <div class="pricing-name">专业版</div>
                <div class="pricing-price">¥99<span>/月</span></div>
                <ul class="pricing-features">
                    <li>无限项目</li>
                    <li>高级功能</li>
                    <li>优先支持</li>
                </ul>
                <button class="btn btn-primary" style="width: 100%;">立即订阅</button>
            </div>
            <div class="pricing-card">
                <div class="pricing-name">企业版</div>
                <div class="pricing-price">定制</div>
                <ul class="pricing-features">
                    <li>私有部署</li>
                    <li>定制功能</li>
                    <li>专属客服</li>
                </ul>
                <button class="btn btn-secondary" style="width: 100%;">联系我们</button>
            </div>
        </div>
    </section>

    <section class="cta-section">
        <h2>立即开始您的旅程</h2>
        <p>加入 10,000+ 用户的选择</p>
        <button class="btn btn-white">免费注册</button>
    </section>

    <footer>© 2026 产品名. All rights reserved.</footer>
</body>
</html>'''

# 支付/结账页模板
CHECKOUT_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>结算</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f5f5f5; }
        .header { background: white; padding: 16px 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
        .header-logo { font-size: 20px; font-weight: 600; cursor: pointer; }
        .container { display: flex; gap: 24px; max-width: 1200px; margin: 24px auto; padding: 0 24px; flex-wrap: wrap; }
        .main { flex: 1; min-width: 300px; }
        .sidebar { width: 360px; }
        .card { background: white; border-radius: 8px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
        .card-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid #eee; }
        .form-row { display: flex; gap: 16px; margin-bottom: 16px; }
        .form-group { flex: 1; margin-bottom: 16px; }
        .form-label { display: block; margin-bottom: 6px; font-size: 14px; color: #333; }
        .form-input { width: 100%; padding: 10px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
        .form-input:focus { outline: none; border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1); }
        .payment-methods { display: flex; gap: 12px; margin-bottom: 16px; }
        .payment-method { flex: 1; padding: 16px; border: 2px solid #eee; border-radius: 8px; text-align: center; cursor: pointer; transition: all 200ms; }
        .payment-method:hover { border-color: #667eea; }
        .payment-method.active { border-color: #667eea; background: #f0f4ff; }
        .payment-icon { font-size: 24px; margin-bottom: 4px; }
        .payment-name { font-size: 12px; color: #666; }
        .order-item { display: flex; gap: 12px; padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
        .order-item-img { width: 60px; height: 60px; background: #f5f5f5; border-radius: 4px; }
        .order-item-info { flex: 1; }
        .order-item-name { font-size: 14px; font-weight: 500; margin-bottom: 4px; }
        .order-item-qty { font-size: 12px; color: #666; }
        .order-item-price { font-size: 14px; font-weight: 600; }
        .summary-row { display: flex; justify-content: space-between; padding: 8px 0; font-size: 14px; }
        .summary-row.total { font-size: 18px; font-weight: 700; padding-top: 16px; border-top: 1px solid #eee; margin-top: 8px; }
        .btn { width: 100%; padding: 14px; border-radius: 6px; font-size: 16px; cursor: pointer; border: none; transition: all 200ms; font-weight: 600; }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
        .btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }
        .security-note { text-align: center; margin-top: 12px; font-size: 12px; color: #666; }
        @media (max-width: 768px) {
            .container { flex-direction: column-reverse; }
            .sidebar { width: 100%; }
            .form-row { flex-direction: column; }
        }
    </style>
</head>
<body>
    <header class="header"><div class="header-logo">结算</div></header>

    <div class="container">
        <div class="main">
            <div class="card">
                <h2 class="card-title">配送信息</h2>
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label">姓名</label>
                        <input type="text" class="form-input" placeholder="收货人姓名">
                    </div>
                    <div class="form-group">
                        <label class="form-label">手机号</label>
                        <input type="tel" class="form-input" placeholder="联系手机">
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label">地址</label>
                    <input type="text" class="form-input" placeholder="详细地址">
                </div>
            </div>

            <div class="card">
                <h2 class="card-title">支付方式</h2>
                <div class="payment-methods">
                    <div class="payment-method active">
                        <div class="payment-icon">💳</div>
                        <div class="payment-name">微信支付</div>
                    </div>
                    <div class="payment-method">
                        <div class="payment-icon">💰</div>
                        <div class="payment-name">支付宝</div>
                    </div>
                    <div class="payment-method">
                        <div class="payment-icon">🏦</div>
                        <div class="payment-name">银行卡</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="sidebar">
            <div class="card">
                <h2 class="card-title">订单详情</h2>
                <div class="order-item">
                    <div class="order-item-img"></div>
                    <div class="order-item-info">
                        <div class="order-item-name">产品名称 A</div>
                        <div class="order-item-qty">x 1</div>
                    </div>
                    <div class="order-item-price">¥299.00</div>
                </div>
                <div class="order-item">
                    <div class="order-item-img"></div>
                    <div class="order-item-info">
                        <div class="order-item-name">产品名称 B</div>
                        <div class="order-item-qty">x 2</div>
                    </div>
                    <div class="order-item-price">¥199.00</div>
                </div>
                <div class="summary-row">
                    <span>小计</span>
                    <span>¥498.00</span>
                </div>
                <div class="summary-row">
                    <span>运费</span>
                    <span>¥0.00</span>
                </div>
                <div class="summary-row total">
                    <span>合计</span>
                    <span>¥498.00</span>
                </div>
            </div>

            <button class="btn btn-primary">确认支付 ¥498.00</button>
            <p class="security-note">🔒 安全支付 · 数据加密传输</p>
        </div>
    </div>
</body>
</html>'''


def get_template(page_type: str) -> str:
    """获取页面模板"""
    templates = {
        'list': LIST_PAGE_TEMPLATE,
        'form': FORM_PAGE_TEMPLATE,
        'dashboard': DASHBOARD_TEMPLATE,
        'login': LOGIN_PAGE_TEMPLATE,
        'landing': LANDING_PAGE_TEMPLATE,
        'checkout': CHECKOUT_PAGE_TEMPLATE,
        'detail': LIST_PAGE_TEMPLATE,  # 复用列表页
        'pricing': LANDING_PAGE_TEMPLATE,  # 复用落地页的价格部分
        'empty': LIST_PAGE_TEMPLATE,  # 占位
    }
    return templates.get(page_type, LIST_PAGE_TEMPLATE)


def get_available_templates() -> list:
    """获取所有可用模板列表"""
    return [
        {'type': 'list', 'name': '列表页', 'description': '数据表格、筛选、分页'},
        {'type': 'form', 'name': '表单页', 'description': '数据录入、提交'},
        {'type': 'dashboard', 'name': '仪表盘', 'description': '数据卡片、图表、统计'},
        {'type': 'login', 'name': '登录页', 'description': '用户认证、登录注册'},
        {'type': 'landing', 'name': '落地页', 'description': '营销推广、转化'},
        {'type': 'checkout', 'name': '结算页', 'description': '支付流程、订单确认'},
    ]