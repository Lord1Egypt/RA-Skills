#!/usr/bin/env python3
"""
💊 药片精确计数工具 v10 - 双模式 + 多参数投票
OpenCV模式使用3种参数组合投票，提高鲁棒性

用法:
    python3 pill_counter.py 图片.jpg                          # OpenCV模式（推荐）
    python3 pill_counter.py 图片.jpg --ai                    # AI模式（需MiMo API）
    python3 pill_counter.py 图片.jpg --save 标注图.jpg
    python3 pill_counter.py 图片.jpg --export-csv 统计.csv
"""

import sys, os, json, csv, base64, argparse
import numpy as np
from pathlib import Path
from collections import Counter

SHAPE_DEFS = {
    'round_s':  {'name': '小圆形',  'icon': '🟢', 'color': (0, 200, 0)},
    'round_m':  {'name': '中圆形',  'icon': '🔵', 'color': (255, 200, 0)},
    'round_l':  {'name': '大圆形',  'icon': '🟣', 'color': (200, 0, 255)},
    'oval':     {'name': '椭圆形',  'icon': '🟠', 'color': (0, 140, 255)},
    'capsule':  {'name': '胶囊形',  'icon': '🔴', 'color': (0, 0, 255)},
    'triangle': {'name': '三角形',  'icon': '🔺', 'color': (255, 0, 255)},
    'square':   {'name': '四方形',  'icon': '⬜', 'color': (255, 255, 0)},
    'diamond':  {'name': '菱形',    'icon': '🔷', 'color': (255, 128, 0)},
    'hexagon':  {'name': '六边形',  'icon': '⬡',  'color': (0, 255, 255)},
    'pentagon': {'name': '五边形',  'icon': '⬠',  'color': (128, 255, 128)},
    'octagon':  {'name': '八边形',  'icon': '🛑', 'color': (128, 128, 255)},
    'polygon':  {'name': '多边形',  'icon': '⬠',  'color': (200, 200, 200)},
    'other':    {'name': '其他',    'icon': '❓', 'color': (128, 128, 128)},
}
SHAPE_ORDER = list(SHAPE_DEFS.keys())

# ==================== AI模式 ====================

def detect_with_ai(image_path):
    import urllib.request
    config_path = os.path.expanduser('~/.openclaw/openclaw.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    api_key = config.get('models', {}).get('providers', {}).get('xiaomi-coding', {}).get('apiKey')
    if not api_key:
        print("❌ 未找到 MiMo API 密钥"); sys.exit(1)

    from PIL import Image
    import io
    img = Image.open(image_path)
    img.thumbnail((1024, 1024))
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=70)
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    prompt = """请仔细数一数这张图片中的药片数量。要求：数出每一粒，注意重叠的药片要分别计数，按形状分类。用JSON格式回复：
{"total":总数,"categories":{"小圆形":数量,"中圆形":数量,"大圆形":数量,"椭圆形":数量,"胶囊形":数量,"三角形":数量,"四方形":数量,"其他":数量}}"""

    payload = {"model": "mimo-v2-omni", "max_tokens": 1024, "messages": [{"role": "user", "content": [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
    ]}]}

    req = urllib.request.Request("https://api.xiaomimimo.com/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"})

    print("🤖 正在调用 MiMo V2 Omni 分析...")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            content = result['choices'][0]['message']['content']
            import re
            json_match = re.search(r'\{[^{}]*\{[^{}]*\}[^{}]*\}', content, re.DOTALL)
            if json_match:
                ai_result = json.loads(json_match.group())
                name_map = {'小圆形':'round_s','中圆形':'round_m','大圆形':'round_l',
                           '椭圆形':'oval','胶囊形':'capsule','三角形':'triangle',
                           '四方形':'square','菱形':'diamond','六边形':'hexagon',
                           '五边形':'pentagon','八边形':'octagon','多边形':'polygon','其他':'other'}
                categories = []
                for name, count in ai_result.get('categories', {}).items():
                    type_key = name_map.get(name, 'other')
                    if count > 0:
                        defn = SHAPE_DEFS.get(type_key, SHAPE_DEFS['other'])
                        categories.append({'type': type_key, 'name': defn['name'], 'icon': defn['icon'], 'count': count})
                return ai_result.get('total', 0), categories, None
    except Exception as e:
        print(f"❌ AI调用失败: {e}")
    return None, None, None

# ==================== OpenCV模式（多参数投票） ====================

def detect_single_param(image_path, threshold, morph_kernel, dist_ratio, min_area_ratio, max_area_ratio):
    """单组参数检测"""
    import cv2
    import numpy as np

    img = cv2.imread(image_path)
    if img is None:
        return []
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)
    kernel = np.ones((morph_kernel, morph_kernel), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    _, dt = cv2.threshold(dist, dist_ratio * dist.max(), 255, 0)
    dt = np.uint8(dt)

    contours, _ = cv2.findContours(dt, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img_area = h * w
    min_a = max(100, img_area * min_area_ratio)  # 最小100px²防止漏检
    max_a = img_area * max_area_ratio

    pills = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_a or area > max_a:
            continue
        x, y, bw, bh = cv2.boundingRect(cnt)
        pills.append({
            'x': int(x), 'y': int(y), 'w': int(bw), 'h': int(bh),
            'area': float(area), 'cx': x + bw//2, 'cy': y + bh//2,
            'aspect_ratio': round(float(bw)/bh if bh>0 else 0, 3),
            'circularity': round(4*np.pi*area/(cv2.arcLength(cnt,True)**2) if cv2.arcLength(cnt,True)>0 else 0, 4),
            'num_vertices': len(cv2.approxPolyDP(cnt, 0.04*cv2.arcLength(cnt,True), True)),
        })
    return pills

def merge_pills_groups(groups):
    """合并多组检测结果，基于位置重叠判断"""
    if not groups:
        return []

    # 找出所有药片位置
    all_pills = []
    for pills in groups:
        all_pills.extend(pills)

    if not all_pills:
        return []

    # 基于位置聚类：两个药片中心距离 < 阈值则视为同一药片
    merged = []
    used = set()

    for i, p in enumerate(all_pills):
        if i in used:
            continue
        # 找所有接近的药片
        cluster = [p]
        used.add(i)
        for j, q in enumerate(all_pills):
            if j in used:
                continue
            dist = ((p['cx']-q['cx'])**2 + (p['cy']-q['cy'])**2)**0.5
            avg_size = (p['w'] + p['h'] + q['w'] + q['h']) / 4
            if dist < avg_size * 0.40:  # 中心距离 < 平均尺寸的40%
                cluster.append(q)
                used.add(j)

        # 选择面积最接近中位数的作为代表
        areas = [c['area'] for c in cluster]
        median_area = sorted(areas)[len(areas)//2]
        best = min(cluster, key=lambda c: abs(c['area'] - median_area))
        best['confidence'] = len(cluster)  # 被多少组检测到
        merged.append(best)

    return merged

def classify_shape(pill, areas_median):
    ar = pill['aspect_ratio']
    cr = pill['circularity']
    nv = pill['num_vertices']
    area = pill['area']

    if cr > 0.70:
        if area < areas_median * 0.65: return 'round_s'
        elif area > areas_median * 1.45: return 'round_l'
        else: return 'round_m'
    if cr > 0.55:
        if area < areas_median * 0.65: return 'round_s'
        elif area > areas_median * 1.45: return 'round_l'
        else: return 'round_m'
    if ar > 2.0 or ar < 0.5: return 'capsule'
    if ar > 1.45 or ar < 0.69: return 'oval'
    if nv == 3: return 'triangle'
    if nv == 4: return 'square' if 0.78 < ar < 1.28 else 'diamond'
    if nv == 5: return 'pentagon'
    if nv == 6: return 'hexagon'
    if nv >= 7: return 'polygon'
    return 'other'

def detect_with_opencv(image_path):
    """多参数投票检测"""
    # 3组参数（覆盖不同阈值偏好）
    param_sets = [
        {'threshold': 175, 'morph_kernel': 3, 'dist_ratio': 0.33, 'min_area_ratio': 0.00003, 'max_area_ratio': 0.035},
        {'threshold': 180, 'morph_kernel': 3, 'dist_ratio': 0.35, 'min_area_ratio': 0.00003, 'max_area_ratio': 0.035},
        {'threshold': 185, 'morph_kernel': 3, 'dist_ratio': 0.37, 'min_area_ratio': 0.00003, 'max_area_ratio': 0.035},
    ]

    groups = []
    for params in param_sets:
        pills = detect_single_param(image_path, **params)
        groups.append(pills)

    # 用中位数结果（更稳定）
    counts = [len(g) for g in groups]
    median_count = sorted(counts)[len(counts)//2]
    # 找最接近中位数的那组
    best_group = min(groups, key=lambda g: abs(len(g) - median_count))
    merged = best_group

    # 分类
    areas = [p['area'] for p in merged]
    median_area = np.median(areas) if areas else 0
    for p in merged:
        p['shape'] = classify_shape(p, median_area)

    # 统计
    counter = Counter(p['shape'] for p in merged)
    categories = []
    for key in SHAPE_ORDER:
        cnt = counter.get(key, 0)
        if cnt > 0:
            defn = SHAPE_DEFS[key]
            categories.append({'type': key, 'name': defn['name'], 'icon': defn['icon'], 'count': cnt})

    return len(merged), categories, merged

# ==================== 输出 ====================

def format_text(total, categories, mode):
    lines = [
        "=" * 50,
        "        📊 药片计数结果",
        "=" * 50,
        f"  🤖 识别模式: {mode}",
        f"  ✅ 检测总数: {total} 粒",
        "",
        f"  {'类型':<10} {'数量':>6}  {'占比':>8}",
        "  " + "-" * 38,
    ]
    for cat in categories:
        pct = cat['count'] / total * 100 if total else 0
        lines.append(f"  {cat['icon']} {cat['name']:<8} {cat['count']:>5} 粒  {pct:>6.1f}%")
    lines.append("  " + "-" * 38)
    lines.append(f"  {'合计':<10} {total:>5} 粒  100.0%")
    lines.append("=" * 50)
    return "\n".join(lines)

def export_csv(csv_path, total, categories):
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['类型', '数量', '占比'])
        for cat in categories:
            pct = cat['count'] / total * 100 if total else 0
            writer.writerow([cat['name'], cat['count'], f"{pct:.1f}%"])
        writer.writerow(['合计', total, '100.0%'])

def draw_result(img_path, pills, output_path):
    import cv2
    img = cv2.imread(img_path)
    font = cv2.FONT_HERSHEY_SIMPLEX

    for i, p in enumerate(pills):
        defn = SHAPE_DEFS.get(p.get('shape', 'other'), SHAPE_DEFS['other'])
        color = defn['color']
        x, y, w, h = p['x'], p['y'], p['w'], p['h']
        thickness = 3 if p.get('confidence', 1) >= 2 else 2  # 高置信度加粗
        cv2.rectangle(img, (x, y), (x+w, y+h), color, thickness)
        cv2.putText(img, str(i+1), (x+3, y+h//2+4), font, 0.32, color, 1)

    # 图例
    counter = Counter(p.get('shape', 'other') for p in pills)
    legend_x = img.shape[1] - 220
    legend_y = 15
    items = [(k, counter[k]) for k in SHAPE_ORDER if counter.get(k, 0) > 0]
    box_h = len(items) * 24 + 10
    cv2.rectangle(img, (legend_x-5, legend_y-5), (img.shape[1]-5, legend_y+box_h), (255,255,255), -1)
    cv2.rectangle(img, (legend_x-5, legend_y-5), (img.shape[1]-5, legend_y+box_h), (0,0,0), 1)
    for key, cnt in items:
        defn = SHAPE_DEFS[key]
        cv2.rectangle(img, (legend_x, legend_y), (legend_x+16, legend_y+16), defn['color'], -1)
        cv2.putText(img, f"{defn['name']}: {cnt}", (legend_x+22, legend_y+14), font, 0.45, (0,0,0), 1)
        legend_y += 24
    cv2.imwrite(output_path, img)

def main():
    parser = argparse.ArgumentParser(description='💊 药片精确计数工具 v10 - 双模式')
    parser.add_argument('image', help='药片图片路径')
    parser.add_argument('--ai', action='store_true', help='使用 MiMo V2 Omni AI 识别')
    parser.add_argument('--save', help='保存标注结果图片路径')
    parser.add_argument('--export-csv', help='导出 CSV 统计表格路径')
    parser.add_argument('--output', choices=['text', 'json'], default='text')
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"❌ 文件不存在: {args.image}"); sys.exit(1)

    if args.ai:
        mode = "MiMo V2 Omni (AI)"
        total, categories, pills = detect_with_ai(args.image)
        if total is None:
            print("⚠️ AI失败，回退到 OpenCV")
            mode = "OpenCV 投票模式"
            total, categories, pills = detect_with_opencv(args.image)
    else:
        mode = "OpenCV 投票模式 (3参数)"
        total, categories, pills = detect_with_opencv(args.image)

    if total == 0:
        print("❌ 未检测到药片"); sys.exit(1)

    if args.output == 'json':
        print(json.dumps({'total': total, 'mode': mode, 'categories': {c['name']:c['count'] for c in categories}}, ensure_ascii=False, indent=2))
    else:
        print(format_text(total, categories, mode))

    if pills:
        default_out = str(Path(args.image).with_suffix('')) + '_result.jpg'
        draw_result(args.image, pills, args.save or default_out)
        print(f"📁 标注图片: {args.save or default_out}")

    csv_path = args.export_csv or str(Path(args.image).with_suffix('')) + '_report.csv'
    export_csv(csv_path, total, categories)
    print(f"📊 统计表格: {csv_path}")

if __name__ == "__main__":
    main()
