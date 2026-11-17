---
name: offer-assistant
slug: offer-assistant
description: >
  简历全流程助手：传一份旧简历拆解为永久素材库，后续任意 JD 一键匹配生成定制简历 + 干净 PDF + 模拟面试。不是每次重写，是从素材库中挑最优组合投递岗位。
version: 1.0.2
topics:
  - 简历
  - 面试
  - 求职
  - career
  - resume
  - interview
  - job-search
  - chinese
metadata:
  openclaw:
    requires:
      bins:
        - node
        - google-chrome-stable
        - tesseract
      packages:
        - tesseract-ocr-chi-sim
    envVars:
      - name: TESSERACT_LANG
        required: false
        description: Tesseract language parameter (default "chi_sim+eng")
      - name: CHROME_PATH
        required: false
        description: Chrome/Chromium executable path (e.g. /opt/google/chrome/chrome)
    emoji: "📄"
    homepage: ""
    install:
      - kind: node
        package: ws
        bins: []
---

# Offer 助手 | Career Assistant

## 一句话

**上传一次旧简历 → 永久素材库。后续任何 JD，一键匹配出简历 + 模拟面试。**

不是每次重写。是从你的真实经历中，按 JD 挑最优组合。

---

## 🗃️ 一次上传，终身素材库

用户只需做一次：上传一份旧简历。

- AI 自动拆解为结构化素材库（教育背景 / 工作经历 / 项目经历 / 技能）
- 按模块独立存储，永久留存
- **后续所有操作都基于这个库** — 不需要重复填写

**和竞品的核心区别**：不是每次求职都要重新写一遍。一次投入，后续所有岗位复用。

---

## 🔍 JD 深度分析 → 匹配度一目了然

无论你发来截图、链接还是文字，自动分析输出：

- 公司背景检索（联网查询）
- 3 层拆解：**硬性要求 / 加分项 / 隐性要求**
- 与素材库的匹配度评估
- 是否建议投递

---

## 📄 智能匹配生成简历

**不是 AI 编造。是从素材库中按 JD 挑选最优组合。**

- 从素材库中按匹配度排序挑选最合适的项目和经历
- 按 JD 核心诉求降序排列
- 输出定制 HTML + 干净 PDF（CDP 生成，无页眉页脚）

---

## 🎤 模拟面试，提前踩坑

基于你的**真实**简历内容和 JD 出题：

- 专挑数据真实性和逻辑漏洞追问
- 面试后自动复盘 + 输出改进项
- 面试记录自动归档到岗位分析手册

---

## 📊 全流程追踪

- 投了哪些公司、面到哪轮、结果如何 — **一问就能查到**
- 所有面试复盘自动归档

---

## 使用流程（用户视角）

1. **首次**：发一份旧简历 → 自动建素材库
2. **每次求职**：发 JD → 自动分析并生成定制简历
3. **面试前**：说「模拟面试」→ 自动出题
4. **面试后**：说「复盘」→ 自动记录

## 能力边界

- ✅ 分析 JD 并生成匹配报告
- ✅ 基于素材库生成定制简历 PDF
- ✅ 模拟面试 + 复盘
- ✅ 记录投递历史和面试日志
- ❌ 代替用户投递简历
- ❌ 编造不存在的项目经历
- ❌ 保证面试通过
- ❌ 主动定时提醒

---

## 目录结构

```
resume-delivery/
├── SKILL.md                              # 主文件
├── config/
│   └── guide.md                          # Agent 运行规则
├── references/
│   ├── resume-parsing.md                 # ① 简历拆解 → 素材库
│   ├── jd-methodology.md                 # ② 岗位分析 & JD 匹配
│   ├── resume-methodology.md             # ③ 简历生成方法论
│   ├── mock-interview.md                 # ④ 模拟面试方法论
│   ├── tracking.md                       # ⑤ 投递记录 & 面试复盘
│   └── pdf-generation.md                 # PDF 生成方法论
└── scripts/
    ├── generate-pdf.js                   # PDF 生成脚本
    ├── workflow.js                       # 工作流跟踪 CLI
    ├── setup.sh                          # 一键依赖检查与安装
    ├── set_chrome_path.sh                # 指定 Chrome 路径
    ├── create-material-doc.sh            # 创建素材库文档
    ├── analyze-jd.sh                     # JD 分析 + 公司调研
    └── record-interview.sh               # 面试记录
```

## Quick Start

### 安装依赖

```bash
cd ~/.openclaw/workspace/skills/offer-assistant
bash scripts/setup.sh

# 如 Chrome 不在默认路径
export CHROME_PATH=/opt/google/chrome/chrome
```

### 生成 PDF

```bash
node scripts/generate-pdf.js ./resume.html ./resume.pdf
```

### 第三方依赖

| 软件 | 用途 | 安装方式 |
|------|------|---------|
| **google-chrome-stable** | PDF 生成（CDP） | `apt install google-chrome-stable` / `brew install --cask google-chrome` |
| **tesseract** | OCR 截图识图 | `apt install tesseract-ocr` / `brew install tesseract` |
| **tesseract-ocr-chi-sim** | 中文 OCR 语言包 | `apt install tesseract-ocr-chi-sim` |
| **Node.js** | 运行脚本 | Node >= 16 |
| **ws (npm)** | CDP WebSocket 连接 | `npm install ws`（ClawHub 自动处理） |

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CHROME_PATH` | 自动查找 | Chrome/Chromium 路径 |
| `TESSERACT_LANG` | `chi_sim+eng` | OCR 语言参数 |

## License

MIT-0 — free to use, modify, and redistribute.