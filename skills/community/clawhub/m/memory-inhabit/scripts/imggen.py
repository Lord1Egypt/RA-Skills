#!/usr/bin/env python3
"""
Memory-Inhabit Image Generator — 文生图模块

通过 MiniMax API 生成图片，支持：
- 风景/场景图（文生图）
- 角色自拍（文生图版，等基准图做好后接入图生图）

用法：
  python3 imggen.py generate <persona> <scene_description> [--style virtual|real] [--provider minimax]
  python3 imggen.py prompt <persona> <scene_description>
  python3 imggen.py test <persona>
"""

import json
import os
import sys
import tempfile
import mimetypes
import base64
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

PERSONAS_DIR = Path(__file__).parent.parent / "personas"
EXTERNAL_PERSONAS_DIR = Path.home() / ".openclaw" / "personas"

# MiniMax API 配置
MINIMAX_API_URL = "https://api.minimaxi.com/v1/image_generation"
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
DEFAULT_PROVIDER = "minimax"
ENV_PROVIDER_KEY = "IMG_PROVIDER"

# 风格层模板（已含禁止项）
STYLE_TEMPLATES = {
    "virtual": "anime style, illustration, vibrant colors, soft lighting, no watermark, no text, no logo, no AI artifacts",
    "real": "photo, realistic photography, natural lighting, no watermark, no text, no logo, no AI artifacts"
}

# 禁止项
FORBIDDEN = "no watermark, no text, no logo, no AI artifacts"


def resolve_persona_dir(persona_name):
    """找到人格包目录"""
    local = PERSONAS_DIR / persona_name
    external = EXTERNAL_PERSONAS_DIR / persona_name
    if local.exists():
        return local
    if external.exists():
        return external
    return None


def load_profile(persona_name):
    """加载 profile.json"""
    persona_dir = resolve_persona_dir(persona_name)
    if not persona_dir:
        raise FileNotFoundError(f"Persona '{persona_name}' not found")
    profile_path = persona_dir / "profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"profile.json not found for '{persona_name}'")
    with open(profile_path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_reference_image(persona_name):
    """
    从人格包中解析角色参考图（用于图生图）

    优先级：
    1) profile.json["assets"]["images"][0]
    2) personas/<name>/assets/images 下第一张图片
    """
    persona_dir = resolve_persona_dir(persona_name)
    if not persona_dir:
        return None

    profile = load_profile(persona_name)
    assets = profile.get("assets", {})
    images = assets.get("images", [])
    if isinstance(images, list) and images:
        first = images[0]
        if isinstance(first, str):
            # 支持 URL 或相对路径
            if first.startswith("http://") or first.startswith("https://"):
                return first
            candidate = persona_dir / first
            if candidate.exists():
                return str(candidate)

    images_dir = persona_dir / "assets" / "images"
    if not images_dir.exists():
        return None

    exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    candidates = sorted([p for p in images_dir.iterdir() if p.is_file() and p.suffix.lower() in exts])
    if candidates:
        return str(candidates[0])

    return None


def to_data_uri(image_path):
    """将本地图片转为 data URI，供 MiniMax subject_reference.image_file 使用"""
    mime, _ = mimetypes.guess_type(image_path)
    if not mime:
        mime = "image/jpeg"
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def infer_source_type(profile):
    """从 profile.json 推断角色类型"""
    # 优先用 source_type 字段
    if profile.get("source_type"):
        return profile["source_type"]

    # 从 relation 判断
    relation = profile.get("relation", "")
    if "真实" in relation or "real" in relation.lower():
        return "real"

    # 有 source 字段 → 虚拟角色
    if profile.get("source"):
        return "virtual"

    # 从职业判断（游戏/小说角色 → 虚拟）
    occupation = profile.get("occupation", "")
    if occupation in ("荣耀职业选手",):
        return "virtual"

    # 默认虚拟
    return "virtual"


def infer_character_appearance(profile):
    """从 profile.json 提取角色外观描述"""
    appearance = profile.get("appearance", {})
    name = profile.get("name", "")

    parts = []

    # 性别（根据名字简单判断，中文语境）
    gender_hint = profile.get("gender", "")
    if not gender_hint:
        # 夏以昼 → male, 叶修 → male
        gender_hint = "male"

    # 发型发色
    hair = appearance.get("hair", "")
    if hair:
        parts.append(hair)

    # 五官/脸
    face = appearance.get("face", "")
    if face:
        parts.append(face)

    # 穿着风格
    style = appearance.get("style", "")
    if style:
        parts.append(style)

    # 体型
    body = appearance.get("body", "")
    if body:
        parts.append(body)

    return ", ".join(parts) if parts else ""


def build_prompt(profile, scene_description, source_type, include_appearance=False):
    """
    构建完整的文生图提示词

    结构：[场景描述] + [外观描述?] + [风格层] + [禁止项]
    - include_appearance=True 时才加入角色外观描述（自拍场景）
    - include_appearance=False 时只生成纯风景/场景图
    """
    parts = []

    # 场景描述
    if scene_description:
        parts.append(scene_description)

    # 外观描述（仅自拍等角色场景时加入）
    if include_appearance:
        appearance = infer_character_appearance(profile)
        if appearance:
            parts.append(appearance)

    # 风格层（已含禁止项）
    style_str = STYLE_TEMPLATES.get(source_type, STYLE_TEMPLATES["real"])
    parts.append(style_str)

    return ", ".join(parts)


def detect_include_appearance(scene_description):
    """
    根据场景描述判断是否需要包含角色外观

    包含自拍/人像类关键词 → 需要外观
    纯风景/场景类关键词 → 不需要外观
    """
    if not scene_description:
        return False

    # 自拍/人像类关键词
    selfie_keywords = ["自拍", "selfie", "人像", "portrait", "照片", "看看你", "给我看"]
    # 纯风景/场景类关键词
    scene_keywords = ["风景", "景色", "scene", "landscape", "view", "环境", "训练室", "房间", "窗外", "街道", "城市", "咖啡厅", " outdoor", " indoor"]

    desc_lower = scene_description.lower()

    # 先检查是否是纯风景
    is_scene = any(kw in desc_lower for kw in ["风景", "景色", "scene", "landscape", "view", "环境", "窗外", "街道", "城市"])
    has_selfie_kw = any(kw in desc_lower for kw in selfie_keywords)

    if has_selfie_kw:
        return True
    if is_scene:
        return False

    # 默认不含外观（纯风景优先）
    return False


def get_effective_provider(provider_override=None):
    """解析生图后端：命令行参数 > 环境变量 > 默认值"""
    provider = (provider_override or os.environ.get(ENV_PROVIDER_KEY, DEFAULT_PROVIDER)).strip().lower()
    return provider or DEFAULT_PROVIDER


def get_supported_providers():
    """返回当前已注册的生图后端"""
    return {"minimax"}


def generate_image_minimax(prompt, model="image-01", aspect_ratio="16:9", subject_reference=None):
    """
    调用 MiniMax 图文生成 API

    Returns: (image_url, revised_prompt)
    """
    if not MINIMAX_API_KEY:
        raise ValueError("MINIMAX_API_KEY not set in environment")

    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": "url",
        "n": 1
    }
    if subject_reference:
        payload["subject_reference"] = subject_reference

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        MINIMAX_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"MiniMax API error {e.code}: {error_body}")

    # 解析返回 — MiniMax 图生图返回结构
    # 成功: { "data": { "image_urls": ["..."] }, "base_resp": { "status_code": 0 } }
    # 失败: { "base_resp": { "status_code": 非0, "status_msg": "..." } }
    base_resp = result.get("base_resp", {})
    if base_resp.get("status_code") != 0:
        raise RuntimeError(f"MiniMax API error: {base_resp.get('status_msg', 'unknown')}")

    data = result.get("data", {})
    image_urls = data.get("image_urls", [])
    if not image_urls:
        raise RuntimeError(f"No image URL in response: {result}")

    image_url = image_urls[0]
    # MiniMax 图生图一般不返回 revised_prompt，取空字符串
    revised_prompt = prompt
    return image_url, revised_prompt


def generate_image_with_provider(provider, prompt, model="image-01", aspect_ratio="16:9", subject_reference=None):
    """
    统一生图入口，按 provider 分发

    目前支持：
    - minimax
    """
    if provider == "minimax":
        return generate_image_minimax(
            prompt,
            model=model,
            aspect_ratio=aspect_ratio,
            subject_reference=subject_reference
        )

    supported = ", ".join(sorted(get_supported_providers()))
    raise ValueError(f"Unsupported provider '{provider}'. Supported providers: {supported}")


def download_image(url, save_dir=None):
    """
    下载图片到临时目录

    Returns: 本地文件路径
    """
    if save_dir is None:
        save_dir = tempfile.gettempdir()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mi_imggen_{timestamp}.jpg"
    save_path = Path(save_dir) / filename

    req = urllib.request.Request(url)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            with open(save_path, "wb") as out:
                out.write(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Failed to download image: {e.code}")

    return str(save_path)


def cleanup_image(path):
    """删除临时图片"""
    try:
        Path(path).unlink(missing_ok=True)
    except Exception:
        pass


def generate_and_save(persona_name, scene_description, aspect_ratio="16:9", reference_image=None, provider=None):
    """
    完整流程：构建提示词 → 生成 → 下载 → 返回本地路径
    """
    # 1. 加载 profile
    profile = load_profile(persona_name)

    # 2. 推断风格
    source_type = infer_source_type(profile)

    # 3. 构建提示词
    include_app = detect_include_appearance(scene_description)
    prompt = build_prompt(profile, scene_description, source_type, include_appearance=include_app)

    # 3.5 图生图主体参考（可选）
    subject_reference = None
    ref = reference_image
    if ref is None and include_app:
        ref = resolve_reference_image(persona_name)
    if ref:
        ref_value = ref
        if not (ref.startswith("http://") or ref.startswith("https://") or ref.startswith("data:")):
            ref_value = to_data_uri(ref)
        subject_reference = [{"type": "character", "image_file": ref_value}]

    # 4. 生成
    effective_provider = get_effective_provider(provider)
    image_url, revised_prompt = generate_image_with_provider(
        effective_provider,
        prompt,
        aspect_ratio=aspect_ratio,
        subject_reference=subject_reference
    )

    # 5. 下载
    local_path = download_image(image_url)

    return {
        "persona": persona_name,
        "provider": effective_provider,
        "source_type": source_type,
        "reference_image": ref if ref else "",
        "original_prompt": prompt,
        "revised_prompt": revised_prompt,
        "image_url": image_url,
        "local_path": local_path
    }


def cmd_generate(persona, scene, style_override=None, reference_image=None, provider=None):
    """generate 命令"""
    if not MINIMAX_API_KEY:
        print("Error: MINIMAX_API_KEY not set", file=sys.stderr)
        print("Set it with: export MINIMAX_API_KEY=your_key", file=sys.stderr)
        sys.exit(1)

    profile = load_profile(persona)
    source_type = style_override or infer_source_type(profile)
    include_app = detect_include_appearance(scene)
    prompt = build_prompt(profile, scene, source_type, include_appearance=include_app)

    subject_reference = None
    ref = reference_image
    if ref is None and include_app:
        ref = resolve_reference_image(persona)
    if ref:
        ref_value = ref
        if not (ref.startswith("http://") or ref.startswith("https://") or ref.startswith("data:")):
            ref_value = to_data_uri(ref)
        subject_reference = [{"type": "character", "image_file": ref_value}]

    effective_provider = get_effective_provider(provider)

    print(f"[{persona}] generating image...")
    print(f"provider: {effective_provider}")
    print(f"source_type: {source_type}")
    print(f"include_appearance: {include_app}")
    print(f"subject_reference: {'enabled' if subject_reference else 'disabled'}")
    if ref:
        print(f"reference_image: {ref}")
    print(f"prompt: {prompt}")

    image_url, revised_prompt = generate_image_with_provider(
        effective_provider,
        prompt,
        subject_reference=subject_reference
    )
    print(f"image_url: {image_url}")

    local_path = download_image(image_url)
    print(f"saved to: {local_path}")

    return local_path


def cmd_prompt(persona, scene):
    """prompt 命令：只输出提示词，不生成"""
    profile = load_profile(persona)
    source_type = infer_source_type(profile)
    include_app = detect_include_appearance(scene)
    prompt = build_prompt(profile, scene, source_type, include_appearance=include_app)
    print(f"[{persona}] prompt preview:")
    print(f"source_type: {source_type}")
    print(f"include_appearance: {include_app}")
    print(f"prompt: {prompt}")


def cmd_test(persona):
    """test 命令：用默认场景测试"""
    scenes = [
        "Indoor gaming training room, multiple computers on desk, Blue Light shielding cover visible",
        "Cozy cafe corner, warm afternoon sunlight, scattered books on table"
    ]
    for scene in scenes:
        print(f"\n{'='*50}")
        cmd_prompt(persona, scene)
        print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "generate":
        if len(sys.argv) < 4:
            print("Usage: imggen.py generate <persona> <scene_description>")
            sys.exit(1)
        persona = sys.argv[2]
        scene = sys.argv[3]
        style_override = None
        reference_image = None
        provider_override = None
        for i, arg in enumerate(sys.argv):
            if arg == "--style" and i + 1 < len(sys.argv):
                style_override = sys.argv[i + 1]
            if arg == "--ref-image" and i + 1 < len(sys.argv):
                reference_image = sys.argv[i + 1]
            if arg == "--provider" and i + 1 < len(sys.argv):
                provider_override = sys.argv[i + 1]
        cmd_generate(
            persona,
            scene,
            style_override,
            reference_image=reference_image,
            provider=provider_override
        )

    elif cmd == "prompt":
        if len(sys.argv) < 4:
            print("Usage: imggen.py prompt <persona> <scene_description>")
            sys.exit(1)
        persona = sys.argv[2]
        scene = sys.argv[3]
        cmd_prompt(persona, scene)

    elif cmd == "test":
        persona = sys.argv[2] if len(sys.argv) > 2 else "叶修"
        cmd_test(persona)

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)
