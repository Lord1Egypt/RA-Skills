#!/usr/bin/env python3
"""
毛球项目 - 照片一键转3D模型 Pipeline
Step 1: Gemini (Nano Banana) 将照片转为白底45度俯视图
Step 2: Tripo3D API 将俯视图转为3D模型
"""

import os
import sys
import time
import json
import base64
import argparse
import requests
from pathlib import Path

# ============ 配置 ============
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
TRIPO_API_KEY = os.environ.get("TRIPO_API_KEY", "")
GEMINI_MODEL = "gemini-2.5-flash-preview-05-20"  # Nano Banana

# Nano Banana 预处理 prompt
PREPROCESS_PROMPT = """Use the provided photo as reference. Generate a high-fidelity 3D model rendering in the look of a "3D-printed model."
Preserve the object's massing and key texture details, lightly stylized.
Render with realistic, physically-based lighting and shadows.
Show a 45-degree top-down (isometric) view to emphasize depth.
Define materials clearly so it reads as a high-quality, game-engine-ready render.
Pure white background. No text, no watermark."""

OUTPUT_DIR = Path("output")


def step1_gemini_preprocess(image_path: str, custom_prompt: str = None) -> str:
    """Step 1: 用 Gemini 将照片转为白底45度俯视图"""
    if not GEMINI_API_KEY:
        print("❌ 缺少 GEMINI_API_KEY，请设置环境变量")
        sys.exit(1)

    print("🎨 Step 1: Gemini 预处理 - 生成白底俯视图...")

    # 读取图片并编码
    img_path = Path(image_path)
    if not img_path.exists():
        print(f"❌ 图片不存在: {image_path}")
        sys.exit(1)

    with open(img_path, "rb") as f:
        img_data = base64.b64encode(f.read()).decode()

    # 判断 mime type
    suffix = img_path.suffix.lower()
    mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    mime_type = mime_map.get(suffix, "image/jpeg")

    prompt = custom_prompt or PREPROCESS_PROMPT

    # 调用 Gemini API (generateContent with image generation)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"inline_data": {"mime_type": mime_type, "data": img_data}},
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"],
        },
    }

    resp = requests.post(url, json=payload, timeout=120)
    if resp.status_code != 200:
        print(f"❌ Gemini API 错误: {resp.status_code}")
        print(resp.text[:500])
        sys.exit(1)

    result = resp.json()

    # 提取生成的图片
    output_path = OUTPUT_DIR / f"{img_path.stem}_isometric.png"
    found_image = False

    try:
        for part in result["candidates"][0]["content"]["parts"]:
            if "inlineData" in part:
                img_bytes = base64.b64decode(part["inlineData"]["data"])
                output_path.write_bytes(img_bytes)
                found_image = True
                print(f"✅ 俯视图已生成: {output_path}")
                break
    except (KeyError, IndexError) as e:
        print(f"❌ 解析 Gemini 响应失败: {e}")
        print(json.dumps(result, indent=2, ensure_ascii=False)[:500])
        sys.exit(1)

    if not found_image:
        print("❌ Gemini 未返回图片，可能需要调整 prompt")
        print(json.dumps(result, indent=2, ensure_ascii=False)[:500])
        sys.exit(1)

    return str(output_path)


def step2_tripo_generate_3d(image_path: str) -> str:
    """Step 2: 用 Tripo3D API 将俯视图转为3D模型"""
    if not TRIPO_API_KEY:
        print("❌ 缺少 TRIPO_API_KEY，请设置环境变量")
        sys.exit(1)

    print("🔨 Step 2: Tripo3D - 生成3D模型...")

    # 上传图片
    headers = {"Authorization": f"Bearer {TRIPO_API_KEY}"}

    img_path = Path(image_path)
    with open(img_path, "rb") as f:
        upload_resp = requests.post(
            "https://api.tripo3d.ai/v2/openapi/upload",
            headers=headers,
            files={"file": (img_path.name, f, "image/png")},
            timeout=60,
        )

    if upload_resp.status_code != 200:
        print(f"❌ Tripo 上传失败: {upload_resp.status_code}")
        print(upload_resp.text[:500])
        sys.exit(1)

    upload_data = upload_resp.json()
    image_token = upload_data.get("data", {}).get("image_token", "")
    if not image_token:
        print(f"❌ 未获取到 image_token: {upload_data}")
        sys.exit(1)

    print(f"  📤 图片已上传, token: {image_token[:20]}...")

    # 创建 image-to-3d 任务
    task_resp = requests.post(
        "https://api.tripo3d.ai/v2/openapi/task",
        headers={**headers, "Content-Type": "application/json"},
        json={"type": "image_to_model", "file": {"type": "png", "file_token": image_token}},
        timeout=60,
    )

    if task_resp.status_code != 200:
        print(f"❌ Tripo 创建任务失败: {task_resp.status_code}")
        print(task_resp.text[:500])
        sys.exit(1)

    task_data = task_resp.json()
    task_id = task_data.get("data", {}).get("task_id", "")
    if not task_id:
        print(f"❌ 未获取到 task_id: {task_data}")
        sys.exit(1)

    print(f"  🚀 任务已创建: {task_id}")

    # 轮询任务状态
    max_wait = 300  # 最多等5分钟
    start = time.time()
    while time.time() - start < max_wait:
        time.sleep(5)
        status_resp = requests.get(
            f"https://api.tripo3d.ai/v2/openapi/task/{task_id}",
            headers=headers,
            timeout=30,
        )
        status_data = status_resp.json().get("data", {})
        status = status_data.get("status", "unknown")
        progress = status_data.get("progress", 0)

        print(f"  ⏳ 状态: {status} | 进度: {progress}%", end="\r")

        if status == "success":
            print(f"\n  ✅ 3D模型生成完成!")
            # 下载模型
            model_url = status_data.get("output", {}).get("model", "")
            if model_url:
                output_path = OUTPUT_DIR / f"{img_path.stem}_model.glb"
                model_resp = requests.get(model_url, timeout=120)
                output_path.write_bytes(model_resp.content)
                print(f"  📦 模型已保存: {output_path}")
                return str(output_path)
            else:
                # 尝试其他输出格式
                print(f"  ℹ️ 输出数据: {json.dumps(status_data.get('output', {}), indent=2)}")
                return ""

        elif status == "failed":
            print(f"\n  ❌ 任务失败: {status_data.get('message', 'unknown error')}")
            sys.exit(1)

    print(f"\n  ❌ 超时（{max_wait}秒），任务可能仍在处理中，task_id: {task_id}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="📸 照片一键转3D模型")
    parser.add_argument("image", help="输入图片路径")
    parser.add_argument("--prompt", help="自定义 Gemini 预处理 prompt", default=None)
    parser.add_argument("--skip-preprocess", action="store_true", help="跳过预处理，直接用原图生成3D")
    parser.add_argument("--output-dir", help="输出目录", default="output")
    args = parser.parse_args()

    global OUTPUT_DIR
    OUTPUT_DIR = Path(args.output_dir)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 50)
    print("🧶 毛球项目 - 照片一键转3D模型")
    print("=" * 50)

    if args.skip_preprocess:
        print("⏭️  跳过预处理，直接使用原图")
        isometric_path = args.image
    else:
        isometric_path = step1_gemini_preprocess(args.image, args.prompt)

    model_path = step2_tripo_generate_3d(isometric_path)

    print("\n" + "=" * 50)
    print("🎉 完成!")
    if model_path:
        print(f"   3D模型: {model_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
