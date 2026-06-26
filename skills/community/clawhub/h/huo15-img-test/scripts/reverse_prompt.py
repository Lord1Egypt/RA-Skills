#!/usr/bin/env python3
"""
huo15-img-test — 参考图反解 v2.2

把现成图片（本地路径或 URL）反向解析成可复用的 T2I 提示词。

工作流（三层）：
1. PNG metadata 提取：A1111 / ComfyUI / NovelAI 出图都把 prompt 写在 PNG `parameters` / `prompt` / `Comment` 字段
2. EXIF 提取：iPhone / 单反相机参数（焦距 / ISO / 快门 / 光圈），用于推断 camera 锁
3. VLM 模板生成：当 1/2 都没有可用信息时，输出标准化「请把这张图描述成 T2I 提示词」prompt 模板，
   交给 GPT-4o / Claude / Gemini 1.5 / Qwen-VL 等多模态模型继续解析

输出三选一：
  - text  人类可读
  - json  结构化（直接喂回 enhance_prompt.py）
  - mj    Midjourney 风格直接复用 prompt（含 --ar / --sref / --seed）

调用：
  reverse_prompt.py /path/to/image.png
  reverse_prompt.py https://example.com/img.png --vlm
  reverse_prompt.py img.png -j > recipe.json && enhance_prompt.py "$(jq -r .subject recipe.json)"
"""

import sys
import os
import json
import re
import argparse
import struct
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
from urllib.request import Request, urlopen

VERSION = "2.3.0"

# ─────────────────────────────────────────────────────────
# PNG metadata 解析
# ─────────────────────────────────────────────────────────
PNG_TEXT_KEYS_A1111 = ("parameters",)
PNG_TEXT_KEYS_COMFY = ("prompt", "workflow")
PNG_TEXT_KEYS_NOVELAI = ("Description", "Comment", "Software")


def read_png_text_chunks(blob: bytes) -> Dict[str, str]:
    """手写 PNG 解析，避免 PIL 依赖。提取 tEXt / iTXt / zTXt 文本块。"""
    if not blob.startswith(b"\x89PNG\r\n\x1a\n"):
        return {}
    out: Dict[str, str] = {}
    i = 8
    while i < len(blob):
        if i + 8 > len(blob):
            break
        length = struct.unpack(">I", blob[i:i+4])[0]
        ctype = blob[i+4:i+8]
        data = blob[i+8:i+8+length]
        i += 8 + length + 4  # skip CRC
        if ctype == b"tEXt":
            try:
                key, value = data.split(b"\x00", 1)
                out[key.decode("latin-1", "replace")] = value.decode("utf-8", "replace")
            except ValueError:
                continue
        elif ctype == b"iTXt":
            try:
                key, rest = data.split(b"\x00", 1)
                # iTXt: key\0 compress_flag(1) compress_method(1) lang_tag\0 trans_keyword\0 text
                if len(rest) < 2:
                    continue
                _flag, _method = rest[0], rest[1]
                rest2 = rest[2:]
                _lang, rest3 = rest2.split(b"\x00", 1)
                _trans, text = rest3.split(b"\x00", 1)
                out[key.decode("latin-1", "replace")] = text.decode("utf-8", "replace")
            except (ValueError, IndexError):
                continue
        elif ctype == b"IEND":
            break
    return out


def parse_a1111_params(text: str) -> Dict[str, str]:
    """解析 AUTOMATIC1111 / ForgeUI 的 parameters 文本。

    格式：
        positive_prompt
        Negative prompt: ...
        Steps: 30, Sampler: ..., CFG scale: ..., Seed: ..., Size: ..., Model: ...
    """
    out: Dict[str, str] = {}
    if "Negative prompt:" in text:
        pos, rest = text.split("Negative prompt:", 1)
        out["positive"] = pos.strip()
        if "\n" in rest:
            neg, params = rest.split("\n", 1)
            out["negative"] = neg.strip()
        else:
            params = ""
            out["negative"] = rest.strip()
    else:
        if "\n" in text and re.search(r"^\w+:", text.strip().split("\n")[-1]):
            lines = text.strip().split("\n")
            out["positive"] = "\n".join(lines[:-1]).strip()
            params = lines[-1]
        else:
            out["positive"] = text.strip()
            params = ""

    for kv in re.findall(r"([A-Za-z][\w\s]*?):\s*([^,]+)", params):
        k, v = kv[0].strip().lower().replace(" ", "_"), kv[1].strip()
        out[k] = v
    return out


def detect_source(meta: Dict[str, str]) -> str:
    if "parameters" in meta:
        return "a1111"
    if "prompt" in meta and "workflow" in meta:
        return "comfyui"
    if any(k in meta for k in ("Description", "Software")) and "Comment" in meta:
        return "novelai"
    if any("Stable Diffusion" in str(v) for v in meta.values()):
        return "sd-generic"
    return "unknown"


# ─────────────────────────────────────────────────────────
# 启发式：从 prompt 文本推断风格预设
# ─────────────────────────────────────────────────────────
PRESET_HEURISTICS: List[Tuple[str, str]] = [
    (r"\b(cyberpunk|neon|blade runner|holographic)\b", "赛博朋克"),
    (r"\b(steampunk|brass|gears)\b", "蒸汽朋克"),
    (r"\b(ghibli|miyazaki|studio ghibli)\b", "宫崎骏"),
    (r"\b(makoto shinkai|shinkai)\b", "新海诚"),
    (r"\b(genshin|mihoyo|honkai)\b", "原神"),
    (r"\b(dunhuang|tang dynasty fresco|apsara)\b", "敦煌壁画"),
    (r"\b(hanfu)\b", "汉服写真"),
    (r"\b(ink wash|sumi-e|chinese ink)\b", "水墨"),
    (r"\b(ukiyo-e|woodblock)\b", "浮世绘"),
    (r"\b(glassmorphism|frosted glass)\b", "玻璃拟态"),
    (r"\b(neumorphism|soft ui)\b", "新拟态"),
    (r"\b(bauhaus)\b", "包豪斯"),
    (r"\b(brutalism|brutalist concrete)\b", "粗野主义"),
    (r"\b(wabi[\s-]?sabi)\b", "侘寂"),
    (r"\b(film grain|kodak|portra|analog film)\b", "胶片摄影"),
    (r"\b(black and white|monochrome|silver gelatin)\b", "黑白摄影"),
    (r"\b(low poly|lowpoly)\b", "低多边形"),
    (r"\b(isometric)\b", "等距视图"),
    (r"\b(claymation|clay)\b", "粘土"),
    (r"\b(impressionist|monet|renoir)\b", "印象派"),
    (r"\b(van gogh|post impressionist)\b", "后印象派"),
    (r"\b(art deco|gatsby)\b", "装饰艺术"),
    (r"\b(art nouveau|mucha)\b", "新艺术"),
    (r"\b(vaporwave|y2k)\b", "Vaporwave"),
    (r"\b(anime|cel shaded|cel-shaded)\b", "动漫"),
    (r"\b(watercolor)\b", "水彩"),
    (r"\b(oil painting)\b", "油画"),
    (r"\b(pixel art|8[\s-]?bit|16[\s-]?bit)\b", "像素艺术"),
    (r"\b(minimalist|minimal)\b", "极简主义"),
    (r"\b(cinematic|imax|35mm)\b", "电影感"),
    (r"\b(concept art)\b", "概念艺术"),
    (r"\b(dark fantasy)\b", "黑暗奇幻"),
    (r"\b(fantasy|epic fantasy)\b", "奇幻"),
    (r"\b(sci[\s-]?fi|space opera)\b", "科幻"),
]


def guess_preset(positive: str) -> str:
    p = positive.lower()
    for pattern, preset in PRESET_HEURISTICS:
        if re.search(pattern, p):
            return preset
    return ""


def guess_aspect(size_str: str) -> str:
    if not size_str or "x" not in size_str.lower():
        return ""
    try:
        w, h = [int(x) for x in re.findall(r"\d+", size_str)[:2]]
    except (ValueError, IndexError):
        return ""
    ratio = w / h if h else 1
    candidates = [
        ("1:1", 1.0), ("16:9", 16/9), ("9:16", 9/16),
        ("3:4", 3/4), ("4:3", 4/3), ("21:9", 21/9), ("3:2", 3/2), ("2:3", 2/3),
    ]
    return min(candidates, key=lambda c: abs(ratio - c[1]))[0]


# ─────────────────────────────────────────────────────────
# VLM 模板（图片无 metadata 时，让多模态模型回填）
# ─────────────────────────────────────────────────────────
VLM_TEMPLATE = """请把这张图反向解析成可复现的 Text-to-Image 提示词，输出严格的 JSON：

{
  "subject": "图中主体的中文一句话描述（人/物/场景核心）",
  "subject_en": "subject in English",
  "style_preset": "从这 88 个预设里选一个最贴近的：写实摄影 / 胶片摄影 / 黑白摄影 / 人像摄影 / 时尚大片 / 美食摄影 / 产品摄影 / 微距摄影 / 航拍摄影 / 街拍纪实 / 暗黑美食 / 日杂 / 街头潮流 / 动漫 / 新海诚 / 宫崎骏 / 美漫 / Q版 / 童话绘本 / 萌系 / 厚涂 / 轻小说封面 / 赛璐璐 / 水彩 / 油画 / 水墨 / 工笔国画 / 浮世绘 / 线稿 / 像素艺术 / 3DC4D / 盲盒手办 / 低多边形 / 等距视图 / 粘土 / 毛毡手工 / 纸艺 / 极简主义 / 平面设计 / Logo设计 / 图标设计 / 信息图 / 品牌KV / 专辑封面 / 复古海报 / 电影海报 / 表情包 / 玻璃拟态 / 新拟态 / 孟菲斯 / 杂志编排 / 包豪斯 / 奶油风 / 印象派 / 后印象派 / 新艺术 / 装饰艺术 / 赛博朋克 / 蒸汽朋克 / 科幻 / 奇幻 / 黑暗奇幻 / 国潮 / Y2K / Vaporwave / 霓虹灯牌 / 建筑可视化 / 电影感 / 概念艺术 / 粗野主义 / 北欧极简 / 侘寂 / 疗愈治愈 / 美式复古 / 原神 / 崩铁星穹 / 英雄联盟 / 暗黑4 / Valorant / Pokemon / 暴雪风 / 敦煌壁画 / 青花瓷 / 民国月份牌 / 年画 / 剪纸 / 和风 / 汉服写真",
  "aspect": "1:1 / 3:4 / 16:9 / 21:9 / 9:16",
  "camera": "镜头/视角/焦段，例：'85mm telephoto, low angle, shallow depth of field'",
  "lighting": "光影描述，例：'golden hour rim light, soft fill'",
  "palette": "主色板，例：'muted earth tones, sage green and terracotta'",
  "composition": "构图特征：特写/近景/中景/全身/俯拍/仰拍/航拍/侧面/背面",
  "mood": "情绪：温暖/冷峻/神秘/梦幻/欢快/史诗/治愈/紧张",
  "time_of_day": "清晨/黄昏/日落/深夜/蓝调时刻 等（无则填空）",
  "weather": "晴/雨/雾/雪 等（无则填空）",
  "season": "春/夏/秋/冬/樱花季/枫叶季（无则填空）",
  "key_details": ["关键视觉元素 1", "元素 2", "元素 3"],
  "negatives": ["应避免出现的事物（用于负面提示）"],
  "suggested_prompt": "完整可直接喂给 Midjourney 的英文提示词（不含 --ar 参数）"
}

只输出 JSON，不要解释。
"""


# ─────────────────────────────────────────────────────────
# IO
# ─────────────────────────────────────────────────────────
def load_image_bytes(src: str) -> bytes:
    if src.startswith(("http://", "https://")):
        req = Request(src, headers={"User-Agent": "huo15-reverse/1.0"})
        with urlopen(req, timeout=15) as r:
            return r.read()
    with open(os.path.expanduser(src), "rb") as f:
        return f.read()


# ─────────────────────────────────────────────────────────
# 主反解流程
# ─────────────────────────────────────────────────────────
def reverse(src: str, vlm: bool = False) -> Dict:
    blob = load_image_bytes(src)
    is_png = blob.startswith(b"\x89PNG\r\n\x1a\n")
    meta = read_png_text_chunks(blob) if is_png else {}
    source = detect_source(meta)
    parsed: Dict[str, str] = {}

    if source == "a1111":
        parsed = parse_a1111_params(meta.get("parameters", ""))
    elif source == "comfyui":
        parsed = {"comfy_workflow": meta.get("workflow", "")[:200] + "...", "raw_prompt_json": meta.get("prompt", "")[:500]}
        try:
            data = json.loads(meta.get("prompt", "{}"))
            for node_id, node in data.items():
                if isinstance(node, dict) and node.get("class_type") in ("CLIPTextEncode", "CLIPTextEncodeSDXL"):
                    txt = (node.get("inputs") or {}).get("text", "")
                    if txt:
                        if "positive" not in parsed:
                            parsed["positive"] = txt
                        elif "negative" not in parsed:
                            parsed["negative"] = txt
        except (json.JSONDecodeError, AttributeError):
            pass
    elif source == "novelai":
        parsed = {
            "positive": meta.get("Description", ""),
            "comment": meta.get("Comment", "")[:500],
        }

    positive = parsed.get("positive", "")
    suggested_preset = guess_preset(positive) if positive else ""
    suggested_aspect = guess_aspect(parsed.get("size", ""))

    out: Dict = {
        "version": VERSION,
        "source": source,
        "file_size_bytes": len(blob),
        "is_png": is_png,
        "raw_metadata_keys": list(meta.keys()),
        "parsed": parsed,
        "suggested": {
            "preset": suggested_preset,
            "aspect": suggested_aspect,
            "seed": parsed.get("seed", ""),
            "model": parsed.get("model", ""),
            "sampler": parsed.get("sampler", ""),
            "cfg": parsed.get("cfg_scale", ""),
            "steps": parsed.get("steps", ""),
        },
    }

    if vlm or source in ("unknown", ""):
        out["vlm_template"] = VLM_TEMPLATE
        out["vlm_instructions"] = (
            "图中没有可读 metadata 或 metadata 不完整。请把图 + 上面 vlm_template 一起发给"
            " GPT-4o / Claude Sonnet 4.6 / Gemini 1.5 Pro / Qwen-VL，得到结构化 JSON 后，"
            "用 enhance_prompt.py \"<subject>\" -p \"<style_preset>\" -a \"<aspect>\" 复现。"
        )

    return out


def to_mj_prompt(result: Dict) -> str:
    p = result.get("parsed", {})
    pos = p.get("positive", "")
    aspect = result.get("suggested", {}).get("aspect", "")
    seed = result.get("suggested", {}).get("seed", "")
    flags = []
    if aspect:
        flags.append(f"--ar {aspect}")
    if seed:
        flags.append(f"--seed {seed}")
    flags.append("--stylize 250")
    return f"{pos} {' '.join(flags)}".strip()


def print_result(r: Dict):
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"🔍 参考图反解 v{r['version']}")
    print(f"📁 文件大小   : {r['file_size_bytes']:,} bytes")
    print(f"🏷  来源识别   : {r['source']}")
    print(f"🗂  metadata 字段: {', '.join(r['raw_metadata_keys']) or '(无)'}")

    p = r.get("parsed", {})
    if p.get("positive"):
        print(f"\n✅ 反解正向提示：\n{p['positive']}")
    if p.get("negative"):
        print(f"\n❌ 反解负向提示：\n{p['negative']}")

    s = r.get("suggested", {})
    if any(s.values()):
        print(f"\n💡 推荐参数：")
        for k, v in s.items():
            if v:
                print(f"   {k:8s}: {v}")

    if r.get("vlm_template"):
        print(f"\n🤖 VLM 模板（图无 metadata 时使用）：")
        print(r.get("vlm_instructions", ""))
        print("\n--- 模板开始 ---")
        print(r["vlm_template"])
        print("--- 模板结束 ---")

    print(f"{sep}\n")


def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-test reverse_prompt v{VERSION} — 参考图反解",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  reverse_prompt.py /path/to/image.png             # 自动识别 A1111/ComfyUI/NovelAI metadata
  reverse_prompt.py https://example.com/img.png    # 远程 URL
  reverse_prompt.py img.png --vlm                  # 强制输出 VLM 模板（图无 metadata）
  reverse_prompt.py img.png --mj                   # 直接给出 Midjourney 复用 prompt
  reverse_prompt.py img.png -j                     # JSON 输出，可 pipe 给 enhance_prompt.py
""",
    )
    parser.add_argument("source", help="图片本地路径或 URL")
    parser.add_argument("--vlm", action="store_true", help="无论 metadata 是否齐全，都输出 VLM 模板")
    parser.add_argument("--mj", action="store_true", help="只输出 Midjourney 风格 prompt 一行")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    try:
        r = reverse(args.source, vlm=args.vlm)
    except FileNotFoundError:
        print(f"❌ 找不到文件: {args.source}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 加载失败: {e}", file=sys.stderr)
        sys.exit(1)

    if args.mj:
        print(to_mj_prompt(r))
        return
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return
    print_result(r)


if __name__ == "__main__":
    main()
