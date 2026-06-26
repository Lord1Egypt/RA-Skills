# -*- coding: utf-8 -*-
"""
专业形象顾问提示词生成器 & 评估 Payload 构建器
身材分析 (骨架量感×线条曲直理论方向)
肤色分析 (四季色彩理论方向)
个人风格识别 (PCCS色彩×Kibbe身形理论方向)
功能：将用户数据自动填充至标准分析提示词模版，并构建 MiniMax 多模态请求 Payload
"""
import os
import re
import base64
import io
import shutil
import tempfile
from PIL import Image

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 修正：读取同级别文件夹“PROMPT”下的提示词文件
_PROMPT_DIR = os.path.normpath(os.path.join(_BASE_DIR, "..", "PROMPT"))

def _load_prompt_template(filename: str) -> str:
    """读取 PROMPT 文件夹下的提示词模版文件"""
    filepath = os.path.join(_PROMPT_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"提示词模板未找到: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# 清理了原代码中键名末尾的多余空格
BODY_DEFAULT_DATA = {
    "height": "-",
    "weight": "-",
    "shoulder_width": "-",
    "bust": "-",
    "waist": "-",
    "hip": "-",
    "wrist": "-",
    "leg_circumference": "-",
    "leg_length": "-",
    "body_features": "-"
}

def generate_consultant_prompt(user_data: dict) -> str:
    """生成填充后的身材形象顾问提示词"""
    final_data = BODY_DEFAULT_DATA.copy()
    if user_data:
        final_data.update(user_data)

    prompt_template = _load_prompt_template("body_data_prompt.md")
    try:
        filled_prompt = prompt_template.format(**final_data)
    except KeyError as e:
        print(f"[警告] 数据键名缺失：{e}，已自动替换为默认值")
        for key in BODY_DEFAULT_DATA.keys():
            if key not in final_data:
                final_data[key] = "-"
        filled_prompt = prompt_template.format(**final_data)

    return filled_prompt

SKIN_PARAM_KEYS = [
    "hair_color",        # 发色
    "pupil_color",       # 瞳孔色
    "face_tone",         # 自然光下面部色调
    "cheek_redness",     # 脸颊是否易泛红
    "skin_gloss",        # 肤质光泽感
    "vein_color",        # 血管测试结果
    "paper_test",        # 白纸测试结果
    "dress_preference",  # 日常穿搭偏好
    "visual_improvement" # 希望改善的视觉问题
]

def generate_skin_prompt(user_data: dict) -> str:
    """生成填充后的肤色形象顾问提示词（缺失项自动删除整行）"""
    user_data = user_data or {}
    prompt_template = _load_prompt_template("skin_data_prompt.md")

    missing_keys = [k for k in SKIN_PARAM_KEYS if k not in user_data]
    result = prompt_template
    for key in missing_keys:
        result = re.sub(r'[ \t]*.*\{' + key + r'\}.*\n?', '', result)

    try:
        result = result.format(**user_data)
    except KeyError as e:
        print(f"[警告] 肤色数据键名缺失：{e}")

    result = re.sub(r'\n{3,}', '\n\n', result)
    return result

STYLE_PARAM_KEYS = [
    "photo_count",         # 照片数量（由代码自动计算）
    "outfit_scenes",       # 穿搭常用场景
    "preferred_materials", # 偏好材质
    "avoided_items"        # 避雷单品
]

def save_uploaded_photos(file_data_list: list) -> dict:
    """将前端上传的照片保存到临时文件夹"""
    if not file_data_list:
        return {"status": "error", "message": "未接收到任何照片文件"}

    temp_dir = tempfile.mkdtemp(prefix="style_photos_")
    temp_photo_paths = []

    for i, file_info in enumerate(file_data_list):
        filename = file_info.get("filename", f"upload_{i + 1}.jpg")
        content = file_info.get("content", b"")
        if not content:
            print(f"[警告] 第 {i + 1} 张照片内容为空，已跳过")
            continue

        ext = os.path.splitext(filename)[1] or ".jpg"
        dst_name = f"outfit_{i + 1}{ext}"
        dst_path = os.path.join(temp_dir, dst_name)

        with open(dst_path, "wb") as f:
            f.write(content)
        temp_photo_paths.append(dst_path)

    if not temp_photo_paths:
        shutil.rmtree(temp_dir, ignore_errors=True)
        return {"status": "error", "message": "所有照片内容均为空，保存失败"}

    return {
        "status": "success",
        "temp_dir": temp_dir,
        "temp_photo_paths": temp_photo_paths
    }

def _compress_and_encode_image(image_path: str, max_size=1024, quality=85) -> str:
    """图片预压缩 + Base64 编码，返回 Data URI"""
    img = Image.open(image_path)
    img.thumbnail((max_size, max_size))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=quality)
    pure_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{pure_base64}"

_REQUIRED_FIELDS = {
    "body": {
        "must": ["height", "weight"],
        "preferred": ["shoulder_width", "bust", "waist", "hip", "wrist"],
        "min_preferred": 3,
        "description": "身材分析"
    },
    "skin": {
        "must": ["hair_color", "pupil_color", "face_tone"],
        "preferred": ["vein_color", "paper_test", "cheek_redness", "skin_gloss"],
        "min_preferred": 1,
        "description": "肤色诊断"
    },
    "style": {
        "must": [],
        "preferred": ["outfit_scenes", "preferred_materials", "avoided_items"],
        "min_preferred": 0,
        "min_photos": 3,
        "description": "风格识别"
    }
}

def check_data_sufficiency(category: str, user_data: dict, photo_count: int = 0) -> dict:
    """检查指定类别的用户数据是否满足触发大模型评估的最低要求"""
    if category not in _REQUIRED_FIELDS:
        return {"ready": False, "missing": [], "message": f"未知类别：{category}，有效值为 body/skin/style"}

    spec = _REQUIRED_FIELDS[category]
    user_data = user_data or {}

    missing_must = [k for k in spec["must"] if k not in user_data or not user_data[k]]
    if missing_must:
        return {
            "ready": False,
            "missing": missing_must,
            "message": f"【{spec['description']}】缺少必填信息：{', '.join(missing_must)}，请继续引导用户提供。"
        }

    provided_preferred = [k for k in spec["preferred"] if k in user_data and user_data[k]]
    if len(provided_preferred) < spec["min_preferred"]:
        still_need = spec["min_preferred"] - len(provided_preferred)
        candidates = [k for k in spec["preferred"] if k not in user_data or not user_data[k]]
        return {
            "ready": False,
            "missing": candidates[:still_need],
            "message": f"【{spec['description']}】建议至少再补充 {still_need} 项：{', '.join(candidates[:still_need])}。"
        }

    if category == "style":
        min_photos = spec.get("min_photos", 3)
        if photo_count < min_photos:
            return {
                "ready": False,
                "missing": [],
                "message": f"【{spec['description']}】照片不足，当前 {photo_count} 张，至少需要 {min_photos} 张 OOTD 照片。"
            }

    return {
        "ready": True,
        "missing": [],
        "message": f"【{spec['description']}】数据充分，可以触发大模型评估。"
    }


def build_evaluation_payload(category: str, user_data: dict,
                             photo_paths: list = None,
                             model: str = "MiniMax-M2.7",
                             max_tokens: int = 2000) -> dict:
    """
    统一评估 Payload 构建入口（需确保已调用 check_data_sufficiency 且 ready=True）
    自动区分纯文本（身材/肤色）与多模态（风格+图片）场景
    """
    content_parts = []
    prompt_text = ""

    if category == "body":
        prompt_text = generate_consultant_prompt(user_data)
        content_parts.append({"type": "text", "text": prompt_text})

    elif category == "skin":
        prompt_text = generate_skin_prompt(user_data)
        content_parts.append({"type": "text", "text": prompt_text})

    elif category == "style":
        if not photo_paths:
            return {"status": "error", "message": "风格评估需要照片路径列表", "category": category}

        # 1. 动态生成风格提示词
        fill_data = user_data.copy()
        fill_data["photo_count"] = str(len(photo_paths))
        prompt_template = _load_prompt_template("self_style_prompt.md")
        missing_keys = [k for k in STYLE_PARAM_KEYS if k not in fill_data]
        prompt_text = prompt_template
        for key in missing_keys:
            prompt_text = re.sub(r'[ \t]*.*\{' + key + r'\}.*\n?', '', prompt_text)
        try:
            prompt_text = prompt_text.format(**fill_data)
        except KeyError as e:
            print(f"[警告] 风格数据键名缺失：{e}")
        prompt_text = re.sub(r'\n{3,}', '\n\n', prompt_text)
        content_parts.append({"type": "text", "text": prompt_text})

        # 2. 处理多模态图片
        valid_img_count = 0
        for p in photo_paths:
            if not os.path.isfile(p):
                print(f"[警告] 照片路径不存在，已跳过：{p}")
                continue
            try:
                data_uri = _compress_and_encode_image(p)
                content_parts.append({"type": "image_url", "image_url": {"url": data_uri}})
                valid_img_count += 1
            except Exception as e:
                print(f"[警告] 照片编码失败({p}): {e}")

        if valid_img_count == 0:
            return {"status": "error", "message": "有效图片数量为0，无法构建多模态Payload", "category": category}
    else:
        return {"status": "error", "message": f"未知评估类别：{category}", "category": category}

    # 3. 组装 MiniMax 兼容 Payload
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content_parts}],
        "max_tokens": max_tokens
    }

    return {"status": "success", "payload": payload, "prompt": prompt_text, "category": category}

def cleanup_style_temp(temp_dir: str):
    """清理风格识别的临时照片文件夹"""
    if temp_dir and os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"[信息] 已清理临时照片文件夹：{temp_dir}")

if __name__ == "__main__":
    # 准备测试数据（已清理键名空格）
    body_data = {
        "height": "165cm", "weight": "50kg", "shoulder_width": "42cm",
        "bust": "70cm", "waist": "65cm", "hip": "73cm", "wrist": "14cm",
        "leg_circumference": "22cm", "leg_length": "101cm", "body_features": "侧面身体较薄、锁骨明显"
    }
    skin_data = {
        "hair_color": "自然黑", "pupil_color": "深棕",
        "face_tone": "暖黄调", "vein_color": "蓝绿"
    }
    style_data = {"outfit_scenes": "通勤/休闲", "preferred_materials": "棉麻/丝绸"}

    print("="*50)
    print("【标准调用流程演示】")
    print("="*50)

    # 1. 先检查数据充分性
    checks = {
        "body": check_data_sufficiency("body", body_data),
        "skin": check_data_sufficiency("skin", skin_data),
        "style": check_data_sufficiency("style", style_data, photo_count=5)
    }

    for cat, res in checks.items():
        print(f"✅ {cat.upper()} 检查: {res['message']}")

    # 2. 充分性通过后，统一构建 Payload
    print("\n--- 构建 Payload ---")
    # 身材/肤色（纯文本）
    body_payload = build_evaluation_payload("body", body_data)
    print(f"📦 Body Payload 状态: {body_payload['status']} | 包含文本长度: {len(body_payload['prompt'])}")

    skin_payload = build_evaluation_payload("skin", skin_data)
    print(f"📦 Skin Payload 状态: {skin_payload['status']} | 包含文本长度: {len(skin_payload['prompt'])}")

    # 风格（多模态：文本+图片）
    # 模拟临时图片路径（实际由 save_uploaded_photos 返回）
    mock_temp_dir = tempfile.mkdtemp(prefix="test_style_")
    mock_photo_paths = [os.path.join(mock_temp_dir, f"mock_{i}.jpg") for i in range(3)]
    for p in mock_photo_paths:
        with open(p, "wb") as f: f.write(b"\xff\xd8\xff\xe0" + os.urandom(100))

    style_payload = build_evaluation_payload("style", style_data, photo_paths=mock_photo_paths)
    print(f"📦 Style Payload 状态: {style_payload['status']} | Content Parts 数量: {len(style_payload['payload']['messages'][0]['content'])}")

    # 清理测试文件
    for p in mock_photo_paths:
        if os.path.exists(p): os.remove(p)
    if os.path.exists(mock_temp_dir): os.rmdir(mock_temp_dir)

    print("\n✅ 整合优化完成，可直接接入 LLM API 调用循环。")