---
name: pet-emotion
version: 1.0.0
description: "🐱🐶 AI宠物情绪识别技能。上传猫狗照片，自动识别宠物情绪（快乐/悲伤/愤怒/恐惧/放松/警觉6种），生成可视化HTML报告含情绪雷达图和AI解读。基于DashScope多模态大模型。Triggers: 拍照识别宠物情绪, 宠物情绪, 宠物表情, 猫咪心情, 狗狗情绪, 猫狗情绪, 宠物表情识别, 看看我家猫, 看看我家狗, 帮我看看宠物, pet emotion, pet mood."
author: bettermen
tags: [pet, emotion-recognition, dashscope, multimodal, cat, dog]
agent_created: true
allowed-tools: Read, Write, Bash, WebFetch
metadata:
  openclaw:
    requires:
      bins:
        - python.exe
      env:
        - DASHSCOPE_API_KEY
    emoji: "🐱"
    homepage: https://github.com/bettermen/pet-emotion
---

# 🐱🐶 宠物情绪识别 Pet Emotion

> AI驱动的宠物情绪识别技能 | 拍照即得 | 6种情绪分类 | 可视化报告

## 概述

上传猫或狗的照片，AI自动分析宠物情绪。支持6种情绪分类（快乐/悲伤/愤怒/恐惧/放松/警觉），生成包含情绪雷达图、置信度评分和AI解读的HTML可视化报告。

### 触发场景

- 用户说"看看我家猫/狗的情绪"、"宠物情绪识别"、"拍照识别宠物情绪"
- 用户提供宠物照片路径，想知道宠物状态
- 用户分享宠物照片想了解情绪

### 核心功能

| 功能 | 说明 |
|------|------|
| 📸 拍照识别 | 上传照片，自动识别猫狗情绪 |
| 🎯 6情绪分类 | 快乐/悲伤/愤怒/恐惧/放松/警觉 |
| 📊 可视化报告 | Chart.js雷达图+置信度条+emoji表情 |
| 💬 AI解读 | 自然语言情绪解读和互动建议 |
| 🐱🐶 双物种 | 同时支持猫和狗 |

---

## 执行流程

### Step 1: 接收图片

用户提供图片路径或URL。如果用户没有提供路径，询问用户上传或拖拽图片。

### Step 2: 检查环境与 API Key

首次使用前需配置 DashScope API Key：

```bash
# 检查 API Key 是否已配置
/c/Users/PC/.workbuddy/binaries/python/versions/3.13.12/python.exe -c "
from pet_emotion import find_api_key
key = find_api_key()
print('API Key:', '已配置' if key and key != 'YOUR_DASHSCOPE_API_KEY_HERE' else '未配置')
"
```

**如果未配置，两种方式设置：**

方式一（推荐）：编辑配置文件
```bash
# 编辑 C:/Users/PC/.workbuddy/config/dashscope.json
# 将 YOUR_DASHSCOPE_API_KEY_HERE 替换为实际的 API Key
```

方式二：设置环境变量
```bash
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxx"
```

**获取 API Key：** https://dashscope.console.aliyun.com/apiKey

### Step 3: 运行情绪识别

使用技能内置脚本 `scripts/pet_emotion.py`：

```bash
/c/Users/PC/.workbuddy/binaries/python/versions/3.13.12/python.exe \
  /c/Users/PC/.workbuddy/skills/pet-emotion/scripts/pet_emotion.py \
  --image "<用户提供的图片路径>" \
  --output "/c/Users/PC/WorkBuddy/2026-06-13-22-22-46/pet_emotion_report.html"
```

**参数说明：**
| 参数 | 说明 |
|------|------|
| `--image PATH` | 宠物照片路径（必填） |
| `--output PATH` | HTML报告输出路径（可选，默认当前目录） |
| `--api ENDPOINT` | API类型，默认 dashscope（也支持 openai） |

### Step 4: 展示结果

脚本执行完成后：
1. 在对话中展示识别结果摘要（情绪+置信度+解读）
2. 使用 `preview_url` 预览HTML报告
3. 使用 `deliver_attachments` 交付报告文件

---

## API 配置

脚本自动从以下位置读取 DashScope API Key（按优先级）：

1. 环境变量 `DASHSCOPE_API_KEY`
2. 环境变量 `OPENAI_API_KEY`（兼容模式）
3. 配置文件 `~/.workbuddy/config/dashscope.json`

**DashScope API 端点：**
```
POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
Model: qwen-vl-max (推荐) 或 qwen-vl-plus
```

---

## 情绪分类参考

| 情绪 | Emoji | 典型特征 |
|------|-------|---------|
| 快乐 😊 | 放松姿势、尾巴摇摆、耳朵自然、眼神柔和 |
| 悲伤 😢 | 耷拉耳朵、蜷缩、无精打采、回避眼神 |
| 愤怒 😠 | 龇牙、竖毛、身体僵硬、耳朵后压 |
| 恐惧 😨 | 夹尾、躲藏、瞳孔放大、身体低伏 |
| 放松 😌 | 眯眼、打盹、肚皮朝上、耳朵自然 |
| 警觉 🧐 | 竖耳、凝视、身体紧绷、尾巴直立 |

---

## 独立使用（直接调用 API）

不运行脚本时，可直接用以下代码调用 DashScope API 进行情绪识别：

```python
import base64, json, os, requests

def analyze_pet_emotion(image_path):
    """直接调用 DashScope 分析宠物情绪"""
    api_key = os.environ.get("DASHSCOPE_API_KEY", "")
    if not api_key:
        # 尝试读取配置文件
        config_path = os.path.expanduser("~/.workbuddy/config/dashscope.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                api_key = json.load(f).get("api_key", "")
    
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png", ".webp": "webp"}
    mime = mime_map.get(ext, "jpeg")
    
    payload = {
        "model": "qwen-vl-max",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/{mime};base64,{img_b64}"}},
                {"type": "text", "text": """请分析这张宠物（猫或狗）照片中的情绪状态。
返回JSON格式：
{"species": "cat或dog或unknown", "emotion": "快乐/悲伤/愤怒/恐惧/放松/警觉", "confidence": 0.0-1.0, "reason": "判断依据简短说明", "suggestion": "给主人的互动建议"}
如果图片中没有猫或狗，species返回unknown。只返回JSON，不要其他内容。"""}
            ]
        }],
        "temperature": 0.1
    }
    
    resp = requests.post(
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload, timeout=30
    )
    return resp.json()
```

---

## 文件结构

```
pet-emotion/
├── SKILL.md                    # 本文件
├── scripts/
│   └── pet_emotion.py          # 主脚本：图片→API→报告
├── assets/
│   └── report_template.html    # HTML报告模板
└── references/
    └── emotion_guide.md        # 情绪解读知识库
```
