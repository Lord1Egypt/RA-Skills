#!/usr/bin/env python3
"""
文化分析器 - 基于段永平的"本分"文化分析

无需外部数据，定性分析企业文化
"""

import sys
import os
from datetime import datetime


# 企业文化评估维度
CULTURE_DIMENSIONS = {
    'benfen': {
        'name': '本分',
        'questions': [
            '公司是否诚信对待客户和员工？',
            '是否专注于做好产品而非短期利益？',
            '是否在能力圈内做事？',
        ],
    },
    'user_focus': {
        'name': '用户导向',
        'questions': [
            '公司是否真正以用户为中心？',
            '产品是否解决用户真实需求？',
            '是否持续改进用户体验？',
        ],
    },
    'long_term': {
        'name': '长期主义',
        'questions': [
            '公司是否注重长期价值而非短期业绩？',
            '是否愿意为长期利益牺牲短期利益？',
            '是否有清晰的长期愿景？',
        ],
    },
    'talent': {
        'name': '人才理念',
        'questions': [
            '公司是否重视人才？',
            '是否有公平的激励机制？',
            '员工是否认同公司文化？',
        ],
    },
}


def evaluate_culture_dimension(dimension_key: str, user_answers: list = None) -> dict:
    """
    评估文化维度
    
    Args:
        dimension_key: 维度键
        user_answers: 用户回答列表
    
    Returns:
        评估结果
    """
    dimension = CULTURE_DIMENSIONS[dimension_key]
    
    result = {
        'name': dimension['name'],
        'score': 0,
        'max_score': len(dimension['questions']),
        'answers': [],
    }
    
    for i, question in enumerate(dimension['questions']):
        answer = {
            'question': question,
            'score': 3,  # 默认中等
            'note': '',
        }
        
        # 如果有用户回答，根据回答评分
        if user_answers and i < len(user_answers):
            user_ans = user_answers[i]
            if '是' in user_ans or '符合' in user_ans:
                answer['score'] = 5
            elif '否' in user_ans or '不符合' in user_ans:
                answer['score'] = 1
        
        result['answers'].append(answer)
        result['score'] += answer['score']
    
    return result


def analyze_culture(company_name: str, user_answers: dict = None) -> dict:
    """
    企业文化完整分析
    
    Args:
        company_name: 公司名称
        user_answers: 用户回答字典
    
    Returns:
        分析结果字典
    """
    result = {
        'company': company_name,
        'timestamp': datetime.now().isoformat(),
        'framework': '段永平文化分析框架',
    }
    
    # 评估各维度
    result['dimensions'] = {}
    total_score = 0
    max_score = 0
    
    for dim_key in CULTURE_DIMENSIONS.keys():
        answers = user_answers.get(dim_key, []) if user_answers else None
        result['dimensions'][dim_key] = evaluate_culture_dimension(dim_key, answers)
        total_score += result['dimensions'][dim_key]['score']
        max_score += result['dimensions'][dim_key]['max_score']
    
    # 综合评分
    result['total_score'] = total_score
    result['max_score'] = max_score
    result['percentage'] = (total_score / max_score * 100) if max_score > 0 else 0
    
    # 文化评级
    if result['percentage'] >= 80:
        result['rating'] = '优秀'
        result['description'] = '强大的企业文化，长期竞争优势'
    elif result['percentage'] >= 60:
        result['rating'] = '良好'
        result['description'] = '较好的企业文化，有一定竞争优势'
    elif result['percentage'] >= 40:
        result['rating'] = '一般'
        result['description'] = '企业文化一般，无明显优势'
    else:
        result['rating'] = '需改进'
        result['description'] = '企业文化存在问题，需谨慎'
    
    return result


def print_analysis(result: dict) -> None:
    """打印分析结果"""
    print("="*60)
    print(f"🏛️ 文化分析器：{result['company']}")
    print("="*60)
    
    print(f"\n📋 分析框架")
    print(f"   {result['framework']}")
    
    print(f"\n📊 文化维度评估")
    for dim_key, dim_data in result['dimensions'].items():
        score_pct = dim_data['score'] / dim_data['max_score'] * 100
        score_icon = '⭐' * int(score_pct / 20)
        print(f"\n   {dim_data['name']} ({dim_data['score']}/{dim_data['max_score']}分) {score_icon}")
        for ans in dim_data['answers']:
            ans_icon = '✅' if ans['score'] >= 4 else '➡️' if ans['score'] >= 3 else '❌'
            print(f"     {ans_icon} {ans['question']}")
    
    print(f"\n📈 综合评分")
    print(f"   总分：{result['total_score']}/{result['max_score']} ({result['percentage']:.1f}%)")
    print(f"   评级：{result['rating']}")
    print(f"   描述：{result['description']}")
    
    print(f"\n📝 使用说明")
    print(f"   1. 诚实回答每个问题")
    print(f"   2. 基于事实和观察，而非印象")
    print(f"   3. 关注长期表现，而非短期行为")
    print(f"   4. 文化需要时间验证")


def main():
    """主函数"""
    company_name = sys.argv[1] if len(sys.argv) > 1 else '目标公司'
    
    result = analyze_culture(company_name)
    print_analysis(result)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
