# -*- coding: utf-8 -*-

import os
import subprocess
import json
import requests
from pathlib import Path
from PIL import Image
import re


# =============================
# 读取配置
# =============================
def load_config():

    config_path = Path(__file__).parent / "config.json"

    if not config_path.exists():
        raise Exception("未找到 config.json")

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


# =============================
# PPT → PDF
# =============================
def ppt_to_pdf(ppt_path, output_dir, libreoffice_path):

    cmd = [
        libreoffice_path,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", str(output_dir),
        str(ppt_path)
    ]

    print("正在转换 PPT → PDF")
    subprocess.run(cmd, check=True)

    pdf_path = output_dir / (ppt_path.stem + ".pdf")

    return pdf_path


# =============================
# PDF → PNG
# =============================
def pdf_to_png(pdf_path, output_dir, dpi, ghostscript_path):

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

    print("PDF → PNG")
    subprocess.run(cmd, check=True)

    images = sorted(output_dir.glob(f"{pdf_path.stem}_page_*.png"))

    print("图片数量:", len(images))

    return images


# =============================
# 缩略图
# =============================
def make_thumbnails(images, output_dir, cols, rows):

    thumb_dir = output_dir / "thumbnails"
    thumb_dir.mkdir(exist_ok=True)

    group_size = cols * rows

    for i in range(0, len(images), group_size):

        group = images[i:i + group_size]

        imgs = [Image.open(p) for p in group]

        w, h = imgs[0].size

        thumb_w = w // 3
        thumb_h = h // 3

        resized = [img.resize((thumb_w, thumb_h), Image.LANCZOS) for img in imgs]

        canvas = Image.new("RGB", (thumb_w * cols, thumb_h * rows), "white")

        for idx, img in enumerate(resized):

            row = idx // cols
            col = idx % cols

            canvas.paste(img, (col * thumb_w, row * thumb_h))

        canvas.save(thumb_dir / f"thumb_{i//group_size + 1:03d}.png")


# =============================
# Markdown 图集
# =============================
def generate_markdown(images, output_dir, ppt_name):

    md_path = output_dir / f"{ppt_name}.md"

    with open(md_path, "w", encoding="utf-8") as f:

        f.write(f"# {ppt_name}\n\n")

        for i, img in enumerate(images, 1):

            f.write(f"## 第{i}页\n\n")
            f.write(f"![{img.name}]({img.name})\n\n")

    print("Markdown 已生成")


# =============================
# 微信接口
# =============================
def get_access_token(appid, secret):

    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'

    r = requests.get(url).json()

    return r.get("access_token")


def upload_permanent_image(access_token, file_path):

    url = f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image'

    with open(file_path, 'rb') as f:

        r = requests.post(url, files={'media': f}).json()

    return r.get("media_id")


def upload_image_get_url(access_token, file_path):

    url = f'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}'

    with open(file_path, 'rb') as f:

        r = requests.post(url, files={'media': f}).json()

    return r.get("url")


# =============================
# 压缩图片
# =============================
def compress_image(path, max_size=1024 * 1024):

    quality = 85

    while os.path.getsize(path) > max_size and quality > 10:

        img = Image.open(path)

        img.save(path, quality=quality)

        quality -= 5


# =============================
# HTML内容
# =============================
def build_article_content(image_urls):

    content = "<p>"

    for url in image_urls:

        content += f'<img src="{url}" data-width="100%" /><br/>'

    content += "</p>"

    return content


# =============================
# 创建草稿
# =============================
def create_draft(access_token, article):

    data = {"articles": [article]}

    r = requests.post(
        "https://api.weixin.qq.com/cgi-bin/draft/add",
        params={"access_token": access_token},
        data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    return r.json()


# =============================
# 发布微信草稿
# =============================
def publish_wechat(config, image_dir):

    access_token = get_access_token(
        config["wechat_appid"],
        config["wechat_appsecret"]
    )

    if not access_token:
        print("access_token 获取失败")
        return

    images = sorted(Path(image_dir).glob("*.png"))

    cover = images[0]

    compress_image(cover)

    thumb_media_id = upload_permanent_image(access_token, cover)

    image_urls = []

    for img in images[1:]:

        compress_image(img)

        url = upload_image_get_url(access_token, img)

        if url:
            image_urls.append(url)

    article = {

        "title": Path(image_dir).name + "（无中缝，无水印，高清PPT，带教案）",

        "author": config["wechat_author"],

        "digest": Path(image_dir).name,

        "content": build_article_content(image_urls),

        "thumb_media_id": thumb_media_id,

        "show_cover_pic": 1
    }

    result = create_draft(access_token, article)

    print("微信草稿返回:", result)


# =============================
# 主流程
# =============================
def main():

    config = load_config()

    ppt_dir = Path(config["ppt_dir"])
    ppt_file = config["ppt_file"]

    ppt_path = ppt_dir / ppt_file

    work_dir = ppt_dir / ppt_path.stem

    work_dir.mkdir(exist_ok=True)

    pdf = ppt_to_pdf(ppt_path, work_dir, config["libreoffice_path"])

    images = pdf_to_png(pdf, work_dir, config["dpi"], config["ghostscript_path"])

    make_thumbnails(images, work_dir, config["thumbnail_cols"], config["thumbnail_rows"])

    generate_markdown(images, work_dir, ppt_path.stem)

    publish_wechat(config, work_dir)

    print("🎉 全流程完成")


if __name__ == "__main__":
    main()