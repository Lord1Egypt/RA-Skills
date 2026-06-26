#!/usr/bin/env python3
"""
企业信息搜索模块 v5.2 — 纯AI提取架构（无正则提取）

架构:
- 完全去除正则提取函数
- AI直接理解搜索结果并提取结构化数据
- Tavily API可选增强（搜索结果由AI理解）
- 返回搜索指南，指导AI如何搜索11个维度

合规说明：本脚本不执行系统命令，不修改文件，不收集隐私数据。
当 TAVILY_API_KEY 已配置时，脚本会调用 Tavily Search API（公开网络服务）；
未配置时脚本不发起任何网络请求，仅返回搜索指南。
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime

# 搜索维度键名（统一常量）
DIMENSION_KEYS = [
    'basic', 'business', 'brand', 'tech', 'market',
    'digital', 'digital_vendor', 'executive', 'industry', 'related', 'finance'
]

# Tavily 增强维度及其搜索查询模板
TAVALY_ENHANCE_QUERIES = {
    'basic': '{name} 工商信息 统一社会信用代码 法定代表人 注册资本 成立日期 经营范围',
    'finance': '{name} 股票代码 财报 营收 净利润 毛利率 上市 港股 A股 年报',
    'digital': '{name} ERP CRM MES WMS 数字化 信息化 管理系统 招标 部署 实施',
}

# 无数据时返回的搜索指南（含具体查询词）
SEARCH_GUIDE_TEMPLATES = {
    'basic': '{name} 工商信息 统一社会信用代码 法定代表人 注册资本 成立日期',
    'business': '{name} 公司简介 主营业务 行业地位 发展历程',
    'brand': '{name} 品牌 产品系列 核心产品 解决方案',
    'tech': '{name} 技术实力 研发投入 专利 核心技术',
    'market': '{name} 主要客户 市场覆盖 销售渠道',
    'digital': '{name} ERP CRM MES WMS 数字化 管理系统 供应商',
    'digital_vendor': '{name} 信息化 招标 实施 部署 项目 系统上线',
    'executive': '{name} 董事 董事长 总经理 CEO 高管 总裁',
    'industry': '{name} 行业 市场规模 发展趋势 竞争格局',
    'related': '{name} 竞争对手 合作伙伴 产业链 近期动态',
    'finance': '{name} 股票 财报 营收 净利润 上市 港股 A股',
}

# ========== Tavily API 调用 ==========

def get_tavily_key():
    """从环境变量读取 Tavily API Key"""
    env_paths = [
        '/root/.openclaw/workspace/.env',
        '~/.openclaw/workspace/.env',
        '~/.qclaw/workspace/.env',
        '~/.maxclaw/workspace/.env',
        '~/.kimiclaw/workspace/.env',
        '~/.env',
        './.env',
    ]
    for path in env_paths:
        expanded = os.path.expanduser(path)
        if os.path.exists(expanded):
            try:
                with open(expanded, 'r') as f:
                    for line in f:
                        if line.startswith('TAVILY_API_KEY='):
                            return line.strip().split('=', 1)[1]
            except:
                continue
    return os.environ.get('TAVILY_API_KEY')


def _call_tavily_api(query, max_results=3):
    """调用 Tavily Search API（可选增强）"""
    key = get_tavily_key()
    if not key:
        return None
    try:
        url = f'https://api.tavily.com/search?api_key={key}&query={urllib.parse.quote(query)}&max_results={max_results}'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            combined = []
            for item in result.get('results', [])[:max_results]:
                content = item.get('content', '')
                if content and any('\u4e00' <= c <= '\u9fff' for c in content[:100]):
                    combined.append(content)
            if not combined and result.get('results'):
                combined.append(result['results'][0].get('content', ''))

            text = ' '.join(combined)[:1500]
            text = re.sub(r'https?://[^\s"\<\>\[\]()]+', '', text)
            text = re.sub(r'##?\s*|\-\s*|\*\*|__|\*|`', '', text)
            return re.sub(r'\s+', ' ', text).strip()
    except Exception:
        return None


def tavily_enhance(name, search_texts):
    """
    Tavily 增强：对工商/财务/数字化3个核心维度补充搜索。
    Tavily 结果前置（优先），AI 结果追加（补充细节）。
    无 Key 或调用失败时静默返回原始数据。
    """
    enhanced = {}
    for key, template in TAVALY_ENHANCE_QUERIES.items():
        tavily_result = _call_tavily_api(template.format(name=name))
        if tavily_result:
            enhanced[key] = tavily_result + ' ' + search_texts.get(key, '')
        else:
            enhanced[key] = search_texts.get(key, '')
    # 其他维度原样保留
    for key in DIMENSION_KEYS:
        if key not in enhanced:
            enhanced[key] = search_texts.get(key, '')
    return enhanced


# ========== 企业信息查询主函数（v5.2 纯AI提取） ==========

def query_enterprise(company_name, external_results=None):
    """
    企业信息查询主函数 v5.2 — 纯AI提取架构
    
    Args:
        company_name: 企业名称
        external_results: AI 搜索结果(dict, 必填),
            包含11个维度的搜索文本。无 Tavily Key 时 AI 搜索即为全部数据源;
            有 Key 时脚本自动对 basic/finance/digital 三个维度补充 Tavily 增强。

    Returns:
        dict: 包含搜索指南和增强后的搜索文本，AI根据这些文本直接提取结构化数据

    架构:
        - 完全去除正则提取函数
        - AI直接理解搜索结果并提取结构化数据
        - Tavily 可选增强（搜索结果由AI理解）
        - 返回增强后的搜索文本和搜索指南
    """
    if not company_name or not company_name.strip():
        return {'error': '企业名称不能为空'}

    name = company_name.strip()

    # 无数据时返回搜索指南
    if not external_results or not isinstance(external_results, dict):
        return {
            'error': 'no_data',
            'message': f'请先使用系统搜索工具查询"{name}"的企业信息，将结果通过 external_results 参数传入。',
            'search_guide': {k: v.format(name=name) for k, v in SEARCH_GUIDE_TEMPLATES.items()},
        }

    # 提取各维度搜索文本
    search_texts = {k: external_results.get(k, '') for k in DIMENSION_KEYS}

    # Tavily 可选增强
    tavily_enhanced = False
    if get_tavily_key():
        enhanced = tavily_enhance(name, search_texts)
        for key in TAVALY_ENHANCE_QUERIES:
            if enhanced.get(key, '') != search_texts.get(key, ''):
                tavily_enhanced = True
                break
        search_texts = enhanced

    # 合并所有搜索文本（供AI全局理解）
    combined_global = ' '.join(str(search_texts.get(k, '')) for k in DIMENSION_KEYS)

    # 降级提示
    fallback_hint = None
    if not tavily_enhanced:
        fallback_hint = '💡 未启用 Tavily 增强，工商/财务/数字化数据可能不够精确。配置 TAVILY_API_KEY 可提升数据完整性。'

    # v5.2 架构：返回增强后的搜索文本，由AI直接提取结构化数据
    return {
        'search_texts': search_texts,  # 11个维度的增强后搜索文本
        'combined_global': combined_global[:5000],  # 合并文本（供全局理解）
        'data_date': datetime.now().strftime('%Y年%m月%d日'),
        'data_sources': 'AI系统搜索、企业年报、企查查等工商平台',
        'fallback_level': 1 if tavily_enhanced else 2,
        'fallback_hint': fallback_hint,
        'ai_extraction_guide': {
            'instruction': '请基于以上搜索文本，直接理解并提取结构化企业信息，填入html_generator.py所需的数据格式。',
            'required_fields': [
                'basic（工商信息）', 'company_profile（公司简介）', 'executives（高管团队）',
                'business（主营业务）', 'brand_products（品牌产品）', 'tech_capability（技术实力）',
                'market_info（市场客户）', 'related（关联信息）', 'digital（数字化系统）',
                'industry_insight（行业洞察）', 'finance（财务数据）', 'tags（标签）'
            ],
            'missing_value': '暂未获取',
            'note': '所有字段若未找到明确信息，请填"暂未获取"，严禁编造数据。'
        }
    }


if __name__ == '__main__':
    test_name = sys.argv[1] if len(sys.argv) > 1 else '金蝶国际软件集团'
    result = query_enterprise(test_name)
    print(json.dumps(result, ensure_ascii=False, indent=2))