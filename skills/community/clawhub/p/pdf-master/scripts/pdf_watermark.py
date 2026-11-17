#!/usr/bin/env python3
"""pdf_watermark.py — 动态水印 + AES-256 加密 + 权限控制（能力 #4）

水印变量：{user_id} {date} {time} {custom}；对角平铺、半透明、避开四角。
用法：
  python3 pdf_watermark.py in.pdf out.pdf --text "工号{user_id} {date}" --user-id A1024
  python3 pdf_watermark.py in.pdf out.pdf --text "机密" --password pw123 --no-print --no-copy
"""
import argparse, datetime, sys

def render_text(tpl, user_id, custom):
    now = datetime.datetime.now()
    return (tpl.replace("{user_id}", user_id or "")
               .replace("{date}", now.strftime("%Y-%m-%d"))
               .replace("{time}", now.strftime("%H:%M"))
               .replace("{custom}", custom or ""))

def main():
    ap = argparse.ArgumentParser(description="PDF 水印+加密+权限")
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--text", default="{custom}", help='水印模板，支持 {user_id}{date}{time}{custom}')
    ap.add_argument("--user-id")
    ap.add_argument("--custom", default="机密文件")
    ap.add_argument("--opacity", type=float, default=0.15)
    ap.add_argument("--fontsize", type=int, default=48)
    ap.add_argument("--password", help="用户密码（打开密码）")
    ap.add_argument("--owner-password", help="所有者密码（默认随机）")
    ap.add_argument("--no-print", action="store_true")
    ap.add_argument("--no-copy", action="store_true")
    a = ap.parse_args()
    import fitz
    text = render_text(a.text, a.user_id, a.custom)
    # 含 CJK 字符时必须用内置中文字体，否则提取为乱码且显示缺字
    fontname = "china-s" if any(ord(c) > 127 for c in text) else "helv"
    doc = fitz.open(a.input)
    for page in doc:
        w, h = page.rect.width, page.rect.height
        # 对角平铺，间距 1.6 倍字号，避开四角 15% 区域（公章/签名位）
        step = a.fontsize * 8
        y = step * 0.5
        while y < h:
            x = step * 0.3
            while x < w:
                cx, cy = x / w, y / h
                if not (cx < 0.15 and cy < 0.15) and not (cx > 0.85 and cy < 0.15) \
                   and not (cx < 0.15 and cy > 0.85) and not (cx > 0.85 and cy > 0.85):
                    # 任意角度旋转用 morph 矩阵（insert_text 的 rotate 仅支持 90 的倍数）
                    page.insert_text((x, y), text, fontsize=a.fontsize, fontname=fontname,
                                     morph=(fitz.Point(x, y), fitz.Matrix(30)),
                                     color=(0.5, 0.5, 0.5), fill_opacity=a.opacity)
                x += step
            y += step
    perms = fitz.PDF_PERM_ACCESSIBILITY
    if not a.no_print:
        perms |= fitz.PDF_PERM_PRINT
    if not a.no_copy:
        perms |= fitz.PDF_PERM_COPY
    owner = a.owner_password or "owner-" + datetime.datetime.now().strftime("%s")
    if a.password:
        doc.save(a.output, encryption=fitz.PDF_ENCRYPT_AES_256,
                 user_pw=a.password, owner_pw=owner, permissions=perms,
                 garbage=3, deflate=True)
        print(f"✅ 已加密（AES-256）+ 权限：{'禁打印 ' if a.no_print else ''}{'禁复制' if a.no_copy else ''}")
        print("⚠️ 提醒：密码请与文件分渠道发送；权限控制依赖阅读器遵守，配合水印追溯才是完整方案")
    else:
        doc.save(a.output, garbage=3, deflate=True)
        print(f"✅ 水印已添加（未加密）")
    print(f"水印内容：{text}  不透明度：{a.opacity}")
    doc.close()

if __name__ == "__main__":
    main()
