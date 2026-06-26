# 图片提示词生成器

基于「五层拆解法」的 AI 图像提示词生成工具，将模糊的创意想法转化为结构严谨、可执行的图像生成提示词。

## 安装

```bash
clawhub install image-prompt-generator
```

或手动安装：将整个文件夹复制到 `~/.openclaw/skills/image-prompt-generator/`。

## 功能特性

- **五层拆解法**：画面介绍 → 整体基调 → 质感材质 → 笔触细节 → 构图规则，系统化拆解创意需求
- **6 种风格预设**：童趣涂鸦、极简现代、复古胶片、日系插画、赛博朋克、学术信息图，一键切换
- **多工具输出**：支持同时生成 Midjourney、DALL-E、Stable Diffusion 及通用中文格式的提示词
- **Markdown 渲染**：生成结果以结构化排版呈现，支持一键复制

## 项目结构

```
image-prompt-generator/
├── SKILL.md       # 技能说明（ClawHub 必需）
├── claw.json      # ClawHub 清单文件
├── README.md      # 项目文档
└── app/
    ├── App.jsx    # 主应用组件（UI + 业务逻辑）
    └── config.js  # API 配置（Gateway 端点、模型参数）
```

## 配置说明

API 相关配置集中在 `app/config.js` 中：

```js
const API_CONFIG = {
  baseURL: "http://127.0.0.1:18789/v1/chat/completions",  // OpenClaw Gateway 端点
  model: "openclaw",                                        // 使用 OpenClaw 配置的模型
  maxTokens: 4096,                                           // 最大输出 token 数
};
```

默认通过 OpenClaw Gateway 调用模型，无需手动配置 API 密钥。Gateway 会自动路由到你在 `openclaw.json` 中配置的模型。

## 使用方式

1. 选择一个**风格预设**（可选），或直接在输入框描述想要的图片内容
2. 选择**目标生成工具**（全部 / Midjourney / DALL-E / Stable Diffusion）
3. 点击「生成提示词」，等待 AI 返回结构化的提示词规格书
4. 点击「复制全文」将结果复制到剪贴板，粘贴到对应的 AI 绘图工具中使用

## 前置条件

- OpenClaw 已安装并运行
- Gateway 已启用 chat completions 端点：
  ```json5
  { gateway: { http: { endpoints: { chatCompletions: { enabled: true } } } } }
  ```

## 技术栈

- React（JSX）
- OpenClaw Gateway（OpenAI-compatible API）
