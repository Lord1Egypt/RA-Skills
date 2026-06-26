#!/usr/bin/env python3
"""
brand_init.py — v3.7 品牌 Theme 系统（媲美 Gamma 一键 brand 注入）

输入 logo 图片 → 提取主色调 + 字体推荐 → 输出：
  1. brand-pack.json   StylePack 增量配置（覆盖 accent / accent_soft）
  2. brand-spec.md     人类可读规范（用于 huo15-openclaw-brand-protocol 5 步流程）

主色提取算法（纯 PIL 实现，无第三方依赖）：
  1. 缩放到 200x200
  2. 像素聚类（量化到 16 色调色板）
  3. 排除接近白/黑/灰色（HSL S < 0.15 或 V > 95% 或 V < 5%）
  4. 按面积排序取 top-3
  5. 推断 primary（最饱和或最大面积）

集成 huo15-openclaw-brand-protocol v1.0 的 Ask/Search/Download/Verify/Codify 5 步：
  - 本工具是 Codify 步：把 logo 提取到 design tokens
  - 前 4 步（品牌官方资料调研）由 brand-protocol skill 引导

用法：
    python3 scripts/brand_init.py --logo company-logo.png \\
        --base-pack apple-light \\
        --output-pack ./brand-pack.json \\
        --output-spec ./brand-spec.md

    # 输出后用 brand-pack.json 覆盖 base pack
    python3 scripts/create-pptx.py --spec deck.json --pack-override brand-pack.json
"""

from __future__ import annotations
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def extract_top_colors(image_path: str, top_n: int = 5) -> list[tuple[str, int]]:
    """从 logo 提取主色调，返回 [(hex, count), ...]"""
    try:
        from PIL import Image
    except ImportError:
        raise RuntimeError("PIL 必填：pip install Pillow")

    img = Image.open(image_path).convert('RGBA')
    # 缩放到 200x200 加速
    img = img.resize((200, 200))

    pixels = list(img.getdata())
    # 跳过透明像素 + 接近白/黑/灰
    valid = []
    for r, g, b, a in pixels:
        if a < 128:
            continue
        # HSL 简化判定
        mx, mn = max(r, g, b), min(r, g, b)
        v = mx / 255
        s = (mx - mn) / mx if mx > 0 else 0
        if v > 0.95 or v < 0.05:  # 太亮太暗
            continue
        if s < 0.15:  # 灰
            continue
        # 量化到 32 级（每通道 8 桶）减少噪音
        valid.append((r // 32 * 32, g // 32 * 32, b // 32 * 32))

    if not valid:
        # 全是灰色 logo（如黑白），fallback 用最暗色
        for r, g, b, a in pixels:
            if a >= 128:
                valid.append((r // 32 * 32, g // 32 * 32, b // 32 * 32))

    counter = Counter(valid)
    top = counter.most_common(top_n)

    return [(f'#{r:02X}{g:02X}{b:02X}', cnt) for (r, g, b), cnt in top]


def hex_to_hsl(hex_str: str) -> tuple[float, float, float]:
    s = hex_str.lstrip('#')
    r, g, b = int(s[0:2], 16) / 255, int(s[2:4], 16) / 255, int(s[4:6], 16) / 255
    mx, mn = max(r, g, b), min(r, g, b)
    delta = mx - mn
    L = (mx + mn) / 2
    if delta == 0:
        return 0, 0, L
    S = delta / (1 - abs(2 * L - 1)) if L != 0 and L != 1 else 0
    if mx == r:
        H = (60 * ((g - b) / delta) + 360) % 360
    elif mx == g:
        H = 60 * ((b - r) / delta) + 120
    else:
        H = 60 * ((r - g) / delta) + 240
    return H, S, L


def adjust_brightness(hex_str: str, factor: float) -> str:
    """factor < 1 变深，> 1 变浅"""
    s = hex_str.lstrip('#')
    r, g, b = int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)
    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))
    return f'#{r:02X}{g:02X}{b:02X}'


def pick_primary(colors: list[tuple[str, int]]) -> str:
    """从 top-N 中挑 primary：优先饱和度高 + 面积大的"""
    if not colors:
        return '#0071E3'  # 默认青蓝
    scored = []
    total = sum(c for _, c in colors)
    for hex_c, count in colors:
        h, s, l = hex_to_hsl(hex_c)
        # 饱和度 + 面积权重
        score = s * 0.6 + (count / total) * 0.4
        # 极暗极亮扣分
        if l < 0.15 or l > 0.85:
            score *= 0.3
        scored.append((score, hex_c))
    scored.sort(reverse=True)
    return scored[0][1]


def build_brand_pack(*,
                     base_pack: str,
                     primary: str,
                     all_colors: list[tuple[str, int]],
                     company: str = '') -> dict:
    """生成 brand-pack JSON 增量"""
    accent_soft = adjust_brightness(primary, 0.85)  # 深 15%
    return {
        'extends': base_pack,
        '_company': company,
        '_extracted_from_logo': True,
        'palette_override': {
            'accent': primary,
            'accent_soft': accent_soft,
        },
        '_top_colors': [c for c, _ in all_colors],
    }


def build_brand_spec(*, company: str, logo_path: str, base_pack: str,
                     primary: str, all_colors: list[tuple[str, int]]) -> str:
    """人类可读规范（brand-spec.md）"""
    palette_table = '\n'.join(
        f'| #{i+1} | `{c}` | {cnt} 像素权重 |'
        for i, (c, cnt) in enumerate(all_colors[:5])
    )
    return f"""# {company or '客户'} 品牌规范（v3.7 自动提取）

## Logo

- 源文件：`{logo_path}`
- 基底 pack：`{base_pack}`

## 主色（自动提取，按饱和度+面积加权）

**Primary（accent）**: `{primary}`

| # | hex | 来源 |
|---|---|---|
{palette_table}

## 应用方式

```bash
# 用 brand-pack.json 覆盖 base pack 的 accent
python3 scripts/create-pptx.py --spec deck.json --pack-override brand-pack.json
```

## 后续：huo15-openclaw-brand-protocol 5 步深化

本工具完成 5 步流程的「Codify」步。其余 4 步：

1. **Ask** — 问客户品牌官方手册 / VI 手册 / 字体规范是否存在
2. **Search** — 公司官网 / 微信公众号 / 招股书 / B2B 资料挖掘官方色卡
3. **Download** — 拿到 logo SVG / 品牌字体 / 官方色板原文件
4. **Verify** — 与客户市场部 / 品牌负责人确认提取的色彩是否准确
5. **Codify**（本工具）—— 把验证后的色彩 → design tokens → PPT pack

如未做前 4 步，本工具只是「视觉对齐」级别（基于 logo 像素），不是品牌官方授权的设计令牌。
"""


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v3.7 品牌 Theme 自动注入')
    parser.add_argument('--logo', required=True, help='公司 logo 路径（PNG/JPG）')
    parser.add_argument('--base-pack', default='apple-light',
                        help='基底 pack（21 套之一），默认 apple-light')
    parser.add_argument('--company', default='', help='公司名（写入 spec）')
    parser.add_argument('--output-pack', default='brand-pack.json',
                        help='brand-pack.json 输出路径')
    parser.add_argument('--output-spec', default='brand-spec.md',
                        help='brand-spec.md 输出路径')
    parser.add_argument('--top-n', type=int, default=5)
    args = parser.parse_args()

    if not Path(args.logo).exists():
        print(f"  ✗ logo 不存在: {args.logo}", file=sys.stderr)
        sys.exit(1)

    print(f"  🎨 提取 {args.logo} 主色...", file=sys.stderr)
    colors = extract_top_colors(args.logo, top_n=args.top_n)
    primary = pick_primary(colors)
    print(f"  📌 Top {len(colors)} 色:", file=sys.stderr)
    for c, cnt in colors:
        print(f"     {c}  ({cnt} 像素权重)", file=sys.stderr)
    print(f"  ⭐ Primary: {primary}", file=sys.stderr)

    pack = build_brand_pack(
        base_pack=args.base_pack,
        primary=primary,
        all_colors=colors,
        company=args.company,
    )
    Path(args.output_pack).write_text(
        json.dumps(pack, ensure_ascii=False, indent=2))
    print(f"  📄 {args.output_pack}", file=sys.stderr)

    spec = build_brand_spec(
        company=args.company, logo_path=args.logo,
        base_pack=args.base_pack, primary=primary,
        all_colors=colors,
    )
    Path(args.output_spec).write_text(spec)
    print(f"  📋 {args.output_spec}", file=sys.stderr)


if __name__ == '__main__':
    main()
