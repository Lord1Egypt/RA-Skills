#!/usr/bin/env python3
"""
认知偏差检测器 - 深度分析投资决策中的认知偏差

无需外部数据，基于心理学原理
"""

import sys
import os
from datetime import datetime


# 详细认知偏差库
BIAS_LIBRARY = {
    '投资相关': [
        {
            'name': '确认偏误',
            'description': '只寻找支持自己观点的信息',
            'symptoms': [
                '只关注利好消息，忽略利空',
                '加入看多的社群，回避看空观点',
                '认为反对者"不懂"或"错了"',
            ],
            'mitigation': '主动寻找反面证据，列出 3 个看空理由',
            'severity': '高',
        },
        {
            'name': '过度自信',
            'description': '高估自己的预测能力',
            'symptoms': [
                '认为自己能"跑赢市场"',
                '频繁交易，相信自己的判断',
                '忽视运气因素，归因于能力',
            ],
            'mitigation': '记录所有预测，定期回顾准确率',
            'severity': '高',
        },
        {
            'name': '后见之明',
            'description': '事后认为"我早就知道"',
            'symptoms': [
                '事后说"我早就预料到了"',
                '认为成功是必然的',
                '忽视当时的不确定性',
            ],
            'mitigation': '保存决策时的思考过程，定期复盘',
            'severity': '中',
        },
        {
            'name': '代表性偏误',
            'description': '根据刻板印象做判断',
            'symptoms': [
                '认为"好公司=好股票"',
                '因为行业热门就买入',
                '忽视估值，只看故事',
            ],
            'mitigation': '区分"好公司"和"好投资"，检查估值',
            'severity': '中',
        },
    ],
    '情绪相关': [
        {
            'name': '损失厌恶',
            'description': '对损失的痛苦大于获得的快乐',
            'symptoms': [
                '死守亏损股票，不愿止损',
                '过早卖出盈利股票，锁定收益',
                '因为害怕而错过机会',
            ],
            'mitigation': '设定明确止损点，基于逻辑而非情绪',
            'severity': '高',
        },
        {
            'name': 'FOMO（错失恐惧）',
            'description': '害怕错过机会而盲目跟风',
            'symptoms': [
                '看到别人赚钱就着急买入',
                '在高位追涨',
                '因为"怕错过"而决策',
            ],
            'mitigation': '制定投资计划，严格执行，不跟风',
            'severity': '高',
        },
        {
            'name': '处置效应',
            'description': '过早卖出赢家，过久持有输家',
            'symptoms': [
                '盈利股票拿不住',
                '亏损股票变"长期投资"',
                '账户里都是亏损股',
            ],
            'mitigation': '基于基本面决策，而非盈亏状态',
            'severity': '中',
        },
    ],
    '信息处理': [
        {
            'name': '锚定效应',
            'description': '过度依赖某个初始信息',
            'symptoms': [
                '死守某个目标价',
                '以买入价为参考点',
                '忽视新信息，坚持原有判断',
            ],
            'mitigation': '多角度分析，定期更新假设',
            'severity': '中',
        },
        {
            'name': '可得性偏误',
            'description': '过度依赖容易获得的信息',
            'symptoms': [
                '只分析财报，不看行业',
                '相信媒体报道，不做独立研究',
                '忽视难以量化的因素',
            ],
            'mitigation': '主动搜寻全面信息，包括负面信息',
            'severity': '中',
        },
        {
            'name': '叙事谬误',
            'description': '被好听的故事迷惑',
            'symptoms': [
                '因为"赛道好"就买入',
                '相信"这次不一样"',
                '忽视数据，听信故事',
            ],
            'mitigation': '要求数据支持，验证故事真实性',
            'severity': '高',
        },
    ],
}


def detect_biases(user_responses: dict = None) -> dict:
    """
    检测认知偏差
    
    Args:
        user_responses: 用户回答（可选）
    
    Returns:
        检测结果字典
    """
    result = {
        'timestamp': datetime.now().isoformat(),
        'categories': {},
        'high_risk': [],
        'medium_risk': [],
        'total_biases': 0,
    }
    
    for category, biases in BIAS_LIBRARY.items():
        category_result = {
            'name': category,
            'biases': [],
            'risk_count': 0,
        }
        
        for bias in biases:
            bias_item = {
                'name': bias['name'],
                'description': bias['description'],
                'symptoms': bias['symptoms'],
                'mitigation': bias['mitigation'],
                'severity': bias['severity'],
                'detected': '可能',  # 默认需要用户确认
            }
            
            # 如果有用户回答，根据回答判断
            if user_responses:
                response = user_responses.get(bias['name'], 0)
                if response >= 3:  # 3 分以上认为可能存在
                    bias_item['detected'] = '是'
                    category_result['risk_count'] += 1
                    if bias['severity'] == '高':
                        result['high_risk'].append(bias['name'])
                    else:
                        result['medium_risk'].append(bias['name'])
                else:
                    bias_item['detected'] = '否'
            
            category_result['biases'].append(bias_item)
            result['total_biases'] += 1
        
        result['categories'][category] = category_result
    
    return result


def generate_report(detection_result: dict) -> dict:
    """
    生成偏差检测报告
    
    Args:
        detection_result: 检测结果
    
    Returns:
        报告字典
    """
    report = {
        'timestamp': detection_result['timestamp'],
        'summary': '',
        'risk_level': '未知',
        'recommendations': [],
        'action_items': [],
    }
    
    high_count = len(detection_result['high_risk'])
    medium_count = len(detection_result['medium_risk'])
    
    # 风险等级评估
    if high_count >= 3:
        report['risk_level'] = '高'
        report['summary'] = f'检测到 {high_count} 个高风险偏差，决策质量堪忧'
    elif high_count >= 1 or medium_count >= 3:
        report['risk_level'] = '中'
        report['summary'] = f'检测到 {high_count + medium_count} 个认知偏差，需要注意'
    else:
        report['risk_level'] = '低'
        report['summary'] = '认知偏差较少，决策质量良好'
    
    # 建议
    if high_count > 0:
        report['recommendations'].append('⚠️ 暂停决策，先处理高风险偏差')
        report['recommendations'].append('📝 列出反面证据，挑战自己的观点')
        report['recommendations'].append('🤔 寻求独立第三方意见')
    
    if medium_count > 0:
        report['recommendations'].append('📊 应用多元思维模型检查')
        report['recommendations'].append('📈 设定明确的决策标准')
    
    # 行动项
    for bias_name in detection_result['high_risk']:
        # 查找对应的缓解措施
        for category, biases in BIAS_LIBRARY.items():
            for bias in biases:
                if bias['name'] == bias_name:
                    report['action_items'].append({
                        'bias': bias_name,
                        'action': bias['mitigation'],
                    })
    
    return report


def print_report(result: dict, report: dict) -> None:
    """打印检测报告"""
    print("="*60)
    print("🧠 认知偏差检测报告")
    print("="*60)
    print(f"\n检测时间：{result['timestamp']}")
    
    # 按类别展示
    for category_name, category_data in result['categories'].items():
        print(f"\n📁 {category_name}")
        print(f"   已识别：{category_data['risk_count']}/{len(category_data['biases'])}")
        
        for bias in category_data['biases']:
            detected_icon = '⚠️' if bias['detected'] == '是' else '➡️'
            print(f"\n   {detected_icon} {bias['name']}")
            print(f"      描述：{bias['description']}")
            print(f"      症状：")
            for symptom in bias['symptoms'][:3]:
                print(f"        • {symptom}")
            print(f"      缓解：{bias['mitigation']}")
    
    # 总结
    print(f"\n{'='*60}")
    print(f"📊 总结")
    print(f"   风险等级：{report['risk_level']}")
    print(f"   高风险偏差：{len(report.get('high_risk', []))}")
    print(f"   中风险偏差：{len(report.get('medium_risk', []))}")
    print(f"\n{report['summary']}")
    
    # 建议
    print(f"\n💡 建议")
    for rec in report['recommendations']:
        print(f"   {rec}")
    
    # 行动项
    if report['action_items']:
        print(f"\n📋 行动项")
        for item in report['action_items']:
            print(f"   ⚠️ {item['bias']}")
            print(f"      → {item['action']}")
    
    # 使用说明
    print(f"\n📝 使用说明")
    print(f"   1. 诚实回答每个问题（0-5 分）")
    print(f"   2. 重点关注高风险偏差")
    print(f"   3. 执行建议的缓解措施")
    print(f"   4. 定期复盘，持续改进")


def main():
    """主函数"""
    # 简单演示模式（无用户输入）
    detection_result = detect_biases()
    report = generate_report(detection_result)
    print_report(detection_result, report)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
