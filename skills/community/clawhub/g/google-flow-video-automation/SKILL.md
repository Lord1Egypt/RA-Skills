---
name: google-flow-video-automation
description: Automatically generate AI videos on Google Flow (labs.google/fx/tools/flow) via Chrome CDP. Supports 16:9 aspect ratio, 10s duration, auto-download MP4.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
        - node
        - google-chrome
    emoji: "🎬"
---

# Google Flow 视频自动化 Skill

## 🚀 快速使用流程

### 首次使用（一次性设置）

**1. 启动 Chrome（CDP 远程调试）**
```bash
pkill -9 "Google Chrome"
sleep 2
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default" \
  "https://labs.google/fx/tools/flow" &
sleep 5
```

**2. 手动登录 Google 账号**
- 在打开的 Chrome 窗口中登录你的 Google 账号
- 登录后保持 Chrome 窗口打开（Cookie 会保持登录状态）

**3. 探索可用选项（保存配置）**
```bash
cd ~/.workbuddy/skills/google-flow-automation
node explore-options.js
```

**4. 生成第一条视频**
```bash
node generate-one.js --prompt "Video of a joyful horse..." --output ./videos
```

---

### 日常使用（非首次）

```bash
# 1. 检查 Chrome 是否已启动
cd ~/.workbuddy/skills/google-flow-automation
node check-chrome.js

# 2. 如果没启动，运行：
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/Library/Application Support/Google/Chrome/Default" &

# 3. 生成视频（一次一条）
node generate-one.js --prompt "你的提示词" --output ./videos
```

---

## ⚠️ 关键要求

### 1. 提示词必须以 "Video of" 开头！

**原因：** Google Flow AI 解析提示词时，如果开头不是视频关键词，会默认生成**图片**（JPG）而非**视频**（MP4）。

✅ **正确：** `Video of a joyful horse magically stepping out...`  
❌ **错误：** `A joyful horse magically stepping out...`（会生成图片）

**脚本会自动处理：** 如果提示词不是以视频关键词开头，`generate-one.js` 会自动添加 `"Video of "` 前缀。

### 2. 一次只生成一条视频

避免浪费积分（Omni Flash 模型：15 credits/条）

---

## 🎨 提示词模板

```
Video of [主体] + [动作：从屏幕走出] + [目标：到用户手里] + [风格/光照]
```

### 示例（直接可用）

| 中文意图 | 英文提示词 |
|---------|------------|
| 快乐的马从屏幕走出 | `Video of a joyful horse magically stepping out of a glowing screen into the viewer's hands, warm cinematic lighting` |
| 快乐的狗从屏幕走出 | `Video of a happy golden dog leaping out of a bright screen into the viewer's open hands, playful and magical` |
| 快乐的龙从屏幕走出 | `Video of a friendly dragon crawling out of a mystical screen into the user's hands, fantasy style, glowing particles` |
| 快乐的兔子从屏幕走出 | `Video of a cute bunny hopping out of a colorful screen into the viewer's palms, cheerful and vibrant` |

**💡 技巧：**
- 用 `"magically stepping out"` 或 `"leaping out"` 描述"从屏幕走出"
- 用 `"into the viewer's hands"` 描述"到用户手里"
- 加 `"cinematic lighting"` 提升画面质量
- 保持 **50 词以内**

---

## 📁 文件结构

```
~/.workbuddy/skills/google-flow-automation/
├── SKILL.md                   # 本文档
├── QUICKSTART.md              # 5分钟快速入门
├── explore-options.js         # 探索可用选项（首次使用）
├── generate-one.js            # 生成单条视频（日常使用）★
├── check-chrome.js           # 检查 Chrome CDP 状态
├── config.json                # 用户配置（自动生成）
├── available-options.json     # 可用选项（探索后生成）
└── examples/
    └── prompts-example.txt   # 提示词示例
```

---

## 🔧 配置说明

### `available-options.json`（探索后自动生成）

```json
{
  "videoGeneration": {
    "models": [
      {"name": "Omni Flash", "credits": 15},
      {"name": "Omni Pro", "credits": 30}
    ],
    "aspectRatios": ["16:9", "9:16"],
    "durations": ["1x", "x2", "x3", "x4"]
  }
}
```

### 推荐参数配置

- **模型：** Omni Flash（15 credits，性价比高）
- **比例：** 16:9（横屏）
- **时长：** x2（10秒）

---

## 🚨 常见问题

### Chrome 启动失败？
```bash
# 检查 9222 端口是否监听
curl -s http://127.0.0.1:9222/json/version

# 如果没反应，重新启动 Chrome
```

### 积分不足？
- Omni Flash：15 credits/条
- Omni Pro：30 credits/条
- 检查账号剩余积分（Google Flow 网页右上角）

### 视频下载失败？
脚本会自动等待，但如果超时：
1. 在 Chrome 里找到生成的视频
2. 右键 → "Save video as..."
3. 选择保存位置

---

## 📝 更新日志

### v3.0（当前版本 - 精简高效版）
- ✅ 精简文档，移除冗余说明
- ✅ 突出关键要求（"Video of" 开头）
- ✅ 优化提示词模板
- ✅ 增强 `generate-one.js` 自动添加视频关键词前缀

### v2.0
- ✅ 改为一次只生成一条（避免浪费积分）
- ✅ 新增首次使用完整引导
- ✅ 新增 `explore-options.js` 和 `generate-one.js`

---

**🎬 快速开始：直接运行 `node generate-one.js --prompt "Video of ..." --output ./videos`**
