# -*- coding: utf-8 -*-
"""根据 security_results.json 生成自包含 SVG 雷达对比图（实测 vs 行业基线 vs 企业级）。

纯标准库，无外部依赖；输出 security_radar.html（内嵌 SVG，离线可看）。
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RES = os.path.join(ROOT, "security_results.json")
OUT = os.path.join(ROOT, "security_radar.html")

SERIES_COLOR = {
    "实测": "#1f77b4",
    "行业基线": "#ff7f0e",
    "企业级标准": "#2ca02c",
}


def polygon_points(cx, cy, r, values, max_v, n):
    pts = []
    for i, v in enumerate(values):
        ang = -90 + 360.0 / n * i
        rad = ang * 3.14159265358979 / 180.0
        rr = r * (v / max_v)
        x = cx + rr * pow(abs(__import__("math").cos(rad)), 1) * (1 if __import__("math").cos(rad) >= 0 else -1)
        y = cy + rr * pow(abs(__import__("math").sin(rad)), 1) * (1 if __import__("math").sin(rad) >= 0 else -1)
        pts.append((x, y))
    return pts


def main():
    data = json.load(open(RES, encoding="utf-8"))
    dims = [d["name"] for d in data["dimensions"]]
    series = data["series"]
    n = len(dims)
    cx, cy, R = 320, 300, 210
    max_v = 5

    import math
    # 网格圈
    grid = ""
    for lvl in (1, 2, 3, 4, 5):
        pts = []
        for i in range(n):
            ang = (-90 + 360.0 / n * i) * math.pi / 180.0
            rr = R * lvl / max_v
            pts.append(f"{cx + rr*math.cos(ang):.1f},{cy + rr*math.sin(ang):.1f}")
        grid += f'<polygon points="{" ".join(pts)}" fill="none" stroke="#ddd" stroke-width="1"/>\n'

    # 轴线 + 标签
    axes = ""
    labels = ""
    for i, name in enumerate(dims):
        ang = (-90 + 360.0 / n * i) * math.pi / 180.0
        x2 = cx + R * math.cos(ang)
        y2 = cy + R * math.sin(ang)
        axes += f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#ccc"/>\n'
        lx = cx + (R + 28) * math.cos(ang)
        ly = cy + (R + 28) * math.sin(ang)
        anchor = "middle"
        if math.cos(ang) > 0.3:
            anchor = "start"
        elif math.cos(ang) < -0.3:
            anchor = "end"
        labels += f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="13" fill="#333">{name}</text>\n'

    # 各序列多边形
    polys = ""
    for sname, vals in series.items():
        pts = []
        for i, v in enumerate(vals):
            ang = (-90 + 360.0 / n * i) * math.pi / 180.0
            rr = R * v / max_v
            pts.append(f"{cx + rr*math.cos(ang):.1f},{cy + rr*math.sin(ang):.1f}")
        color = SERIES_COLOR.get(sname, "#888")
        polys += f'<polygon points="{" ".join(pts)}" fill="{color}" fill-opacity="0.15" stroke="{color}" stroke-width="2"/>\n'
        for i, v in enumerate(vals):
            ang = (-90 + 360.0 / n * i) * math.pi / 180.0
            rr = R * v / max_v
            sx = cx + rr * math.cos(ang)
            sy = cy + rr * math.sin(ang)
            polys += f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="3" fill="{color}"/>\n'

    legend = ""
    for sname, color in SERIES_COLOR.items():
        legend += f'<span style="display:inline-block;margin-right:18px"><span style="display:inline-block;width:12px;height:12px;background:{color};border-radius:2px;margin-right:6px"></span>{sname}</span>'

    avg = sum(data["series"]["实测"]) / n
    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>安全·稳定性雷达 · {data['display_name']}</title></head>
<body style="font-family:-apple-system,'Microsoft YaHei',sans-serif;background:#fff;color:#222;margin:0;padding:24px">
<h2>🔐 {data['display_name']} · 安全·稳定性多维雷达对比</h2>
<p style="color:#666">版本 {data['version']} ｜ 测试时间 {data['test_time']} ｜ 模式：{data['mode']}</p>
<div style="text-align:center">{legend}</div>
<svg viewBox="0 0 640 620" width="640" height="620" xmlns="http://www.w3.org/2000/svg">
{grid}{axes}{labels}{polys}
</svg>
<div style="margin-top:8px">
<p><b>实测平均</b>：{avg:.2f} / 5 ｜ <b>维度</b>：{n}（密钥隔离 / 预算硬拦截 / 输入校验 / 错误处理 / 台账完整性 / 离线兜底 / 配置健壮性）</p>
<p style="color:#666">说明：雷达仅描述行为表现（如"预算达 100% 是否硬拦截"），不披露实现方法。行业基线取通用开源工具常见水位（3.0），企业级标准取 5.0 满分参照。</p>
</div>
</body></html>"""
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"雷达图已生成 -> {OUT}（实测平均 {avg:.2f}/5）")


if __name__ == "__main__":
    main()
