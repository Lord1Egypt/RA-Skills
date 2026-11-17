# -*- coding: utf-8 -*-
"""
生成带二维码的简历分享卡片图 (1200x630)。
微信聊天框粘贴链接只显示纯蓝链、不渲染 OG 封面卡片（微信机制）；
发这张带二维码的图，朋友长按识别即开网页，是最稳的分享方案。
依赖: pip install Pillow qrcode
字体: Windows C:/Windows/Fonts/msyh.ttc (雅黑, .ttc 不是 .ttf)

用法:
  python gen_share_card.py --url "https://xxxx.gz3.agentos-app.net" \
        --name "您的姓名" --out share_card.png
"""
import argparse
import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/msyh.ttc"
FONT_B = "C:/Windows/Fonts/msyhbd.ttc"


def font(sz, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, sz)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="简历网页分享链接")
    ap.add_argument("--name", default="您的姓名")
    ap.add_argument("--title", default="《您的姓名 · 个人简历（对话版）》")
    ap.add_argument("--desc", default="10年+大厂AI落地实战派 · 可对话式了解工作经历/项目/论文")
    ap.add_argument("--out", default="share_card.png")
    a = ap.parse_args()

    # 二维码
    qr = qrcode.QRCode(box_size=10, border=2,
                       error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(a.url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#0b1220", back_color="white").convert("RGB").resize((300, 300))

    W, H = 1200, 630
    card = Image.new("RGB", (W, H), "#0b1220")

    # 左半：深蓝信息区
    left = Image.new("RGB", (760, H), "#0b1220")
    ld = ImageDraw.Draw(left)
    ld.rectangle([40, 250, 46, 410], fill="#38bdf8")
    ld.text((80, 210), a.name, font=font(64, True), fill="#ffffff")
    ld.text((82, 312), "AI博士 · 个人简历（对话版）", font=font(30, False), fill="#7dd3fc")
    ld.text((82, 372), "扫码查看完整简历", font=font(26, False), fill="#cbd5e1")
    card.paste(left, (0, 0))

    # 右半：白底面板 + 标题 + 二维码
    panel = Image.new("RGB", (W - 760, H), "#ffffff")
    pd = ImageDraw.Draw(panel)
    tx, ty = 40, 70
    pd.text((tx, ty), "扫码查看简历", font=font(40, True), fill="#0b1220"); ty += 60
    pd.text((tx, ty), a.title, font=font(20, False), fill="#33415c"); ty += 40
    pd.text((tx, ty), a.desc, font=font(18, False), fill="#5b6b85")
    qx, qy = 150, H - 300 - 60
    pd.rectangle([qx - 12, qy - 12, qx + 300 + 12, qy + 300 + 12], fill="#f1f5fb")
    panel.paste(qr_img, (qx, qy))
    card.paste(panel, (760, 0))

    card.save(a.out)
    print("share_card saved:", os.path.abspath(a.out))


if __name__ == "__main__":
    main()
