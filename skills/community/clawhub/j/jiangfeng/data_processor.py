"""
数据处理模块 - 负责数据读取、清洗和预处理
"""

import pandas as pd
import numpy as np
import os
import glob
import chardet
from datetime import datetime

class DataProcessor:
    def __init__(self, data_dir):
        self.data_dir = data_dir
    
    def detect_encoding(self, file_path):
        """自动检测文件编码"""
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # 只读取前10000字节来检测编码
            result = chardet.detect(raw_data)
            return result['encoding']
    
    def read_csv_with_encoding(self, file_path):
        """自动检测编码并读取CSV文件"""
        encoding = self.detect_encoding(file_path)
        encodings_to_try = [encoding, 'utf-8', 'gbk', 'gb2312', 'latin1']
        
        for enc in encodings_to_try:
            if enc:
                try:
                    df = pd.read_csv(file_path, encoding=enc)
                    print(f"✅ 成功读取文件: {file_path}, 编码: {enc}")
                    return df
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f"⚠️  读取文件 {file_path} 时出错: {e}")
                    continue
        
        raise Exception(f"无法读取文件 {file_path}，尝试了编码: {encodings_to_try}")
    
    def auto_detect_files(self):
        """自动识别三类数据文件"""
        super_files = []
        taobao_files = []
        financial_files = []
        
        # 查找所有CSV文件
        csv_files = glob.glob(os.path.join(self.data_dir, "**/*.csv"), recursive=True)
        csv_files.extend(glob.glob(os.path.join(self.data_dir, "**/*.xlsx"), recursive=True))
        
        for file_path in csv_files:
            filename = os.path.basename(file_path).lower()
            
            if "超级直播" in filename:
                super_files.append(file_path)
            elif "淘宝直播" in filename:
                taobao_files.append(file_path)
            elif "财务" in filename:
                financial_files.append(file_path)
        
        return super_files, taobao_files, financial_files
    
    def read_data(self, file_paths, data_type):
        """读取指定类型的数据"""
        if not file_paths:
            print(f"⚠️  未找到{data_type}数据文件")
            return pd.DataFrame()
        
        dfs = []
        for file_path in file_paths:
            try:
                df = self.read_csv_with_encoding(file_path)
                dfs.append(df)
            except Exception as e:
                print(f"❌ 读取{data_type}文件 {file_path} 失败: {e}")
        
        if dfs:
            # 合并多个文件
            combined_df = pd.concat(dfs, ignore_index=True)
            print(f"✅ 成功读取{data_type}数据，形状: {combined_df.shape}")
            return combined_df
        else:
            return pd.DataFrame()
    
    def preprocess_data(self, df, data_type):
        """数据预处理"""
        if df.empty:
            return df
        
        # 标准化日期字段
        df = self.standardize_dates(df, data_type)
        
        # 处理数值字段
        df = self.process_numeric_fields(df, data_type)
        
        # 去除重复数据
        df = df.drop_duplicates()
        
        print(f"✅ {data_type}数据预处理完成，形状: {df.shape}")
        return df
    
    def standardize_dates(self, df, data_type):
        """标准化日期字段"""
        date_columns = []
        
        # 识别日期字段
        for col in df.columns:
            col_lower = str(col).lower()
            if '日期' in col_lower or 'date' in col_lower:
                date_columns.append(col)
        
        # 标准化日期格式
        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                # 转换为YYYY-MM-DD格式
                df[col] = df[col].dt.strftime('%Y-%m-%d')
            except Exception as e:
                print(f"⚠️  标准化日期字段 {col} 时出错: {e}")
        
        return df
    
    def process_numeric_fields(self, df, data_type):
        """处理数值字段"""
        # 识别数值字段（排除日期字段）
        numeric_patterns = ['花费', '金额', '成本', '笔数', '次数', '量', '率', '价']
        
        for col in df.columns:
            col_str = str(col)
            
            # 检查是否是数值字段
            is_numeric = any(pattern in col_str for pattern in numeric_patterns)
            
            if is_numeric and df[col].dtype == 'object':
                try:
                    # 尝试转换为数值
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except Exception as e:
                    print(f"⚠️  转换数值字段 {col} 时出错: {e}")
        
        return df
    
    def validate_data_quality(self, df, data_type):
        """数据质量验证"""
        if df.empty:
            return {"status": "empty", "message": "数据为空"}
        
        quality_report = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "missing_values": {},
            "data_types": {},
            "date_range": {}
        }
        
        # 检查缺失值
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_percentage = missing_count / len(df) * 100
            quality_report["missing_values"][col] = {
                "count": missing_count,
                "percentage": f"{missing_percentage:.2f}%"
            }
        
        # 记录数据类型
        for col in df.columns:
            quality_report["data_types"][col] = str(df[col].dtype)
        
        # 检查日期范围（如果有日期字段）
        date_cols = [col for col in df.columns if '日期' in str(col)]
        if date_cols:
            for col in date_cols:
                try:
                    dates = pd.to_datetime(df[col], errors='coerce')
                    valid_dates = dates.dropna()
                    if not valid_dates.empty:
                        quality_report["date_range"][col] = {
                            "min": valid_dates.min().strftime('%Y-%m-%d'),
                            "max": valid_dates.max().strftime('%Y-%m-%d'),
                            "days": (valid_dates.max() - valid_dates.min()).days
                        }
                except:
                    pass
        
        return quality_report