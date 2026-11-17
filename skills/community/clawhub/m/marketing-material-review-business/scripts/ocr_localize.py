#!/usr/bin/env python3
"""
本地OCR文字定位脚本（业务版 v1.1.1）
仅使用百度 OCR API：
  - 默认：高精度含位置版（accurate）
  - 可选：标准含位置版（general）
"""

import sys
import os

# 添加脚本目录到路径
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from PIL import Image, ImageDraw, ImageFont

# 颜色定义
HIGH_RISK_COLOR = (220, 50, 50)
MEDIUM_RISK_COLOR = (255, 165, 0)
LOW_RISK_COLOR = (50, 180, 50)
BLACK_COLOR = (40, 40, 40)
WHITE_BG = (255, 255, 255)
LIGHT_GRAY = (248, 248, 248)
CONNECTOR_COLOR = (100, 100, 100)

FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
]


def load_cjk_font(size):
    for font_path in FONT_CANDIDATES:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _get_baidu_access_token():
    """Get Baidu OCR access token from env or API key/secret."""
    access_token = os.environ.get('BAIDU_ACCESS_TOKEN', '').strip()
    if access_token:
        return access_token

    api_key = os.environ.get('BAIDU_API_KEY', '').strip()
    secret_key = os.environ.get('BAIDU_SECRET_KEY', '').strip()
    if not (api_key and secret_key):
        raise RuntimeError(
            "未配置百度 OCR。请设置 BAIDU_API_KEY 和 BAIDU_SECRET_KEY，"
            "或直接设置 BAIDU_ACCESS_TOKEN。"
        )

    import urllib.parse

    query = urllib.parse.urlencode({
        'grant_type': 'client_credentials',
        'client_id': api_key,
        'client_secret': secret_key,
    })
    data = _post_form(
        f'https://aip.baidubce.com/oauth/2.0/token?{query}',
        {},
        timeout=20,
    )
    if 'access_token' not in data:
        raise RuntimeError(f"Baidu token failed: {data}")
    return data['access_token']


def _post_form(url, params, timeout):
    """Post form data as JSON response; fall back to curl if Python DNS fails."""
    import json
    import subprocess
    import urllib.parse
    import urllib.request
    import urllib.error

    body = urllib.parse.urlencode(params).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=body,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.URLError as e:
        if 'nodename nor servname provided' not in str(e.reason):
            raise

    config = "\n".join([
        "silent",
        "show-error",
        f"max-time = {timeout}",
        f"url = \"{url}\"",
        "request = \"POST\"",
        "header = \"Content-Type: application/x-www-form-urlencoded\"",
        f"data = \"{body.decode('utf-8')}\"",
        "",
    ])
    proc = subprocess.run(
        ["curl", "-K", "-"],
        input=config,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"curl request failed: {proc.stderr.strip()}")
    return json.loads(proc.stdout)


def _baidu_vertices_from_item(item):
    """Return polygon vertices when Baidu provides them."""
    vertices = item.get('vertexes_location')
    if vertices:
        return [{'x': int(p.get('x', 0)), 'y': int(p.get('y', 0))} for p in vertices]
    return None


def _baidu_bbox_from_item(item):
    """Prefer polygon vertices, fall back to rectangular location."""
    vertices = _baidu_vertices_from_item(item)
    if vertices:
        xs = [p['x'] for p in vertices]
        ys = [p['y'] for p in vertices]
        return int(min(xs)), int(min(ys)), int(max(xs)), int(max(ys))

    loc = item.get('location', {})
    left = loc.get('left', 0)
    top = loc.get('top', 0)
    width = loc.get('width', 0)
    height = loc.get('height', 0)
    return int(left), int(top), int(left + width), int(top + height)


def ocr_with_baiduocr(img_path):
    """Use Baidu OCR high-accuracy-with-location REST API."""
    access_token = _get_baidu_access_token()
    if not access_token:
        return [], "baiduocr_skipped_no_env"

    import base64
    import urllib.parse

    endpoint_by_mode = {
        'accurate': 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate',
        'general': 'https://aip.baidubce.com/rest/2.0/ocr/v1/general',
    }
    mode = os.environ.get('BAIDU_OCR_MODE', 'accurate').strip().lower()
    endpoint = os.environ.get('BAIDU_OCR_ENDPOINT', endpoint_by_mode.get(mode, endpoint_by_mode['accurate'])).strip()

    with open(img_path, 'rb') as f:
        image_b64 = base64.b64encode(f.read())

    params = {
        'image': image_b64,
        'language_type': os.environ.get('BAIDU_OCR_LANGUAGE_TYPE', 'CHN_ENG'),
        'detect_direction': 'true',
        'vertexes_location': 'true',
        'paragraph': 'true',
        'probability': 'true',
        'multidirectional_recognize': os.environ.get('BAIDU_OCR_MULTIDIRECTIONAL', 'false'),
    }

    query = urllib.parse.urlencode({'access_token': access_token})
    result = _post_form(
        f'{endpoint}?{query}',
        params,
        timeout=int(os.environ.get('BAIDU_OCR_TIMEOUT', '60')),
    )
    if result.get('error_code'):
        raise RuntimeError(f"Baidu OCR failed: {result}")

    text_results = []
    for r in result.get('words_result', []):
        text = r.get('words', '').strip()
        if not text:
            continue

        x1, y1, x2, y2 = _baidu_bbox_from_item(r)
        vertices = _baidu_vertices_from_item(r)
        probability = r.get('probability') or {}
        confidence = probability.get('average', 0.9)

        region = {
            'x1': x1, 'y1': y1,
            'x2': x2, 'y2': y2,
            'text': text,
            'confidence': float(confidence),
            'source': f'baiduocr_{mode}',
        }
        if vertices:
            region['vertices'] = vertices
        text_results.append(region)

    return text_results, f"baiduocr_{mode}"


def find_text_by_content(image_path, target_text):
    """在图片中找到文字位置。target_text 保留为兼容旧调用。"""
    results, source = ocr_with_baiduocr(image_path)
    print(f"  [✓] {source} 成功，识别到 {len(results)} 个文字区域", file=sys.stderr)
    return results, source


def draw_bounding_boxes(img_path, regions, output_path):
    """在图片上绘制边界框"""
    img = Image.open(img_path)
    draw = ImageDraw.Draw(img)
    
    font = load_cjk_font(20)
    
    for i, reg in enumerate(regions):
        x1, y1, x2, y2 = reg['x1'], reg['y1'], reg['x2'], reg['y2']
        
        # 画框
        for offset in range(3):
            draw.rectangle([x1+offset, y1+offset, x2-offset, y2-offset],
                         outline=MEDIUM_RISK_COLOR, width=2)
        
        # 写编号
        draw.ellipse([x1-15, y1-15, x1+15, y1+15], fill=MEDIUM_RISK_COLOR)
        draw.text((x1-5, y1-8), str(i+1), fill=(255,255,255), font=font)
    
    img.save(output_path)
    print(f"边界框已保存: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("用法: python3 ocr_localize.py <图片路径> <输出路径>")
        print("示例: python3 ocr_localize.py input.jpg output.jpg")
        sys.exit(1)
    
    img_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not os.path.exists(img_path):
        print(f"错误: 图片不存在 {img_path}")
        sys.exit(1)
    
    print(f"正在分析图片: {img_path}")
    
    # 找文字区域
    try:
        regions, method = find_text_by_content(img_path, '')
    except Exception as e:
        print(f"错误: OCR 失败：{e}", file=sys.stderr)
        sys.exit(2)
    
    print(f"\n识别方法: {method}")
    print(f"识别到 {len(regions)} 个文字区域:\n")
    
    for i, reg in enumerate(regions):
        print(f"  {i+1}. x={reg['x1']}-{reg['x2']}, y={reg['y1']}-{reg['y2']}, conf={reg.get('confidence', 'N/A')}")
        if reg.get('text'):
            print(f"     文字: {reg['text']}")
    
    # 绘制边界框
    draw_bounding_boxes(img_path, regions, output_path)


if __name__ == "__main__":
    main()
