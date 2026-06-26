#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
-*--*--*--*--*--*--*--*--*--*--*-

createBy: wanghao

createTime: 2026-03-27 14:21:00

-*--*--*--*--*--*--*--*--*--*--*-

Excel工具库 - 基础增删改查功能
与业务逻辑完全解耦，只提供Excel文件操作的基础功能

使用方法：
    from openclawkit_excel import ExcelToolkit
    excel = ExcelToolkit()
    excel.create_excel('文件.xlsx', data)
"""

import os
import pandas as pd
from datetime import datetime
from typing import Union, List, Dict, Any, Optional
import warnings


class ExcelToolkit:
    """Excel基础操作工具库 - 与业务逻辑解耦"""
    
    def __init__(self, debug: bool = False):
        """
        初始化Excel工具库
        
        Args:
            debug: 是否启用调试模式，输出详细日志
        """
        self.debug = debug
        self._log("Excel工具库初始化完成")
    
    def _log(self, message: str):
        """内部日志方法"""
        if self.debug:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[ExcelToolkit {timestamp}] {message}")
    
    # ==================== 文件操作 ====================
    
    def file_exists(self, filepath: str) -> bool:
        """
        检查Excel文件是否存在
        
        Args:
            filepath: Excel文件路径
            
        Returns:
            bool: 文件是否存在
        """
        exists = os.path.exists(filepath)
        self._log(f"检查文件是否存在: {filepath} -> {exists}")
        return exists
    
    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        """
        获取Excel文件基本信息
        
        Args:
            filepath: Excel文件路径
            
        Returns:
            Dict: 包含文件信息的字典
        """
        if not self.file_exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        try:
            stat_info = os.stat(filepath)
            file_size = stat_info.st_size
            modified_time = datetime.fromtimestamp(stat_info.st_mtime)
            
            # 获取Excel文件的工作表信息
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                excel_file = pd.ExcelFile(filepath)
                sheet_names = excel_file.sheet_names
            
            info = {
                'filepath': filepath,
                'filename': os.path.basename(filepath),
                'size_bytes': file_size,
                'size_human': self._format_size(file_size),
                'modified_time': modified_time.strftime('%Y-%m-%d %H:%M:%S'),
                'sheet_count': len(sheet_names),
                'sheet_names': sheet_names,
                'file_type': 'Excel'
            }
            
            self._log(f"获取文件信息: {filepath} -> {len(sheet_names)}个工作表")
            return info
            
        except Exception as e:
            raise Exception(f"获取文件信息失败: {e}")
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    # ==================== 读取操作 ====================
    
    def read_excel(self, filepath: str, sheet_name: Union[str, int, List, None] = None, 
                   header: int = 0, usecols: Optional[List] = None) -> Dict[str, pd.DataFrame]:
        """
        读取Excel文件
        
        Args:
            filepath: Excel文件路径
            sheet_name: 工作表名称或索引，None表示所有工作表
            header: 表头行索引
            usecols: 要读取的列
            
        Returns:
            Dict: 工作表名到DataFrame的映射
        """
        if not self.file_exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        try:
            self._log(f"开始读取Excel文件: {filepath}")
            
            # 读取Excel文件
            if sheet_name is None:
                # 读取所有工作表
                excel_file = pd.ExcelFile(filepath)
                result = {}
                for sheet in excel_file.sheet_names:
                    df = pd.read_excel(filepath, sheet_name=sheet, header=header, usecols=usecols)
                    result[sheet] = df
                    self._log(f"  读取工作表: {sheet} -> {df.shape[0]}行×{df.shape[1]}列")
            else:
                # 读取指定工作表
                df = pd.read_excel(filepath, sheet_name=sheet_name, header=header, usecols=usecols)
                if isinstance(sheet_name, str):
                    result = {sheet_name: df}
                else:
                    # 如果是索引，获取实际名称
                    excel_file = pd.ExcelFile(filepath)
                    actual_name = excel_file.sheet_names[sheet_name] if isinstance(sheet_name, int) else str(sheet_name)
                    result = {actual_name: df}
                self._log(f"  读取工作表: {list(result.keys())[0]} -> {df.shape[0]}行×{df.shape[1]}列")
            
            self._log(f"Excel文件读取完成: {filepath}")
            return result
            
        except Exception as e:
            raise Exception(f"读取Excel文件失败: {e}")
    
    def read_sheet(self, filepath: str, sheet_name: Union[str, int] = 0, 
                   header: int = 0, usecols: Optional[List] = None) -> pd.DataFrame:
        """
        读取Excel文件的单个工作表
        
        Args:
            filepath: Excel文件路径
            sheet_name: 工作表名称或索引
            header: 表头行索引
            usecols: 要读取的列
            
        Returns:
            DataFrame: 工作表数据
        """
        result = self.read_excel(filepath, sheet_name=sheet_name, header=header, usecols=usecols)
        return list(result.values())[0]
    
    # ==================== 写入操作 ====================
    
    def create_excel(self, filepath: str, data: Optional[Dict[str, pd.DataFrame]] = None, 
                     engine: str = 'openpyxl') -> str:
        """
        创建新的Excel文件
        
        Args:
            filepath: 要创建的Excel文件路径
            data: 工作表数据字典 {sheet_name: DataFrame}
            engine: 写入引擎（'openpyxl'或'xlsxwriter'）
            
        Returns:
            str: 创建的文件路径
        """
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            
            if data is None or len(data) == 0:
                # 创建空Excel文件
                with pd.ExcelWriter(filepath, engine=engine) as writer:
                    # 创建一个空的工作表
                    pd.DataFrame().to_excel(writer, sheet_name='Sheet1', index=False)
                self._log(f"创建空Excel文件: {filepath}")
            else:
                # 创建包含数据的Excel文件
                with pd.ExcelWriter(filepath, engine=engine) as writer:
                    for sheet_name, df in data.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                        self._log(f"  写入工作表: {sheet_name} -> {df.shape[0]}行×{df.shape[1]}列")
                self._log(f"创建Excel文件: {filepath}，包含{len(data)}个工作表")
            
            return filepath
            
        except Exception as e:
            raise Exception(f"创建Excel文件失败: {e}")
    
    def write_excel(self, filepath: str, data: Dict[str, pd.DataFrame], 
                    mode: str = 'w', engine: str = 'openpyxl') -> str:
        """
        写入数据到Excel文件
        
        Args:
            filepath: Excel文件路径
            data: 工作表数据字典 {sheet_name: DataFrame}
            mode: 写入模式 'w'覆盖 / 'a'追加（仅对xlsxwriter有效）
            engine: 写入引擎
            
        Returns:
            str: 写入的文件路径
        """
        if mode == 'w' or not self.file_exists(filepath):
            # 覆盖模式或文件不存在，直接创建
            return self.create_excel(filepath, data, engine)
        else:
            # 追加模式（需要特殊处理，因为pandas默认不支持追加）
            try:
                # 先读取现有文件
                existing_data = self.read_excel(filepath)
                # 合并数据（新数据覆盖同名工作表）
                existing_data.update(data)
                # 重新写入
                return self.create_excel(filepath, existing_data, engine)
            except Exception as e:
                raise Exception(f"追加写入Excel文件失败: {e}")
    
    def add_sheet(self, filepath: str, sheet_name: str, data: pd.DataFrame, 
                  engine: str = 'openpyxl') -> str:
        """
        向现有Excel文件添加新工作表
        
        Args:
            filepath: Excel文件路径
            sheet_name: 新工作表名称
            data: 工作表数据
            engine: 写入引擎
            
        Returns:
            str: 更新后的文件路径
        """
        if not self.file_exists(filepath):
            # 文件不存在，创建新文件
            return self.create_excel(filepath, {sheet_name: data}, engine)
        
        try:
            # 读取现有数据
            existing_data = self.read_excel(filepath)
            
            # 检查工作表名是否已存在
            if sheet_name in existing_data:
                self._log(f"工作表已存在: {sheet_name}，将被覆盖")
            
            # 添加/更新工作表
            existing_data[sheet_name] = data
            
            # 重新写入
            return self.create_excel(filepath, existing_data, engine)
            
        except Exception as e:
            raise Exception(f"添加工作表失败: {e}")
    
    # ==================== 编辑操作 ====================
    
    def update_sheet(self, filepath: str, sheet_name: str, data: pd.DataFrame, 
                     engine: str = 'openpyxl') -> str:
        """
        更新指定工作表的数据
        
        Args:
            filepath: Excel文件路径
            sheet_name: 要更新的工作表名称
            data: 新的工作表数据
            engine: 写入引擎
            
        Returns:
            str: 更新后的文件路径
        """
        if not self.file_exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        try:
            # 读取现有数据
            existing_data = self.read_excel(filepath)
            
            # 检查工作表是否存在
            if sheet_name not in existing_data:
                raise KeyError(f"工作表不存在: {sheet_name}")
            
            # 更新数据
            existing_data[sheet_name] = data
            
            # 重新写入
            return self.create_excel(filepath, existing_data, engine)
            
        except Exception as e:
            raise Exception(f"更新工作表失败: {e}")
    
    def delete_sheet(self, filepath: str, sheet_name: str, engine: str = 'openpyxl') -> str:
        """
        删除指定工作表
        
        Args:
            filepath: Excel文件路径
            sheet_name: 要删除的工作表名称
            engine: 写入引擎
            
        Returns:
            str: 更新后的文件路径
        """
        if not self.file_exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        try:
            # 读取现有数据
            existing_data = self.read_excel(filepath)
            
            # 检查工作表是否存在
            if sheet_name not in existing_data:
                raise KeyError(f"工作表不存在: {sheet_name}")
            
            # 删除工作表
            del existing_data[sheet_name]
            
            # 如果所有工作表都被删除，创建一个空工作表
            if len(existing_data) == 0:
                existing_data['Sheet1'] = pd.DataFrame()
            
            # 重新写入
            return self.create_excel(filepath, existing_data, engine)
            
        except Exception as e:
            raise Exception(f"删除工作表失败: {e}")
    
    def rename_sheet(self, filepath: str, old_name: str, new_name: str, 
                     engine: str = 'openpyxl') -> str:
        """
        重命名工作表
        
        Args:
            filepath: Excel文件路径
            old_name: 原工作表名称
            new_name: 新工作表名称
            engine: 写入引擎
            
        Returns:
            str: 更新后的文件路径
        """
        if not self.file_exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        try:
            # 读取现有数据
            existing_data = self.read_excel(filepath)
            
            # 检查原工作表是否存在
            if old_name not in existing_data:
                raise KeyError(f"原工作表不存在: {old_name}")
            
            # 检查新名称是否已存在
            if new_name in existing_data:
                raise ValueError(f"新工作表名称已存在: {new_name}")
            
            # 重命名
            existing_data[new_name] = existing_data.pop(old_name)
            
            # 重新写入
            return self.create_excel(filepath, existing_data, engine)
            
        except Exception as e:
            raise Exception(f"重命名工作表失败: {e}")
    
    # ==================== 查询操作 ====================
    
    def get_sheet_names(self, filepath: str) -> List[str]:
        """
        获取Excel文件中的所有工作表名称
        
        Args:
            filepath: Excel文件路径
            
        Returns:
            List[str]: 工作表名称列表
        """
        if not self.file_exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        try:
            excel_file = pd.ExcelFile(filepath)
            sheet_names = excel_file.sheet_names
            self._log(f"获取工作表名称: {filepath} -> {len(sheet_names)}个工作表")
            return sheet_names
        except Exception as e:
            raise Exception(f"获取工作表名称失败: {e}")
    
    def get_sheet_info(self, filepath: str, sheet_name: Union[str, int] = 0) -> Dict[str, Any]:
        """
        获取工作表的详细信息
        
        Args:
            filepath: Excel文件路径
            sheet_name: 工作表名称或索引
            
        Returns:
            Dict: 工作表信息
        """
        try:
            df = self.read_sheet(filepath, sheet_name)
            
            info = {
                'sheet_name': sheet_name if isinstance(sheet_name, str) else self.get_sheet_names(filepath)[sheet_name],
                'row_count': df.shape[0],
                'column_count': df.shape[1],
                'columns': list(df.columns),
                'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
                'has_nulls': df.isnull().any().any(),
                'null_count': df.isnull().sum().sum(),
                'memory_usage': df.memory_usage(deep=True).sum()
            }
            
            self._log(f"获取工作表信息: {info['sheet_name']} -> {info['row_count']}行×{info['column_count']}列")
            return info
            
        except Exception as e:
            raise Exception(f"获取工作表信息失败: {e}")
    
    def search_data(self, filepath: str, sheet_name: Union[str, int] = 0, 
                    search_term: str = '', case_sensitive: bool = False) -> pd.DataFrame:
        """
        在工作表中搜索包含特定文本的数据
        
        Args:
            filepath: Excel文件路径
            sheet_name: 工作表名称或索引
            search_term: 搜索关键词
            case_sensitive: 是否区分大小写
            
        Returns:
            DataFrame: 包含搜索结果的DataFrame
        """
        try:
            df = self.read_sheet(filepath, sheet_name)
            
            if not search_term:
                return df
            
            # 将DataFrame转换为字符串进行搜索
            if case_sensitive:
                mask = df.astype(str).apply(lambda x: x.str.contains(search_term, na=False))
            else:
                mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False))
            
            # 获取至少有一列匹配的行
            result_mask = mask.any(axis=1)
            result_df = df[result_mask].copy()
            
            self._log(f"搜索数据: '{search_term}' -> 找到{len(result_df)}条记录")
            return result_df
            
        except Exception as e:
            raise Exception(f"搜索数据失败: {e}")
    
    # ==================== 工具方法 ====================
    
    def merge_excel_files(self, filepaths: List[str], output_path: str, 
                          sheet_name: str = 'Merged', engine: str = 'openpyxl') -> str:
        """
        合并多个Excel文件（假设结构相同）
        
        Args:
            filepaths: 要合并的Excel文件路径列表
            output_path: 输出文件路径
            sheet_name: 合并后的工作表名称
            engine: 写入引擎
            
        Returns:
            str: 合并后的文件路径
        """
        try:
            all_data = []
            
            for filepath in filepaths:
                if not self.file_exists(filepath):
                    self._log(f"警告: 文件不存在，跳过: {filepath}")
                    continue
                
                # 读取第一个工作表
                df = self.read_sheet(filepath, 0)
                all_data.append(df)
                self._log(f"  读取文件: {filepath} -> {df.shape[0]}行")
            
            if not all_data:
                raise ValueError("没有可合并的数据")
            
            # 合并所有DataFrame
            merged_df = pd.concat(all_data, ignore_index=True)
            
            # 写入新文件
            return self.create_excel(output_path, {sheet_name: merged_df}, engine)
            
        except Exception as e:
            raise