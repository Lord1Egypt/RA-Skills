#!/usr/bin/env python3
"""
PDF 和圖片 OCR 處理工具（進階版）
使用 Ollama GLM-OCR 模型，根據內容類型（文字/表格/圖表）智能轉換 PDF 和圖片為 Markdown
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

# 將當前目錄加入 Python 路徑
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from utils.ollama_client import OllamaClient
from utils.pdf_utils import pdf_to_images, get_pdf_page_count
from analyzer import PageAnalyzer, PageAnalysis, RegionType
from processor import RegionProcessor
from integrator import MarkdownIntegrator, assemble_markdown
from prompts import get_prompt


def check_environment(args) -> bool:
    """檢查環境需求。"""
    errors = []
    
    # 檢查 Ollama
    client = OllamaClient(host=args.host, port=args.port, model=args.model)
    ok, errs = client.check_status()
    if not ok:
        errors.extend(errs)
    
    # 檢查 pdftoppm
    if args.input.lower().endswith('.pdf'):
        try:
            import subprocess
            subprocess.run(["pdftoppm", "-h"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            errors.append("⚠️ pdftoppm 未安裝，請安裝 poppler-utils 以支援 PDF 處理")
    
    if errors:
        print("環境檢查警告：")
        for err in errors:
            print(f"  {err}")
        print("\n繼續執行可能失敗...\n")
    
    return len(errors) == 0


def process_pdf(
    pdf_path: str,
    output_path: str,
    mode: str = "auto",
    granularity: str = "page",
    host: str = "localhost",
    port: str = "11434",
    model: str = "glm-ocr:q8_0",
    save_images: bool = False,
    custom_prompt: Optional[str] = None
) -> bool:
    """處理 PDF 檔案。"""
    print(f"📄 處理 PDF: {Path(pdf_path).name}")
    print(f"   模式：{mode}")
    print(f"   粒度：{granularity}")
    print(f"   模型：{model}")
    
    # 轉換 PDF 為圖片
    try:
        images = pdf_to_images(pdf_path, output_prefix=Path(pdf_path).stem + "_page")
        print(f"   轉換為 {len(images)} 張圖片")
    except Exception as e:
        print(f"❌ PDF 轉換失敗：{e}")
        return False
    
    # 初始化組件
    client = OllamaClient(host=host, port=port, model=model)
    analyzer = PageAnalyzer(ollama_client=client)
    processor = RegionProcessor(ollama_client=client, save_cropped_images=save_images)
    integrator = MarkdownIntegrator(save_images=save_images)
    
    # 逐頁處理
    analyses = []
    for i, img_path in enumerate(images, 1):
        page_num = Path(img_path).stem.split("_")[-1] if "_" in Path(img_path).stem else str(i)
        print(f"   📝 第 {i}/{len(images)} 頁 ({page_num})...", end=" ")
        
        # 分析頁面
        auto_detect = (mode == "auto")
        analysis = analyzer.analyze_page(img_path, page_number=i, auto_detect=auto_detect)
        
        # 處理區域
        processor.process_page_analysis(analysis)
        
        # 保存結果
        analyses.append(analysis)
        
        # 清理臨時圖片
        try:
            os.remove(img_path)
        except:
            pass
        
        print("✅")
    
    # 整合輸出
    metadata = {
        "model": model,
        "mode": mode,
        "granularity": granularity,
        "source": Path(pdf_path).name
    }
    
    assemble_markdown(
        analyses,
        output_path,
        metadata=metadata,
        simple_mode=(granularity == "page")
    )
    
    print(f"\n✅ 完成！結果已保存至：{output_path}")
    print(f"📊 文件大小：{Path(output_path).stat().st_size / 1024:.1f} KB")
    
    return True


def process_image(
    image_path: str,
    output_path: str,
    mode: str = "mixed",
    host: str = "localhost",
    port: str = "11434",
    model: str = "glm-ocr:q8_0",
    custom_prompt: Optional[str] = None
) -> bool:
    """處理單一圖片。"""
    print(f"🖼️ 處理圖片：{Path(image_path).name}")
    print(f"   模式：{mode}")
    print(f"   模型：{model}")
    
    # 初始化組件
    client = OllamaClient(host=host, port=port, model=model)
    analyzer = PageAnalyzer(ollama_client=client)
    processor = RegionProcessor(ollama_client=client)
    integrator = MarkdownIntegrator(save_images=False)
    
    # 分析頁面
    auto_detect = (mode == "auto")
    analysis = analyzer.analyze_page(image_path, page_number=1, auto_detect=auto_detect)
    
    # 處理區域
    processor.process_page_analysis(analysis)
    
    # 整合輸出
    metadata = {
        "model": model,
        "mode": mode,
        "source": Path(image_path).name
    }
    
    assemble_markdown(
        [analysis],
        output_path,
        metadata=metadata,
        simple_mode=True
    )
    
    print(f"✅ 完成！結果已保存至：{output_path}")
    print(f"📊 文件大小：{Path(output_path).stat().st_size / 1024:.1f} KB")
    
    return True


def main():
    """主函數。"""
    parser = argparse.ArgumentParser(
        description="使用 Ollama GLM-OCR 將 PDF 或圖片轉換為 Markdown（智能分類處理）"
    )
    
    # 必要參數
    parser.add_argument("--input", "-i", required=True, help="輸入檔案路徑 (PDF 或圖片)")
    parser.add_argument("--output", "-o", required=True, help="輸出 Markdown 檔案路徑")
    
    # 模式選擇
    parser.add_argument(
        "--mode", "-m",
        choices=["text", "table", "figure", "mixed", "auto"],
        default="auto",
        help="識別模式：text(純文字)/table(表格)/figure(圖表)/mixed(混合)/auto(自動檢測)"
    )
    
    # 處理粒度
    parser.add_argument(
        "--granularity", "-g",
        choices=["page", "region", "block"],
        default="page",
        help="處理粒度：page(整頁)/region(區域)/block(區塊)"
    )
    
    # 模型配置
    parser.add_argument(
        "--model",
        default="glm-ocr:q8_0",
        help=f"使用的模型 (預設：glm-ocr:q8_0)"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help=f"Ollama 主機位置 (預設：localhost)"
    )
    parser.add_argument(
        "--port",
        default="11434",
        help=f"Ollama 端口 (預設：11434)"
    )
    
    # 其他選項
    parser.add_argument(
        "--prompt", "-p",
        help="自訂提示詞（會覆蓋預設提示詞）"
    )
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="僅檢查環境需求"
    )
    parser.add_argument(
        "--save-images",
        action="store_true",
        help="保存圖表區域的圖片"
    )
    
    args = parser.parse_args()
    
    # 檢查環境
    if args.check:
        check_environment(args)
        sys.exit(0)
    
    check_environment(args)
    
    # 處理檔案
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"❌ 輸入檔案不存在：{input_path}")
        sys.exit(1)
    
    if input_path.suffix.lower() in [".pdf"]:
        success = process_pdf(
            str(input_path),
            args.output,
            mode=args.mode,
            granularity=args.granularity,
            host=args.host,
            port=args.port,
            model=args.model,
            save_images=args.save_images,
            custom_prompt=args.prompt
        )
    elif input_path.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp", ".gif"]:
        success = process_image(
            str(input_path),
            args.output,
            mode=args.mode,
            host=args.host,
            port=args.port,
            model=args.model,
            custom_prompt=args.prompt
        )
    else:
        print(f"❌ 不支援的檔案格式：{input_path.suffix}")
        print("支援的格式：PDF, PNG, JPG, JPEG, WEBP, GIF")
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
