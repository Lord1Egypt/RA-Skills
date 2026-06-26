#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word 转 PDF 转换器 v1.0
支持单个文件和批量转换
依赖：LibreOffice (brew install --cask libreoffice)
"""

import os
import sys
import subprocess
import glob
import shutil
from pathlib import Path

# ============== 配置 ==============
LIBREOFFICE_PATHS = [
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/opt/homebrew/bin/soffice",
    "/usr/local/bin/soffice",
    "soffice",  # PATH 中
]

def find_libreoffice():
    """查找 LibreOffice 安装路径"""
    for path in LIBREOFFICE_PATHS:
        if path == "soffice":
            # 检查 PATH 中是否有
            result = shutil.which("soffice")
            if result:
                return result
        elif os.path.exists(path):
            return path
    return None

def check_libreoffice():
    """检查 LibreOffice 是否安装"""
    path = find_libreoffice()
    if path:
        return True, path
    return False, None

def convert_to_pdf(input_path, output_path=None, timeout=60):
    """
    将 Word 文档转换为 PDF
    
    参数:
        input_path: Word 文件路径 (.docx 或 .doc)
        output_path: PDF 输出路径（可选，默认与输入文件同目录）
        timeout: 超时时间（秒）
    
    返回:
        (成功标志, 输出路径或错误信息)
    """
    input_path = os.path.abspath(input_path)
    
    if not os.path.exists(input_path):
        return False, f"文件不存在: {input_path}"
    
    if not input_path.lower().endswith(('.docx', '.doc')):
        return False, "只支持 .docx 或 .doc 文件"
    
    # 检查 LibreOffice
    lo_path = find_libreoffice()
    if not lo_path:
        return False, "LibreOffice 未安装。请运行: brew install --cask libreoffice"
    
    # 确定输出路径
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".pdf"
    else:
        output_path = os.path.abspath(output_path)
    
    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    # 创建临时目录用于转换
    temp_dir = os.path.join(os.path.dirname(output_path), ".pdf_convert_tmp")
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # 复制源文件到临时目录（避免路径问题）
        temp_input = os.path.join(temp_dir, os.path.basename(input_path))
        shutil.copy2(input_path, temp_input)
        
        # 执行转换
        cmd = [
            lo_path,
            "--headless",
            "--convert-to", "pdf",
            "--outdir", temp_dir,
            os.path.basename(temp_input)
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=temp_dir
        )
        
        if result.returncode != 0:
            return False, f"转换失败: {result.stderr}"
        
        # 移动 PDF 到目标位置
        temp_pdf = os.path.splitext(os.path.basename(temp_input))[0] + ".pdf"
        temp_pdf_path = os.path.join(temp_dir, temp_pdf)
        
        if not os.path.exists(temp_pdf_path):
            return False, "转换后未找到 PDF 文件"
        
        shutil.move(temp_pdf_path, output_path)
        return True, output_path
        
    except subprocess.TimeoutExpired:
        return False, "转换超时"
    except Exception as e:
        return False, f"转换错误: {str(e)}"
    finally:
        # 清理临时目录
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

def convert_batch(input_paths, output_dir=None):
    """
    批量转换 Word 文档为 PDF
    
    参数:
        input_paths: 文件路径列表或通配符表达式
        output_dir: PDF 输出目录（可选）
    
    返回:
        成功和失败的结果列表
    """
    # 展开通配符
    expanded_paths = []
    for path in input_paths:
        if '*' in path or '?' in path:
            expanded_paths.extend(glob.glob(path))
        else:
            expanded_paths.append(path)
    
    results = {
        "success": [],
        "failed": []
    }
    
    for input_path in expanded_paths:
        if output_dir:
            filename = os.path.basename(input_path)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".pdf")
        else:
            output_path = None
        
        success, result = convert_to_pdf(input_path, output_path)
        if success:
            results["success"].append(result)
        else:
            results["failed"].append({"file": input_path, "error": result})
    
    return results

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Word 转 PDF 转换器 v1.0")
        print("")
        print("用法:")
        print("  python word-to-pdf.py <输入文件.docx> [输出文件.pdf]")
        print("  python word-to-pdf.py <通配符表达式> --output-dir <输出目录>")
        print("")
        print("示例:")
        print("  python word-to-pdf.py 合同.docx")
        print("  python word-to-pdf.py 合同.docx 合同.pdf")
        print("  python word-to-pdf.py *.docx --output-dir ./pdf/")
        print("")
        
        # 检查 LibreOffice
        installed, path = check_libreoffice()
        if installed:
            print(f"[OK] LibreOffice 已安装: {path}")
        else:
            print("[WARN] LibreOffice 未安装，请运行: brew install --cask libreoffice")
        return
    
    # 解析参数
    output_dir = None
    input_files = []
    
    for arg in sys.argv[1:]:
        if arg == "--output-dir" or arg == "-o":
            continue
        elif arg in sys.argv[sys.argv.index(arg)-1:  # 简单判断前一个是否是 -o
            output_dir = arg
        elif arg.startswith("-"):
            continue
        else:
            input_files.append(arg)
    
    if not input_files:
        print("错误: 请指定输入文件")
        return 1
    
    # 检查 LibreOffice
    installed, path = check_libreoffice()
    if not installed:
        print("错误: LibreOffice 未安装")
        print("请运行: brew install --cask libreoffice")
        return 1
    
    # 转换
    if len(input_files) == 1 and os.path.isfile(input_files[0]):
        # 单文件转换
        output_path = None
        if len(sys.argv) >= 3 and not sys.argv[-1].startswith("-"):
            output_path = sys.argv[2]
        
        success, result = convert_to_pdf(input_files[0], output_path)
        if success:
            print(f"[OK] 已生成: {result}")
            return 0
        else:
            print(f"[ERROR] {result}")
            return 1
    else:
        # 批量转换
        results = convert_batch(input_files, output_dir)
        print(f"\n转换完成:")
        print(f"  成功: {len(results['success'])} 个")
        print(f"  失败: {len(results['failed'])} 个")
        
        if results["failed"]:
            print("\n失败文件:")
            for item in results["failed"]:
                print(f"  - {item['file']}: {item['error']}")
        
        return 0 if not results["failed"] else 1

if __name__ == "__main__":
    sys.exit(main() or 0)
