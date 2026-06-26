import sys
import os
import subprocess
import logging
from pathlib import Path

def ensure_ocrmypdf():
    """Check if ocrmypdf is installed, otherwise raise informative error."""
    try:
        subprocess.run(["ocrmypdf", "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        raise RuntimeError(
            "ocrmypdf 未安装或未在 PATH 中。请先运行: \n"
            "    pip install ocrmypdf\n"
            "并确保 Tesseract 已正确安装（Windows 推荐 MSI 安装包），其路径已加入系统 PATH。"
        ) from e

def ocr_file(input_pdf: Path, output_pdf: Path, lang: str = "chi_sim"):
    cmd = ["ocrmypdf", "-l", lang, str(input_pdf), str(output_pdf)]
    subprocess.run(cmd, check=True)

def batch_dir(dir_path: Path, lang: str = "chi_sim"):
    for pdf_path in dir_path.rglob("*.pdf"):
        out_path = pdf_path.with_name(pdf_path.stem + "_ocr.pdf")
        try:
            ocr_file(pdf_path, out_path, lang)
            logging.info(f"OCR 成功: {pdf_path} -> {out_path}")
        except Exception as exc:
            logging.error(f"OCR 失败: {pdf_path}: {exc}")

def main(argv):
    import argparse
    parser = argparse.ArgumentParser(description="批量 OCR 扫描 PDF 并生成带文字层的 PDF")
    parser.add_argument("input_pdf", nargs="?", help="单个 PDF 文件路径")
    parser.add_argument("output_pdf", nargs="?", help="输出 PDF 路径（单文件模式）")
    parser.add_argument("--batch-dir", help="批量处理目录，递归查找 *.pdf")
    parser.add_argument("--lang", default="chi_sim", help="OCR 语言代码，默认 chi_sim（简体中文）")
    args = parser.parse_args(argv)

    logging.basicConfig(filename=str(Path("logs") / "pdf_ocr_error.log"), level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")

    try:
        ensure_ocrmypdf()
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    if args.batch_dir:
        batch_dir(Path(args.batch_dir), args.lang)
    elif args.input_pdf and args.output_pdf:
        ocr_file(Path(args.input_pdf), Path(args.output_pdf), args.lang)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
