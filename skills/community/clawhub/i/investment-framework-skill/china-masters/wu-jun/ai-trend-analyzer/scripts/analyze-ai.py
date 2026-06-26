#!/usr/bin/env python3
"""
AI 趋势分析器 - 基于吴军的 AI 投资逻辑

集成 searxng 搜索获取 AI 趋势数据
"""

import sys
import os
import subprocess
import json

# 添加投资框架目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
framework_dir = os.path.dirname(script_dir)
sys.path.insert(0, framework_dir)

from datetime import datetime


def search_ai_trends(topic: str = '人工智能') -> dict:
    """
    使用 searxng 搜索 AI 趋势
    
    Args:
        topic: 主题
    
    Returns:
        搜索结果
    """
    result = {
        'topic': topic,
        'sources': [],
    }
    
    try:
        queries = [
            f"{topic} 发展趋势 2025 2026",
            f"{topic} 投资机会 前景",
            f"{topic} 技术突破 应用",
        ]
        
        for query in queries:
            cmd = [
                'uv', 'run',
                f'{framework_dir}/../../skills/searxng/scripts/searxng.py',
                'search', query,
                '-n', '5',
                '--format', 'json'
            ]
            
            proc_result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if proc_result.returncode == 0:
                search_data = json.loads(proc_result.stdout)
                if 'results' in search_data:
                    result['sources'].extend(search_data['results'][:5])
    except Exception as e:
        result['error'] = str(e)
    
    return result


def analyze_ai_waves() -> dict:
    """
    分析 AI 发展浪潮
    
    Returns:
        分析结果
    """
    return {
        'waves': [
            {
                'name': '第一次浪潮',
                'period': '1950s-1970s',
                'feature': '符号主义 AI',
                'limitation': '计算能力不足',
            },
            {
                'name': '第二次浪潮',
                'period': '1980s-2000s',
                'feature': '连接主义 AI',
                'limitation': '数据不足',
            },
            {
                'name': '第三次浪潮',
                'period': '2010s-现在',
                'feature': '深度学习 + 大数据',
                'driver': '算力 + 数据 + 算法',
            },
        ],
        'current_stage': '第三次浪潮中期',
        'next_breakthrough': '通用人工智能（AGI）',
    }


def analyze_investment_opportunities() -> dict:
    """
    分析 AI 投资机会
    
    Returns:
        机会分析
    """
    return {
        'layers': [
            {
                'name': '基础层',
                'description': '芯片、算力、数据',
                'examples': ['GPU/TPU', '云计算', '数据中心'],
                'characteristics': '高壁垒，高投入',
            },
            {
                'name': '技术层',
                'description': '算法、框架、模型',
                'examples': ['大模型', '机器学习平台', 'AI 框架'],
                'characteristics': '技术密集，赢家通吃',
            },
            {
                'name': '应用层',
                'description': '行业应用、产品',
                'examples': ['AI+ 医疗', 'AI+ 金融', 'AI+ 制造'],
                'characteristics': '场景驱动，百花齐放',
            },
        ],
        'recommendation': '关注应用层落地，基础层长期布局',
    }


def analyze_trend(topic: str = '人工智能', use_search: bool = True) -> dict:
    """
    AI 趋势完整分析
    
    Args:
        topic: 主题
        use_search: 是否使用搜索
    
    Returns:
        分析结果
    """
    result = {
        'topic': topic,
        'timestamp': datetime.now().isoformat(),
        'data_sources': [],
    }
    
    # 使用 searxng 搜索
    if use_search:
        search_data = search_ai_trends(topic)
        result['search_data'] = search_data
        if search_data.get('sources'):
            result['data_sources'].append(f"searxng: {len(search_data['sources'])} 条结果")
    
    # AI 浪潮分析
    result['waves'] = analyze_ai_waves()
    
    # 投资机会分析
    result['opportunities'] = analyze_investment_opportunities()
    
    # 吴军投资原则
    result['principles'] = [
        '关注技术落地的实际场景',
        '选择有数据优势的公司',
        '避免纯概念炒作',
        '长期视角，耐心等待',
    ]
    
    return result


def print_analysis(result: dict) -> None:
    """打印分析结果"""
    print("="*60)
    print(f"🤖 AI 趋势分析：{result['topic']}")
    print("="*60)
    
    print(f"\n📊 数据来源")
    for source in result.get('data_sources', []):
        print(f"   • {source}")
    if not result.get('data_sources'):
        print(f"   ⚠️  无数据（需要 searxng 服务）")
    
    print(f"\n📈 AI 发展浪潮")
    for wave in result['waves']['waves']:
        print(f"\n   {wave['name']}")
        print(f"   时期：{wave['period']}")
        print(f"   特征：{wave['feature']}")
        if 'limitation' in wave:
            print(f"   局限：{wave['limitation']}")
    
    print(f"\n   当前阶段：{result['waves']['current_stage']}")
    print(f"   下一突破：{result['waves']['next_breakthrough']}")
    
    print(f"\n💰 投资机会")
    for layer in result['opportunities']['layers']:
        print(f"\n   {layer['name']}")
        print(f"   描述：{layer['description']}")
        print(f"   例子：{', '.join(layer['examples'])}")
        print(f"   特点：{layer['characteristics']}")
    
    print(f"\n💡 投资建议")
    print(f"   {result['opportunities']['recommendation']}")
    
    print(f"\n📝 投资原则")
    for principle in result['principles']:
        print(f"   • {principle}")
    
    print(f"\n📝 使用说明")
    print(f"   1. 使用 searxng 搜索获取最新趋势")
    print(f"   2. 理解 AI 发展浪潮")
    print(f"   3. 选择合适投资层次")
    print(f"   4. 长期视角，避免炒作")


def main():
    """主函数"""
    topic = sys.argv[1] if len(sys.argv) > 1 else '人工智能'
    use_search = '--search' in sys.argv
    
    if use_search:
        print(f"🔍 搜索 {topic} 趋势数据...")
    
    result = analyze_trend(topic, use_search)
    print_analysis(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
