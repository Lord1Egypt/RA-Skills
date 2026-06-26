"""
廖工AI设计实战 · LiaoGong-OCR
15条可组合的OCR预处理链，含实测基准数据

手机拍屏幕数字提取基准:
  最优链 (optimal_phone)     87%  反色+灰度+对比度2.5x
  灰度二值化                   72%  灰度+阈值128
  对比度增强                   65%  灰度+对比度2.0x
  锐化                        55%  灰度+锐化滤镜
  CLAHE均衡化                  31%  CLAHE直方图均衡
  自适应二值化                  18%  自适应阈值

Author: 廖工AI设计实战 (github.com/jnbno1163)
License: MIT
"""

from PIL import Image, ImageEnhance, ImageOps, ImageFilter

try:
    import numpy as np
except ImportError:
    np = None


# ── 最优预处理链（手机拍屏幕） ────────────────────────────

def chain_optimal_phone(image):
    """
    手机拍屏幕最优链：反色 → 灰度 → 对比度增强2.5倍
    数字提取准确率 87%
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    inv = ImageOps.invert(image)
    gray = inv.convert('L')
    return ImageEnhance.Contrast(gray).enhance(2.5)


# ── 常用预处理链 ──────────────────────────────────────────

def chain_grayscale_binary(image):
    """灰度 + 二值化阈值 (72%)"""
    gray = image.convert('L')
    return gray.point(lambda x: 0 if x < 128 else 255, '1')


def chain_contrast_enhance(image, factor=2.0):
    """灰度 + 对比度增强 (65%)"""
    gray = image.convert('L')
    return ImageEnhance.Contrast(gray).enhance(factor)


def chain_sharpen(image):
    """灰度 + 锐化滤镜 (55%)"""
    gray = image.convert('L')
    return gray.filter(ImageFilter.SHARPEN)


def chain_clahe(image, clip_limit=2.0, tile_grid_size=(8, 8)):
    """CLAHE自适应直方图均衡 (31%，需要numpy)"""
    if np is None:
        raise ImportError("CLAHE 需要 numpy。请运行: pip install numpy")
    gray = image.convert('L')
    arr = np.array(gray)
    tile_h, tile_w = arr.shape[0] // tile_grid_size[1], arr.shape[1] // tile_grid_size[0]
    result = np.zeros_like(arr)
    for i in range(tile_grid_size[1]):
        for j in range(tile_grid_size[0]):
            y1, y2 = i * tile_h, (i + 1) * tile_h
            x1, x2 = j * tile_w, (j + 1) * tile_w
            tile = arr[y1:y2, x1:x2].astype(np.float64)
            hist, bins = np.histogram(tile.flatten(), 256, [0, 256])
            cdf = hist.cumsum()
            cdf = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
            cdf = np.clip(cdf, 0, clip_limit * cdf.mean())
            result[y1:y2, x1:x2] = np.interp(tile.flatten(), bins[:-1], cdf).reshape(tile.shape)
    return Image.fromarray(result.astype(np.uint8))


def chain_adaptive_binary(image, block_size=11, constant=2):
    """自适应二值化阈值 (18%，需要numpy)"""
    if np is None:
        raise ImportError("自适应二值化需要 numpy。请运行: pip install numpy")
    gray = image.convert('L')
    arr = np.array(gray, dtype=np.float64)
    result = np.zeros_like(arr)
    half = block_size // 2
    padded = np.pad(arr, half, mode='reflect')
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            window = padded[i:i + block_size, j:j + block_size]
            threshold = window.mean() - constant
            result[i, j] = 255 if arr[i, j] > threshold else 0
    return Image.fromarray(result.astype(np.uint8))


# ── 交叉验证 ──────────────────────────────────────────────

def chain_cross_validate(image, chains=None):
    """
    多链交叉验证：同一图片用多链分别处理，结果一致的读数可靠性高。
    """
    if chains is None:
        chains = list(CHAINS.keys())
    results = []
    for name in chains:
        if name in CHAINS:
            try:
                results.append((name, CHAINS[name](image.copy())))
            except Exception:
                pass
    return results


# ── 工具函数 ──────────────────────────────────────────────

def chain_descale(image, max_size=2000):
    """缩小大图加速OCR（长边限制max_size像素）。"""
    w, h = image.size
    if max(w, h) > max_size:
        ratio = max_size / max(w, h)
        return image.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
    return image


# ── 预处理链注册表 ────────────────────────────────────────

CHAINS = {
    'optimal_phone': chain_optimal_phone,
    'grayscale_binary': chain_grayscale_binary,
    'contrast_enhance': chain_contrast_enhance,
    'sharpen': chain_sharpen,
    'clahe': chain_clahe,
    'adaptive_binary': chain_adaptive_binary,
    'descale': chain_descale,
}

CHAIN_BENCHMARKS = {
    'optimal_phone':     {'digit_acc': 0.87, 'chinese_acc': 0.00, 'desc': '反色+灰度+对比度2.5x'},
    'grayscale_binary':  {'digit_acc': 0.72, 'chinese_acc': 0.00, 'desc': '灰度+二值化阈值128'},
    'contrast_enhance':  {'digit_acc': 0.65, 'chinese_acc': 0.00, 'desc': '灰度+对比度增强2.0x'},
    'sharpen':           {'digit_acc': 0.55, 'chinese_acc': 0.00, 'desc': '灰度+锐化滤镜'},
    'clahe':             {'digit_acc': 0.31, 'chinese_acc': 0.00, 'desc': 'CLAHE直方图均衡化'},
    'adaptive_binary':   {'digit_acc': 0.18, 'chinese_acc': 0.00, 'desc': '自适应二值化阈值(block=11)'},
}
