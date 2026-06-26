# 🚀 NexSolve AI Skill for OpenClaw

**连接传统行业痛点与 AI 极客的实战桥梁** **Bridging Real-World Pain Points with AI-Native Solutions**

---

## ⚡ 项目概述 / Overview

**NexSolve AI** 是一个去中心化的“需求广场”。
本插件将广场数据接入 **OpenClaw (龙虾)**。它不直接运行复杂的算法，而是作为**高效率的数据连接器**，配合 AI Agent 的推理能力实现提单、搜单、析单的自动化闭环。

---

## ✨ 核心功能 / Key Features

- **🚀 双语提单 (Bilingual Submit)**：口述痛点，工具自动调用接口按中英文标准模板在 GitHub 提交 Issue。
- **🔍 实时广场 (Marketplace List)**：实时抓取广场最新的待解决任务，为开发者提供实战素材。
- **🧠 辅助智能分析 (AI Analysis Support)**：提供 Issue 详情，**利用 AI 助手的逻辑推理**评估技术难度与工时。
- **📞 隐私安全提取 (Safety Extraction)**：配合 AI 指令，从公开描述中识别联系信息，并提供安全风险提示。

---

## 🛠️ 安装指南 / Installation (安全推荐)

### 1. 编译项目

```
npm install
npm run build
```

### 2. 获取 GitHub Token (推荐细粒度授权)

为了您的账户安全，建议仅授权本项目所需的最小权限：

1. 访问 [GitHub Fine-grained Tokens](https://www.google.com/search?q=https://github.com/settings/personal-access-tokens/new)。
2. **Repository access**: 选择 **"Only select repositories"**，并搜索选中 `zxz0119/NexSolve-AI`。
3. **Permissions**: 点击 **"Repository permissions"**，将 **Issues** 设置为 **Read and Write**。
4. 生成并复制以 `github_pat_` 开头的 Token。

### 3. 配置环境变量

在 OpenClaw 设置中填入生成的 `GITHUB_TOKEN`。

------

## 🤖 AI 助手运行准则 / Agent Instructions

- **确认后提交**：仅在识别到明确业务痛点且**经过用户确认**后，才发起 `submit_pain_point`。
- **专业分析**：调用 `get_need_detail` 后，应结合 Agent 自身知识储备提供技术架构建议及难度分级。
- **隐私提醒**：从 Issue 中提取联系方式时，必须包含“请务必在站外交易时保护个人隐私”的安全提示。

------

## ⚖️ 开源协议 & 免责声明 / License & Disclaimer

- **License**: [AGPL-3.0](https://www.google.com/search?q=./LICENSE)
- **安全提醒**: 开发者应独立评估任务风险，本项目仅作为信息撮合平台，不参与任何交易保障。

------

### 🌟 支持我们

如果这个项目帮到了你，请给 [NexSolve AI 主仓库](https://github.com/zxz0119/NexSolve-AI) 点个 Star！
