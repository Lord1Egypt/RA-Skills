# 📚 AI 伴学助手 (Homework Companion)

一个面向 K12 孩子的**引导式**作业辅导智能体 Skill。内置腾讯云 OCR / ASR / TTS 能力，把"陪孩子写作业"这件让无数家长头疼的事，变成可复用、有方法、有沉淀的 AI 伴学流程。

> 核心理念：**不替孩子写作业，而是教他如何思考。** 用苏格拉底式提问引导孩子一步步想通，而非直接抛答案。

---

## 能力一览

- 📷 **题目识别**：拍照 / 截图 → 腾讯云 OCR 高精度识别题目（含公式、表格、手写体）
- 🎙️ **语音口述**：孩子口述题目 → 腾讯云 ASR 转写
- 💡 **引导式讲解**：分步骤提问引导，定位卡点，给提示而非答案，适配小学到高中
- 🔊 **语音讲解**：讲解转儿童友好语气音频（腾讯云 TTS），低龄孩子可听可回放
- 📒 **错题本**：自动生成可累积 Excel 错题本，按知识点筛选复习
- 📊 **家长报告**：日常小结 + 周报 + 月报，给家长可执行的辅导建议
- 🛡️ **内容安全**：全程儿童内容安全规范兜底，绝不代写、绝不输出不适宜内容

---

## 前置依赖

本 skill 已将 OCR / ASR / TTS 三个能力**内置**为 `scripts/` 下的 Python 脚本，**只需安装本 skill 一个即可**，无需再装三个独立 skill。

| 依赖 | 作用 | 安装 |
|:---|:---|:---|
| Python 3.8+ | 运行内置脚本 | 一般已自带 |
| `tencentcloud-sdk-python` | 调用腾讯云 OCR/ASR/TTS | `pip install -r scripts/requirements.txt` |
| 腾讯云密钥 | API 调用凭证 | 环境变量 `TENCENTCLOUD_SECRET_ID` / `TENCENTCLOUD_SECRET_KEY` |

```bash
# 首次使用，安装腾讯云 SDK（只需一次）
pip install -r scripts/requirements.txt

# 配置密钥
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
```

---

## 在 WorkBuddy / OpenClaw 中安装

```bash
# 方式一：从 ClawHub 安装（发布后可用）
npx clawhub@latest install homework-companion

# 方式二：本地使用（开发 / 测试）
# 把本目录复制到智能体的 skills 目录：
#   WorkBuddy:  <工作区>/.workbuddy/skills/homework-companion/
#   OpenClaw:   ~/.openclaw/skills/homework-companion/
```

---

## 使用方式

装好后在对话里直接说就行，例如：

- "帮孩子讲一下这道数学题（附图）"
- "这是一道分数应用题，孩子卡住了，引导他做"
- "把今天做错的题整理成错题本"
- "生成这周的学习报告给家长"

---

## 目录结构

```
homework-companion/
├── SKILL.md                      # 技能主体（触发条件、工作流、原则）
├── README.md                     # 本文件
├── scripts/                      # 内置腾讯云 OCR/ASR/TTS 调用脚本
│   ├── requirements.txt          # 依赖：tencentcloud-sdk-python
│   ├── ocr.py                    # 题目识别（印刷体 / 手写体）
│   ├── asr.py                    # 语音口述转写
│   └── tts.py                    # 文本转儿童友好语音
└── references/
    ├── subject-playbooks.md      # 各学科 / 学段引导式讲解方法 + 语音风格
    ├── safety-rules.md           # 儿童内容安全规范（强制）
    ├── wrong-question-notebook.md# 错题本字段定义 + Excel 生成模板
    └── parent-report.md          # 家长报告模板
```

---

## 适用场景

- 家长辅导作业"一看就上火" → 交给 AI 冷静引导
- 双职工家庭，晚上没空陪读 → AI 先陪，家长看报告
- 孩子错题散落各处 → 自动沉淀成可复习错题库
- 异地家长想了解学习情况 → 周报同步

---

## 设计原则

1. **引导 > 告知**：提问激活思考，答案消灭思考。
2. **安全 > 效率**：任何输出必须符合儿童内容安全规范。
3. **沉淀 > 一次性**：错题本与家长报告让辅导可累积、可追踪。
4. **适配 > 通用**：小学用比喻，初高中讲逻辑，分学段对待。
