#!/usr/bin/env python3
"""
MyStock Skill Trigger Test Script

This script tests various scenarios that should trigger the MyStock skill.
"""

import requests
import json
from typing import Dict, List


class SkillTriggerTest:
    """Test skill trigger conditions"""
    
    def __init__(self, api_base: str = "http://localhost:8000"):
        self.api_base = api_base
        self.results = []
    
    def test_trigger(self, query: str, expected_trigger: bool, description: str):
        """Test if a query should trigger the skill"""
        # Check trigger keywords
        trigger_keywords = [
            # Stock related
            '股票', '股价', '行情', '涨跌', '报价',
            # Analysis related
            '分析', '走势', '趋势',
            # Limit-up related
            '打板', '涨停', '首板',
            # Shareholder related
            '股东增持', '回购', '高管增持',
            # Portfolio related
            '持仓', '自选', '投资组合',
            # Research related
            '研究', '查询', '获取'
        ]
        
        should_trigger = any(kw in query.lower() for kw in trigger_keywords)
        
        result = {
            'query': query,
            'description': description,
            'should_trigger': should_trigger,
            'expected': expected_trigger,
            'passed': should_trigger == expected_trigger
        }
        
        self.results.append(result)
        return should_trigger
    
    def test_api_functionality(self):
        """Test if API endpoints are working"""
        tests = []
        
        # Test 1: Get portfolio
        try:
            resp = requests.get(f"{self.api_base}/api/portfolio", timeout=5)
            tests.append({
                'name': 'Get Portfolio',
                'success': resp.status_code == 200,
                'status_code': resp.status_code
            })
        except Exception as e:
            tests.append({
                'name': 'Get Portfolio',
                'success': False,
                'error': str(e)
            })
        
        # Test 2: Get shareholder activity
        try:
            resp = requests.get(f"{self.api_base}/api/shareholder-activity", timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                tests.append({
                    'name': 'Get Shareholder Activity',
                    'success': True,
                    'status_code': resp.status_code,
                    'items': {
                        'shareholding_increase': data.get('shareholding_increase', {}).get('total', 0),
                        'buyback': data.get('buyback', {}).get('total', 0),
                        'executive_increase': data.get('executive_increase', {}).get('total', 0)
                    }
                })
            else:
                tests.append({
                    'name': 'Get Shareholder Activity',
                    'success': False,
                    'status_code': resp.status_code
                })
        except Exception as e:
            tests.append({
                'name': 'Get Shareholder Activity',
                'success': False,
                'error': str(e)
            })
        
        # Test 3: Search stock
        try:
            resp = requests.get(f"{self.api_base}/api/search-stock?q=茅台", timeout=5)
            tests.append({
                'name': 'Search Stock',
                'success': resp.status_code == 200,
                'status_code': resp.status_code
            })
        except Exception as e:
            tests.append({
                'name': 'Search Stock',
                'success': False,
                'error': str(e)
            })
        
        return tests
    
    def print_report(self):
        """Print test report"""
        print("=" * 80)
        print("MyStock Skill 测试报告")
        print("=" * 80)
        print()
        
        print("📋 触发条件测试:")
        print("-" * 80)
        for i, result in enumerate(self.results, 1):
            status = "✅" if result['passed'] else "❌"
            print(f"{i}. {status} {result['description']}")
            print(f"   查询: {result['query']}")
            print(f"   应触发: {result['expected']} | 实际: {result['should_trigger']}")
            print()
        
        print()
        print("🔧 API 功能测试:")
        print("-" * 80)
        api_tests = self.test_api_functionality()
        for test in api_tests:
            status = "✅" if test['success'] else "❌"
            print(f"{status} {test['name']}")
            if test['success']:
                print(f"   Status: {test.get('status_code', 'N/A')}")
                if 'items' in test:
                    print(f"   数据: {test['items']}")
            else:
                print(f"   Error: {test.get('error', 'Unknown error')}")
        
        print()
        print("=" * 80)
        total = len(self.results)
        passed = sum(1 for r in self.results if r['passed'])
        api_passed = sum(1 for t in api_tests if t['success'])
        print(f"总结: 触发测试 {passed}/{total} 通过, API测试 {api_passed}/{len(api_tests)} 通过")
        print("=" * 80)


def main():
    """Run all tests"""
    tester = SkillTriggerTest()
    
    print("开始 MyStock Skill 测试...")
    print()
    
    # Test trigger conditions
    test_cases = [
        # Should trigger cases
        (True, "查询贵州茅台的股价", "股票查询"),
        (True, "今天有哪些涨停板", "打板分析"),
        (True, "查看最近的股东增持", "股东动态"),
        (True, "分析回购概念的股票", "回购概念"),
        (True, "管理我的投资组合", "投资组合"),
        (True, "茅台走势怎么样", "股票分析"),
        (True, "获取高管增持数据", "高管增持"),
        
        # Should not trigger cases
        (False, "今天天气怎么样", "无关查询"),
        (False, "帮我写一首诗", "无关查询"),
        (False, "计算1+1等于多少", "无关查询"),
    ]
    
    for expected, query, description in test_cases:
        tester.test_trigger(query, expected, description)
    
    # Print report
    tester.print_report()


if __name__ == "__main__":
    main()
