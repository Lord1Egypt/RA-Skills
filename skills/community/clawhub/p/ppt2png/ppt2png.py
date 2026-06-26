import os
import subprocess
import json
from pathlib import Path
from PIL import Image


# =============================
# 读取配置文件
# =============================
def load_config():
    config_path = Path(__file__).parent / "config.json"
    if not config_path.exists():
        raise Exception("未找到 config.json 配置文件")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


# =============================
# 1️⃣ PPT 转 PDF
# =============================
def ppt_to_pdf(ppt_path, output_dir, libreoffice_path):
    ppt_path = Path(ppt_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        libreoffice_path,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_dir),
        str(ppt_path)
    ]

    print("正在转换 PPT → PDF ...")
    subprocess.run(cmd, check=True)

    pdf_path = output_dir / (ppt_path.stem + ".pdf")
    if not pdf_path.exists():
        raise Exception("PDF 生成失败")

    print("PDF 生成完成:", pdf_path)
    return pdf_path


# =============================
# 2️⃣ PDF 每页转 PNG
# =============================
def pdf_to_png(pdf_path, output_dir, dpi, ghostscript_path):
    pdf_path = Path(pdf_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = output_dir / f"{pdf_path.stem}_page_%03d.png"

    cmd = [
        ghostscript_path,
        "-dSAFER",
        "-dBATCH",
        "-dNOPAUSE",
        "-sDEVICE=png16m",
        f"-r{dpi}",
        f"-sOutputFile={output_pattern}",
        str(pdf_path)
    ]

    print("正在转换 PDF → PNG ...")
    subprocess.run(cmd, check=True)

    print("PNG 生成完成")

    images = sorted(output_dir.glob(f"{pdf_path.stem}_page_*.png"))
    print(f"共生成 {len(images)} 张图片")
    return images


# =============================
# 3️⃣ 生成缩略图
# =============================
def make_thumbnails(images, output_dir, cols, rows):
    output_dir = Path(output_dir)
    thumb_dir = output_dir / "thumbnails"
    thumb_dir.mkdir(exist_ok=True)

    group_size = cols * rows
    total = len(images)

    print("正在生成缩略图...")

    for i in range(0, total, group_size):
        group = images[i:i + group_size]

        imgs = [Image.open(p) for p in group]

        w, h = imgs[0].size
        thumb_w = w // 3
        thumb_h = h // 3

        resized = [img.resize((thumb_w, thumb_h), Image.LANCZOS) for img in imgs]

        canvas_w = thumb_w * cols
        canvas_h = thumb_h * rows
        canvas = Image.new("RGB", (canvas_w, canvas_h), "white")

        for idx, img in enumerate(resized):
            row = idx // cols
            col = idx % cols
            x = col * thumb_w
            y = row * thumb_h
            canvas.paste(img, (x, y))

        output_path = thumb_dir / f"thumb_{i//group_size + 1:03d}.png"
        canvas.save(output_path)

    total_thumbs = (total - 1) // group_size + 1
    print(f"缩略图生成完成，共 {total_thumbs} 张")


# =============================
# 主流程
# =============================
def main():
    config = load_config()

    ppt_path = config["ppt_file"]
    output_root = config["output_folder"]
    libreoffice_path = config["libreoffice_path"]
    ghostscript_path = config["ghostscript_path"]
    dpi = config["dpi"]
    cols = config["thumbnail_cols"]
    rows = config["thumbnail_rows"]

    ppt_path = Path(ppt_path).resolve()
    output_root = Path(output_root).resolve()

    work_dir = output_root / ppt_path.stem
    work_dir.mkdir(parents=True, exist_ok=True)

    # Step 1
    pdf_path = ppt_to_pdf(ppt_path, work_dir, libreoffice_path)

    # Step 2
    images = pdf_to_png(pdf_path, work_dir, dpi, ghostscript_path)

    # Step 3
    make_thumbnails(images, work_dir, cols, rows)

    print("\n🎉 全部完成")


# =============================
# 运行入口
# =============================
if __name__ == "__main__":
    main()