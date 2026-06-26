#!/usr/bin/env python3
"""
规则检查脚本 - 检查idea是否符合要求
"""
import os
import re
import sys
from pathlib import Path

# 禁止的关键词（加密货币相关）
FORBIDDEN_KEYWORDS = [
    '加密货币', '加密', 'crypto', 'Cryptocurrency',
    'DeFi', 'Web3', 'web3',
    '智能合约', 'smart contract', 'Smart Contract',
    '区块链', 'blockchain', 'Blockchain',
    '比特币', 'bitcoin', 'Bitcoin', 'BTC',
    '以太坊', 'ethereum', 'Ethereum', 'ETH',
    '币圈', '链圈',
    'ICO', 'IDO', 'IEO',
    'NFT', 'nft',
    '交易所', 'exchange'
]

# 允许的主题
ALLOWED_TOPICS = ['市场行情', 'A股', '基金']

# 允许的受众类型
ALLOWED_AUDIENCES = ['小白向', '普通向']


def check_idea_file(idea_file: Path) -> list:
    """检查单个idea文件"""
    errors = []
    
    if not idea_file.exists():
        errors.append(f"❌ 文件不存在: {idea_file}")
        return errors
    
    content = idea_file.read_text()
    
    # 1. 检查标签
    label_match = re.search(r'\*\*标签\*\*:\s*([^\|]+)\s*\|\s*([^\n]+)', content)
    if not label_match:
        errors.append("❌ 缺少标签，格式应为：**标签**: [市场行情/A股/基金] | [小白向/普通向]")
    else:
        topic = label_match.group(1).strip()
        audience = label_match.group(2).strip()
        
        if topic not in ALLOWED_TOPICS:
            errors.append(f"❌ 主题 '{topic}' 不合法，必须是: {ALLOWED_TOPICS}")
        
        if audience not in ALLOWED_AUDIENCES:
            errors.append(f"❌ 受众类型 '{audience}' 不合法，必须是: {ALLOWED_AUDIENCES}")
    
    # 2. 检查禁止关键词
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in content:
            errors.append(f"❌ 发现禁止关键词: '{keyword}'")
    
    return errors


def check_date_ideas(date_str: str) -> dict:
    """检查某一天的所有idea"""
    project_root = Path(__file__).parent.parent
    ideas_dir = project_root / 'ideas'
    
    results = {
        'date': date_str,
        'total': 0,
        'passed': 0,
        'failed': 0,
        'details': {}
    }
    
    # 查找当天的所有idea目录
    for idea_dir in ideas_dir.glob(f'{date_str}-*'):
        if not idea_dir.is_dir():
            continue
        
        results['total'] += 1
        idea_file = idea_dir / 'idea.md'
        
        errors = check_idea_file(idea_file)
        
        results['details'][idea_dir.name] = {
            'passed': len(errors) == 0,
            'errors': errors
        }
        
        if errors:
            results['failed'] += 1
        else:
            results['passed'] += 1
    
    return results


def print_results(results: dict):
    """打印检查结果"""
    print(f"\n📋 检查日期: {results['date']}")
    print(f"📊 总计: {results['total']} 个idea")
    print(f"✅ 通过: {results['passed']}")
    print(f"❌ 失败: {results['failed']}")
    
    if results['details']:
        print("\n🔍 详细结果:")
        for idea_name, detail in results['details'].items():
            status = "✅" if detail['passed'] else "❌"
            print(f"\n{status} {idea_name}")
            if not detail['passed']:
                for error in detail['errors']:
                    print(f"   {error}")
    
    print()


def main():
    """主函数"""
    from datetime import datetime
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    
    results = check_date_ideas(date_str)
    print_results(results)
    
    return 0 if results['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
