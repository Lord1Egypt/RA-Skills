#!/usr/bin/env python3
"""
灵境 JoyCreator 三阶段智能调用脚本
  阶段一 (Router)  : 解析用户自然语言 → 结构化意图 JSON
  阶段二 (Choice)  : 意图 JSON → 推荐最优模型 + apiId
  阶段三 (Executor): 构造请求 → 提交任务

用法：
  python joycreator.py                          # 智能交互模式（推荐）
  python joycreator.py --prompt "画一只猫"       # 快速参数模式
  python joycreator.py --brand kling \          # 跳过推荐，直接指定品牌
    --task text2video --prompt "..."

环境变量：
  JOYCREATOR_APP_KEY   App Key（优先级高于交互输入）
"""

import os, sys, time, uuid, json, argparse, getpass, requests

BASE_URL = "https://model.jdcloud.com/joycreator/openApi/submitTask"

# ============================================================
# 模型推荐规则表（与 references/choice-rules.md 保持同步）
# ============================================================

# 结构：{brand: {task: [{apiId, model_key, model_val, label}, ...]}}
API_CONFIG = {
    "doubao": {
        "text2image": [
            {"apiId": "701", "model_key": "model", "model_val": "doubao-seedream-4-5-251128", "label": "Seedream 4.5"},
            {"apiId": "700", "model_key": "model", "model_val": "doubao-seedream-4-0-250828", "label": "Seedream 4.0"},
        ],
        "text2video": [
            {"apiId": "750", "model_key": "model_name", "model_val": "Doubao-Seedance-1.5-pro", "label": "Seedance 1.5 Pro"},
        ],
        "image2video": [
            {"apiId": "751", "model_key": "model_name", "model_val": "Doubao-Seedance-1.5-pro", "label": "Seedance 1.5 Pro"},
        ],
        "ref2video": None,
    },
    "hailuo": {
        "text2image": [
            {"apiId": "456", "model_key": "model", "model_val": "image-01", "label": "image-01"},
        ],
        "text2video": [
            {"apiId": "460", "model_key": "model", "model_val": "MiniMax-Hailuo-2.3",      "label": "Hailuo-2.3"},
            {"apiId": "462", "model_key": "model", "model_val": "MiniMax-Hailuo-2.3-Fast", "label": "Hailuo-2.3-Fast（极速）"},
            {"apiId": "458", "model_key": "model", "model_val": "MiniMax-Hailuo-02",       "label": "Hailuo-02"},
        ],
        "image2video": [
            {"apiId": "461", "model_key": "model", "model_val": "MiniMax-Hailuo-2.3",      "label": "Hailuo-2.3"},
            {"apiId": "462", "model_key": "model", "model_val": "MiniMax-Hailuo-2.3-Fast", "label": "Hailuo-2.3-Fast（极速）"},
            {"apiId": "457", "model_key": "model", "model_val": "MiniMax-Hailuo-02",       "label": "Hailuo-02（支持尾帧）"},
        ],
        "ref2video": [
            {"apiId": "459", "model_key": "model", "model_val": "S2V-01", "label": "S2V-01（主体一致性）"},
        ],
    },
    "kling": {
        "text2image": [
            {"apiId": "553", "model_key": "model_name", "model_val": "kling-v2-1", "label": "Kling-V2.1"},
        ],
        "image2image": [
            {"apiId": "554", "model_key": "model_name", "model_val": "kling-v2", "label": "Kling-V2（图生图）"},
        ],
        "text2video": [
            {"apiId": "565", "model_key": "model_name", "model_val": "Kling-V3",          "label": "Kling-V3（多镜头）"},
            {"apiId": "563", "model_key": "model_name", "model_val": "kling-v2-6",        "label": "Kling-V2.6"},
            {"apiId": "560", "model_key": "model_name", "model_val": "kling-video-o1",    "label": "Kling-O1（叙事/方言）"},
            {"apiId": "551", "model_key": "model_name", "model_val": "kling-v2-5-turbo",  "label": "Kling-V2.5-Turbo"},
        ],
        "image2video": [
            {"apiId": "566", "model_key": "model_name", "model_val": "Kling-V3",       "label": "Kling-V3（首尾帧）"},
            {"apiId": "564", "model_key": "model_name", "model_val": "kling-v2-6",     "label": "Kling-V2.6"},
            {"apiId": "561", "model_key": "model_name", "model_val": "kling-video-o1", "label": "Kling-O1"},
            {"apiId": "550", "model_key": "model_name", "model_val": "kling-v2-1",     "label": "Kling-V2.1"},
        ],
        "ref2video": [
            {"apiId": "552", "model_key": "model_name", "model_val": "kling-v1-6",     "label": "Kling-V1.6（多图参考）"},
            {"apiId": "562", "model_key": "model_name", "model_val": "kling-video-o1", "label": "Kling-O1（视频参考）"},
        ],
    },
    "paiwo": {
        "text2image": None,
        "text2video": [
            {"apiId": "401", "model_key": "model", "model_val": "v5.5", "label": "V5.5（音频/对口型）"},
            {"apiId": "400", "model_key": "model", "model_val": "v5",   "label": "V5"},
        ],
        "image2video": [
            {"apiId": "402", "model_key": "model", "model_val": "v5.5", "label": "V5.5（首尾帧）"},
            {"apiId": "501", "model_key": "model", "model_val": "v5",   "label": "V5（多图）"},
            {"apiId": "502", "model_key": "model", "model_val": "v5",   "label": "V5（单图 img_id）"},
        ],
        "ref2video": [
            {"apiId": "503", "model_key": "model", "model_val": "v5", "label": "V5（主体一致性）"},
        ],
    },
}

# ============================================================
# 阶段一：意图路由 (Router)
# ============================================================

ROUTER_SYSTEM_PROMPT = """你是灵境 AIGC 平台的前置意图路由节点。
将用户的自然语言输入解析为结构化 JSON，规则如下：

intent_type：
- IMAGE_GENERATION：含"画"、"图片"、"照片"、"海报"、"壁纸"、"产品图"等
- VIDEO_GENERATION：含"视频"、"动画"、"短片"、"运镜"、"推镜头"、"短剧"等
- UNKNOWN：无法归类

core_prompt：提炼用户意图为高质量创作提示词，剔除口语，补充主体/光影/视角细节。

base_params.aspect_ratio：横屏/电脑→16:9，竖屏/手机→9:16，头像/正方→1:1，封面→4:3，默认16:9
base_params.has_reference：用户提到参考图/上传图片为true
base_params.brand_preference：识别 Kling/Vidu/Doubao/Hailuo/Paiwo，否则null

video_features（仅VIDEO）：
- needs_audio：提到音频/配乐/方言/对口型为true
- camera_movement：提取运镜词，无则null
- duration：提取秒数，默认5

image_features（仅IMAGE）：
- task_num：提取数量，默认1
- high_quality_req：提到2K/4K/超高清为true

严格仅输出合法JSON，禁止任何Markdown标记或解释文字。"""

def run_router(app_key: str, user_input: str) -> dict:
    """阶段一：将自然语言解析为意图JSON"""
    print("\n🔍 阶段一：解析意图中...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {app_key}",
        "x-jdcloud-request-id": str(uuid.uuid4()),
    }
    # 注：此处使用灵境LLM能力，若无对话接口则使用本地规则解析
    # 以下为示例，实际需替换为灵境对话API端点
    router_result = _local_router_fallback(user_input)
    print(f"   意图类型: {router_result.get('intent_type')}")
    print(f"   核心Prompt: {router_result.get('core_prompt', '')[:60]}...")
    return router_result

def _local_router_fallback(user_input: str) -> dict:
    """本地规则兜底路由（当无LLM API时使用）"""
    text = user_input.lower()

    # 意图识别
    video_keywords = ["视频", "动画", "短片", "运镜", "推镜", "短剧", "mv", "宣传片", "广告片"]
    image_keywords = ["画", "图片", "照片", "海报", "壁纸", "产品图", "头像", "封面", "插图"]
    intent = "UNKNOWN"
    if any(k in text for k in video_keywords):
        intent = "VIDEO_GENERATION"
    elif any(k in text for k in image_keywords):
        intent = "IMAGE_GENERATION"

    # 画幅
    ar = "16:9"
    if any(k in text for k in ["竖屏", "手机", "竖版", "9:16"]):
        ar = "9:16"
    elif any(k in text for k in ["头像", "正方", "1:1"]):
        ar = "1:1"
    elif any(k in text for k in ["封面", "4:3"]):
        ar = "4:3"

    # 品牌
    brand = None
    brand_map = {"可灵": "Kling", "kling": "Kling", "vidu": "Vidu",
                 "豆包": "Doubao", "seedream": "Doubao", "海螺": "Hailuo",
                 "hailuo": "Hailuo", "拍我": "Paiwo"}
    for k, v in brand_map.items():
        if k in text:
            brand = v
            break

    # 音频
    needs_audio = any(k in text for k in ["音频", "配乐", "声音", "对口型", "方言", "台词", "配音"])

    # 时长
    import re
    dur_match = re.search(r'(\d+)\s*秒', user_input)
    duration = int(dur_match.group(1)) if dur_match else 5

    # 数量
    num_match = re.search(r'(\d+)\s*张', user_input)
    task_num = int(num_match.group(1)) if num_match else 1

    # 高分辨率
    high_q = any(k in text for k in ["2k", "4k", "8k", "超高清", "高分辨率"])

    # 参考图（简单判断：有URL或提到参考图）
    has_ref = any(k in text for k in ["参考图", "这张图", "图生", "http"])

    return {
        "intent_type": intent,
        "core_prompt": user_input,  # 本地模式直接透传，LLM模式会优化
        "base_params": {
            "aspect_ratio": ar,
            "has_reference": has_ref,
            "brand_preference": brand,
        },
        "video_features": {
            "needs_audio": needs_audio,
            "camera_movement": None,
            "duration": duration,
        },
        "image_features": {
            "task_num": min(task_num, 4),
            "high_quality_req": high_q,
        },
    }

# ============================================================
# 阶段二：模型推荐 (Choice)
# ============================================================

def run_choice(intent_json: dict) -> dict:
    """阶段二：根据意图JSON推荐最优模型"""
    print("\n🧠 阶段二：推荐最优模型...")

    intent = intent_json.get("intent_type")
    prompt = intent_json.get("core_prompt", "").lower()
    base = intent_json.get("base_params", {})
    vf = intent_json.get("video_features", {})
    imf = intent_json.get("image_features", {})

    has_ref = base.get("has_reference", False)
    needs_audio = vf.get("needs_audio", False)
    high_q = imf.get("high_quality_req", False)

    result = None

    if intent == "VIDEO_GENERATION":
        # V1: 极速/批量
        if any(k in prompt for k in ["快速", "批量", "预览", "便宜", "性价比"]):
            result = {"recommended_model": "海螺 Hailuo-2.3-Fast",
                      "reason": "用户强调速度或批量生成，Hailuo-2.3-Fast 生成效率最高。",
                      "api_id": "462", "brand": "hailuo", "_task": "text2video"}
        # V2: 复杂动作/物理
        elif any(k in prompt for k in ["打斗", "格斗", "武侠", "舞蹈", "运动", "激烈", "跑酷", "动作"]):
            result = {"recommended_model": "海螺 Hailuo-2.3",
                      "reason": "场景含复杂动作，海螺 Hailuo-2.3 动作稳定性和物理真实感最佳。",
                      "api_id": "460", "brand": "hailuo", "_task": "text2video"}
        # V3: 对口型/精细音效
        elif needs_audio and any(k in prompt for k in ["对口型", "台词", "说话", "演讲", "唱歌"]):
            result = {"recommended_model": "拍我 V5.5",
                      "reason": "明确需要对口型及精细音效，拍我 V5.5 音频同步能力最强。",
                      "api_id": "401", "brand": "paiwo", "_task": "text2video"}
        # V4: 方言/多语言/多镜头短剧
        elif needs_audio and any(k in prompt for k in ["方言", "四川", "粤语", "多角色", "短剧", "多镜头", "分镜"]):
            result = {"recommended_model": "可灵 Kling-O1",
                      "reason": "需要方言/多角色/多镜头叙事，可灵 O1 支持音色绑定与复杂叙事场景。",
                      "api_id": "560", "brand": "kling", "_task": "text2video"}
        # V5: IP/角色复刻/分镜
        elif any(k in prompt for k in ["ip", "角色复刻", "固定角色", "自动分镜", "系列"]):
            result = {"recommended_model": "豆包 Seedance-1.5-Pro",
                      "reason": "涉及 IP 角色复刻或自动分镜，Seedance 在角色一致性和分镜方面最优。",
                      "api_id": "750", "brand": "doubao", "_task": "text2video"}
        # V6: 参考图生视频（主体一致）
        elif has_ref and any(k in prompt for k in ["一致", "同一角色", "保持人物", "角色不变"]):
            result = {"recommended_model": "海螺 S2V-01",
                      "reason": "有参考图且需要主体一致性，S2V-01 专为主体一致性参考生视频设计。",
                      "api_id": "459", "brand": "hailuo", "_task": "ref2video"}
        # V7: 多镜头+音频
        elif needs_audio and any(k in prompt for k in ["多镜头", "叙事", "故事"]):
            result = {"recommended_model": "可灵 Kling-V3",
                      "reason": "需要多镜头叙事和音频，可灵 V3 在多镜头和音频方面综合表现最佳。",
                      "api_id": "565", "brand": "kling", "_task": "text2video"}
        # V8: 默认兜底
        else:
            result = {"recommended_model": "可灵 Kling-V3",
                      "reason": "无特殊场景需求，可灵 V3 综合能力均衡，适合通用视频生成。",
                      "api_id": "565", "brand": "kling", "_task": "text2video"}
        # 有参考图时切换到图生视频 apiId
        if has_ref and result["brand"] in ("kling", "hailuo", "doubao", "paiwo") and result.get("_task") == "text2video":
            _switch_to_image2video(result)

    elif intent == "IMAGE_GENERATION":
        # I1: 电商/参考图
        if any(k in prompt for k in ["产品", "商品", "电商", "白底", "展示"]) or has_ref:
            result = {"recommended_model": "豆包 Seedream-4.5",
                      "reason": "电商产品图或提供了参考图，Seedream 4.5 商业图像与垫图学习能力最强。",
                      "api_id": "701", "brand": "doubao", "_task": "text2image"}
        # I2: 极致真实感/文字渲染
        elif any(k in prompt for k in ["皮肤", "纹理", "光影细节", "超真实"]) or _has_text_in_image(prompt):
            result = {"recommended_model": "可灵 Kling-V2.1",
                      "reason": "需要极致写实细节或图内文字渲染，可灵 V2.1 写实与文字生成能力最佳。",
                      "api_id": "553", "brand": "kling", "_task": "text2image"}
        # I3: 人像
        elif any(k in prompt for k in ["人像", "面部", "写真", "肖像", "人物"]):
            result = {"recommended_model": "海螺 image-01",
                      "reason": "核心主体为人像，海螺 image-01 人像一致性和细节表现最佳。",
                      "api_id": "456", "brand": "hailuo", "_task": "text2image"}
        # I4: 高分辨率
        elif high_q:
            result = {"recommended_model": "可灵 Kling-V2.1",
                      "reason": "明确需要高分辨率直出，可灵 V2.1 支持 2K/4K 规格输出。",
                      "api_id": "553", "brand": "kling", "_task": "text2image"}
        # I5: 图生图（有参考图）
        elif has_ref:
            result = {"recommended_model": "可灵 Kling-V2（图生图）",
                      "reason": "有参考图且非人像场景，可灵 V2 图生图参考学习能力强。",
                      "api_id": "554", "brand": "kling", "_task": "image2image"}
        # I6: 默认兜底
        else:
            result = {"recommended_model": "豆包 Seedream-4.5",
                      "reason": "无特殊需求，Seedream 4.5 在质量与速度之间综合表现最均衡。",
                      "api_id": "701", "brand": "doubao", "_task": "text2image"}

    else:
        result = {"recommended_model": "无法推荐",
                  "reason": "无法识别用户意图，请更详细地描述您的需求。",
                  "api_id": None, "brand": None, "_task": None}

    print(f"   推荐模型: {result['recommended_model']}")
    print(f"   推荐理由: {result['reason']}")
    return result

def _switch_to_image2video(result: dict):
    """将文生视频的 apiId 切换为图生视频版本"""
    brand_switch = {"kling": "566", "hailuo": "461", "doubao": "751", "paiwo": "402"}
    brand = result.get("brand")
    if brand in brand_switch:
        result["api_id"] = brand_switch[brand]
        result["_task"] = "image2video"

def _has_text_in_image(prompt: str) -> bool:
    """检测提示词中是否包含需要在图片里渲染的文字"""
    import re
    return bool(re.search(r'[写写上|标题|写着|文字|字|SUMMER|LOGO|logo]', prompt)) or \
           bool(re.search(r"['\"「」【】].+['\"「」【】]", prompt))

# ============================================================
# 阶段三：API 调用 (Executor)
# ============================================================

def build_headers(app_key: str) -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {app_key}",
        "x-jdcloud-request-id": str(uuid.uuid4()),
    }

def build_params(brand: str, task: str, api_id: str, intent_json: dict,
                 extra: dict = None) -> dict:
    """根据品牌+任务+意图JSON构造 params"""
    base = intent_json.get("base_params", {})
    vf = intent_json.get("video_features", {})
    imf = intent_json.get("image_features", {})
    prompt = intent_json.get("core_prompt", "")

    # 找到对应模型配置
    versions = API_CONFIG.get(brand, {}).get(task, [])
    cfg = next((v for v in (versions or []) if v["apiId"] == api_id), None)
    if not cfg and versions:
        cfg = versions[0]

    params = {}
    if cfg:
        params[cfg["model_key"]] = cfg["model_val"]

    params["prompt"] = prompt

    if task in ("text2video", "image2video", "ref2video"):
        params["aspect_ratio"] = base.get("aspect_ratio", "16:9")
        dur = str(vf.get("duration", 5))

        if brand == "doubao":
            params["duration"] = dur
            params["mode"] = "1080p"
            params["generate_audio"] = vf.get("needs_audio", False)
            if task == "image2video" and extra and extra.get("image_url"):
                params["image_urls"] = [extra["image_url"]]

        elif brand == "hailuo":
            params["duration"] = int(dur)
            params["resolution"] = "768P" if int(dur) >= 10 else "1080P"
            if task == "image2video" and extra:
                if extra.get("first_frame"): params["first_frame_image"] = extra["first_frame"]
                if extra.get("last_frame") and api_id == "457":
                    params["last_frame_image"] = extra["last_frame"]
            if task == "ref2video" and extra and extra.get("ref_image"):
                params["subject_reference"] = {"image_url": extra["ref_image"]}

        elif brand == "kling":
            params["duration"] = dur
            params["mode"] = "pro"
            params["sound"] = "on" if vf.get("needs_audio") else "off"
            if api_id in ("565", "566"):
                params["multi_shot"] = "true"
                params["shot_type"] = "intelligence"
            if task == "image2video" and extra:
                if extra.get("first_frame"): params["image"] = extra["first_frame"]
                if extra.get("last_frame"):  params["image_tail"] = extra["last_frame"]
            if task == "ref2video" and extra:
                if extra.get("ref_images"):
                    params["image_references"] = [{"image_url": u} for u in extra["ref_images"]]

        elif brand == "paiwo":
            params["duration"] = int(dur)
            params["quality"] = "1080p"
            if cfg and cfg["model_val"] == "v5.5":
                params["generate_audio_switch"] = vf.get("needs_audio", False)
            if task == "image2video" and extra:
                if extra.get("first_frame"): params["first_frame_img"] = extra["first_frame"]
                if extra.get("last_frame"):  params["last_frame_img"] = extra["last_frame"]
            if task == "ref2video" and extra and extra.get("ref_images"):
                params["image_references"] = [{"image_url": u} for u in extra["ref_images"]]

    elif task in ("text2image", "image2image"):
        params["aspect_ratio"] = base.get("aspect_ratio", "16:9")
        if brand in ("doubao",):
            size_map = {"16:9": "2560x1440", "9:16": "1440x2560", "1:1": "2048x2048", "4:3": "2304x1728"}
            params["size"] = size_map.get(base.get("aspect_ratio", "16:9"), "2048x2048")
            del params["aspect_ratio"]
            params["taskNum"] = imf.get("task_num", 1)
        elif brand == "kling":
            params["taskNum"] = imf.get("task_num", 1)
            if task == "image2image" and extra and extra.get("ref_image"):
                params["image"] = extra["ref_image"]
        elif brand == "hailuo":
            pass  # aspect_ratio 已设置

    return params

def submit_task(app_key: str, api_id: str, params: dict) -> str:
    payload = {"apiId": api_id, "params": params}
    print(f"\n📤 阶段三：提交任务 (apiId={api_id})...")
    resp = requests.post(BASE_URL, json=payload, headers=build_headers(app_key), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise RuntimeError(f"提交失败: error={data.get('error')}, errorParamName={data.get('errorParamName')}")
    task_id = data.get("genTaskId")
    print(f"✅ 任务提交成功！genTaskId: {task_id}")
    return task_id

# ============================================================
# 辅助：收集额外参数（图片URL等）
# ============================================================

def collect_extra_params(task: str, brand: str) -> dict:
    extra = {}
    if task == "image2video":
        extra["first_frame"] = input("首帧图片公网 URL: ").strip()
        if brand in ("hailuo", "kling", "paiwo"):
            tail = input("尾帧图片 URL（可回车跳过）: ").strip()
            if tail: extra["last_frame"] = tail
    elif task == "ref2video":
        if brand == "kling" and input("使用视频参考？y/n（默认 n）: ").strip().lower() == "y":
            extra["ref_video"] = input("参考视频 URL: ").strip()
        refs = []
        while len(refs) < 4:
            url = input(f"参考图 URL #{len(refs)+1}（回车结束）: ").strip()
            if not url: break
            refs.append(url)
        extra["ref_images"] = refs
    elif task == "image2image":
        extra["ref_image"] = input("参考图片公网 URL: ").strip()
    return extra

# ============================================================
# 鉴权
# ============================================================

def get_app_key() -> str:
    key = os.environ.get("JOYCREATOR_APP_KEY", "").strip()
    if not key:
        print("\n" + "=" * 55)
        print("🔑 JoyCreator 鉴权")
        print("   提示：可设置环境变量 JOYCREATOR_APP_KEY 跳过此步")
        print("=" * 55)
        key = getpass.getpass("App Key（输入时不显示）: ").strip()
    if not key:
        raise ValueError("App Key 不能为空")
    return key

# ============================================================
# 智能交互模式（三阶段自动管线）
# ============================================================

def smart_mode(app_key: str):
    print("\n" + "=" * 55)
    print("🎨 灵境 JoyCreator 智能生成助手")
    print("   无需指定模型，描述您的需求即可自动匹配")
    print("=" * 55)
    user_input = input("\n请描述您想生成的内容（越详细越好）:\n> ").strip()
    if not user_input:
        print("❌ 输入不能为空")
        return

    # 阶段一：路由
    intent_json = run_router(app_key, user_input)
    intent = intent_json.get("intent_type")
    if intent == "UNKNOWN":
        print("⚠️  无法识别意图，请更详细地描述需求（如：画一张.../ 做一个...视频）")
        return

    # 若有品牌偏好，直接跳转
    brand_pref = intent_json.get("base_params", {}).get("brand_preference")
    if brand_pref:
        print(f"\n   检测到品牌偏好：{brand_pref}，跳过模型推荐阶段")
        choice = _brand_pref_to_config(brand_pref, intent_json)
    else:
        # 阶段二：推荐
        choice = run_choice(intent_json)
        if not choice.get("api_id"):
            print(f"⚠️  {choice['reason']}")
            return

    # 展示推荐并确认
    print(f"\n{'='*55}")
    print(f"🤖 推荐模型：{choice['recommended_model']}")
    print(f"   理由：{choice['reason']}")
    confirm = input("确认使用此模型？y/n（默认 y）: ").strip().lower()
    if confirm == "n":
        print("请手动指定模型后重新运行，或使用 --brand 参数")
        return

    # 收集图片URL（如需）
    task = choice.get("_task", "text2video" if intent == "VIDEO_GENERATION" else "text2image")
    extra = collect_extra_params(task, choice.get("brand", ""))

    # 阶段三：构造并提交
    params = build_params(choice["brand"], task, choice["api_id"], intent_json, extra)
    task_id = submit_task(app_key, choice["api_id"], params)

    print(f"\n{'='*55}")
    print(f"🎉 任务已提交！")
    print(f"   genTaskId : {task_id}")
    print(f"   推荐模型  : {choice['recommended_model']}")
    print(f"   请前往 JoyCreator 控制台查看结果")

def _brand_pref_to_config(brand_pref: str, intent_json: dict) -> dict:
    brand_map = {"Kling": "kling", "Doubao": "doubao", "Hailuo": "hailuo", "Paiwo": "paiwo"}
    brand = brand_map.get(brand_pref, "kling")
    intent = intent_json.get("intent_type")
    if intent == "VIDEO_GENERATION":
        has_ref = intent_json.get("base_params", {}).get("has_reference", False)
        task = "image2video" if has_ref else "text2video"
    else:
        task = "text2image"
    versions = API_CONFIG.get(brand, {}).get(task, []) or []
    cfg = versions[0] if versions else {}
    return {
        "recommended_model": cfg.get("label", brand),
        "reason": f"用户指定品牌 {brand_pref}，已选用该品牌推荐版本。",
        "api_id": cfg.get("apiId"),
        "brand": brand,
        "_task": task,
    }

# ============================================================
# 参数模式（直接指定品牌）
# ============================================================

def argparse_mode():
    parser = argparse.ArgumentParser(description="JoyCreator API 工具")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--brand", choices=["doubao","hailuo","kling","paiwo"])
    parser.add_argument("--task", choices=["text2image","text2video","image2video","ref2video","image2image"])
    parser.add_argument("--api-key")
    parser.add_argument("--duration", default="5")
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--image-url")
    args = parser.parse_args()

    app_key = args.api_key or os.environ.get("JOYCREATOR_APP_KEY","").strip()
    if not app_key:
        app_key = getpass.getpass("App Key: ").strip()

    # 构造简化意图JSON
    intent_json = {
        "intent_type": "VIDEO_GENERATION" if args.task and "video" in args.task else "IMAGE_GENERATION",
        "core_prompt": args.prompt,
        "base_params": {"aspect_ratio": args.aspect_ratio, "has_reference": bool(args.image_url), "brand_preference": None},
        "video_features": {"needs_audio": False, "camera_movement": None, "duration": int(args.duration)},
        "image_features": {"task_num": 1, "high_quality_req": False},
    }

    if args.brand and args.task:
        versions = API_CONFIG.get(args.brand, {}).get(args.task, []) or []
        cfg = versions[0] if versions else None
        if not cfg:
            print(f"❌ {args.brand} 不支持 {args.task}")
            sys.exit(1)
        extra = {"first_frame": args.image_url} if args.image_url else {}
        params = build_params(args.brand, args.task, cfg["apiId"], intent_json, extra)
        task_id = submit_task(app_key, cfg["apiId"], params)
    else:
        # 走智能推荐
        choice = run_choice(run_router(app_key, args.prompt))
        if not choice.get("api_id"):
            print(f"⚠️  {choice['reason']}")
            sys.exit(1)
        task = choice.get("_task", "text2video")
        extra = {"first_frame": args.image_url} if args.image_url else {}
        params = build_params(choice["brand"], task, choice["api_id"], intent_json, extra)
        task_id = submit_task(app_key, choice["api_id"], params)

    print(f"\n🎉 genTaskId: {task_id}")

# ============================================================
# 入口
# ============================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        argparse_mode()
    else:
        try:
            app_key = get_app_key()
            smart_mode(app_key)
        except KeyboardInterrupt:
            print("\n\n👋 已退出")
        except Exception as e:
            print(f"\n❌ 错误: {e}")
            sys.exit(1)
