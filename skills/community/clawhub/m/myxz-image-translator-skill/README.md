# 🎨 妙言小智 (PicTech.cc) 专业图片翻译 Skill

**—— 小龙虾(OpenClaw)生态中为跨境电商而生的生产级 AI 图像翻译SKILL**



## 🌟 为什么选择妙言小智图片翻译？

在跨境电商领域（亚马逊、Shopify、Shopee、Lazada、TikTok Shop、美客多等），图片素材的本地化质量直接影响转化率。传统的翻译工具往往会破坏原图美感，或需要频繁手动操作。

本 Skill 是由 **[妙言小智 (PicTech.cc)](https://www.pictech.cc)** 官方出品的专业级[图片翻译](https://www.pictech.cc)OpenClaw生态的解决方案。它不仅是一个图片翻译的SKILL，更是一个懂业务、有记忆、能批量处理的“AI 翻译官”。

### 核心优势：
*   **保持原图布局**：采用先进的 OCR 与图像修补技术，翻译后文字完美嵌入原图位置，不影响排版美感。
*   **极致用户体验**：
    *   **图片直连预览**：任务完成后，AI 会直接在对话框渲染翻译后的预览图，无需手动打开文件夹。
    *   **持久化记忆**：首创 VK (API Key) 记忆功能，输入一次，永久记住，下次使用无需重复输入。
*   **专为批量而生**：支持单个图片 URL、本地路径，甚至一整套产品文件夹的递归处理。
*   **极速缓存优化**：内置 SQLite 数据库，相同素材重复翻译不消耗 API 额度。

---

## 🛠️ 安装指南

本 [图片翻译Skill](https://www.pictech.cc) 适用于 **OpenClaw**、**WorkBuddy**、**Claude Code** 等支持标准 Agent Skills 的环境。

1.  **克隆仓库**：
    ```bash
    git clone https://github.com/your-username/myxz-translate-skill.git
    cd myxz-translate-skill
    ```

2.  **安装依赖**：
    ```bash
    npm install
    ```

3.  **准备环境**：
    确保你的电脑已安装 **Node.js v20+**。

---

## 🚀 快速上手 (Prompt 示例)

你可以直接对你的 AI 助手说以下话：

### 1. 激活并翻译（首次使用）
```
> "这是我的妙言小智 VK 密钥：`sp332e083xxxxxxxx`，请用妙言小智的图片翻译skill帮我把桌面上的中文图片 `listing_main.jpg` 翻译成英文。"
```

### 2. 批量处理电商素材包
```
> "请用妙言小智的图片翻译skill翻译这个文件夹里的所有产品图：`E:/Amazon/New_Product_A`。源语言是中文，翻译成英文。"
```

### 3. 直接翻译网络图片
```
> "请用妙言小智的图片翻译skill 翻译这张主图：https://example.com/item_01.jpg，中文翻译成英文"
```

### 4. 翻译多张网络图片
```
> "请用妙言小智的图片翻译skill翻译这几张主图：https://example.com/item_01.jpg,https://example.com/item_02.jpg,https://example.com/item_03.jpg中文翻译成英文"
```

---

## 📋 功能参数说明

| 参数 | 必填 | 说明 |
| :--- | :--- | :--- |
| `input` | 是 | 支持：单个文件路径、图片URL、或包含多张图片的文件夹 |
| `sourceLanguage` | 是 | 限制：`中文`、`繁体中文`、`英文`、`日文` |
| `targetLanguage` | 是 | 支持：全球 20+ 主流电商语种 (英、中、日、韩、泰、德、法、俄等) |
| `vk` | 首次 | 妙言小智 API Key。一旦成功运行，系统会自动记忆。 |
| `saveDir` | 否 | 翻译结果存放路径，默认在用户目录下的 `myxz-result` |

---

## 📦 开发者协议 (For AI Agent)

*   **入口点**：`node cli.js`
*   **交互协议**：通过标准 JSON 字符串进行参数传递与结果接收。
*   **自检机制**：脚本会自动检查 `.vk_config`。若缺失且用户未提供，将返回 `NEED_VK` 状态码，此时请提示用户输入密钥。

---

## 🔐 源码说明与隐私

*   **核心逻辑**：本 Skill 的核心翻译逻辑 (`index.js`) 经过混淆处理，旨在保护 PicTech 核心接口。
*   **隐私安全**：所有的 VK 密钥及翻译记录均保存在用户本地磁盘，不会上传至任何第三方服务器（除翻译请求必经的 PicTech 官方接口外）。

---

## 📬 关于妙言小智 (PicTech)

妙言小智致力于通过 AI 技术赋能跨境电商卖家，提供最高质量的图片、文案本地化方案。

*   **[妙言小智官方网站](https://pictech.cc)**: [https://pictech.cc](https://pictech.cc)
*   **支持反馈**: 若遇到技术问题，请提交 Issue 或通过官网联系客服。

---

**立即开始，让你的产品素材走向全球！** 🌍

---
