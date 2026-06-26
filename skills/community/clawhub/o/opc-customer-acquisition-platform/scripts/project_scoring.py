#!/usr/bin/env python3
"""
评标打分计算脚本
功能：根据竞标方的各项得分计算综合得分并生成排名
"""

def calculate_credit_score(credit_level, bonus=0):
    """计算信用评级得分（权重30%，满分30分）"""
    level_coefficients = {'S': 1.2, 'A': 1.0, 'B': 0.9, 'C': 0.7, 'D': 0.5}
    if credit_level not in level_coefficients:
        return 0
    score = level_coefficients[credit_level] * 30 + bonus
    return min(score, 30)  # 封顶30分

def calculate_performance_score(project_count, good_rate, deductions=0):
    """计算历史业绩得分（权重25%，满分25分）"""
    count_score = min(project_count * 3, 15)  # 最多15分
    rate_score = min(good_rate / 10 * 2, 10)  # 最多10分
    return count_score + rate_score - deductions

def calculate_proposal_score(Completeness, Innovation, Feasibility):
    """计算方案质量得分（权重25%，满分25分）"""
    return Completeness + Innovation + Feasibility

def calculate_price_score(offered_price, guide_price_low, guide_price_high):
    """计算报价合理性得分（权重15%，满分15分）"""
    guide_mid = (guide_price_low + guide_price_high) / 2
    
    if offered_price == guide_mid:
        return 15
    elif guide_price_low * 0.8 <= offered_price <= guide_mid:
        ratio = (offered_price - guide_price_low * 0.8) / (guide_mid - guide_price_low * 0.8)
        return 13 + ratio * 2
    elif guide_mid <= offered_price <= guide_price_high * 1.2:
        ratio = (guide_price_high * 1.2 - offered_price) / (guide_price_high * 1.2 - guide_mid)
        return 13 + ratio * 2
    elif guide_price_low * 0.6 <= offered_price < guide_price_low * 0.8:
        return 10 + (offered_price - guide_price_low * 0.6) / (guide_price_low * 0.2) * 2
    elif guide_price_high * 1.2 < offered_price <= guide_price_high * 1.5:
        return 10 + (guide_price_high * 1.5 - offered_price) / (guide_price_high * 0.3) * 2
    else:
        return 5  # 恶意低价或虚高

def calculate_time_score(commit_days, required_days):
    """计算时间承诺得分（权重5%，满分5分）"""
    if commit_days < required_days:
        return 5
    elif commit_days == required_days:
        return 4
    elif commit_days <= required_days * 1.2:
        return 3
    elif commit_days <= required_days * 1.5:
        return 1
    else:
        return 0

def calculate_total_score(credit_score, performance_score, proposal_score, price_score, time_score):
    """计算综合得分（满分100分）"""
    return credit_score + performance_score + proposal_score + price_score + time_score

def generate_ranking(bidders):
    """
    生成竞标排名
    
    参数:
        bidders: 竞标方列表，每个元素是包含以下字段的字典:
            - name: 竞标方名称
            - credit_level: 信用等级 (S/A/B/C/D)
            - credit_bonus: 信用加分
            - project_count: 历史项目数
            - good_rate: 好评率 (0-100)
            - deductions: 扣分记录
            - completeness: 方案完整性得分 (0-10)
            - innovation: 创新性得分 (0-8)
            - feasibility: 可行性得分 (0-7)
            - offered_price: 报价
            - guide_price_low: 指导价下限
            - guide_price_high: 指导价上限
            - commit_days: 承诺工期
            - required_days: 要求工期
    
    返回:
        排序后的竞标方列表
    """
    results = []
    
    for bidder in bidders:
        credit_score = calculate_credit_score(bidder.get('credit_level', 'C'), bidder.get('credit_bonus', 0))
        performance_score = calculate_performance_score(
            bidder.get('project_count', 0),
            bidder.get('good_rate', 0),
            bidder.get('deductions', 0)
        )
        proposal_score = calculate_proposal_score(
            bidder.get('completeness', 0),
            bidder.get('innovation', 0),
            bidder.get('feasibility', 0)
        )
        price_score = calculate_price_score(
            bidder.get('offered_price', 0),
            bidder.get('guide_price_low', 0),
            bidder.get('guide_price_high', 0)
        )
        time_score = calculate_time_score(
            bidder.get('commit_days', 0),
            bidder.get('required_days', 0)
        )
        total_score = calculate_total_score(
            credit_score, performance_score, proposal_score, price_score, time_score
        )
        
        results.append({
            'name': bidder.get('name', '未知'),
            'credit_score': round(credit_score, 2),
            'performance_score': round(performance_score, 2),
            'proposal_score': round(proposal_score, 2),
            'price_score': round(price_score, 2),
            'time_score': round(time_score, 2),
            'total_score': round(total_score, 2)
        })
    
    # 按总分排序
    results.sort(key=lambda x: x['total_score'], reverse=True)
    
    # 添加排名
    for i, result in enumerate(results):
        result['rank'] = i + 1
    
    return results

def print_evaluation_report(results, guide_price_low, guide_price_high, required_days):
    """打印评标报告"""
    print("=" * 80)
    print("评标打分报告".center(70))
    print("=" * 80)
    print(f"指导价区间：{guide_price_low:.2f} - {guide_price_high:.2f} 元")
    print(f"要求工期：{required_days} 天")
    print("=" * 80)
    
    for result in results:
        print(f"\n【第{result['rank']}名】{result['name']}")
        print("-" * 40)
        print(f"  信用评级得分(30分)：{result['credit_score']:.2f}")
        print(f"  历史业绩得分(25分)：{result['performance_score']:.2f}")
        print(f"  方案质量得分(25分)：{result['proposal_score']:.2f}")
        print(f"  报价合理性(15分)：{result['price_score']:.2f}")
        print(f"  时间承诺得分(5分)：{result['time_score']:.2f}")
        print(f"  {'=' * 30}")
        print(f"  综合得分(100分)：{result['total_score']:.2f}")
    
    print("\n" + "=" * 80)
    print(f"推荐挂帅人：{results[0]['name']}")
    print("=" * 80)

# 示例使用
if __name__ == "__main__":
    # 示例竞标方数据
    bidders = [
        {
            'name': '竞标方A',
            'credit_level': 'A',
            'credit_bonus': 0,
            'project_count': 5,
            'good_rate': 95,
            'deductions': 0,
            'completeness': 9,
            'innovation': 6,
            'feasibility': 6,
            'offered_price': 50000,
            'guide_price_low': 40000,
            'guide_price_high': 60000,
            'commit_days': 30,
            'required_days': 30
        },
        {
            'name': '竞标方B',
            'credit_level': 'B',
            'credit_bonus': 2,
            'project_count': 3,
            'good_rate': 85,
            'deductions': 0,
            'completeness': 8,
            'innovation': 5,
            'feasibility': 5,
            'offered_price': 48000,
            'guide_price_low': 40000,
            'guide_price_high': 60000,
            'commit_days': 28,
            'required_days': 30
        },
        {
            'name': '竞标方C',
            'credit_level': 'S',
            'credit_bonus': 0,
            'project_count': 8,
            'good_rate': 98,
            'deductions': 0,
            'completeness': 10,
            'innovation': 7,
            'feasibility': 7,
            'offered_price': 55000,
            'guide_price_low': 40000,
            'guide_price_high': 60000,
            'commit_days': 25,
            'required_days': 30
        }
    ]
    
    # 生成排名
    results = generate_ranking(bidders)
    
    # 打印报告
    print_evaluation_report(results, 40000, 60000, 30)
