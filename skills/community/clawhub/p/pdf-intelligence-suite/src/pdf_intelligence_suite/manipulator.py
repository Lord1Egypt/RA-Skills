"""
PDF页面操作模块
支持合并、拆分、旋转、删除等页面操作
"""

import os
from typing import List, Union, Optional, Tuple

import PyPDF2
from PyPDF2 import PdfReader, PdfWriter


class PDFManipulator:
    """PDF页面操作器"""
    
    @staticmethod
    def merge(
        pdf_paths: List[str],
        output_path: str,
        bookmark_names: Optional[List[str]] = None
    ) -> str:
        """
        合并多个PDF文件
        
        Args:
            pdf_paths: PDF文件路径列表
            output_path: 输出文件路径
            bookmark_names: 为每个PDF添加书签名称
            
        Returns:
            输出文件路径
        """
        merger = PyPDF2.PdfMerger()
        
        for i, pdf_path in enumerate(pdf_paths):
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
            
            bookmark = bookmark_names[i] if bookmark_names and i < len(bookmark_names) else None
            merger.append(pdf_path, bookmark)
        
        merger.write(output_path)
        merger.close()
        
        return output_path
    
    @staticmethod
    def split(
        pdf_path: str,
        split_points: List[int],
        output_pattern: str = "part_{}.pdf"
    ) -> List[str]:
        """
        按页码拆分PDF
        
        Args:
            pdf_path: PDF文件路径
            split_points: 拆分点页码列表（在该页后拆分）
            output_pattern: 输出文件名模板，如 "part_{}.pdf"
            
        Returns:
            生成的文件路径列表
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        # 排序并去重拆分点
        split_points = sorted(set([p for p in split_points if 0 < p < total_pages]))
        split_points = [0] + split_points + [total_pages]
        
        output_paths = []
        
        for i in range(len(split_points) - 1):
            writer = PdfWriter()
            start = split_points[i]
            end = split_points[i + 1]
            
            for page_num in range(start, end):
                writer.add_page(reader.pages[page_num])
            
            output_path = output_pattern.format(i + 1)
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            output_paths.append(output_path)
        
        return output_paths
    
    @staticmethod
    def rotate(
        pdf_path: str,
        pages: List[int],
        degrees: int,
        output_path: str
    ) -> str:
        """
        旋转指定页面
        
        Args:
            pdf_path: PDF文件路径
            pages: 要旋转的页面索引列表（从0开始）
            degrees: 旋转角度（90, 180, 270）
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # 标准化旋转角度
        rotation = degrees % 360
        if rotation not in [0, 90, 180, 270]:
            rotation = 90  # 默认90度
        
        for i, page in enumerate(reader.pages):
            if i in pages:
                page.rotate(rotation)
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @staticmethod
    def remove_pages(
        pdf_path: str,
        pages_to_remove: List[int],
        output_path: str
    ) -> str:
        """
        删除指定页面
        
        Args:
            pdf_path: PDF文件路径
            pages_to_remove: 要删除的页面索引列表（从0开始）
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        pages_to_remove = set(pages_to_remove)
        
        for i, page in enumerate(reader.pages):
            if i not in pages_to_remove:
                writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @staticmethod
    def extract_pages(
        pdf_path: str,
        pages: List[int],
        output_path: str
    ) -> str:
        """
        提取指定页面到新PDF
        
        Args:
            pdf_path: PDF文件路径
            pages: 要提取的页面索引列表（从0开始）
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page_num in pages:
            if 0 <= page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @staticmethod
    def insert_pages(
        base_pdf_path: str,
        insert_pdf_path: str,
        position: int,
        output_path: str,
        pages: Optional[List[int]] = None
    ) -> str:
        """
        在指定位置插入页面
        
        Args:
            base_pdf_path: 基础PDF文件路径
            insert_pdf_path: 要插入的PDF文件路径
            position: 插入位置（从0开始）
            output_path: 输出文件路径
            pages: 要插入的页面列表，None表示全部
            
        Returns:
            输出文件路径
        """
        if not os.path.exists(base_pdf_path):
            raise FileNotFoundError(f"基础PDF文件不存在: {base_pdf_path}")
        if not os.path.exists(insert_pdf_path):
            raise FileNotFoundError(f"插入PDF文件不存在: {insert_pdf_path}")
        
        base_reader = PdfReader(base_pdf_path)
        insert_reader = PdfReader(insert_pdf_path)
        writer = PdfWriter()
        
        # 添加基础PDF的前半部分
        for i in range(min(position, len(base_reader.pages))):
            writer.add_page(base_reader.pages[i])
        
        # 添加要插入的页面
        if pages:
            for page_num in pages:
                if 0 <= page_num < len(insert_reader.pages):
                    writer.add_page(insert_reader.pages[page_num])
        else:
            for page in insert_reader.pages:
                writer.add_page(page)
        
        # 添加基础PDF的后半部分
        for i in range(position, len(base_reader.pages)):
            writer.add_page(base_reader.pages[i])
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @staticmethod
    def reorder_pages(
        pdf_path: str,
        new_order: List[int],
        output_path: str
    ) -> str:
        """
        重新排列页面顺序
        
        Args:
            pdf_path: PDF文件路径
            new_order: 新的页面顺序列表（从0开始）
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page_num in new_order:
            if 0 <= page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @staticmethod
    def duplicate_pages(
        pdf_path: str,
        pages_to_duplicate: List[int],
        output_path: str
    ) -> str:
        """
        复制指定页面
        
        Args:
            pdf_path: PDF文件路径
            pages_to_duplicate: 要复制的页面索引列表
            output_path: 输出文件路径
            
        Returns:
            输出文件路径
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        duplicates = set(pages_to_duplicate)
        
        for i, page in enumerate(reader.pages):
            writer.add_page(page)
            if i in duplicates:
                writer.add_page(page)  # 复制一次
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
