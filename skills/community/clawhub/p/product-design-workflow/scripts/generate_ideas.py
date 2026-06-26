#!/usr/bin/env python3
"""
财经探子头脑风暴 - 生成点子脚本
"""
import os
import sys
from datetime import datetime

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDEAS_DIR = os.path.join(PROJECT_ROOT, 'ideas')

def get_date_str():
    """获取今天的日期字符串"""
    return datetime.now().strftime('%Y-%m-%d')

def create_idea_dir(slug):
    """创建点子目录"""
    date_str = get_date_str()
    idea_dir = os.path.join(IDEAS_DIR, f'{date_str}-{slug}')
    os.makedirs(idea_dir, exist_ok=True)
    return idea_dir

def main():
    """主函数"""
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"点子目录: {IDEAS_DIR}")
    print("请手动生成点子，或使用AI生成")

if __name__ == '__main__':
    main()
