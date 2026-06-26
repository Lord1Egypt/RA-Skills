"""
PDF处理工具函数
"""

import os
from typing import Dict, Any, Optional, Tuple

from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


def get_pdf_info(pdf_path: str) -> Dict[str, Any]:
    """
    获取PDF文件信息
    
    Args:
        pdf_path: PDF文件路径
        
    Returns:
        PDF信息字典
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
    
    reader = PdfReader(pdf_path)
    
    # 基础信息
    info = {
        'path': pdf_path,
        'filename': os.path.basename(pdf_path),
        'size_bytes': os.path.getsize(pdf_path),
        'page_count': len(reader.pages),
        'is_encrypted': reader.is_encrypted,
        'metadata': {}
    }
    
    # 元数据
    if reader.metadata:
        for key, value in reader.metadata.items():
            clean_key = key.replace('/', '').lower()
            info['metadata'][clean_key] = str(value) if value else None
    
    # 第一页尺寸
    if reader.pages:
        first_page = reader.pages[0]
        width = float(first_page.mediabox.width)
        height = float(first_page.mediabox.height)
        info['page_size'] = {
            'width': width,
            'height': height,
            'unit': 'points'
        }
        info['page_size_mm'] = {
            'width': round(width * 0.352778, 2),
            'height': round(height * 0.352778, 2),
            'unit': 'mm'
        }
    
    return info


def validate_pdf(pdf_path: str) -> Tuple[bool, str]:
    """
    验证PDF文件是否有效
    
    Args:
        pdf_path: PDF文件路径
        
    Returns:
        (是否有效, 错误信息)
    """
    if not os.path.exists(pdf_path):
        return False, "文件不存在"
    
    if not pdf_path.lower().endswith('.pdf'):
        return False, "文件扩展名不是.pdf"
    
    try:
        reader = PdfReader(pdf_path)
        # 尝试读取第一页
        if reader.pages:
            _ = reader.pages[0].extract_text()
        return True, "有效"
    except Exception as e:
        return False, f"PDF读取错误: {str(e)}"


def create_sample_pdf(
    output_path: str,
    num_pages: int = 3,
    title: str = "Sample PDF"
) -> str:
    """
    创建示例PDF文件（用于测试）
    
    Args:
        output_path: 输出路径
        num_pages: 页数
        title: 标题
        
    Returns:
        输出文件路径
    """
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    for i in range(num_pages):
        # 标题
        story.append(Paragraph(f"{title} - Page {i+1}", styles['Heading1']))
        story.append(Spacer(1, 0.2*inch))
        
        # 内容
        content = f"""
        This is a sample PDF document created for testing purposes.
        <br/><br/>
        Page number: {i+1} of {num_pages}
        <br/><br/>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.
        """
        story.append(Paragraph(content, styles['Normal']))
        
        # 添加表格示例
        if i == 1:
            story.append(Spacer(1, 0.3*inch))
            table_data = """
            Sample Table:<br/>
            | Name | Age | City |<br/>
            |------|-----|------|<br/>
            | John | 30  | NYC  |<br/>
            | Jane | 25  | LA   |<br/>
            | Bob  | 35  | SF   |<br/>
            """
            story.append(Paragraph(table_data, styles['Code']))
        
        if i < num_pages - 1:
            story.append(PageBreak())
    
    doc.build(story)
    return output_path


def estimate_processing_time(
    pdf_path: str,
    operation: str = 'extract'
) -> Dict[str, Any]:
    """
    估算PDF处理时间
    
    Args:
        pdf_path: PDF文件路径
        operation: 操作类型
        
    Returns:
        估算信息
    """
    info = get_pdf_info(pdf_path)
    page_count = info['page_count']
    file_size_mb = info['size_bytes'] / (1024 * 1024)
    
    # 粗略估算（基于经验值）
    base_times = {
        'extract': 0.5,      # 每页0.5秒
        'ocr': 3.0,          # 每页3秒
        'convert': 1.0,      # 每页1秒
        'table': 2.0,        # 每页2秒
    }
    
    time_per_page = base_times.get(operation, 1.0)
    estimated_seconds = page_count * time_per_page
    
    # 根据文件大小调整
    if file_size_mb > 10:
        estimated_seconds *= 1.5
    
    return {
        'page_count': page_count,
        'file_size_mb': round(file_size_mb, 2),
        'estimated_seconds': round(estimated_seconds, 1),
        'estimated_minutes': round(estimated_seconds / 60, 2),
        'operation': operation
    }


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def merge_dicts(*dicts: Dict) -> Dict:
    """合并多个字典"""
    result = {}
    for d in dicts:
        result.update(d)
    return result
