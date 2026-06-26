#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化测试版本
"""

import pandas as pd
import numpy as np
import os
import glob
import chardet
from datetime import datetime

def simple_test():
    """简单测试函数"""
    data_dir = "/Users/zhouhao/Documents/投放数据"
    
    print("🚀 开始简单测试...")
    
    # 只测试2026年1月的数据
    super_file = "/Users/zhouhao/Documents/投放数据/26年/超级直播/2026-01超级直播.csv"
    
    if os.path.exists(super_file):
        print(f"✅ 找到文件: {super_file}")
        
        # 读取文件
        df = pd.read_csv(super_file, encoding='utf-8')
        print(f"✅ 读取成功，形状: {df.shape}")
        print(f"字段: {list(df.columns)[:10]}...")  # 只显示前10个字段
        
        # 简单的数值转换测试
        if '花费' in df.columns:
            df['花费'] = pd.to_numeric(df['花费'], errors='coerce')
            print(f"花费字段类型: {df['花费'].dtype}")
            print(f"花费统计: 总和={df['花费'].sum():.2f}, 均值={df['花费'].mean():.2f}")
        
        if '总成交金额' in df.columns:
            df['总成交金额'] = pd.to_numeric(df['总成交金额'], errors='coerce')
            print(f"总成交金额字段类型: {df['总成交金额'].dtype}")
        
        # 简单计算ROI
        if '花费' in df.columns and '总成交金额' in df.columns:
            roi = df['总成交金额'] / df['花费'].replace(0, np.nan)
            print(f"ROI计算成功，均值: {roi.mean():.2f}")
        
        print("✅ 简单测试完成!")
        return True
    else:
        print("❌ 文件不存在")
        return False

if __name__ == "__main__":
    simple_test()