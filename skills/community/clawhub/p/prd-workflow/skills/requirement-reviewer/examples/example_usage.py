#!/usr/bin/env python3
"""
Requirement Reviewer 使用示例

演示如何使用迭代评审引擎
"""

import sys
import os

# 添加引擎路径
engines_path = os.path.join(os.path.dirname(__file__), '..', 'engines')
sys.path.insert(0, engines_path)

from review_engine import IterativeReviewer, PRDReviewer
from format_checker import FormatChecker


def simple_review_example():
    """基础评审示例"""
    print("="*60)
    print("示例 1: 基础评审")
    print("="*60)
    
    test_prd = """
# AI 养老规划助手 PRD

## 产品概述
产品风险等级：R3（平衡型）
目标用户：银行理财经理

## 功能设计
功能 1: 用户注册
功能 2: 养老测算
功能 3: 产品推荐

## 验收标准
用例 1: 用户注册
Given 用户打开注册页面
When 填写手机号
Then 注册成功
    """
    
    reviewer = PRDReviewer()
    result = reviewer.review(test_prd)
    
    print(f"\n评审结果:")
    print(f"得分：{result['overall_score']}/100")
    print(f"状态：{result['status']}")
    print(f"问题数：{result['total_issues']}")
    print(f"严重问题：{result['critical_issues']}")
    
    print(f"\n检查项得分:")
    for check_type, check_result in result['check_results'].items():
        print(f"  {check_type}: {check_result['score']}/100")
    
    print(f"\n改进建议 (Top 5):")
    for i, sug in enumerate(result['suggestions'][:5], 1):
        print(f"  {i}. [{sug['priority']}] {sug['title']}")


def iterative_review_example():
    """迭代评审示例"""
    print("\n" + "="*60)
    print("示例 2: 迭代评审")
    print("="*60)
    
    test_prd = """
# AI 养老规划助手 PRD

## 产品概述
产品风险等级：R3

## 功能设计
功能 1: 用户注册
功能 2: 养老测算
    """
    
    # 模拟改进函数
    def improve_prd(prd_content, issues):
        improved = prd_content
        for issue in issues:
            if "风险等级" in issue.get('title', ''):
                improved += "\n\n## 风险揭示\n产品风险等级：R3（平衡型）\n客户风险等级：R3"
            if "边界场景" in issue.get('title', ''):
                improved += "\n\n## 异常处理\n支持网络中断重试、支付失败处理"
        return improved
    
    reviewer = IterativeReviewer(max_loops=3, threshold=0.05)
    result = reviewer.review_with_iteration(test_prd, improve_func=improve_prd)
    
    print(f"\n迭代结果:")
    print(f"迭代轮数：{result['loop_count']}")
    print(f"退出原因：{result['exit_reason']}")
    print(f"最终得分：{result['final_report']['overall_score']}/100")
    
    print(f"\n改进历史:")
    for i, hist in enumerate(result['improvement_history'], 1):
        print(f"  第{i+1}轮：新增{hist['new_issues_count']}个问题，修复{hist['fixed_issues_count']}个问题")


def format_check_example(word_path=None):
    """表面规范检查示例"""
    print("\n" + "="*60)
    print("示例 3: 表面规范检查")
    print("="*60)
    
    if not word_path:
        print("请提供 Word 文档路径")
        print("用法：python example_usage.py <word 文档路径>")
        return
    
    checker = FormatChecker()
    result = checker.check(word_path)
    
    print(f"\n检查结果:")
    print(f"文件：{os.path.basename(word_path)}")
    print(f"得分：{result['score']}/100")
    print(f"状态：{result['status']}")
    
    print(f"\n统计信息:")
    for key, value in result.get('statistics', {}).items():
        print(f"  {key}: {value}")
    
    print(f"\n问题列表:")
    if result['issues']:
        for issue in result['issues'][:10]:
            print(f"  - [{issue['severity']}] {issue['title']}")
    else:
        print("  ✅ 无问题")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        # 有参数：检查 Word 文档
        word_path = sys.argv[1]
        format_check_example(word_path)
    else:
        # 无参数：运行示例
        print("Requirement Reviewer v2.0 使用示例")
        print("="*60)
        
        simple_review_example()
        iterative_review_example()
        
        print("\n" + "="*60)
        print("提示:")
        print("  python example_usage.py <Word 文档路径>  # 检查 Word 文档")
        print("  python example_usage.py                  # 运行示例")
        print("="*60)


if __name__ == "__main__":
    main()
