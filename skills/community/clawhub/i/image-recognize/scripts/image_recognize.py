"""
image_recognize.py

根据用户提供的图片，可以是本地图片路径，也可以是网络图片URL，或者 base64编码的图片
对提供的图片进行识别，输出识别结果，并查找网上相似图片的列表，默认只输出3个

环境变量：
    BAIDU_API_KEY: 百度 API 认证密钥（必需）

输出：
    - 图片分类/意图识别
    - 猜词结果（动物、植物、品牌、汽车、美食等）
    - 图片描述和详细信息（来自 display_data 的 markdown 和 reference 组件）
    - 相似图片列表（从 rag_data.search_results 获取，可配置数量）
"""

import base64
import os
import argparse
import requests
from urllib.parse import urlparse
from typing import Tuple, Dict

# 猜词类型枚举
TYPE_SPOT = 1  # 景点猜词
TYPE_VERT_ANIMAL = 2  # 动物猜词
TYPE_VERT_PLANT = 3  # 植物猜词
TYPE_BRANDLOGO = 4  # 品牌猜词
TYPE_CUFENLEI_270 = 5  # 粗分类词
TYPE_IDL_CAR = 6  # 汽车猜词
TYPE_IDL_DISHES = 7  # 美食猜词
TYPE_IMGFACE = 8  # 名人
TYPE_PANO = 9  # 通用精准猜词
TYPE_PRODUCTS = 10  # 商品猜词
TYPE_SKINDISEASE = 11  # 皮肤病猜词
TYPE_VIS_GUESSWORD = 12  # vis猜词
TYPE_MLLM_GUESSWORD = 13  # MLLM大模型猜词

# 类型名称映射
TYPE_NAMES = {
    "TYPE_SPOT": "景点",
    "TYPE_VERT_ANIMAL": "动物",
    "TYPE_VERT_PLANT": "植物",
    "TYPE_BRANDLOGO": "品牌",
    "TYPE_CUFENLEI_270": "粗分类",
    "TYPE_IDL_CAR": "汽车",
    "TYPE_IDL_DISHES": "美食",
    "TYPE_IMGFACE": "名人",
    "TYPE_PANO": "通用精准",
    "TYPE_PRODUCTS": "商品",
    "TYPE_SKINDISEASE": "皮肤病",
    "TYPE_VIS_GUESSWORD": "VIS猜词",
    "TYPE_MLLM_GUESSWORD": "MLLM猜词"
}

# 意图识别代码映射
INTENTION_NAMES = {
    "question": "题目识别",
    "chars": "文字识别",
    "products": "商品识别",
    "imgface": "图片中人脸",
    "face": "人脸识别",
    "plant": "植物识别",
    "common": "通用识别",
    "animal": "动物识别",
    "products_chars": "商品+文字联合识别",
    "material_emoji": "表情素材识别",
    "material_sucai": "素材内容识别",
    "symbol": "水洗标识别",
    "translate": "翻译",
    "health_report": "健康报告解析",
    "toy": "玩具识别",
    "red_wine": "红酒识别",
    "travel": "旅游/景点识别"
}

QIANFAN_BASE_URL = "https://qianfan.baidubce.com"

def _normalize_image(value: str) -> str:
    """
    将图片参数统一转为 base64 编码格式：
      - 本地文件路径 → 读文件并编码为 base64
      - data URI（data:image/...;base64,xxx）→ 去除头部前缀，保留裸 base64
      - http/https URL → 下载图片并编码为 base64
      - 裸 base64 → 原样返回
    """
    if not value:
        return value

    # 处理 data URI 格式
    if value.startswith("data:"):
        _, _, encoded = value.partition(",")
        return encoded.strip()

    # 处理网络 URL
    if value.startswith(("http://", "https://")):
        try:
            response = requests.get(value, timeout=30)
            response.raise_for_status()
            return base64.b64encode(response.content).decode()
        except requests.RequestException as e:
            raise Exception(f"下载网络图片失败: {e}")

    # 处理本地文件路径
    if os.path.exists(value):
        with open(value, "rb") as f:
            return base64.b64encode(f.read()).decode()
    else:
        raise FileNotFoundError(f"图片文件不存在: {value}")


def recognize_image(image_b64: str, api_key: str) -> dict:
    """
    调用图片识别 API
    Args:
        image_b64: base64 编码的图片
        api_key: 百度 API Key
    Returns:
        API 返回结果
    """
    api_url = QIANFAN_BASE_URL + "/v2/tools/image_general"
    api_url, headers = resolve_sandbox_url(api_url, api_key)


    payload = {
        "image_b64": image_b64
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        if result.get("code") != "0":
            raise Exception(f"图片识别失败，错误码: {result.get('code')}, 错误信息: {result.get('message', '未知错误')}")

        return result
    except requests.RequestException as e:
        raise Exception(f"API 请求失败: {e}")


def parse_guesswords(guesswords: list) -> dict:
    """
    解析猜词结果
    返回最高置信度的猜词及其详细信息
    """
    if not guesswords:
        return None

    # 按置信度排序，取最高的
    sorted_guesses = sorted(guesswords, key=lambda x: x.get("confidence", 0), reverse=True)

    top_guess = sorted_guesses[0]

    type_str = top_guess.get("type", "")

    confidence = "1(高执行度)"
    confidenceValue = top_guess.get("confidence", 0)
    if confidenceValue == 1:
        confidence = "1(高)"
    elif confidenceValue == 2:
        confidence = "2(中)"
    elif confidenceValue == 3:
        confidence = "3(低)"
    result = {
        "word": top_guess.get("word", ""),
        "type_code": type_str,
        "type_name": TYPE_NAMES.get(type_str, type_str),
        "confidence": confidence,
        "image_url": top_guess.get("image_url", ""),
        "extend_brief": top_guess.get("extend_brief", {}),
        "all_guesses": sorted_guesses
    }

    return result


def format_guessword_details(guessword: dict) -> str:
    """
    格式化猜词的详细信息
    从 extend_brief 中提取 abstract 和 reference
    """
    output_parts = []

    # 提取 word 和类型信息
    word = guessword.get("word", "")
    type_name = guessword.get("type_name", "")
    confidence = guessword.get("confidence", 0)

    if word:
        output_parts.append(f"## 识别结果: {word}")
    if type_name:
        output_parts.append(f"**类型**: {type_name}")
    if confidence:
        output_parts.append(f"**置信度**: {confidence}\n")

    # 检查是否有图片URL
    if guessword.get("image_url"):
        output_parts.append(f"**参考图片**: {guessword['image_url']}\n")

    # 从 all_guesses 中提取第一个猜词的 extend_brief
    extend_brief = guessword.get("extend_brief", {})

    # 提取 animal_abstract
    if "animal_abstract" in extend_brief:
        animal_abs = extend_brief["animal_abstract"].get("abstract", "")
        if animal_abs:
            output_parts.append(f"### 简要描述\n{animal_abs}\n")
    # 提取 plant_abstract
    if "plant_abstract" in extend_brief:
        plant_abs = extend_brief["plant_abstract"].get("abstract", "")
        if plant_abs:
            output_parts.append(f"### 简要描述\n{plant_abs}\n")

    # 提取 product_abstract
    if "product_abstract" in extend_brief:
        product_abs = extend_brief["product_abstract"].get("abstract", "")
        if product_abs:
            output_parts.append(f"### 简要描述\n{product_abs}\n")
    # 提取 imgface_abstract
    if "imgface_abstract" in extend_brief:
        imgface_abs = extend_brief["imgface_abstract"].get("abstract", "")
        if imgface_abs:
            output_parts.append(f"### 简要描述\n{imgface_abs}\n")
    # 提取 car_abstract
    if "car_abstract" in extend_brief:
        car_abs = extend_brief["car_abstract"].get("abstract", "")
        if car_abs:
            output_parts.append(f"### 简要描述\n{car_abs}\n")
    # 提取 health_skindisease_abstract
    if "health_skindisease_abstract" in extend_brief:
        health_skindisease_abs = extend_brief["health_skindisease_abstract"].get("abstract", "")
        if health_skindisease_abs:
            output_parts.append(f"### 简要描述\n{health_skindisease_abs}\n")

    # 提取 mllm_abstract
    if "mllm_abstract" in extend_brief:
        mllm_abs = extend_brief["mllm_abstract"]
        components = mllm_abs.get("component", [])

        for component in components:
            component_name = component.get("component_name")
            component_data = component.get("data", "")

            if component_name == "first_abstract":
                output_parts.append(f"### 识别摘要\n{component_data}\n")
            elif component_name == "other_abstract":
                output_parts.append(f"### 详细信息\n{component_data}\n")
            elif component_name == "reference":
                # 解析参考资源
                import json
                try:
                    ref_data = json.loads(component_data)
                    titles = ref_data.get("title", [])
                    fromurls = ref_data.get("fromurl", [])
                    if titles:
                        output_parts.append("### 参考资源\n")
                        for i, (title, url) in enumerate(zip(titles, fromurls), 1):
                            output_parts.append(f"{i}. [{title}]({url})")
                except json.JSONDecodeError:
                    pass
    return "\n".join(output_parts) if output_parts else None


def extract_similar_images(data: dict, limit: int = 3) -> list:
    """
    提取相似图片列表
    优先从 rag_data.search_results 获取
    """
    similar_images = []

    # 优先从 rag_data.search_results 获取
    search_results = data.get("rag_data", {}).get("search_results", [])
    for result in search_results[:limit]:
        thumb_url = result.get("thumburl")
        if thumb_url:
            similar_images.append({
                "url": thumb_url,
                "title": result.get("title", ""),
                "content": result.get("content", ""),
                "objurl": result.get("objurl", "")
            })

    return similar_images


def resolve_sandbox_url(original_url: str, api_key: str) -> Tuple[str, Dict[str, str]]:
    """若当前在沙盒环境中，将目标 URL 替换为代理 URL，并返回需要附加的 headers。"""
    # session_id = os.environ.get("DUMATE_SESSION_ID")
    # scheduler_url = os.environ.get("DUMATE_SCHEDULER_URL")

    # headers = {
    #     "Content-Type": "application/json",
    # }
    # if not session_id or not scheduler_url:
        # 优先使用传入的 api_key，否则从环境变量读取
    api_key = api_key or os.environ.get("BAIDU_API_KEY")
    if not api_key:
        raise ValueError("未设置 API Key，请通过环境变量 BAIDU_API_KEY 设置或使用")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-Appbuilder-From": "openclaw",
    }
    return original_url, headers
    #
    # parsed = urlparse(original_url)
    # proxy_url = f"{scheduler_url}/api/qianfanproxy{parsed.path}"
    # if parsed.query:
    #     proxy_url += f"?{parsed.query}"
    #
    # headers.update({
    #     "Host": parsed.netloc,
    #     "X-Dumate-Session-Id": session_id,
    #     "X-Appbuilder-From": "desktop",
    # })
    # return proxy_url, headers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="图片识别并查找网上相似图片")
    parser.add_argument("--image", required=True, help="图片路径、URL 或 base64 编码")
    parser.add_argument("--api-key", default=os.environ.get("BAIDU_API_KEY"),
                        help="百度 API Key（或设置环境变量 BAIDU_API_KEY）")
    parser.add_argument("--similar_count", type=int, default=3, help="返回相似图片数量，默认 3")
    args = parser.parse_args()

    image = args.image

    # 将图片统一转换为 base64
    normalized_image = _normalize_image(image)

    # 调用识别 API
    result = recognize_image(normalized_image, args.api_key)
    # 检测是否命中风控，如果命中风控，直接输出提示信息
    risk_check = result.get("data", {}).get("query_context", {}).get("intervened", [])
    if risk_check:
        print("# 图片识别结果:")
        print("⚠️ 命中风控，无法继续识别")

    # 输出识别结果
    print("# 图片识别结果:\n")
    # 提取猜词结果
    guesswords = result.get("data", {}).get("query_context", {}).get("guesswords", [])
    if guesswords:
        parsed_guess = parse_guesswords(guesswords)
        if parsed_guess:
            guess_details = format_guessword_details(parsed_guess)
            if guess_details:
                print(guess_details)

                # 显示其他候选猜词
                all_guesses = parsed_guess.get("all_guesses", [])
                if len(all_guesses) > 1:
                    print("\n**其他候选识别结果:**")
                    for i, guess in enumerate(all_guesses[1:], 2):
                        guess_word = guess.get("word", "")
                        type_code = guess.get("type", "")
                        guess_type = TYPE_NAMES.get(type_code, type_code)
                        print(f"{i-1}. {guess_word} ({guess_type})")

    # 提取图片意图/分类
    post_intentions = result.get("data", {}).get("query_context", {}).get("post_intention", [])
    if post_intentions:
        print("\n" + "-"*60)
        print("图片意图识别")
        print("-"*60)
        # 使用映射转换意图代码为中文描述
        intention_list = []
        for item in post_intentions:
            intention_code = item.get("intention", "")
            intention_name = INTENTION_NAMES.get(intention_code, intention_code)
            intention_list.append(intention_name)
        print(f"意图: {', '.join(intention_list)}")

    # 提取并显示相似图片
    similar_images = extract_similar_images(result.get("data", {}), args.similar_count)
    if similar_images:
        print("\n" + "-"*60)
        print(f"相似图片 (共 {len(similar_images)} 张):")
        print("-"*60)
        for i, img in enumerate(similar_images, 1):
            print(f"\n{i}. {img['url']}")
            if img.get('title'):
                print(f"   标题: {img['title']}")
            if img.get('content'):
                print(f"   内容: {img['content']}")
            if img.get('objurl'):
                print(f"   URL: {img['objurl']}")
    else:
        print("\n未找到相似图片")
