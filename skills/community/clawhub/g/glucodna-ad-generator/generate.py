#!/usr/bin/env python3
"""
GlucoDNA Ad Generator — OpenClaw Skill
Usage: python3 generate.py [--output path.png]
"""
import google.genai as genai
from google.genai import types
import os, sys, json, requests

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.abspath(os.path.join(SKILL_DIR, "..", ".."))

# Try reading Gemini key from TOOLS.md
GEMINI_API_KEY = None
tools_path = os.path.join(WORKSPACE, "TOOLS.md")
if os.path.exists(tools_path):
    with open(tools_path) as f:
        for line in f:
            if "Gemini API" in line and "AIza" in line:
                import re
                m = re.search(r'(AIza\w+)', line)
                if m:
                    GEMINI_API_KEY = m.group(1)
                    break

GEMINI_API_KEY = GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ 需要设置 Gemini API Key（放到 TOOLS.md 或环境变量 GEMINI_API_KEY）")
    sys.exit(1)

# Product image
PRODUCT_IMG_URL = "https://hk3.com.my/wp-content/uploads/2024/04/PRODUCT-SIZE-500PX-07.png"

PROMPT = """
请生成一张中文健康保健品广告图。

产品: GlucoDNA 基因护肾（肾脏保健）

设计要求：
- 1024×1024 正方形
- 深青绿色 + 金色点缀，高端医疗感
- 完美渲染中文文字
- 产品图需要嵌入图中
- 不要出现「专治」「治疗」

图上文字：
[顶部] "夜尿多、尿有泡、腰酸背痛？" "肾脏在求救！"
[中间] "GlucoDNA 基因护肾" "KPMF8 → 激活SIRT1肾脏基因"
[见证] "✅ 夜尿从3-4次降到0-1次" "✅ 尿泡明显减少" "✅ 肾脏指数好转"
[价格] "RM190/盒 ｜ 买2盒以上享回扣" "📦 COD全马免邮"
[底部] "016-7656000 Ms Lai（营养师）"
"""

def main():
    client = genai.Client(api_key=GEMINI_API_KEY)

    print("📥 下载产品图...")
    r = requests.get(PRODUCT_IMG_URL)
    if r.status_code != 200:
        print(f"❌ 下载失败: {r.status_code}")
        sys.exit(1)
    img_bytes = r.content

    print("🎨 生成广告图（约30秒）...")
    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[
            types.Part.from_bytes(data=img_bytes, mime_type="image/png"),
            PROMPT
        ],
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_modalities=["image"],
        )
    )

    out = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/Desktop/GlucoDNA_广告图.png")
    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("image/"):
            with open(out, "wb") as f:
                f.write(part.inline_data.data)
            print(f"✅ 已保存: {out} ({len(part.inline_data.data)/1024:.0f}KB)")
            return
    print("❌ 没生成图片")
    if response.text:
        print(response.text[:300])

if __name__ == "__main__":
    main()
