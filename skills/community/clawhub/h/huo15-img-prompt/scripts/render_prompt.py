#!/usr/bin/env python3
"""
huo15-img-prompt — 提示词直出图片 v2.2

把 enhance_prompt.py 生成的提示词，直接调用本地或云端 API 出图。

支持的后端：
  - comfyui     本地 ComfyUI（HTTP API，默认 http://127.0.0.1:8188）
  - sd-webui    AUTOMATIC1111 / Forge（默认 http://127.0.0.1:7860/sdapi/v1/txt2img）
  - dalle       OpenAI DALL-E 3（OPENAI_API_KEY）
  - openai      同 dalle
  - none        只生成调用脚本，不真实执行（dry-run，方便贴到 ComfyUI 桌面端）

依赖：仅 Python 标准库（urllib），不引入 requests/PIL，避免企业扫描器命中第三方包。

调用：
  render_prompt.py "赛博朋克猫" -p 赛博朋克 -m SD --backend sd-webui
  render_prompt.py "极简logo" -p Logo设计 --backend dalle --size 1024x1024
  render_prompt.py "原神少女" -p 原神 --backend comfyui --workflow ./workflows/sdxl-base.json
  render_prompt.py "敦煌神女" -p 敦煌壁画 --backend none -j > recipe.json   # dry-run

环境变量：
  OPENAI_API_KEY        DALL-E 调用必需
  COMFYUI_URL           覆盖 ComfyUI 端点（默认 http://127.0.0.1:8188）
  SDWEBUI_URL           覆盖 SD WebUI 端点（默认 http://127.0.0.1:7860）
"""

import sys
import os
import json
import time
import base64
import argparse
import uuid
from typing import Dict, Optional
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from enhance_prompt import (
    build_prompt,
    parse_mix_preset,
    resolve_preset,
    parse_requirement,
    STYLE_PRESETS,
    ASPECT_TO_SDXL,
)

VERSION = "3.1.0"


# ─────────────────────────────────────────────────────────
# HTTP 工具
# ─────────────────────────────────────────────────────────
def http_post_json(url: str, body: Dict, headers: Optional[Dict] = None, timeout: int = 600) -> Dict:
    data = json.dumps(body).encode("utf-8")
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    req = Request(url, data=data, headers=h, method="POST")
    with urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def http_get_json(url: str, headers: Optional[Dict] = None, timeout: int = 60) -> Dict:
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def http_get_bytes(url: str, headers: Optional[Dict] = None, timeout: int = 600) -> bytes:
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=timeout) as r:
        return r.read()


# ─────────────────────────────────────────────────────────
# DALL-E 3
# ─────────────────────────────────────────────────────────
DALLE_SIZES = {"1:1": "1024x1024", "16:9": "1792x1024", "9:16": "1024x1792"}


def render_dalle(positive: str, size: str, output_dir: str, n: int = 1) -> Dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 OPENAI_API_KEY 环境变量")
    body = {
        "model": "dall-e-3",
        "prompt": positive[:4000],
        "n": n,
        "size": size,
        "quality": "hd",
        "response_format": "b64_json",
    }
    resp = http_post_json(
        "https://api.openai.com/v1/images/generations",
        body,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=300,
    )
    saved = []
    os.makedirs(output_dir, exist_ok=True)
    for i, item in enumerate(resp.get("data", [])):
        path = os.path.join(output_dir, f"dalle-{int(time.time())}-{i}.png")
        with open(path, "wb") as f:
            f.write(base64.b64decode(item["b64_json"]))
        saved.append(path)
    return {"backend": "dalle", "saved": saved, "raw_response_keys": list(resp.keys())}


# ─────────────────────────────────────────────────────────
# AUTOMATIC1111 / Forge SD WebUI
# ─────────────────────────────────────────────────────────
def aspect_to_size(aspect: str) -> tuple:
    sdxl = ASPECT_TO_SDXL.get(aspect, "1024x1024")
    w, h = sdxl.split("x")
    return int(w), int(h)


def render_sdwebui(positive: str, negative: str, aspect: str, seed: int, steps: int, cfg: float,
                   sampler: str, output_dir: str, base_url: Optional[str] = None) -> Dict:
    base = base_url or os.environ.get("SDWEBUI_URL", "http://127.0.0.1:7860")
    w, h = aspect_to_size(aspect)
    body = {
        "prompt": positive,
        "negative_prompt": negative,
        "width": w,
        "height": h,
        "seed": seed,
        "steps": steps,
        "cfg_scale": cfg,
        "sampler_name": sampler,
        "send_images": True,
    }
    resp = http_post_json(urljoin(base, "/sdapi/v1/txt2img"), body, timeout=900)
    saved = []
    os.makedirs(output_dir, exist_ok=True)
    for i, b64 in enumerate(resp.get("images", [])):
        path = os.path.join(output_dir, f"sdwebui-{seed}-{i}.png")
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64.split(",", 1)[-1]))
        saved.append(path)
    return {"backend": "sd-webui", "saved": saved, "info": resp.get("info", "")[:200]}


# ─────────────────────────────────────────────────────────
# ComfyUI
# ─────────────────────────────────────────────────────────
DEFAULT_COMFY_WORKFLOW = {
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "seed": 0, "steps": 25, "cfg": 7.0, "sampler_name": "dpmpp_2m",
            "scheduler": "karras", "denoise": 1.0,
            "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0],
        },
    },
    "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
    "5": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
    "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "POSITIVE_PLACEHOLDER", "clip": ["4", 1]}},
    "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "NEGATIVE_PLACEHOLDER", "clip": ["4", 1]}},
    "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
    "9": {"class_type": "SaveImage", "inputs": {"images": ["8", 0], "filename_prefix": "huo15"}},
}


def render_comfyui(positive: str, negative: str, aspect: str, seed: int, steps: int, cfg: float,
                   workflow_path: Optional[str], output_dir: str,
                   base_url: Optional[str] = None) -> Dict:
    base = base_url or os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")

    if workflow_path and os.path.isfile(workflow_path):
        with open(workflow_path, "r", encoding="utf-8") as f:
            workflow = json.load(f)
    else:
        workflow = json.loads(json.dumps(DEFAULT_COMFY_WORKFLOW))

    w, h = aspect_to_size(aspect)
    for node in workflow.values():
        ct = node.get("class_type", "")
        ins = node.get("inputs", {})
        if ct == "CLIPTextEncode":
            if ins.get("text") == "POSITIVE_PLACEHOLDER" or "positive" in str(ins.get("text", "")).lower():
                ins["text"] = positive
            elif ins.get("text") == "NEGATIVE_PLACEHOLDER" or "negative" in str(ins.get("text", "")).lower():
                ins["text"] = negative
        elif ct == "EmptyLatentImage":
            ins["width"], ins["height"] = w, h
        elif ct == "KSampler":
            ins["seed"], ins["steps"], ins["cfg"] = seed, steps, cfg

    pos_set = neg_set = False
    for node in workflow.values():
        if node.get("class_type") == "CLIPTextEncode":
            if not pos_set:
                node["inputs"]["text"] = positive
                pos_set = True
            elif not neg_set:
                node["inputs"]["text"] = negative
                neg_set = True

    client_id = str(uuid.uuid4())
    queue_resp = http_post_json(urljoin(base, "/prompt"), {"prompt": workflow, "client_id": client_id}, timeout=30)
    prompt_id = queue_resp.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"ComfyUI 队列失败: {queue_resp}")

    deadline = time.time() + 600
    history = {}
    while time.time() < deadline:
        try:
            history = http_get_json(urljoin(base, f"/history/{prompt_id}"), timeout=10)
            if history.get(prompt_id):
                break
        except (HTTPError, URLError):
            pass
        time.sleep(2)

    if not history.get(prompt_id):
        raise RuntimeError("ComfyUI 任务超时")

    saved = []
    os.makedirs(output_dir, exist_ok=True)
    outputs = history[prompt_id].get("outputs", {})
    for node_id, output in outputs.items():
        for img in output.get("images", []):
            url = urljoin(base, f"/view?filename={img['filename']}&subfolder={img.get('subfolder','')}&type={img.get('type','output')}")
            path = os.path.join(output_dir, f"comfy-{seed}-{img['filename']}")
            with open(path, "wb") as f:
                f.write(http_get_bytes(url))
            saved.append(path)

    return {"backend": "comfyui", "saved": saved, "prompt_id": prompt_id}


# ─────────────────────────────────────────────────────────
# Replicate（v2.4）— 一键调任意开源模型
# ─────────────────────────────────────────────────────────
def render_replicate(positive: str, negative: str, aspect: str, seed: int,
                     model_ref: str, output_dir: str, steps: int = 25,
                     cfg: float = 7.0) -> Dict:
    """调用 Replicate API。

    model_ref 形如 'black-forest-labs/flux-schnell' 或 'stability-ai/sdxl'。
    """
    api_key = os.environ.get("REPLICATE_API_TOKEN")
    if not api_key:
        raise RuntimeError("缺少 REPLICATE_API_TOKEN 环境变量")
    w, h = aspect_to_size(aspect)

    body = {
        "input": {
            "prompt": positive,
            "negative_prompt": negative,
            "width": w,
            "height": h,
            "num_outputs": 1,
            "seed": seed,
            "num_inference_steps": steps,
            "guidance_scale": cfg,
            "aspect_ratio": aspect,
        }
    }
    if "/" in model_ref:
        url = f"https://api.replicate.com/v1/models/{model_ref}/predictions"
    else:
        url = f"https://api.replicate.com/v1/predictions"
        body["version"] = model_ref

    resp = http_post_json(url, body,
                          headers={"Authorization": f"Bearer {api_key}", "Prefer": "wait"},
                          timeout=600)

    # 等待完成（如果 prefer:wait 不够）
    pred_id = resp.get("id", "")
    deadline = time.time() + 600
    while resp.get("status") not in ("succeeded", "failed", "canceled"):
        if time.time() > deadline:
            raise RuntimeError("Replicate 任务超时")
        time.sleep(2)
        resp = http_get_json(f"https://api.replicate.com/v1/predictions/{pred_id}",
                             headers={"Authorization": f"Bearer {api_key}"})

    if resp.get("status") != "succeeded":
        raise RuntimeError(f"Replicate 失败: {resp.get('error', resp.get('status'))}")

    saved = []
    os.makedirs(output_dir, exist_ok=True)
    output = resp.get("output")
    urls = output if isinstance(output, list) else [output]
    for i, img_url in enumerate(urls):
        if not img_url:
            continue
        path = os.path.join(output_dir, f"replicate-{seed}-{i}.png")
        with open(path, "wb") as f:
            f.write(http_get_bytes(img_url))
        saved.append(path)
    return {"backend": "replicate", "saved": saved, "model": model_ref, "prediction_id": pred_id}


# ─────────────────────────────────────────────────────────
# Fal.ai（v2.4）— 速度型推理服务
# ─────────────────────────────────────────────────────────
def render_fal(positive: str, negative: str, aspect: str, seed: int,
               model_ref: str, output_dir: str, steps: int = 25) -> Dict:
    """调用 Fal.ai API。

    model_ref 形如 'fal-ai/flux/schnell' 或 'fal-ai/stable-diffusion-v3-medium'。
    """
    api_key = os.environ.get("FAL_KEY") or os.environ.get("FAL_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 FAL_KEY 环境变量")
    w, h = aspect_to_size(aspect)

    body = {
        "prompt": positive,
        "negative_prompt": negative,
        "image_size": {"width": w, "height": h},
        "seed": seed,
        "num_inference_steps": steps,
        "num_images": 1,
        "enable_safety_checker": True,
    }
    url = f"https://fal.run/{model_ref}"
    resp = http_post_json(url, body,
                          headers={"Authorization": f"Key {api_key}"},
                          timeout=300)

    saved = []
    os.makedirs(output_dir, exist_ok=True)
    images = resp.get("images", [])
    for i, img in enumerate(images):
        img_url = img.get("url") if isinstance(img, dict) else img
        if not img_url:
            continue
        path = os.path.join(output_dir, f"fal-{seed}-{i}.png")
        with open(path, "wb") as f:
            f.write(http_get_bytes(img_url))
        saved.append(path)
    return {"backend": "fal", "saved": saved, "model": model_ref}


# ─────────────────────────────────────────────────────────
# 即梦 / 可灵 / Hailuo（v2.4）— 国产模型适配
# ─────────────────────────────────────────────────────────
def render_jimeng(positive: str, negative: str, aspect: str, seed: int,
                  output_dir: str) -> Dict:
    """字节即梦 / Seedream API。需要 ARK_API_KEY (火山方舟)。

    走火山方舟 OpenAPI compatible 接口。
    """
    api_key = os.environ.get("ARK_API_KEY") or os.environ.get("JIMENG_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 ARK_API_KEY 环境变量（火山方舟）")
    w, h = aspect_to_size(aspect)
    body = {
        "model": os.environ.get("JIMENG_MODEL", "doubao-seedream-3-0-t2i-250415"),
        "prompt": positive,
        "size": f"{w}x{h}",
        "seed": seed,
        "guidance_scale": 7.5,
        "watermark": False,
    }
    resp = http_post_json(
        "https://ark.cn-beijing.volces.com/api/v3/images/generations",
        body,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=300,
    )
    saved = []
    os.makedirs(output_dir, exist_ok=True)
    for i, item in enumerate(resp.get("data", [])):
        img_url = item.get("url")
        if not img_url:
            continue
        path = os.path.join(output_dir, f"jimeng-{seed}-{i}.png")
        with open(path, "wb") as f:
            f.write(http_get_bytes(img_url))
        saved.append(path)
    return {"backend": "jimeng", "saved": saved, "model": body["model"]}


def render_kling(positive: str, negative: str, aspect: str, seed: int,
                 output_dir: str) -> Dict:
    """快手可灵图像 API。需要 KLING_ACCESS_KEY + KLING_SECRET_KEY（JWT 自签）。

    可灵 API 走 JWT 鉴权（HMAC-SHA256）。这里实现最简单的密钥模式。
    """
    api_key = os.environ.get("KLING_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 KLING_API_KEY 环境变量")
    w, h = aspect_to_size(aspect)
    body = {
        "model_name": "kling-v1",
        "prompt": positive,
        "negative_prompt": negative,
        "aspect_ratio": aspect,
        "n": 1,
    }
    # 提交任务
    resp = http_post_json(
        "https://api.klingai.com/v1/images/generations",
        body,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=60,
    )
    task_id = (resp.get("data") or {}).get("task_id", "")
    if not task_id:
        raise RuntimeError(f"可灵任务创建失败: {resp}")

    # 轮询
    deadline = time.time() + 300
    images = []
    while time.time() < deadline:
        status_resp = http_get_json(
            f"https://api.klingai.com/v1/images/generations/{task_id}",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        data = status_resp.get("data") or {}
        if data.get("task_status") == "succeed":
            images = (data.get("task_result") or {}).get("images", [])
            break
        if data.get("task_status") == "failed":
            raise RuntimeError(f"可灵任务失败: {data.get('task_status_msg')}")
        time.sleep(3)

    saved = []
    os.makedirs(output_dir, exist_ok=True)
    for i, img in enumerate(images):
        img_url = img.get("url") if isinstance(img, dict) else img
        if not img_url:
            continue
        path = os.path.join(output_dir, f"kling-{seed}-{i}.png")
        with open(path, "wb") as f:
            f.write(http_get_bytes(img_url))
        saved.append(path)
    return {"backend": "kling", "saved": saved, "task_id": task_id}


def render_hailuo(positive: str, negative: str, aspect: str, seed: int,
                  output_dir: str) -> Dict:
    """海螺 MiniMax 图像 API。需要 MINIMAX_API_KEY。"""
    api_key = os.environ.get("MINIMAX_API_KEY") or os.environ.get("HAILUO_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 MINIMAX_API_KEY 环境变量")
    w, h = aspect_to_size(aspect)
    body = {
        "model": os.environ.get("MINIMAX_IMAGE_MODEL", "image-01"),
        "prompt": positive,
        "aspect_ratio": aspect,
        "n": 1,
        "response_format": "url",
        "seed": seed,
    }
    resp = http_post_json(
        "https://api.minimaxi.chat/v1/image_generation",
        body,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=300,
    )
    saved = []
    os.makedirs(output_dir, exist_ok=True)
    data = resp.get("data") or {}
    image_urls = data.get("image_urls") or []
    if not image_urls:
        for item in resp.get("data", []) if isinstance(resp.get("data"), list) else []:
            if isinstance(item, dict) and item.get("url"):
                image_urls.append(item["url"])
    for i, img_url in enumerate(image_urls):
        if not img_url:
            continue
        path = os.path.join(output_dir, f"hailuo-{seed}-{i}.png")
        with open(path, "wb") as f:
            f.write(http_get_bytes(img_url))
        saved.append(path)
    return {"backend": "hailuo", "saved": saved, "model": body["model"]}


# ─────────────────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description=f"huo15-img-prompt render_prompt v{VERSION} — 提示词直出图片",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  render_prompt.py "赛博朋克猫" -p 赛博朋克 --backend sd-webui
  render_prompt.py "原神少女" -p 原神 --backend comfyui --workflow ./workflows/sdxl.json
  render_prompt.py "极简logo" -p Logo设计 --backend dalle --size 1024x1024
  render_prompt.py "敦煌神女" -p 敦煌壁画 --backend none -j   # dry-run，只输出 recipe

  # v2.4 新后端：
  render_prompt.py "侠客" -p 水墨 --backend replicate --remote-model black-forest-labs/flux-schnell
  render_prompt.py "猫" -p 动漫 --backend fal --remote-model fal-ai/flux/dev
  render_prompt.py "敦煌神女" -p 敦煌壁画 --backend jimeng     # 字节即梦（火山方舟）
  render_prompt.py "汉服少女" -p 汉服写真 --backend kling      # 快手可灵
  render_prompt.py "原神少女" -p 原神 --backend hailuo         # 海螺 MiniMax
""",
    )
    parser.add_argument("subject", help="主体描述")
    parser.add_argument("-p", "--preset", help="风格预设（支持 A+B 混合）")
    parser.add_argument("--mix", type=float, default=0.6, help="混合权重（默认 0.6）")
    parser.add_argument("-a", "--aspect", default="", help="画幅")
    parser.add_argument("-t", "--tier", choices=["basic", "pro", "master"], default="pro")
    parser.add_argument("--avoid", default="", help="额外负面词")
    parser.add_argument("--seed", type=int, help="种子")
    parser.add_argument(
        "--backend",
        choices=["comfyui", "sd-webui", "dalle", "openai",
                 "replicate", "fal", "jimeng", "kling", "hailuo", "minimax",
                 "none"],
        default="none",
        help="后端：comfyui/sd-webui/dalle | replicate/fal | jimeng/kling/hailuo | none(dry-run)（v2.4 扩 7 后端）",
    )
    parser.add_argument(
        "--remote-model", default="",
        help="Replicate/Fal 模型 ref，例: 'black-forest-labs/flux-schnell' / 'fal-ai/flux/schnell'",
    )
    parser.add_argument("-m", "--model", default="SDXL", help="提示词模型适配（不影响后端选择）")
    parser.add_argument("--output", default="./renders", help="输出目录（默认 ./renders）")
    parser.add_argument("--workflow", default="", help="ComfyUI workflow JSON 路径（可选）")
    parser.add_argument("--steps", type=int, default=25, help="采样步数")
    parser.add_argument("--cfg", type=float, default=7.0, help="CFG scale")
    parser.add_argument("--sampler", default="DPM++ 2M Karras", help="采样器")
    parser.add_argument("--size", default="", help="DALL-E 尺寸 1024x1024 / 1792x1024 / 1024x1792")
    parser.add_argument("--n", type=int, default=1, help="生成张数（DALL-E）")
    parser.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s v{VERSION}")
    args = parser.parse_args()

    raw_preset = args.preset or "写实摄影"
    primary_raw, secondary_raw = parse_mix_preset(raw_preset)
    if secondary_raw:
        primary_resolved = resolve_preset(primary_raw)
        secondary_resolved = resolve_preset(secondary_raw)
        if not primary_resolved or not secondary_resolved:
            print(f"❌ 未知预设：{primary_raw} 或 {secondary_raw}", file=sys.stderr)
            sys.exit(1)
        preset, mix_secondary = primary_resolved, secondary_resolved
    else:
        preset, mix_secondary = primary_raw, None

    auto = parse_requirement(args.subject)
    aspect = args.aspect or auto["aspect_suggestion"] or STYLE_PRESETS.get(resolve_preset(preset) or "写实摄影", {}).get("aspect", "1:1")

    recipe = build_prompt(
        args.subject, preset, args.model, aspect,
        extra_negatives=args.avoid, seed=args.seed, quality_tier=args.tier,
        mix_secondary=mix_secondary, mix_ratio=args.mix,
    )
    seed = recipe["seed_suggestion"]

    if args.backend == "none":
        out = {"version": VERSION, "backend": "none", "recipe": recipe, "note": "dry-run，未实际调用模型"}
        if args.json:
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print(f"🧪 dry-run（未出图）")
            print(f"  positive: {recipe['positive'][:200]}...")
            print(f"  seed:     {seed}")
            print(f"  → 用 -j 输出完整 recipe，再 pipe 给 ComfyUI / DALL-E / SD WebUI")
        return

    try:
        if args.backend == "sd-webui":
            result = render_sdwebui(
                recipe["positive"], recipe["negative"], aspect, seed,
                args.steps, args.cfg, args.sampler, args.output,
            )
        elif args.backend == "comfyui":
            result = render_comfyui(
                recipe["positive"], recipe["negative"], aspect, seed,
                args.steps, args.cfg, args.workflow or None, args.output,
            )
        elif args.backend in ("dalle", "openai"):
            size = args.size or DALLE_SIZES.get(aspect, "1024x1024")
            result = render_dalle(recipe["positive"], size, args.output, n=args.n)
        elif args.backend == "replicate":
            model_ref = args.remote_model or "black-forest-labs/flux-schnell"
            result = render_replicate(
                recipe["positive"], recipe["negative"], aspect, seed,
                model_ref, args.output, steps=args.steps, cfg=args.cfg,
            )
        elif args.backend == "fal":
            model_ref = args.remote_model or "fal-ai/flux/schnell"
            result = render_fal(
                recipe["positive"], recipe["negative"], aspect, seed,
                model_ref, args.output, steps=args.steps,
            )
        elif args.backend == "jimeng":
            result = render_jimeng(recipe["positive"], recipe["negative"], aspect, seed, args.output)
        elif args.backend == "kling":
            result = render_kling(recipe["positive"], recipe["negative"], aspect, seed, args.output)
        elif args.backend in ("hailuo", "minimax"):
            result = render_hailuo(recipe["positive"], recipe["negative"], aspect, seed, args.output)
        else:
            raise RuntimeError(f"未知 backend: {args.backend}")
    except Exception as e:
        print(f"❌ 渲染失败: {e}", file=sys.stderr)
        sys.exit(2)

    out = {"version": VERSION, "recipe": recipe, "render": result}
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"✅ 已出图（backend={result['backend']}）")
        for p in result.get("saved", []):
            print(f"   📷 {p}")
        print(f"   🎲 seed = {seed}")


if __name__ == "__main__":
    main()
