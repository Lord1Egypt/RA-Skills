import os
import uuid
import base64
import io
from datetime import datetime

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
RESULT_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

STEPFUN_API_KEY = os.getenv("STEPFUN_API_KEY", "")
STEPFUN_BASE_URL = os.getenv("STEPFUN_BASE_URL", "https://api.stepfun.com/v1")
STEPFUN_EDIT_URL = f"{STEPFUN_BASE_URL}/images/edit"

FEATURE_PROMPTS = {
    "restore": {
        "name": "老照片修复",
        "prompt": (
            "Restore this old, damaged photo to high quality. "
            "Fix scratches, tears, fading, and color degradation. "
            "Enhance clarity, sharpen details, and restore natural colors. "
            "Remove noise and grain while preserving the original composition and subjects. "
            "Make it look like a professionally restored photograph."
        ),
        "description": "修复破损老照片，去划痕、去噪点、恢复色彩",
    },
    "portrait": {
        "name": "人像精修",
        "prompt": (
            "Professional portrait retouching. "
            "Smooth skin naturally without losing texture, brighten eyes, "
            "enhance facial features subtly, improve lighting and contrast, "
            "add a soft professional studio look. "
            "Keep the person recognizable — natural and elegant result."
        ),
        "description": "智能美颜、皮肤优化、五官增强",
    },
    "landscape": {
        "name": "风景调色",
        "prompt": (
            "Professional landscape color grading. "
            "Enhance saturation, contrast, and dynamic range. "
            "Make the sky more vivid, greens richer, and overall scene more cinematic. "
            "Apply a premium travel photography aesthetic. "
            "Preserve all original elements and composition."
        ),
        "description": "增强色彩、提升对比度、电影级调色",
    },
    "style": {
        "name": "风格调整",
        "prompt": (
            "Transform this image into {style} artistic style. "
            "Apply the distinct visual characteristics of this style while "
            "preserving the main subjects and composition of the original image. "
            "High quality, visually striking result."
        ),
        "description": "多种艺术风格转换",
    },
}

STYLE_OPTIONS = {
    "oil": "oil painting with visible brush strokes and rich textures",
    "watercolor": "watercolor painting with soft washes and flowing colors",
    "sketch": "pencil sketch with fine lines and shading",
    "anime": "Japanese anime/manga illustration style with clean lines",
    "cyberpunk": "cyberpunk aesthetic with neon lights and futuristic urban mood",
    "vintage": "vintage film photography look with warm tones and slight grain",
    "ink": "traditional Chinese ink wash painting (水墨画) style",
    "popart": "pop art style with bold colors and halftone patterns",
}


def image_to_base64(filepath):
    with open(filepath, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def save_base64_image(b64_data, output_dir, prefix="result"):
    img_data = base64.b64decode(b64_data)
    filename = f"{prefix}_{uuid.uuid4().hex[:8]}.png"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "wb") as f:
        f.write(img_data)
    return filename


@app.route("/api/features", methods=["GET"])
def get_features():
    """返回所有功能模块"""
    features = []
    for key, info in FEATURE_PROMPTS.items():
        item = {
            "id": key,
            "name": info["name"],
            "description": info["description"],
        }
        if key == "style":
            item["styles"] = [
                {"id": s, "name": n}
                for s, n in [
                    ("oil", "油画"),
                    ("watercolor", "水彩"),
                    ("sketch", "素描"),
                    ("anime", "动漫"),
                    ("cyberpunk", "赛博朋克"),
                    ("vintage", "复古胶片"),
                    ("ink", "水墨画"),
                    ("popart", "波普艺术"),
                ]
            ]
        features.append(item)
    return jsonify({"features": features})


@app.route("/api/edit", methods=["POST"])
def edit_image():
    """图片编辑接口"""
    if "image" not in request.files:
        return jsonify({"error": "请上传图片"}), 400

    image_file = request.files["image"]
    feature = request.form.get("feature", "restore")
    style = request.form.get("style", "oil")

    if feature not in FEATURE_PROMPTS:
        return jsonify({"error": f"不支持的功能: {feature}"}), 400

    # 保存上传图片
    ext = os.path.splitext(image_file.filename)[1] or ".png"
    upload_filename = f"upload_{uuid.uuid4().hex[:8]}{ext}"
    upload_path = os.path.join(UPLOAD_DIR, upload_filename)
    image_file.save(upload_path)

    # 压缩大图
    img = Image.open(upload_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    max_size = 2048
    if max(img.size) > max_size:
        img.thumbnail((max_size, max_size), Image.LANCZOS)
    img.save(upload_path, "PNG")

    # 构建提示词
    prompt_template = FEATURE_PROMPTS[feature]["prompt"]
    prompt = prompt_template.format(style=STYLE_OPTIONS.get(style, STYLE_OPTIONS["oil"]))

    # 调用 StepFun API
    image_b64 = image_to_base64(upload_path)

    headers = {
        "Authorization": f"Bearer {STEPFUN_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "step-image-edit-2",
        "image": image_b64,
        "prompt": prompt,
        "response_format": "b64_json",
    }

    try:
        resp = requests.post(STEPFUN_EDIT_URL, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        # 保存结果
        result_b64 = data.get("data", [{}])[0].get("b64_json", "")
        if not result_b64:
            return jsonify({"error": "API 返回数据异常", "raw": data}), 500

        result_filename = save_base64_image(result_b64, RESULT_DIR)

        return jsonify({
            "success": True,
            "original": f"/uploads/{upload_filename}",
            "result": f"/results/{result_filename}",
            "feature": feature,
            "prompt": prompt,
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API 调用失败: {str(e)}"}), 500


@app.route("/uploads/<filename>")
def serve_upload(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/results/<filename>")
def serve_result(filename):
    return send_from_directory(RESULT_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
