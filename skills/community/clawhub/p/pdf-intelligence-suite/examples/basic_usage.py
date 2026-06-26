#!/usr/bin/env python3
"""
PDF智能处理套件 - 基础使用示例
PDF Intelligence Suite - Basic Usage Examples

本示例演示如何使用PDF智能处理套件的各种功能
"""

import os
import sys

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pdf_intelligence_suite import (
    PDFExtractor,
    TableExtractor,
    OCRProcessor,
    PDFConverter,
    PDFManipulator,
    PDFSecurity,
    get_pdf_info,
    create_sample_pdf
)


def demo_text_extraction():
    """演示文本提取功能"""
    print("\n" + "="*60)
    print("📄 演示1: 文本提取 (Text Extraction)")
    print("="*60)
    
    # 创建示例PDF
    sample_pdf = "sample_demo.pdf"
    create_sample_pdf(sample_pdf, num_pages=2, title="Demo Document")
    
    # 初始化提取器
    extractor = PDFExtractor()
    
    # 1.1 基本文本提取
    print("\n1.1 基本文本提取:")
    text = extractor.extract_text(sample_pdf)
    print(text[:500] + "...")
    
    # 1.2 提取特定页面
    print("\n1.2 提取第1页:")
    page_text = extractor.extract_text(sample_pdf, pages=[0])
    print(page_text[:300])
    
    # 1.3 保留布局提取
    print("\n1.3 保留布局提取:")
    layout_text = extractor.extract_text(sample_pdf, preserve_layout=True)
    print(layout_text[:400])
    
    # 1.4 搜索文本
    print("\n1.4 搜索关键词 'Sample':")
    results = extractor.search_text(sample_pdf, "Sample")
    for r in results:
        print(f"  页面 {r['page']}, 行 {r['line']}: {r['text'][:50]}")
    
    # 清理
    if os.path.exists(sample_pdf):
        os.remove(sample_pdf)
    
    print("\n✅ 文本提取演示完成!")


def demo_table_extraction():
    """演示表格提取功能"""
    print("\n" + "="*60)
    print("📊 演示2: 表格提取 (Table Extraction)")
    print("="*60)
    
    # 注意：需要一个包含表格的真实PDF来演示
    # 这里展示API用法
    
    print("\n2.1 表格提取API示例:")
    print("""
    # 提取所有表格
    tables = TableExtractor.extract_tables("report.pdf")
    print(f"找到 {len(tables)} 个表格")
    
    # 遍历表格
    for i, table in enumerate(tables):
        df = table.df  # 转换为DataFrame
        print(f"表格 {i+1}: {df.shape[0]} 行 x {df.shape[1]} 列")
        print(df.head())
        
        # 导出为Excel
        table.to_excel(f"table_{i+1}.xlsx")
    
    # 指定页面提取
    tables = TableExtractor.extract_tables("report.pdf", pages=[1, 2, 3])
    
    # 指定提取方法
    # 'lattice' - 用于有边框的表格
    # 'stream' - 用于无边框表格
    tables = TableExtractor.extract_tables("report.pdf", method='lattice')
    """)
    
    print("\n✅ 表格提取演示完成!")


def demo_ocr():
    """演示OCR功能"""
    print("\n" + "="*60)
    print("🔍 演示3: OCR文字识别 (OCR Recognition)")
    print("="*60)
    
    print("\n3.1 OCR API示例:")
    print("""
    # 初始化OCR处理器（中英文）
    ocr = OCRProcessor(languages=['chi_sim', 'eng'], dpi=300)
    
    # 检查Tesseract安装
    status = ocr.check_tesseract_installation()
    print(f"Tesseract安装状态: {status}")
    
    # 处理扫描件PDF
    text = ocr.process_pdf("scanned_document.pdf")
    print(text)
    
    # 处理指定页面
    text = ocr.process_pdf("scanned.pdf", pages=[0, 1, 2])
    
    # 获取详细结果（包含位置信息）
    results = ocr.process_pdf_with_data("scanned.pdf")
    for item in results[:5]:
        print(f"文本: {item['text']}, 置信度: {item['confidence']:.2%}")
    
    # 处理单张图片
    from PIL import Image
    img = Image.open("page.png")
    text = ocr.process_image(img)
    """)
    
    print("\n✅ OCR演示完成!")


def demo_conversion():
    """演示格式转换功能"""
    print("\n" + "="*60)
    print("🔄 演示4: 格式转换 (Format Conversion)")
    print("="*60)
    
    # 创建示例PDF
    sample_pdf = "conversion_demo.pdf"
    create_sample_pdf(sample_pdf, num_pages=2)
    
    converter = PDFConverter()
    
    print("\n4.1 PDF转Word:")
    output_docx = "output.docx"
    try:
        converter.to_word(sample_pdf, output_docx)
        print(f"  ✅ 已生成: {output_docx}")
        if os.path.exists(output_docx):
            os.remove(output_docx)
    except Exception as e:
        print(f"  ⚠️  需要安装python-docx: {e}")
    
    print("\n4.2 PDF转Excel:")
    output_xlsx = "output.xlsx"
    try:
        converter.to_excel(sample_pdf, output_xlsx, extract_tables=False, extract_text=True)
        print(f"  ✅ 已生成: {output_xlsx}")
        if os.path.exists(output_xlsx):
            os.remove(output_xlsx)
    except Exception as e:
        print(f"  ⚠️  需要安装openpyxl: {e}")
    
    print("\n4.3 PDF转图片:")
    output_dir = "pdf_images"
    try:
        image_paths = converter.to_images(sample_pdf, output_dir, fmt='png', dpi=150)
        print(f"  ✅ 已生成 {len(image_paths)} 张图片")
        # 清理
        import shutil
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
    except Exception as e:
        print(f"  ⚠️  需要安装pdf2image和poppler: {e}")
    
    print("\n4.4 PDF转文本:")
    output_txt = "output.txt"
    converter.to_text(sample_pdf, output_txt)
    print(f"  ✅ 已生成: {output_txt}")
    if os.path.exists(output_txt):
        os.remove(output_txt)
    
    print("\n4.5 PDF转HTML:")
    output_html = "output.html"
    converter.to_html(sample_pdf, output_html)
    print(f"  ✅ 已生成: {output_html}")
    if os.path.exists(output_html):
        os.remove(output_html)
    
    # 清理
    if os.path.exists(sample_pdf):
        os.remove(sample_pdf)
    
    print("\n✅ 格式转换演示完成!")


def demo_manipulation():
    """演示页面操作功能"""
    print("\n" + "="*60)
    print("✂️ 演示5: 页面操作 (Page Manipulation)")
    print("="*60)
    
    # 创建示例PDF
    sample1 = "sample1.pdf"
    sample2 = "sample2.pdf"
    create_sample_pdf(sample1, num_pages=3, title="Document A")
    create_sample_pdf(sample2, num_pages=2, title="Document B")
    
    manip = PDFManipulator()
    
    print("\n5.1 合并PDF:")
    merged = "merged.pdf"
    manip.merge([sample1, sample2], merged, bookmark_names=['Doc A', 'Doc B'])
    print(f"  ✅ 已合并为: {merged}")
    info = get_pdf_info(merged)
    print(f"  页数: {info['page_count']}")
    if os.path.exists(merged):
        os.remove(merged)
    
    print("\n5.2 拆分PDF:")
    split_files = manip.split(sample1, [1], "part_{}.pdf")
    print(f"  ✅ 已拆分为 {len(split_files)} 个文件")
    for f in split_files:
        if os.path.exists(f):
            os.remove(f)
    
    print("\n5.3 旋转页面:")
    rotated = "rotated.pdf"
    manip.rotate(sample1, [0], 90, rotated)
    print(f"  ✅ 第1页已旋转90度: {rotated}")
    if os.path.exists(rotated):
        os.remove(rotated)
    
    print("\n5.4 删除页面:")
    removed = "removed.pdf"
    manip.remove_pages(sample1, [1], removed)
    print(f"  ✅ 已删除第2页: {removed}")
    info = get_pdf_info(removed)
    print(f"  剩余页数: {info['page_count']}")
    if os.path.exists(removed):
        os.remove(removed)
    
    print("\n5.5 提取页面:")
    extracted = "extracted.pdf"
    manip.extract_pages(sample1, [0, 2], extracted)
    print(f"  ✅ 已提取第1和第3页: {extracted}")
    info = get_pdf_info(extracted)
    print(f"  提取页数: {info['page_count']}")
    if os.path.exists(extracted):
        os.remove(extracted)
    
    print("\n5.6 重新排序:")
    reordered = "reordered.pdf"
    manip.reorder_pages(sample1, [2, 0, 1], reordered)
    print(f"  ✅ 页面已重新排序: {reordered}")
    if os.path.exists(reordered):
        os.remove(reordered)
    
    # 清理
    for f in [sample1, sample2]:
        if os.path.exists(f):
            os.remove(f)
    
    print("\n✅ 页面操作演示完成!")


def demo_security():
    """演示安全处理功能"""
    print("\n" + "="*60)
    print("🔒 演示6: 安全处理 (Security)")
    print("="*60)
    
    # 创建示例PDF
    sample_pdf = "security_demo.pdf"
    create_sample_pdf(sample_pdf, num_pages=2)
    
    security = PDFSecurity()
    
    print("\n6.1 加密PDF:")
    encrypted = "encrypted.pdf"
    security.encrypt(
        sample_pdf, 
        encrypted, 
        password="secret123",
        permissions=['print', 'copy']
    )
    print(f"  ✅ 已加密: {encrypted}")
    print(f"  是否加密: {security.is_encrypted(encrypted)}")
    
    print("\n6.2 解密PDF:")
    decrypted = "decrypted.pdf"
    security.decrypt(encrypted, decrypted, password="secret123")
    print(f"  ✅ 已解密: {decrypted}")
    print(f"  是否加密: {security.is_encrypted(decrypted)}")
    
    print("\n6.3 添加文字水印:")
    watermarked = "watermarked.pdf"
    security.add_text_watermark(
        sample_pdf,
        watermarked,
        text="CONFIDENTIAL",
        opacity=0.3,
        angle=45
    )
    print(f"  ✅ 已添加水印: {watermarked}")
    
    # 清理
    for f in [sample_pdf, encrypted, decrypted, watermarked]:
        if os.path.exists(f):
            os.remove(f)
    
    print("\n✅ 安全处理演示完成!")


def demo_utilities():
    """演示工具函数"""
    print("\n" + "="*60)
    print("🛠️ 演示7: 工具函数 (Utilities)")
    print("="*60)
    
    # 创建示例PDF
    sample_pdf = "utils_demo.pdf"
    create_sample_pdf(sample_pdf, num_pages=5)
    
    print("\n7.1 获取PDF信息:")
    info = get_pdf_info(sample_pdf)
    print(f"  文件名: {info['filename']}")
    print(f"  页数: {info['page_count']}")
    print(f"  文件大小: {info['size_bytes']} bytes")
    print(f"  是否加密: {info['is_encrypted']}")
    if info.get('page_size'):
        print(f"  页面尺寸: {info['page_size']['width']} x {info['page_size']['height']} pt")
    if info['metadata']:
        print(f"  元数据: {info['metadata']}")
    
    print("\n7.2 验证PDF:")
    from pdf_intelligence_suite.utils import validate_pdf
    is_valid, msg = validate_pdf(sample_pdf)
    print(f"  是否有效: {is_valid}, 消息: {msg}")
    
    print("\n7.3 估算处理时间:")
    from pdf_intelligence_suite.utils import estimate_processing_time
    for op in ['extract', 'ocr', 'convert']:
        est = estimate_processing_time(sample_pdf, op)
        print(f"  {op}: 约 {est['estimated_seconds']} 秒")
    
    # 清理
    if os.path.exists(sample_pdf):
        os.remove(sample_pdf)
    
    print("\n✅ 工具函数演示完成!")


def main():
    """主函数"""
    print("\n" + "🎉"*30)
    print("  欢迎使用 PDF智能处理套件 示例程序")
    print("  Welcome to PDF Intelligence Suite Examples")
    print("🎉"*30)
    
    # 运行所有演示
    demo_text_extraction()
    demo_table_extraction()
    demo_ocr()
    demo_conversion()
    demo_manipulation()
    demo_security()
    demo_utilities()
    
    print("\n" + "="*60)
    print("🎊 所有演示完成! All demos completed!")
    print("="*60)
    print("\n更多信息请查看 README.md")
    print("For more information, please see README.md")


if __name__ == "__main__":
    main()
