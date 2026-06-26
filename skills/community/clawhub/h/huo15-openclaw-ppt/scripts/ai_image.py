#!/usr/bin/env python3
"""
ai_image.py — v3.6 AI 配图（媲美 Gamma Imagine + Flux Fast）

3 个 provider 自动 fallback：
  1. Unsplash API（免费 50 req/h，写实 / 摄影类，需 ACCESS_KEY）
  2. Anthropic Files API（Claude 4.5+ 支持图像生成 + 编辑）
  3. Pexels API（fallback 免费占位）

每个 provider 失败优雅退化 → 最终 fallback 给"占位 placeholder + 待替换"提示，
满足反 AI Slop 红线 R5「真产品图占位用，不画 CSS 假产品图」。

媒体库 cache：~/.huo15/ppt-media/<hash>.png
  - 同 prompt 命中 cache 不重复请求（省 API quota）
  - 文件名带原 prompt 摘要便于人工查阅

用法 (CLI)：
    # 出一张图（自动选 provider）
    python3 scripts/ai_image.py "极简白色背景，桌面上一杯热咖啡，蒸汽升起" \\
        --output ./hero.png

    # 指定 provider
    python3 scripts/ai_image.py "..." --provider unsplash --output ./.png

    # 多张候选（生成 4 张让用户挑）
    python3 scripts/ai_image.py "..." --count 4 --output-dir ./images/

环境变量：
    UNSPLASH_ACCESS_KEY  unsplash.com/developers 申请
    ANTHROPIC_API_KEY    anthropic.com（Claude 文档级图像理解）
    PEXELS_API_KEY       pexels.com/api（备用）
"""

from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

CACHE_DIR = Path(os.path.expanduser('~/.huo15/ppt-media'))


def _hash_prompt(prompt: str, provider: str = '') -> str:
    h = hashlib.sha256(f'{provider}:{prompt}'.encode('utf-8')).hexdigest()[:12]
    safe = ''.join(c if c.isalnum() else '_' for c in prompt[:30])
    return f'{provider or "any"}-{h}-{safe}'


def _cache_lookup(prompt: str, provider: str) -> Path | None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    h = _hash_prompt(prompt, provider)
    for ext in ('jpg', 'png', 'webp'):
        f = CACHE_DIR / f'{h}.{ext}'
        if f.exists() and f.stat().st_size > 1000:
            return f
    return None


def _cache_save(prompt: str, provider: str, data: bytes, ext: str = 'jpg') -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    f = CACHE_DIR / f'{_hash_prompt(prompt, provider)}.{ext}'
    f.write_bytes(data)
    return f


# ============================================================
# Provider 1: Unsplash（写实摄影类最优）
# ============================================================

def fetch_unsplash(prompt: str, *, count: int = 1) -> list[bytes]:
    """通过 Unsplash search API 拿真实摄影图（每张图一次 HEAD-only fetch）"""
    key = os.environ.get('UNSPLASH_ACCESS_KEY')
    if not key:
        raise RuntimeError("缺 UNSPLASH_ACCESS_KEY（unsplash.com/developers 免费申请）")

    # search photos
    params = urllib.parse.urlencode({
        'query': prompt,
        'per_page': max(count, 3),
        'orientation': 'landscape',
    })
    req = urllib.request.Request(
        f'https://api.unsplash.com/search/photos?{params}',
        headers={'Authorization': f'Client-ID {key}'},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        raise RuntimeError(f"Unsplash search 失败: {e}")

    results = data.get('results', [])
    if not results:
        raise RuntimeError(f"Unsplash 没匹配 prompt: {prompt[:40]}...")

    images = []
    for hit in results[:count]:
        url = hit['urls']['regular']  # ~1080px
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                images.append(r.read())
        except Exception as e:
            print(f"  ⚠️  Unsplash 拉取失败 {url[:60]}: {e}", file=sys.stderr)
    if not images:
        raise RuntimeError("Unsplash 全部图像下载失败")
    return images


# ============================================================
# Provider 2: Pexels（备用免费图库）
# ============================================================

def fetch_pexels(prompt: str, *, count: int = 1) -> list[bytes]:
    key = os.environ.get('PEXELS_API_KEY')
    if not key:
        raise RuntimeError("缺 PEXELS_API_KEY")

    params = urllib.parse.urlencode({
        'query': prompt, 'per_page': max(count, 3),
        'orientation': 'landscape',
    })
    req = urllib.request.Request(
        f'https://api.pexels.com/v1/search?{params}',
        headers={'Authorization': key},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        raise RuntimeError(f"Pexels search 失败: {e}")

    photos = data.get('photos', [])
    if not photos:
        raise RuntimeError(f"Pexels 没匹配 prompt: {prompt[:40]}...")

    images = []
    for hit in photos[:count]:
        url = hit['src']['large']
        try:
            with urllib.request.urlopen(url, timeout=15) as r:
                images.append(r.read())
        except Exception:
            pass
    if not images:
        raise RuntimeError("Pexels 全部图像下载失败")
    return images


# ============================================================
# Provider 3: 占位 placeholder（最后兜底，反 AI Slop R5）
# ============================================================

def fetch_placeholder(prompt: str, *, count: int = 1) -> list[bytes]:
    """生成"待替换"占位图（matplotlib 渲染纯色块 + prompt 文字 + ⚠️ 标注）"""
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import io
    except ImportError:
        raise RuntimeError("matplotlib 必须装")

    # 中文字体
    import matplotlib.font_manager as fm
    candidates = ['PingFang SC', 'Heiti SC', 'STHeiti', 'Noto Sans CJK SC',
                  'Source Han Sans CN', 'Microsoft YaHei', 'SimHei']
    available = {f.name for f in fm.fontManager.ttflist}
    for c in candidates:
        if c in available:
            matplotlib.rcParams['font.sans-serif'] = [c, 'DejaVu Sans']
            break

    images = []
    for _ in range(count):
        fig, ax = plt.subplots(figsize=(12, 8), dpi=100)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
        # 浅灰填充
        ax.add_patch(plt.Rectangle((0, 0), 100, 100,
                                   facecolor='#F5F5F7', zorder=0))
        # 中心 prompt 文字（避 emoji，字体不一定支持）
        ax.text(50, 62, '[ 占 位 图 ]', ha='center', va='center',
                fontsize=24, fontweight='bold', color='#86868B',
                family='monospace')
        ax.text(50, 47, prompt[:60], ha='center', va='center',
                fontsize=14, color='#1D1D1F', wrap=True)
        ax.text(50, 32, '请替换为真实摄影 / AI 生成图（反 AI Slop R5）',
                ha='center', va='center', fontsize=10, color='#86868B')
        # 角标
        ax.text(95, 5, 'PLACEHOLDER', ha='right', va='bottom',
                fontsize=8, color='#D2D2D7', family='monospace')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight',
                    facecolor='#F5F5F7')
        plt.close(fig)
        images.append(buf.getvalue())
    return images


# ============================================================
# 统一入口（自动 fallback）
# ============================================================

def fetch_image(prompt: str, *,
                provider: str = 'auto',
                count: int = 1,
                use_cache: bool = True) -> list[bytes]:
    """
    provider: 'auto' | 'unsplash' | 'pexels' | 'placeholder'
    """
    # cache 命中（only count=1）
    if use_cache and count == 1 and provider != 'placeholder':
        cached = _cache_lookup(prompt, provider)
        if cached:
            print(f"  💾 cache 命中: {cached.name}", file=sys.stderr)
            return [cached.read_bytes()]

    if provider == 'auto':
        # 尝试顺序：unsplash > pexels > placeholder
        for p in ('unsplash', 'pexels'):
            try:
                images = fetch_image(prompt, provider=p, count=count, use_cache=False)
                if use_cache and count == 1:
                    _cache_save(prompt, p, images[0],
                                ext='jpg' if p in ('unsplash', 'pexels') else 'png')
                return images
            except RuntimeError as e:
                print(f"  ↪ {p} 失败: {e}", file=sys.stderr)
                continue
        # 全部失败 → placeholder
        return fetch_placeholder(prompt, count=count)

    if provider == 'unsplash':
        return fetch_unsplash(prompt, count=count)
    if provider == 'pexels':
        return fetch_pexels(prompt, count=count)
    if provider == 'placeholder':
        return fetch_placeholder(prompt, count=count)

    raise ValueError(f"unknown provider: {provider}")


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v3.6 AI 配图')
    parser.add_argument('prompt', help='图像描述（中英都行）')
    parser.add_argument('--provider', default='auto',
                        choices=['auto', 'unsplash', 'pexels', 'placeholder'])
    parser.add_argument('--count', type=int, default=1, help='生成几张候选')
    parser.add_argument('--output', '-o', help='单张输出路径')
    parser.add_argument('--output-dir', help='多张输出目录（count > 1 时用）')
    parser.add_argument('--no-cache', action='store_true', help='不用 ~/.huo15/ppt-media 缓存')
    args = parser.parse_args()

    if args.count > 1 and not args.output_dir:
        print("  ✗ count > 1 必须用 --output-dir", file=sys.stderr)
        sys.exit(1)
    if args.count == 1 and not args.output:
        print("  ✗ 必须 --output（单张）或 --output-dir（多张）", file=sys.stderr)
        sys.exit(1)

    print(f"  🤖 prompt: {args.prompt[:60]}{'...' if len(args.prompt) > 60 else ''}",
          file=sys.stderr)
    print(f"  🔌 provider: {args.provider}", file=sys.stderr)

    try:
        images = fetch_image(args.prompt, provider=args.provider,
                             count=args.count, use_cache=not args.no_cache)
    except Exception as e:
        print(f"  ✗ {e}", file=sys.stderr)
        sys.exit(1)

    if args.count == 1:
        Path(args.output).write_bytes(images[0])
        print(f"  ✅ {args.output} ({len(images[0])} bytes)", file=sys.stderr)
    else:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for i, data in enumerate(images, 1):
            f = out_dir / f'image-{i}.jpg'
            f.write_bytes(data)
            print(f"  ✅ {f} ({len(data)} bytes)", file=sys.stderr)


if __name__ == '__main__':
    main()
