#!/usr/bin/env python3
"""
MD2DOC - Markdown 转 Word/PDF 工具
OpenClaw 技能入口
"""

import os
import sys
import subprocess
from pathlib import Path

def convert_md(input_file, output_dir=None, output_pdf=False, style='default', include_toc=None):
    """
    转换 Markdown 文件为 Word 和 PDF
    
    参数:
        input_file: MD 文件路径
        output_dir: 输出目录（可选，默认与输入文件同目录）
        output_pdf: 是否同时输出 PDF
        style: 样式模板名称
        include_toc: 是否包含目录 (True/False/None=自动)
    
    返回:
        dict: 包含输出文件路径
    """
    if not os.path.exists(input_file):
        return {"error": f"文件不存在: {input_file}"}
    
    input_path = Path(input_file)
    
    if output_dir is None:
        output_dir = input_path.parent
    
    output_name = input_path.stem
    docx_file = os.path.join(output_dir, f"{output_name}.docx")
    pdf_file = os.path.join(output_dir, f"{output_name}.pdf")
    
    # 获取 convert.py 的路径
    script_dir = Path(__file__).parent
    convert_script = script_dir / "convert.py"
    
    # 构建命令
    cmd = [sys.executable, str(convert_script), str(input_file), "--output", docx_file, "--style", style]
    if output_pdf:
        cmd.extend(["--pdf", pdf_file])
    
    # 目录控制
    if include_toc is False:
        cmd.append("--no-toc")
    elif include_toc is True:
        cmd.append("--toc")
    
    # 运行转换
    try:
        result = subprocess.run(cmd, capture_output=True)
        # 处理编码
        try:
            stderr_text = result.stderr.decode('utf-8') if result.stderr else ""
        except:
            stderr_text = result.stderr.decode('gbk', errors='ignore') if result.stderr else ""
        
        success = os.path.exists(docx_file)
        pdf_success = os.path.exists(pdf_file) if output_pdf else True
        
        if success:
            result_dict = {
                "success": True,
                "docx": docx_file,
                "message": f"Word 文档已保存: {docx_file}"
            }
            if output_pdf and pdf_success:
                result_dict["pdf"] = pdf_file
                result_dict["message"] += f" | PDF 已保存: {pdf_file}"
            return result_dict
        else:
            return {
                "error": f"转换失败: {stderr_text}"
            }
    except Exception as e:
        return {"error": f"运行出错: {str(e)}"}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MD2DOC - Markdown 转 Word/PDF")
    parser.add_argument("input", nargs="?", help="输入的 Markdown 文件路径")
    parser.add_argument("--output-dir", "-o", help="输出目录")
    parser.add_argument("--pdf", "-p", action="store_true", help="同时输出 PDF")
    parser.add_argument("--style", "-s", default="default", help="样式模板 (default/business/tech/minimal/product/academic)")
    parser.add_argument("--list-styles", action="store_true", help="列出所有可用样式")
    parser.add_argument("--no-toc", action="store_true", help="不生成目录")
    parser.add_argument("--toc", action="store_true", help="生成目录（默认）")
    args = parser.parse_args()
    
    # 列出样式
    if args.list_styles:
        sys.path.insert(0, str(Path(__file__).parent.parent / 'templates'))
        from styles import list_styles
        list_styles()
        sys.exit(0)
    
    if not args.input:
        print("错误: 请提供输入文件")
        sys.exit(1)
    
    # 目录控制
    include_toc = None  # 默认自动
    if args.no_toc:
        include_toc = False
    elif args.toc:
        include_toc = True
    
    result = convert_md(args.input, args.output_dir, output_pdf=args.pdf, style=args.style, include_toc=include_toc)
    
    if "error" in result:
        print(f"[错误] {result['error']}")
        sys.exit(1)
    else:
        print(f"[成功] {result['message']}")
        sys.exit(0)
