#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v2.1 功能验证测试
测试数据提取和质量评分功能
"""

import sys
from pathlib import Path

# 添加路径
sys.path.insert(0, str(Path(__file__).parent))

from extractor import DataExtractor
from colorama import init, Fore, Style

init(autoreset=True)


def test_data_extraction():
    """测试数据提取功能"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}测试 1: 数据提取功能{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    extractor = DataExtractor()
    
    # 测试文本（模拟 AI 回复）
    test_texts = [
        {
            'name': '时事分析',
            'text': """
            根据最新数据，2026 年全球油价预计将上涨 15%，达到每桶 95 美元。
            国际能源署（IEA）预测，到 2026 年底，布伦特原油价格可能突破 100 美元大关。
            
            关键洞察：
            1. 中东局势紧张是主要推动因素
            2. 全球需求增长 3.2%
            3. OPEC+ 减产协议延长至 2026 年 12 月
            
            据高盛报告，油价上涨可能导致全球通胀率上升 0.5 个百分点。
            预计美联储将推迟降息至 2026 年 Q4。
            """
        },
        {
            'name': '技术对比',
            'text': """
            Python 在 2025 年的市场份额达到 28.5%，同比增长 12%。
            Java 市场份额为 25.3%，同比下降 2%。
            
            性能对比：
            - Python 启动时间：0.5 秒
            - Java 启动时间：0.2 秒
            
            根据 Stack Overflow 2025 年开发者调查：
            - 45.2% 的开发者使用 Python
            - 35.8% 的开发者使用 Java
            
            预计 2026 年 Python 市场份额将突破 30%。
            """
        },
        {
            'name': '产品评测',
            'text': """
            iPhone 16 Pro 售价 999 美元，比前代上涨 100 美元。
            电池容量 4500mAh，续航提升 20%。
            
            关键改进：
            1. A18 芯片性能提升 35%
            2. 摄像头像素升级到 4800 万
            3. 屏幕亮度达到 2000 尼特
            
            根据我们的测试：
            - 充电速度：0-80% 需 30 分钟
            - 重量：215 克，增加 10 克
            
            推荐指数：8.5/10
            """
        }
    ]
    
    for test in test_texts:
        print(f"{Fore.YELLOW}[{test['name']}]{Style.RESET_ALL}")
        data = extractor.extract_all(test['text'])
        
        print(f"  百分比：{len(data['percentages'])} 个")
        print(f"  日期：{len(data['dates'])} 个")
        print(f"  预测：{len(data['predictions'])} 个")
        print(f"  关键洞察：{len(data['key_insights'])} 条")
        print(f"  数据点：{len(data['data_points'])} 个")
        
        # 显示部分结果
        if data['percentages']:
            values = [f"{p['value']}%" for p in data['percentages'][:3]]
            print(f"  {Fore.GREEN}示例：{', '.join(values)}{Style.RESET_ALL}")
        
        print()
    
    return True


def test_quality_scoring():
    """测试质量评分功能"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}测试 2: 质量评分功能{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    extractor = DataExtractor()
    
    # 不同质量的回复
    test_cases = [
        {
            'name': '优秀回复',
            'text': """
            ## 2026 年全球经济展望
            
            ### 核心观点
            根据 IMF 最新报告，2026 年全球 GDP 预计增长 3.5%，比 2025 年上升 0.3 个百分点。
            
            ### 关键数据
            1. 美国 GDP 增长：2.8%（2025 年：2.5%）
            2. 中国 GDP 增长：5.2%（2025 年：5.0%）
            3. 欧元区 GDP 增长：1.9%（2025 年：1.5%）
            
            ### 通胀预测
            - 美国 CPI：2.5%（2025 年底）
            - 中国 CPI：1.8%（2025 年底）
            - 欧元区 CPI：2.0%（2025 年底）
            
            ### 风险提示
            据高盛分析，主要风险包括：
            1. 地缘政治紧张（概率 40%）
            2. 供应链中断（概率 25%）
            3. 金融市场波动（概率 35%）
            
            ### 参考来源
            - IMF 世界经济展望（2026 年 1 月）
            - 高盛全球经济报告（2026-01-15）
            - 世界银行数据
            """
        },
        {
            'name': '良好回复',
            'text': """
            2026 年经济预计会好转。GDP 增长可能在 3-4% 之间。
            
            主要经济体：
            - 美国：预计增长 2-3%
            - 中国：预计增长 5% 左右
            - 欧洲：复苏较慢
            
            通胀会有所缓解，但不会太快。
            """
        },
        {
            'name': '一般回复',
            'text': """
            经济情况还可以，比今年好一些。
            各国都在努力发展经济。
            具体情况要看各方面因素。
            """
        }
    ]
    
    results = []
    for test in test_cases:
        print(f"{Fore.YELLOW}[{test['name']}]{Style.RESET_ALL}")
        quality = extractor.calculate_quality_score(test['text'], test['name'])
        results.append(quality)
        
        print(f"  总分：{Fore.GREEN}{quality['total_score']}{Style.RESET_ALL} ({quality['level']})")
        print(f"  字数：{quality['breakdown']['word_count']['value']}")
        print(f"  数据点：{quality['breakdown']['data_points']['value']}")
        print()
    
    # 生成对比表
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}质量评分对比表{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    mock_results = [
        {'platform': r['platform'], 'quality_score': r}
        for r in results
    ]
    
    table = extractor.generate_comparison_table(mock_results)
    print(table)
    
    return True


def test_comparison_table():
    """测试对比表生成"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}测试 3: 对比表生成功能{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    extractor = DataExtractor()
    
    # 模拟多家 AI 的结果
    mock_results = [
        {
            'platform': 'DeepSeek',
            'extracted_data': {
                'percentages': [{'value': 15.0}, {'value': 3.2}, {'value': 0.5}],
                'predictions': [{'value': '95', 'unit': '美元'}]
            },
            'quality_score': {
                'total_score': 85.5,
                'breakdown': {
                    'word_count': {'score': 100},
                    'data_points': {'score': 100},
                    'structure': {'score': 75},
                    'sources': {'score': 80},
                    'specificity': {'score': 70}
                },
                'level': '优秀'
            }
        },
        {
            'platform': 'Qwen',
            'extracted_data': {
                'percentages': [{'value': 18.0}, {'value': 4.1}, {'value': 0.7}],
                'predictions': [{'value': '100', 'unit': '美元'}]
            },
            'quality_score': {
                'total_score': 82.0,
                'breakdown': {
                    'word_count': {'score': 80},
                    'data_points': {'score': 80},
                    'structure': {'score': 100},
                    'sources': {'score': 80},
                    'specificity': {'score': 65}
                },
                'level': '优秀'
            }
        },
        {
            'platform': '豆包',
            'extracted_data': {
                'percentages': [{'value': 14.0}, {'value': 3.5}, {'value': 0.6}],
                'predictions': [{'value': '98', 'unit': '美元'}]
            },
            'quality_score': {
                'total_score': 79.5,
                'breakdown': {
                    'word_count': {'score': 100},
                    'data_points': {'score': 80},
                    'structure': {'score': 75},
                    'sources': {'score': 80},
                    'specificity': {'score': 75}
                },
                'level': '良好'
            }
        },
        {
            'platform': 'Kimi',
            'extracted_data': {
                'percentages': [{'value': 16.0}, {'value': 3.8}, {'value': 0.5}],
                'predictions': [{'value': '105', 'unit': '美元'}]
            },
            'quality_score': {
                'total_score': 88.0,
                'breakdown': {
                    'word_count': {'score': 80},
                    'data_points': {'score': 100},
                    'structure': {'score': 75},
                    'sources': {'score': 100},
                    'specificity': {'score': 70}
                },
                'level': '优秀'
            }
        }
    ]
    
    table = extractor.generate_comparison_table(mock_results)
    print(table)
    print()
    
    return True


def main():
    """主测试函数"""
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}  Multi-AI Search Analysis v2.1 - 功能验证测试{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
    
    all_passed = True
    
    # 测试 1: 数据提取
    if not test_data_extraction():
        all_passed = False
    
    # 测试 2: 质量评分
    if not test_quality_scoring():
        all_passed = False
    
    # 测试 3: 对比表生成
    if not test_comparison_table():
        all_passed = False
    
    # 总结
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}测试总结{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    if all_passed:
        print(f"{Fore.GREEN}[OK] 所有测试通过！{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}下一步：{Style.RESET_ALL}")
        print(f"  运行完整分析：python scripts/run.py -t \"你的主题\"")
    else:
        print(f"{Fore.RED}[FAIL] 部分测试失败{Style.RESET_ALL}")
    
    print()


if __name__ == '__main__':
    main()
