#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iBook Widget 打包辅助脚本
用法：python3 pack_widget.py <源项目目录> <widget名称> <游戏中文名> [版本号] [输出目录]

示例：
  python3 pack_widget.py ./my-game my-game "我的游戏" 1.0 /tmp/output
"""

import os
import sys
import shutil
import zipfile
import re
import argparse

# ── 尝试导入 Pillow ──────────────────────────────────────────────────────────
try:
    from PIL import Image, ImageDraw
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False


def make_thumbnail(path, size, game_name):
    """生成渐变色缩略图"""
    if not HAS_PILLOW:
        print(f"  [警告] Pillow 未安装，跳过缩略图生成: {path}")
        print("  请运行: pip3 install Pillow")
        # 创建一个最小有效的 PNG（1×1 白色像素）作为占位
        import struct, zlib
        def png1x1():
            def chunk(name, data):
                c = struct.pack('>I', len(data)) + name + data
                return c + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)
            sig = b'\x89PNG\r\n\x1a\n'
            ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
            idat = chunk(b'IDAT', zlib.compress(b'\x00\xff\xff\xff'))
            iend = chunk(b'IEND', b'')
            return sig + ihdr + idat + iend
        with open(path, 'wb') as f:
            f.write(png1x1())
        return

    w, h = size
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)

    # 渐变背景（紫蓝渐变）
    for i in range(h):
        r = int(80  + (130 - 80)  * i / h)
        g = int(40  + (60  - 40)  * i / h)
        b = int(160 + (220 - 160) * i / h)
        draw.line([(0, i), (w, i)], fill=(r, g, b))

    # 中央圆形装饰
    cx, cy = w // 2, h // 2
    r = min(w, h) // 4
    draw.ellipse([cx - r, cy - r - 10, cx + r, cy + r - 10],
                 outline='white', width=max(2, w // 100))

    # 游戏名称文字（仅绘制ASCII字符，避免中文编码问题）
    ascii_name = ''.join(c for c in game_name if ord(c) < 128)
    if not ascii_name:
        ascii_name = 'Widget'
    name_display = ascii_name[:12] if len(ascii_name) > 12 else ascii_name
    draw.text((cx - len(name_display) * (w // 40), cy - 16),
              name_display, fill='white')

    img.save(path)
    print(f"  ✅ 缩略图: {path} ({w}×{h})")


def generate_info_plist(display_name, identifier, bundle_name, version, width=1024, height=768):
    """生成 Info.plist 内容"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleDisplayName</key>
  <string>{display_name}</string>
  <key>CFBundleIdentifier</key>
  <string>{identifier}</string>
  <key>CFBundleName</key>
  <string>{bundle_name}</string>
  <key>CFBundleShortVersionString</key>
  <string>{version}</string>
  <key>CFBundleVersion</key>
  <string>{version}</string>
  <key>MainHTML</key>
  <string>index.html</string>
  <key>AllowNetworkAccess</key>
  <false/>
  <key>Width</key>
  <integer>{width}</integer>
  <key>Height</key>
  <integer>{height}</integer>
</dict>
</plist>
'''


def fix_resource_paths(html_content, resource_files):
    """
    修正 index.html 中的资源引用路径。
    将平铺的文件名引用改为 peresources/文件名 引用。
    """
    for filename in resource_files:
        # 匹配 src="filename" 或 href="filename"（不含路径前缀）
        pattern_src  = re.compile(r'(src=["\'])(?!https?://|//|peresources/)(' + re.escape(filename) + r')(["\'])')
        pattern_href = re.compile(r'(href=["\'])(?!https?://|//|peresources/)(' + re.escape(filename) + r')(["\'])')
        html_content = pattern_src.sub(r'\1peresources/\2\3', html_content)
        html_content = pattern_href.sub(r'\1peresources/\2\3', html_content)
    return html_content


def pack_widget(src_dir, widget_name, display_name, version='1.0', output_dir=None):
    """
    主打包函数
    :param src_dir: 源项目目录（包含 index.html）
    :param widget_name: widget 名称（英文，如 my-game）
    :param display_name: 游戏中文显示名
    :param version: 版本号
    :param output_dir: 输出目录，默认为 src_dir 的父目录
    """
    src_dir = os.path.abspath(src_dir)
    if output_dir is None:
        output_dir = os.path.dirname(src_dir)
    output_dir = os.path.abspath(output_dir)

    wdgt_dir = os.path.join(output_dir, f'{widget_name}.wdgt')
    res_dir  = os.path.join(wdgt_dir, 'peresources')

    print(f"\n📦 开始打包 Widget: {widget_name}")
    print(f"  源目录: {src_dir}")
    print(f"  输出目录: {wdgt_dir}")

    # ── Step 1: 创建目录结构 ────────────────────────────────────────────────
    if os.path.exists(wdgt_dir):
        shutil.rmtree(wdgt_dir)
    os.makedirs(res_dir, exist_ok=True)
    print("  ✅ 创建目录结构")

    # ── Step 2: 复制资源文件到 peresources/ ────────────────────────────────
    RESOURCE_EXTS = {'.css', '.js', '.json', '.png', '.jpg', '.jpeg',
                     '.gif', '.svg', '.ico', '.woff', '.woff2', '.ttf',
                     '.mp3', '.ogg', '.wav', '.mp4', '.webm'}
    resource_files = []

    index_html_path = os.path.join(src_dir, 'index.html')
    if not os.path.exists(index_html_path):
        print(f"  ❌ 错误：找不到 {index_html_path}")
        sys.exit(1)

    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)
        _, ext = os.path.splitext(item.lower())
        if os.path.isfile(item_path) and ext in RESOURCE_EXTS:
            shutil.copy2(item_path, os.path.join(res_dir, item))
            resource_files.append(item)

    # 如果已有 peresources 子目录，整体复制
    src_res = os.path.join(src_dir, 'peresources')
    if os.path.isdir(src_res):
        for item in os.listdir(src_res):
            shutil.copy2(os.path.join(src_res, item), os.path.join(res_dir, item))
            resource_files.append(item)

    print(f"  ✅ 复制资源文件 {len(resource_files)} 个: {resource_files}")

    # ── Step 3: 修正 index.html 路径并写入 ─────────────────────────────────
    with open(index_html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 仅修正平铺文件（不在 peresources/ 下的引用）
    flat_resources = [f for f in resource_files if '/' not in f]
    html_fixed = fix_resource_paths(html, flat_resources)

    # 确保有 viewport meta
    if 'viewport-fit=cover' not in html_fixed:
        viewport_meta = (
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />\n'
            '  <meta name="apple-mobile-web-app-capable" content="yes" />\n'
            '  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />'
        )
        html_fixed = html_fixed.replace(
            '<meta name="viewport"',
            viewport_meta + '\n  <!-- viewport replaced -->\n  <meta name="viewport-replaced"'
        ) if '<meta name="viewport"' in html_fixed else html_fixed.replace(
            '</head>', f'  {viewport_meta}\n</head>'
        )

    with open(os.path.join(wdgt_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_fixed)
    print("  ✅ 写入 index.html（资源路径已修正）")

    # ── Step 4: 生成 Info.plist ─────────────────────────────────────────────
    identifier  = f"com.{re.sub(r'[^a-z0-9]', '', widget_name.lower())}.widget"
    bundle_name = ''.join(w.capitalize() for w in widget_name.split('-'))

    plist_content = generate_info_plist(display_name, identifier, bundle_name, version)
    with open(os.path.join(wdgt_dir, 'Info.plist'), 'w', encoding='utf-8') as f:
        f.write(plist_content)
    print("  ✅ 生成 Info.plist")

    # ── Step 5: 生成缩略图 ──────────────────────────────────────────────────
    make_thumbnail(os.path.join(wdgt_dir, 'Default.png'),    (1024, 768),  display_name)
    make_thumbnail(os.path.join(wdgt_dir, 'Default@2x.png'), (2048, 1536), display_name)

    # ── Step 6: 打包成 zip ──────────────────────────────────────────────────
    zip_path = os.path.join(output_dir, f'{widget_name}.wdgt.zip')
    if os.path.exists(zip_path):
        os.remove(zip_path)

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(wdgt_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                arc_name = os.path.relpath(abs_path, output_dir)
                zf.write(abs_path, arc_name)

    zip_size = os.path.getsize(zip_path)
    print(f"\n✅ 打包完成！")
    print(f"  输出文件: {zip_path}")
    print(f"  文件大小: {zip_size / 1024:.1f} KB")

    # ── Step 7: 显示包体结构 ────────────────────────────────────────────────
    print(f"\n📁 包体结构:")
    for root, dirs, files in os.walk(wdgt_dir):
        level = root.replace(wdgt_dir, '').count(os.sep)
        indent = '  ' * level
        print(f"  {indent}{os.path.basename(root)}/")
        for f in sorted(files):
            print(f"  {indent}  {f}")

    return zip_path


def main():
    parser = argparse.ArgumentParser(description='将 H5 游戏打包成 iBook Widget (.wdgt)')
    parser.add_argument('src_dir',      help='源项目目录（含 index.html）')
    parser.add_argument('widget_name',  help='Widget 名称（英文+连字符，如 my-game）')
    parser.add_argument('display_name', help='游戏中文显示名（如 我的游戏）')
    parser.add_argument('version',      nargs='?', default='1.0', help='版本号（默认 1.0）')
    parser.add_argument('output_dir',   nargs='?', default=None,  help='输出目录（默认为源目录的父目录）')
    args = parser.parse_args()

    zip_path = pack_widget(
        args.src_dir,
        args.widget_name,
        args.display_name,
        args.version,
        args.output_dir
    )
    print(f"\n🎉 Widget 已就绪: {zip_path}")


if __name__ == '__main__':
    main()
