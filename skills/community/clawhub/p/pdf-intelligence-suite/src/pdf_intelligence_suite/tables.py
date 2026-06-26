"""
PDF表格识别模块
使用camelot-py实现专业级表格提取
"""

import os
from typing import List, Optional, Union, Dict, Any
import warnings

import pandas as pd
import camelot


class TableExtractor:
    """PDF表格提取器"""
    
    # 支持的导出格式
    SUPPORTED_FORMATS = ['csv', 'excel', 'html', 'json', 'markdown', 'sqlite']
    
    @classmethod
    def extract_tables(
        cls,
        pdf_path: str,
        pages: Optional[Union[str, List[int]]] = None,
        method: str = 'auto',
        **kwargs
    ) -> camelot.core.TableList:
        """
        从PDF提取表格
        
        Args:
            pdf_path: PDF文件路径
            pages: 页面指定，如 "1,3,4" 或 "1-5" 或 [1, 3, 4]
            method: 提取方法
                - 'lattice': 用于有清晰线条边框的表格
                - 'stream': 用于无线条或空格分隔的表格
                - 'auto': 自动选择（默认）
            **kwargs: 传递给camelot的其他参数
                - table_areas: 指定表格区域 ["x1,y1,x2,y2"]
                - columns: 指定列分隔线 ["x1,x2,x3"]
                - split_text: 是否拆分文本（默认True）
                - strip_text: 去除文本中的字符（默认'\n'）
                
        Returns:
            TableList对象，包含提取的表格
            
        Example:
            >>> tables = TableExtractor.extract_tables("report.pdf", pages="1-5")
            >>> print(f"提取了 {len(tables)} 个表格")
            >>> df = tables[0].df  # 获取第一个表格为DataFrame
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        # 转换pages格式
        if isinstance(pages, list):
            pages = ','.join(str(p + 1) for p in pages)  # camelot使用1-based索引
        
        # 自动选择方法
        if method == 'auto':
            # 先尝试lattice，如果没有结果则尝试stream
            tables = camelot.read_pdf(
                pdf_path,
                pages=pages or 'all',
                flavor='lattice',
                **kwargs
            )
            if len(tables) == 0:
                tables = camelot.read_pdf(
                    pdf_path,
                    pages=pages or 'all',
                    flavor='stream',
                    **kwargs
                )
        else:
            tables = camelot.read_pdf(
                pdf_path,
                pages=pages or 'all',
                flavor=method,
                **kwargs
            )
        
        return tables
    
    @classmethod
    def extract_to_dataframes(
        cls,
        pdf_path: str,
        pages: Optional[Union[str, List[int]]] = None,
        method: str = 'auto'
    ) -> List[pd.DataFrame]:
        """
        提取表格并转为DataFrame列表
        
        Returns:
            pandas DataFrame列表
        """
        tables = cls.extract_tables(pdf_path, pages, method)
        return [table.df for table in tables]
    
    @classmethod
    def export_tables(
        cls,
        tables: camelot.core.TableList,
        output_dir: str,
        fmt: str = 'excel',
        prefix: str = 'table'
    ) -> List[str]:
        """
        导出表格到文件
        
        Args:
            tables: TableList对象
            output_dir: 输出目录
            fmt: 导出格式 (csv, excel, html, json, markdown, sqlite)
            prefix: 文件名前缀
            
        Returns:
            导出的文件路径列表
        """
        if fmt not in cls.SUPPORTED_FORMATS:
            raise ValueError(f"不支持的格式: {fmt}，支持的格式: {cls.SUPPORTED_FORMATS}")
        
        os.makedirs(output_dir, exist_ok=True)
        exported_files = []
        
        for i, table in enumerate(tables):
            filename = f"{prefix}_{i+1}"
            filepath = os.path.join(output_dir, filename)
            
            if fmt == 'csv':
                path = f"{filepath}.csv"
                table.to_csv(path)
            elif fmt == 'excel':
                path = f"{filepath}.xlsx"
                table.to_excel(path)
            elif fmt == 'html':
                path = f"{filepath}.html"
                table.to_html(path)
            elif fmt == 'json':
                path = f"{filepath}.json"
                table.to_json(path)
            elif fmt == 'markdown':
                path = f"{filepath}.md"
                df = table.df
                df.to_markdown(path, index=False)
            elif fmt == 'sqlite':
                path = f"{filepath}.db"
                table.to_sqlite(path)
            
            exported_files.append(path)
        
        return exported_files
    
    @classmethod
    def merge_tables_to_excel(
        cls,
        tables: camelot.core.TableList,
        output_path: str,
        sheet_names: Optional[List[str]] = None
    ) -> str:
        """
        将所有表格合并到一个Excel文件的不同sheet
        
        Args:
            tables: TableList对象
            output_path: 输出Excel文件路径
            sheet_names: 自定义sheet名称列表
            
        Returns:
            输出文件路径
        """
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            for i, table in enumerate(tables):
                sheet_name = sheet_names[i] if sheet_names and i < len(sheet_names) else f"Table_{i+1}"
                # 限制sheet名称长度
                sheet_name = sheet_name[:31]
                table.df.to_excel(writer, sheet_name=sheet_name, index=False)
        
        return output_path
    
    @classmethod
    def analyze_table_structure(
        cls,
        pdf_path: str,
        page: int = 0
    ) -> Dict[str, Any]:
        """
        分析页面中的表格结构
        
        Returns:
            表格结构分析信息
        """
        tables = cls.extract_tables(pdf_path, pages=str(page + 1))
        
        analysis = {
            'page': page,
            'table_count': len(tables),
            'tables': []
        }
        
        for i, table in enumerate(tables):
            df = table.df
            table_info = {
                'index': i,
                'shape': df.shape,
                'columns': df.columns.tolist(),
                'accuracy': table._accuracy if hasattr(table, '_accuracy') else None,
                'whitespace': table._whitespace if hasattr(table, '_whitespace') else None,
                'sample_data': df.head(3).to_dict(orient='records')
            }
            analysis['tables'].append(table_info)
        
        return analysis
    
    @classmethod
    def extract_with_accuracy_check(
        cls,
        pdf_path: str,
        pages: Optional[Union[str, List[int]]] = None,
        accuracy_threshold: float = 80.0
    ) -> List[Dict[str, Any]]:
        """
        提取表格并检查识别准确度
        
        Args:
            accuracy_threshold: 准确度阈值，低于此值的表格将被标记
            
        Returns:
            包含表格和准确度信息的列表
        """
        tables = cls.extract_tables(pdf_path, pages)
        
        results = []
        for table in tables:
            accuracy = getattr(table, '_accuracy', 100.0)
            results.append({
                'table': table,
                'dataframe': table.df,
                'accuracy': accuracy,
                'is_reliable': accuracy >= accuracy_threshold,
                'shape': table.df.shape
            })
        
        return results
