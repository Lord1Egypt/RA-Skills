#!/usr/bin/env python3
"""
文档读取工具
支持读取.txt和.docx格式的文档内容
"""

import argparse
import sys
from pathlib import Path

try:
    from docx import Document
except ImportError:
    print("错误：缺少依赖包 python-docx，请运行：pip install python-docx==0.8.11")
    sys.exit(1)


def read_txt(file_path: str) -> str:
    """
    读取文本文件内容
    
    参数：
        file_path: 文本文件路径
        
    返回：
        文件的完整文本内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # 尝试其他编码
        for encoding in ['gbk', 'gb18030', 'latin-1']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        raise ValueError(f"无法解码文件 {file_path}，请检查文件编码")
    except Exception as e:
        raise Exception(f"读取文件失败: {str(e)}")


def read_docx(file_path: str) -> str:
    """
    读取Word文档内容
    
    参数：
        file_path: Word文档路径
        
    返回：
        文档的完整文本内容
    """
    try:
        doc = Document(file_path)
        paragraphs = []
        
        for para in doc.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)
        
        return '\n\n'.join(paragraphs)
    except Exception as e:
        raise Exception(f"读取Word文档失败: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description='文档读取工具')
    parser.add_argument('--file', required=True, help='文档文件路径（支持.txt和.docx格式）')
    
    args = parser.parse_args()
    file_path = Path(args.file)
    
    # 检查文件是否存在
    if not file_path.exists():
        print(f"错误：文件不存在 - {file_path}")
        sys.exit(1)
    
    # 根据文件扩展名选择读取方式
    file_ext = file_path.suffix.lower()
    
    try:
        if file_ext == '.txt':
            content = read_txt(str(file_path))
        elif file_ext in ['.docx', '.doc']:
            content = read_docx(str(file_path))
        else:
            print(f"错误：不支持的文件格式 - {file_ext}，仅支持.txt和.docx格式")
            sys.exit(1)
        
        # 输出文档内容
        print(content)
        
    except Exception as e:
        print(f"错误：{str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
