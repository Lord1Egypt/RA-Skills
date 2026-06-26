#!/usr/bin/env python3
"""
招标文件分析脚本
用于分析Excel招标文件并提取关键信息
"""

import pandas as pd
import json
import sys
import os
from datetime import datetime

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_excel_file(file_path):
    """分析Excel文件"""
    try:
        print(f"📖 正在分析文件: {file_path}")
        
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        print(f"✅ 成功读取文件，共 {len(df)} 行数据")
        print(f"📊 数据列: {', '.join(df.columns.tolist())}")
        
        # 分析数据
        analysis_results = {
            "file_info": {
                "file_name": os.path.basename(file_path),
                "file_size": os.path.getsize(file_path),
                "row_count": len(df),
                "column_count": len(df.columns),
                "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "column_analysis": {},
            "data_summary": {},
            "recommendations": []
        }
        
        # 分析每一列
        for column in df.columns:
            col_data = df[column]
            analysis_results["column_analysis"][column] = {
                "data_type": str(col_data.dtype),
                "non_null_count": col_data.count(),
                "null_count": col_data.isnull().sum(),
                "unique_count": col_data.nunique(),
                "sample_values": col_data.dropna().head(3).tolist() if col_data.count() > 0 else []
            }
        
        # 查找关键字段
        key_fields = {
            "项目名称": ["项目名称", "项目名", "名称", "title", "project_name"],
            "发布日期": ["发布日期", "日期", "时间", "date", "publish_date"],
            "招标单位": ["招标单位", "单位", "机构", "bid_unit", "organization"],
            "招标估价": ["招标估价", "预算", "金额", "价格", "bid_estimate", "amount"],
            "省份": ["省", "省份", "province", "location"],
            "城市": ["市", "城市", "city"],
            "区县": ["县", "区", "区县", "county", "district"]
        }
        
        found_fields = {}
        for field_name, possible_names in key_fields.items():
            for col_name in df.columns:
                if any(name in str(col_name) for name in possible_names):
                    found_fields[field_name] = col_name
                    break
        
        analysis_results["key_fields_found"] = found_fields
        
        # 生成建议
        if len(found_fields) >= 5:
            analysis_results["recommendations"].append("✅ 文件包含足够的关键字段，可以导入数据库")
        else:
            analysis_results["recommendations"].append("⚠️ 文件缺少一些关键字段，可能需要手动映射")
        
        if df.isnull().sum().sum() > 0:
            null_count = df.isnull().sum().sum()
            analysis_results["recommendations"].append(f"⚠️ 文件包含 {null_count} 个空值，建议清理数据")
        
        # 显示分析结果
        print("\n📋 分析结果:")
        print("=" * 60)
        print(f"文件: {analysis_results['file_info']['file_name']}")
        print(f"数据量: {analysis_results['file_info']['row_count']} 行 × {analysis_results['file_info']['column_count']} 列")
        print(f"分析时间: {analysis_results['file_info']['analysis_time']}")
        
        print("\n🔍 找到的关键字段:")
        for field, col_name in found_fields.items():
            print(f"  {field}: {col_name}")
        
        print("\n💡 建议:")
        for rec in analysis_results["recommendations"]:
            print(f"  {rec}")
        
        print("\n📊 数据预览 (前3行):")
        print(df.head(3).to_string())
        
        # 保存分析结果
        output_file = file_path.replace('.xlsx', '_analysis.json').replace('.xls', '_analysis.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(analysis_results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 分析结果已保存到: {output_file}")
        
        return analysis_results
        
    except Exception as e:
        print(f"❌ 分析文件失败: {e}")
        return None

def main():
    """主函数"""
    print("🔍 招标文件分析工具")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("使用方法: python analyze.py <Excel文件路径>")
        print("示例: python analyze.py /path/to/bid_file.xlsx")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)
    
    # 分析文件
    results = analyze_excel_file(file_path)
    
    if results:
        print("\n✅ 分析完成！")
        print("\n下一步操作建议:")
        print("1. 如果字段映射正确，可以运行 import.py 导入数据库")
        print("2. 如果需要调整字段映射，可以修改 config.json 文件")
        print("3. 运行 query.py 查询现有数据")
    else:
        print("\n❌ 分析失败，请检查文件格式")

if __name__ == "__main__":
    main()