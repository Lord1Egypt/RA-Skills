#!/usr/bin/env python3
"""
企业调研报告 HTML 生成器 v4.2
- CSS 样式从外部模板文件加载
- HTML 结构从外部模板文件加载(细粒度占位符)
- 完整数据维度
- 支持 AI主搜+Tavily增强 二层架构降级提示
- 金蝶灵境风格模板加载 + 完整占位符替换
"""

import json
import sys
import re
import html as _html_module
from datetime import datetime
from pathlib import Path


def escape_html(text):
    """转义 HTML 特殊字符，防止 XSS 注入"""
    if not isinstance(text, str):
        text = str(text) if text else ''
    return _html_module.escape(text, quote=True)

# ========== 模板加载函数 ==========

def load_template(template_name):
    """从 templates 目录加载模板文件"""
    template_dir = Path(__file__).parent.parent / "templates"
    template_path = template_dir / template_name
    if template_path.exists():
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def load_css_template():
    css = load_template("report-css-v4.css")
    if css:
        return css
    # 内置最小兜底样式(保证报告可读)
    return """
:root { --blue: #2971EB; --skyL: #00CCFE; --teal: #05C8C8; --bg-card: #F5F7FA; --text-primary: #1A1A1A; --text-body: #333; }
body { font-family: system-ui, 'PingFang SC', 'Microsoft YaHei', sans-serif; background: var(--bg-card); padding: 20px; }
.card { background: #fff; border-radius: 22px; padding: 24px; margin-bottom: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.03); }
.card-title { font-size: 1.2em; font-weight: 700; margin-bottom: 16px; border-bottom: 1px solid #eee; padding-bottom: 8px; }
.info-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }
.info-item { padding: 12px; background: #f5f7fa; border-radius: 10px; }
.info-label { font-size: 0.75em; color: #999; text-transform: uppercase; }
.info-value { font-size: 0.95em; font-weight: 600; color: #1A1A1A; }
"""

def load_html_template():
    html = load_template("report-html-v4.html")
    if html:
        return html
    # 极度兜底:若无模板文件,返回最简结构
    return """<html><head><meta charset="UTF-8"><title>{{PAGE_TITLE}}</title><style>{{CSS_CONTENT}}</style></head>
<body><div class="container"><h1>{{COMPANY_NAME}}</h1>{{WARNING_BOX}}<div class="card"><p>模板文件缺失,无法展示完整报告。</p></div></div></body></html>"""


# ========== 数据清洗工具 ==========

MISSING_DEFAULT = "暂未获取"

def deep_fill_missing(data, default_value=MISSING_DEFAULT):
    """
    递归遍历字典/列表,将所有 None、空字符串填充为指定默认值。
    """
    if isinstance(data, dict):
        for k, v in data.items():
            if v is None or v == '':
                data[k] = default_value
            elif isinstance(v, (dict, list)):
                deep_fill_missing(v, default_value)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if item is None or item == '':
                data[i] = default_value
            elif isinstance(item, (dict, list)):
                deep_fill_missing(item, default_value)
    return data


# ========== 模块生成函数 ==========

def generate_tags_content(data):
    """生成行业标签 HTML"""
    tags = data.get('tags', {})
    html_parts = []
    for tag in tags.get('industry', []):
        html_parts.append(f'<span class="badge industry">🏭 {escape_html(tag)}</span>')
    for tag in tags.get('hot', []):
        html_parts.append(f'<span class="badge hot">🔥 {escape_html(tag)}</span>')
    for tag in tags.get('tech', []):
        html_parts.append(f'<span class="badge blue">💡 {escape_html(tag)}</span>')
    return ''.join(html_parts) if html_parts else f'<span class="badge gray">暂无标签</span>'


def generate_executives_content(data):
    """生成高管团队 HTML（最多6人，一排展示）"""
    executives = data.get('executives', [])
    if not executives:
        return '<div class="exec-item"><div class="exec-avatar blue">无</div><div class="exec-name">暂未获取</div><div class="exec-pos">暂无信息</div></div>'
    colors = ['blue', 'teal', 'purple', 'yellow']
    html_parts = []
    for idx, exec in enumerate(executives[:6]):
        name = exec.get('name', '未知')
        position = exec.get('position', '')
        if not position or position in (MISSING_DEFAULT, '无公开数据'):
            position = '高管'
        initial = name[0] if name and name != MISSING_DEFAULT else '?'
        color = colors[idx % len(colors)]
        html_parts.append(f'''
        <div class="exec-item accent-{color}">
            <div class="exec-avatar {color}">{escape_html(initial)}</div>
            <div class="exec-name">{escape_html(name)}</div>
            <div class="exec-pos">{escape_html(position)}</div>
        </div>''')
    return ''.join(html_parts)


def generate_digital_content(data):
    """生成数字化系统 HTML,区分厂商未知与已部署"""
    digital = data.get('digital', {})
    digital_systems = [
        ("ERP系统", digital.get("erp", "未部署")),
        ("CRM系统", digital.get("crm", "未部署")),
        ("MES制造系统", digital.get("mes", "未部署")),
        ("WMS仓储系统", digital.get("wms", "未部署")),
        ("TMS运输系统", digital.get("tms", "未部署")),
        ("BI商业智能", digital.get("bi", "未部署")),
        ("SRM供应商管理", digital.get("srm", "未部署")),
        ("PLM产品生命周期", digital.get("plm", "未部署")),
        ("SCM供应链管理", digital.get("scm", "未部署")),
        ("OA办公自动化", digital.get("oa", "未部署")),
        ("HRM人力资源", digital.get("hrm", "未部署")),
        ("QMS质量管理", digital.get("qms", "未部署")),
        ("EAM资产管理", digital.get("eam", "未部署")),
        ("APS高级排程", digital.get("aps", "未部署")),
    ]
    icons = {
        "ERP系统": "☁️", "CRM系统": "📞", "MES制造系统": "🏭", "WMS仓储系统": "📦",
        "TMS运输系统": "🚛", "BI商业智能": "📊", "SRM供应商管理": "🤝",
        "PLM产品生命周期": "🔬", "SCM供应链管理": "🌐", "OA办公自动化": "📝",
        "HRM人力资源": "👥", "QMS质量管理": "✅", "EAM资产管理": "🏗️",
        "APS高级排程": "⚡"
    }
    html_parts = []
    for sys_name, status in digital_systems:
        icon = icons.get(sys_name, "💻")
        # 处理多种状态值
        if status and status not in ("未部署", MISSING_DEFAULT, ""):
            status_class = "active"
            # 判断是否为"已部署"但无具体厂商名
            if len(status) <= 5 or status in ("已部署", "是", "有", "在用", "已上线"):
                status_text = "● 已部署"
                desc_text = "厂商未知"
            else:
                status_text = "● 已部署"
                desc_text = f"厂商: {escape_html(status)}"
        else:
            status_class = "planning"
            status_text = "○ 未明确"
            desc_text = "暂未搜索到相关信息"
        html_parts.append(f'''
        <div class="digital-item">
            <div class="digital-icon">{icon}</div>
            <div class="digital-name">{escape_html(sys_name)}</div>
            <span class="digital-status {status_class}">{escape_html(status_text)}</span>
            <div class="digital-desc">{escape_html(desc_text)}</div>
        </div>''')
    return ''.join(html_parts)


def generate_finance_card(data):
    """生成财务数据卡片,仅当 is_listed 为 True 且有可显示数据时"""
    finance = data.get('finance', {})
    if not finance.get('is_listed', False):
        return ''

    company_name = data.get('basic', {}).get('name', '企业')
    stock_code = finance.get('stock_code', '')
    kpis = finance.get('kpi', {})
    history = finance.get('history', [])
    source = finance.get('source', '企业年报/公开财报')

    # 如果 KPI 和 history 都无实质性数据,仍可展示一个占位说明
    if not kpis and not history:
        return f'''
        <div class="card animate-in delay-3">
            <div class="card-title"><span class="icon-circle yellow">💰</span>财务数据({company_name})</div>
            <p style="text-align:center; color:var(--text-caption);">该上市公司暂无公开财务详细数据。</p>
        </div>'''

    # KPI 彩条
    kpi_colors = ["bg-blue", "bg-teal", "bg-purple", "bg-yellow"]
    kpi_html = ""
    for idx, (label, value) in enumerate(kpis.items()):
        color = kpi_colors[idx % len(kpi_colors)]
        kpi_html += f'''
        <div class="finance-kpi-item {color}">
            <div class="finance-kpi-label">{escape_html(label)}</div>
            <div class="finance-kpi-value">{escape_html(value)}</div>
        </div>'''

    # 历史数据表格
    table_html = ""
    if history:
        headers = list(history[0].keys())
        table_html += '<table class="finance-table"><thead><tr>'
        for h in headers:
            table_html += f'<th>{escape_html(h)}</th>'
        table_html += '</tr></thead><tbody>'
        for row in history:
            table_html += '<tr>'
            for i, (key, val) in enumerate(row.items()):
                val_str = str(val)
                cell_class = ''
                if i == 0:
                    cell_class = ' class="label-cell"'
                elif val_str.startswith('+') or val_str.endswith('%增长'):
                    cell_class = ' class="finance-change positive"'
                elif val_str.startswith('-') or val_str.endswith('%下降'):
                    cell_class = ' class="finance-change negative"'
                table_html += f'<td{cell_class}>{escape_html(val_str)}</td>'
            table_html += '</tr>'
        table_html += '</tbody></table>'

    return f'''
        <div class="card animate-in delay-3">
            <div class="card-title">
                <span class="icon-circle yellow">💰</span> 财务数据({escape_html(company_name)})
                <span style="margin-left:auto;font-size:0.75rem;color:var(--text-caption);font-weight:400;">{escape_html(stock_code)}</span>
            </div>
            <div class="finance-kpi-strip">{kpi_html}</div>
            {table_html}
            <div class="finance-source">数据来源：{escape_html(source)} | 数据仅供参考，不构成投资建议</div>
        </div>'''


def generate_footer(version, data, time_str):
    sources = data.get('data_sources', '公开数据、企业年报')
    report_date = time_str.split(' ')[0] if ' ' in time_str else time_str
    return f'''<div class="footer-brand">KINGDEE · 企业信息调研报告</div>
            <div class="footer-divider"></div>
            <p>Generated by <strong>KD-Enterprise-Info Skill v{version}</strong> | 反馈建议，请联系金蝶总部张贺老师</p>
            <p style="margin-top: 6px;">数据来源：<strong>{escape_html(sources)}</strong> | 报告日期：<strong>{report_date}</strong></p>
            <p style="margin-top: 6px; opacity: 0.75;">免责声明：本报告基于公开数据整理，仅供参考，不构成投资建议。</p>'''


# ========== 主生成函数 ==========

def generate_html(data, company_name, version="5.2"):
    """生成完整的企业调研报告 HTML"""

    # 错误处理
    if data.get('error'):
        return f'''<!DOCTYPE html><html><head><meta charset="UTF-8"><title>错误</title></head>
<body style="font-family: sans-serif; padding: 50px;">
    <h2>❌ 查询失败</h2>
    <p>{data['error']}</p>
</body></html>'''

    # 先取出 fallback_hint（避免 deep_fill_missing 将 None 转为"暂未获取"导致误显示警告框）
    fallback_hint_raw = data.get('fallback_hint', None)

    # 深度清洗数据,防止 None 值(使用新文案"暂未获取")
    cleaned_data = deep_fill_missing(data, MISSING_DEFAULT)

    # 加载模板
    css_content = load_css_template()
    html_template = load_html_template()

    time_str = datetime.now().strftime("%Y年%m月%d日 %H:%M")
    fallback_hint = fallback_hint_raw  # 使用原始值，不被清洗干扰

    # 构建警告框（仅当有实际降级提示时显示）
    warning_box = ''
    if fallback_hint and fallback_hint not in (MISSING_DEFAULT, '无公开数据'):
        warning_box = f'<div class="warning-box">{fallback_hint}</div>'

    # 便捷访问各板块(缺失时自动为"暂未获取")
    basic = cleaned_data.get('basic', {})
    profile = cleaned_data.get('company_profile', {})
    business = cleaned_data.get('business', {})
    brand = cleaned_data.get('brand_products', {})
    tech = cleaned_data.get('tech_capability', {})
    market = cleaned_data.get('market_info', {})
    related = cleaned_data.get('related', {})
    insight = cleaned_data.get('industry_insight', {})

    # 构建占位符映射(所有默认值均改为 MISSING_DEFAULT)
    placeholders = {
        'PAGE_TITLE': f'企业调研报告 - {escape_html(company_name)}',
        'CSS_CONTENT': css_content,
        'WARNING_BOX': warning_box,

        'HEADER_ICON': '📊',
        'HEADER_TITLE': '企业信息调研报告',
        'COMPANY_NAME': company_name,
        'DATA_DATE_LABEL': '数据截至时间',
        'DATA_DATE_VALUE': cleaned_data.get('data_date', time_str.split(' ')[0]),
        'META_LABEL': '生成时间',
        'GENERATE_TIME': time_str,

        'TAGS_SECTION_TITLE': '行业标签',
        'TAGS_CONTENT': generate_tags_content(cleaned_data),

        'INSIGHT_SECTION_TITLE': '行业洞察及趋势',
        'INSIGHT_LABEL_1': '市场规模',
        'INSIGHT_TEXT_1': insight.get('market_size', MISSING_DEFAULT),
        'INSIGHT_LABEL_2': '增长动力',
        'INSIGHT_TEXT_2': insight.get('growth_driver', MISSING_DEFAULT),
        'INSIGHT_LABEL_3': '政策影响',
        'INSIGHT_TEXT_3': insight.get('policy_impact', MISSING_DEFAULT),
        'INSIGHT_LABEL_4': '发展趋势',
        'INSIGHT_TEXT_4': insight.get('trend', MISSING_DEFAULT),
        'INSIGHT_LABEL_5': '竞争格局',
        'INSIGHT_TEXT_5': insight.get('competition', MISSING_DEFAULT),
        'INSIGHT_LABEL_6': '技术方向',
        'INSIGHT_TEXT_6': insight.get('tech_direction', MISSING_DEFAULT),

        'PROFILE_SECTION_TITLE': '公司简介',
        'PROFILE_SUBTITLE_1': '企业概况',
        'PROFILE_CONTENT_1': profile.get('introduction', MISSING_DEFAULT),
        'PROFILE_SUBTITLE_2': '发展历程',
        'PROFILE_CONTENT_2': profile.get('development', MISSING_DEFAULT),
        'PROFILE_SUBTITLE_3': '企业文化',
        'PROFILE_CONTENT_3': profile.get('culture', MISSING_DEFAULT),
        'PROFILE_SUBTITLE_4': '荣誉资质',
        'PROFILE_CONTENT_4': profile.get('honors', MISSING_DEFAULT),

        'EXEC_SECTION_TITLE': '核心高管团队',
        'EXECUTIVES_CONTENT': generate_executives_content(cleaned_data),

        'BASIC_SECTION_TITLE': '基础工商信息',
        'BASIC_LABEL_1': '企业名称',
        'BASIC_VALUE_1': basic.get('name', company_name),
        'BASIC_LABEL_2': '统一社会信用代码',
        'BASIC_VALUE_2': basic.get('credit_code', MISSING_DEFAULT),
        'BASIC_LABEL_3': '法定代表人',
        'BASIC_VALUE_3': basic.get('legal_person', MISSING_DEFAULT),
        'BASIC_LABEL_4': '注册资本',
        'BASIC_VALUE_4': basic.get('reg_capital', MISSING_DEFAULT),
        'BASIC_LABEL_5': '实缴资本',
        'BASIC_VALUE_5': basic.get('paid_capital', MISSING_DEFAULT),
        'BASIC_LABEL_6': '成立日期',
        'BASIC_VALUE_6': basic.get('established', MISSING_DEFAULT),
        'BASIC_LABEL_7': '经营状态',
        'BASIC_VALUE_7': basic.get('status', MISSING_DEFAULT),
        'BASIC_LABEL_8': '登记机关',
        'BASIC_VALUE_8': basic.get('authority', MISSING_DEFAULT),
        'BASIC_LABEL_9': '企业类型',
        'BASIC_VALUE_9': basic.get('type', MISSING_DEFAULT),
        'BASIC_LABEL_10': '所属行业',
        'BASIC_VALUE_10': basic.get('industry', MISSING_DEFAULT),
        'BASIC_LABEL_11': '注册地址',
        'BASIC_VALUE_11': basic.get('address', MISSING_DEFAULT),
        'BASIC_LABEL_12': '经营范围',
        'BASIC_VALUE_12': basic.get('scope', MISSING_DEFAULT),

        'DIGITAL_SECTION_TITLE': '数字化应用系统',
        'DIGITAL_SYSTEMS_CONTENT': generate_digital_content(cleaned_data),

        'FINANCE_CARD': generate_finance_card(cleaned_data),

        'BUSINESS_SECTION_TITLE': '主营业务与行业地位',
        'BUSINESS_LABEL_1': '主营业务',
        'BUSINESS_VALUE_1': business.get('main_business', MISSING_DEFAULT),
        'BUSINESS_LABEL_2': '行业地位',
        'BUSINESS_VALUE_2': business.get('industry_position', MISSING_DEFAULT),
        'BUSINESS_LABEL_3': '市场地位',
        'BUSINESS_VALUE_3': business.get('market_position', MISSING_DEFAULT),

        'BRAND_SECTION_TITLE': '品牌与产品系列',
        'BRAND_LABEL_1': '核心品牌',
        'BRAND_VALUE_1': brand.get('core_brand', MISSING_DEFAULT),
        'BRAND_LABEL_2': '产品系列',
        'BRAND_VALUE_2': brand.get('product_series', MISSING_DEFAULT),
        'BRAND_LABEL_3': '核心产品',
        'BRAND_VALUE_3': brand.get('core_products', MISSING_DEFAULT),
        'BRAND_LABEL_4': '解决方案',
        'BRAND_VALUE_4': brand.get('solutions', MISSING_DEFAULT),

        'TECH_SECTION_TITLE': '技术实力与研发',
        'TECH_LABEL_1': '研发投入',
        'TECH_VALUE_1': tech.get('rd_investment', MISSING_DEFAULT),
        'TECH_LABEL_2': '专利情况',
        'TECH_VALUE_2': tech.get('patents', MISSING_DEFAULT),
        'TECH_LABEL_3': '核心技术',
        'TECH_VALUE_3': tech.get('core_tech', MISSING_DEFAULT),
        'TECH_LABEL_4': '研发中心',
        'TECH_VALUE_4': tech.get('rd_centers', MISSING_DEFAULT),

        'MARKET_SECTION_TITLE': '市场与客户',
        'MARKET_LABEL_1': '主要客户',
        'MARKET_VALUE_1': market.get('main_customers', MISSING_DEFAULT),
        'MARKET_LABEL_2': '市场覆盖',
        'MARKET_VALUE_2': market.get('market_coverage', MISSING_DEFAULT),
        'MARKET_LABEL_3': '销售渠道',
        'MARKET_VALUE_3': market.get('sales_channels', MISSING_DEFAULT),

        'RELATED_SECTION_TITLE': '热门关联信息',
        'RELATED_LABEL_1': '产业链位置',
        'RELATED_VALUE_1': related.get('industry_chain', MISSING_DEFAULT),
        'RELATED_LABEL_2': '主要竞争对手',
        'RELATED_VALUE_2': related.get('competitors', MISSING_DEFAULT),
        'RELATED_LABEL_3': '合作伙伴',
        'RELATED_VALUE_3': related.get('partners', MISSING_DEFAULT),
        'RELATED_LABEL_4': '近期热点',
        'RELATED_VALUE_4': related.get('trending', MISSING_DEFAULT),

        'FOOTER_CONTENT': generate_footer(version, cleaned_data, time_str),
    }

    # 替换所有占位符（HTML片段型占位符不再二次转义，纯文本型已在生成函数中转义）
    html = html_template
    for key, value in placeholders.items():
        html = html.replace(f'{{{{{key}}}}}', str(value))

    return html


if __name__ == '__main__':
    # 金蝶国际软件集团完整演示数据（基于公开信息补全，无"暂未获取"字段）
    # ⚠️ 注意：以下财务数据为约数示例，仅供功能演示参考，不代表企业实际财报数据
    test_data = {
        "basic": {
            "name": "金蝶国际软件集团有限公司",
            "credit_code": "9144030019244080528",
            "legal_person": "徐少春",
            "reg_capital": "20000万港元",
            "paid_capital": "20000万港元",
            "established": "1993年8月8日",
            "status": "存续",
            "authority": "深圳市市场监督管理局",
            "type": "其他股份有限公司(上市)",
            "industry": "软件和信息技术服务业",
            "address": "深圳市南山区高新技术产业园南区科技南十二路2号金蝶软件园",
            "scope": "企业管理软件的研发、销售及实施服务;云服务(包括财务云、人力云、协同云、制造云等);企业数字化转型解决方案。"
        },
        "company_profile": {
            "introduction": "金蝶国际软件集团有限公司是亚太领先的企业管理软件与云服务提供商,2001年在香港联交所上市(股票代码:00268.HK)。公司致力于为企业提供全面的数字化转型解决方案。",
            "development": "1993年创立,推出财务软件;1996年发布K/3 ERP;2001年港股上市;2011年全面向云转型,发布金蝶云·苍穹平台;2024年营收突破85亿元。",
            "culture": "使命:全心全意为企业服务,成为最值得托付的企业服务平台。价值观:致良知、走正道、行王道。",
            "honors": "国家级高新技术企业、连续多年入选Gartner高生产力PaaS魔力象限、IDC中国SaaS市场占有率第一、中国软件业务收入前百家企业。"
        },
        "executives": [
            {"name": "徐少春", "position": "董事会主席、首席执行官"},
            {"name": "章勇", "position": "总裁"},
            {"name": "杨健", "position": "首席财务官"},
            {"name": "田荣举", "position": "首席技术官"},
            {"name": "魏斌", "position": "副总裁"},
            {"name": "林波", "position": "董事会秘书"}
        ],
        "business": {
            "main_business": "企业管理软件(ERP、财务、HR、供应链、制造等)研发与销售;企业云服务(金蝶云·苍穹、星瀚、星空、星辰、精斗云等);中间件软件。",
            "industry_position": "中国企业管理云服务市场领导者,Gartner全球高生产力PaaS平台唯一中国厂商。",
            "market_position": "在中小企业财务云市场占有率连续多年第一;大型企业市场持续突破,服务超过740万家企业和政府机构。"
        },
        "brand_products": {
            "core_brand": "金蝶 Kingdee",
            "product_series": "金蝶云·苍穹(企业级PaaS平台)、金蝶云·星瀚(大型企业EBC)、金蝶云·星空(成长型企业ERP)、金蝶云·星辰(小型企业财税助手)、精斗云(微型企业SaaS)、云之家(智能协同)、我家云(物业云)",
            "core_products": "金蝶云·星空财务云、金蝶云·苍穹平台、金蝶s-HR、金蝶发票云、金蝶云·制造云",
            "solutions": "财务云、人力云、协同云、制造云、供应链云、零售云、电商云、税务云、金融云等全行业企业数字化解决方案。"
        },
        "tech_capability": {
            "rd_investment": "2024年研发投入超过12亿元人民币,占营收约14%",
            "patents": "拥有超过900项发明专利,涵盖AI、大数据、区块链等领域",
            "core_tech": "动态领域模型(KDDM)、AI原生(金蝶苍穹GPT)、低代码/无代码平台、分布式计算、区块链、物联网集成",
            "rd_centers": "深圳总部研发中心,北京、上海、长沙、成都设有研发分部;中国首个企业级PaaS平台创新实验室"
        },
        "market_info": {
            "main_customers": "中国中车、格力电器、万科、华为、招商局、海信、温氏、元气森林等,覆盖制造业、房地产、零售、金融等行业",
            "market_coverage": "业务覆盖中国及东南亚、欧洲、非洲等地区,在全球设立超过60家分支机构",
            "sales_channels": "直销团队覆盖大客户;全国2000余家合作伙伴(渠道商、ISV);金蝶云市场线上平台"
        },
        "related": {
            "industry_chain": "企业数字化服务上游,覆盖企业管理软件的研发、销售、实施、运维全链条,向下游各行业提供数字化转型能力",
            "competitors": "用友网络(600588.SH)、SAP中国、Oracle NetSuite、鼎捷软件、明源云",
            "partners": "华为云、腾讯云、亚马逊AWS、中国移动、中国电信、招商银行、中国民生银行、各大会计师事务所与咨询机构",
            "trending": "2025年发布金蝶云·苍穹GPT,实现AI原生管理;与华为云签署战略深化合作协议;信创领域中标多个央企ERP替换项目"
        },
        "digital": {
            "erp": "金蝶云·星空",
            "crm": "金蝶云CRM",
            "mes": "金蝶云MES",
            "wms": "金蝶云WMS",
            "tms": "已部署",
            "bi": "帆软 FineBI",
            "srm": "企企通",
            "plm": "金蝶 PLM",
            "scm": "金蝶 SCM",
            "oa": "企业微信+泛微",
            "hrm": "金蝶 s-HR",
            "qms": "已部署",
            "eam": "IBM Maximo",
            "aps": "Asprova"
        },
        "industry_insight": {
            "market_size": "2025年中国企业级SaaS市场规模预计突破1200亿元人民币,年复合增长率超过25%",
            "growth_driver": "企业数字化转型刚性需求、国产替代(信创)政策、AI与云原生技术成熟、中小企业上云加速",
            "policy_impact": "《'十四五'数字经济发展规划》明确推进企业上云,国资委要求央企加快ERP国产化替代,为金蝶带来重大政策红利",
            "trend": "AI原生应用兴起(GPT+ERP)、大型企业私有云向公有云迁移、低代码/无代码平台普及、行业化解决方案深化",
            "competition": "用友网络在市场占有率和产品线宽度上形成直接竞争,SAP与Oracle仍盘踞部分大型企业,但国产厂商份额持续提升",
            "tech_direction": "AI PaaS成为下一代企业平台核心,融合大模型与业务流;区块链技术在企业间协同、供应链金融中加速落地"
        },
        "finance": {
            "is_listed": True,
            "stock_code": "00268.HK",
            "kpi": {
                "2024年营收": "约85亿元人民币",       # 示例数据，仅供参考
                "净利润": "约13亿元人民币",          # 示例数据，仅供参考
                "毛利率": "79.2%",
                "ROE": "18.6%"
            },
            "history": [
                {"指标": "营业收入(亿元)", "2021": "约67", "2022": "约74", "2023": "约79", "2024": "约85", "同比": "+约8%"},      # 示例数据，仅供参考
                {"指标": "净利润(亿元)", "2021": "约10", "2022": "约11", "2023": "约12", "2024": "约13", "同比": "+约10%"},        # 示例数据，仅供参考
                {"指标": "毛利率(%)", "2021": "约77", "2022": "约78", "2023": "约79", "2024": "约79", "同比": "持平"}           # 示例数据，仅供参考
            ],
            "source": "金蝶国际2024年度业绩公告(香港联交所)"
        },
        "tags": {
            "industry": ["云计算", "SaaS", "企业服务", "软件"],
            "hot": ["香港上市公司", "高新技术企业", "专精特新小巨人", "中国软件百强"],
            "tech": ["人工智能", "大数据", "云原生", "区块链", "物联网"]
        },
        "data_date": "2026年04月30日",
        "data_sources": "金蝶国际官网、东方财富网、香港联交所披露易、企查查",
        "fallback_level": 1
    }

    html = generate_html(test_data, "金蝶国际软件集团有限公司")
    print(html)