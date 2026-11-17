# kaka-cardcrafter 🃏

让 WorkBuddy / OpenClaw 等 AI Agent 直接生成**小红书爆款图文、公众号封面、知识卡片**的技能，走卡咔开放平台（远程 MCP 或 REST API）。

## 能力

- **小红书爆款图文**：大纲 → 确认 → 多页配图（3~15 页，3:4），支持整稿改大纲、单页重生
- **多规格封面**：一次出公众号横版 2.35:1、3:4、9:16 等平台规格
- **知识卡片**：一段文字 → 自动润色 → 多页卡片
- 出图异步轮询、部分失败自动提示单页重做；能量计费与卡咔网页端同价，失败自动退款

## 安装（三选一）

**① WorkBuddy 技能市场**：技能面板搜索「卡咔」或 `kaka-cardcrafter` → 一键安装。

**② ClawHub CLI**：

```bash
clawhub install kaka-cardcrafter
```

**③ WorkBuddy 通过 URL 导入**：技能管理 → 添加技能 → 通过 URL 导入 → 填本仓库地址。

也可下载本仓库 zip 后在 WorkBuddy「技能管理 → 上传技能」本地导入。

## 配置

安装后设置环境变量 `KAKA_API_KEY`（`kc-` 开头）：

1. 打开 **https://card.bingotech2022.com** 并登录卡咔账号
2. 进入「API 接入」页面 → 点「生成 API Key」（明文只显示一次）
3. `export KAKA_API_KEY=kc-你复制的key`

可选 `KAKA_BASE_URL`（默认 `https://api.cardcrafter.cn`）。

> 也可以不装本技能、直接在 WorkBuddy 里连卡咔远程 MCP（12 个工具）：
> 插件 → MCP 服务器 → 配置 MCP，端点 `https://api.cardcrafter.cn/mcp`。
> 图文教程：https://www.cardcrafter.cn/platforms/workbuddy

## 使用示例

- 「帮我写一篇三伏天养生茶的小红书图文，6 页」
- 「给这篇公众号文章配一张横版封面，标题《……》」
- 「把这段笔记做成 9:16 的知识卡片」

## 链接

- WorkBuddy 接入教程：https://www.cardcrafter.cn/platforms/workbuddy
- 豆包工作接入教程：https://www.cardcrafter.cn/platforms/doubao
- 完整开放平台 API 文档（skill 版）：https://api.cardcrafter.cn/openapi/skill.md
