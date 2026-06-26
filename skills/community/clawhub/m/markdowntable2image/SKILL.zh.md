---
name: Table2Image
version: 1.1.0
description: 将 Markdown 表格和 JSON 数据转换为 PNG 图片。完美适用于 Discord、Telegram 等 Markdown 表格渲染不佳的平台。当 Claude 需要以视觉吸引人的格式展示表格数据、发送表格到 Discord/Telegram/WhatsApp，或用户要求将表格转换为图片时使用。支持多种主题（discord-light、discord-dark、finance、minimal）、条件格式和自动 Markdown 表格检测。
install: |
  npm install
  npx playwright install chromium
engines:
  node: ">=18.0.0"
---

# Table2Image

> **🇨🇳 中文** | [🇬🇧 English](SKILL.md)

将表格转换为适用于聊天平台的精美 PNG 图片。

**GitHub:** https://github.com/UMRzcz-831/table-to-image-skill

**技术栈：** Playwright + Chromium，实现完美的 Emoji 和字体渲染。

## 前置要求

- **Node.js**: >= 18.0.0
- **网络**: 首次运行需要联网（Chromium 下载约 100MB）

## 安装

```bash
# 安装依赖
npm install

# 下载 Chromium（一次性，约 100MB）
npx playwright install chromium
```

## 性能

| 指标 | 时间 |
|------|------|
| 首次运行（下载 Chromium） | ~30-60秒（一次性） |
| 浏览器启动（首次渲染） | ~2-3秒 |
| 后续渲染 | **< 500毫秒**（浏览器复用） |

> 💡 **提示：** 首次渲染后浏览器实例会自动复用，使后续表格生成几乎瞬间完成。

## 快速开始

### 方法 1：CLI（简单表格）

```bash
# 将 JSON 数据转换为表格图片
echo '[{"name":"Alice","score":95}]' | node scripts/table-cli.mjs --dark --output table.png

# 或使用 JSON 文件
node scripts/table-cli.mjs --data-file data.json --theme discord-dark --output table.png
```

### 方法 2：程序化 API（推荐）

```typescript
import { renderTable, renderDiscordTable } from './scripts/index.js';

// 快速生成 Discord 表格
const image = await renderDiscordTable(
  [{ name: 'AAPL', change: '+2.5%' }],
  [
    { key: 'name', header: '股票' },
    { key: 'change', header: '涨跌', align: 'right' }
  ],
  '📊 行情监控'
);

// 发送到 Discord
await message.send({ attachment: image.buffer });
```

### 方法 3：自动转换 Markdown 表格

```typescript
import { autoConvertMarkdownTable } from './scripts/index.js';

// 自动检测并转换
const result = await autoConvertMarkdownTable(message, 'discord');
if (result.converted) {
  await message.send({ attachment: result.image });
}
```

## 使用场景

- **Discord/Telegram/WhatsApp**：这些平台对 Markdown 表格渲染不佳
- **金融数据**：股票价格、投资组合报告，支持条件格式
- **排行榜**：带奖牌和颜色编码的排名
- **对比表格**：并排功能对比
- **任何表格数据**：当视觉展示很重要时

## 主题

| 主题 | 适用场景 | 预览 |
|------|----------|------|
| `discord-light` | Discord 浅色模式（默认） | ![discord-light](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-discord-light.png) |
| `discord-dark` | Discord 深色模式 | ![discord-dark](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-discord-dark.png) |
| `finance` | 财务报告 | ![finance](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-finance.png) |
| `minimal` | 简洁/简单 | ![minimal](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-minimal.png) |
| `sweet-pink` | 甜酷粉暗色风格 | ![sweet-pink](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-sweet-pink.png) |
| `deep-sea` | 深海蓝经典配色 | ![deep-sea](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-deep-sea.png) |
| `wisteria` | 藤紫复古撞色 | ![wisteria](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-wisteria.png) |
| `pond-blue` | 捣蓝清新配色 | ![pond-blue](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-pond-blue.png) |
| `camellia` | 茶花红暖色调 | ![camellia](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/theme-camellia.png) |

### 自定义主题

你也可以直接向 `theme` 传入**自定义主题对象**。为了方便，只需提供两个颜色 —— `primary`（主色）和 `secondary`（副色）—— 程序会自动生成完整的主题样式：

```typescript
const image = await renderTable({
  data: [{ name: 'Alice', score: 95 }],
  columns: [
    { key: 'name', header: '姓名' },
    { key: 'score', header: '分数', align: 'right' }
  ],
  theme: {
    primary: '#e6397c',    // 强调色（表头、文字、边框）
    secondary: '#1a1a1d'   // 底色（背景、行）
  }
});
```

![custom-primary-secondary](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/custom-primary-secondary.png)

或者传入包含全部 7 个颜色的完整主题对象：

```typescript
const image = await renderTable({
  data: [{ name: 'Alice', score: 95 }],
  columns: [...],
  theme: {
    background: '#1a1a1d',
    headerBg: '#e6397c',
    headerText: '#1a1a1d',
    rowBg: '#1a1a1d',
    rowAltBg: '#2a2a2d',
    text: '#e6397c',
    border: '#e6397c'
  }
});
```

![custom-full](https://raw.githubusercontent.com/UMRzcz-831/table-to-image-skill/refs/heads/main/assets/custom-full.png)

## 高级用法

### 条件格式

```typescript
import { renderTable } from './scripts/index.js';

const image = await renderTable({
  data: stocks,
  columns: [
    { key: 'symbol', header: '代码' },
    { 
      key: 'change', 
      header: '涨跌',
      align: 'right',
      formatter: (v) => `${v > 0 ? '+' : ''}${v}%`,
      style: (v) => ({ color: v > 0 ? '#43b581' : '#f04747' })
    }
  ],
  theme: 'discord-dark'
});
```

### 自定义列宽

```typescript
columns: [
  { key: 'name', header: '名称', width: 150 },
  { key: 'description', header: '描述', width: 300, wrap: true, maxLines: 3 }
]
```

## 脚本

- `scripts/table-cli.mjs` - 命令行界面
- `scripts/index.js` - 程序化 API

参见 `references/api.md` 获取完整 API 文档。

## 示例

参见 `references/examples.md` 获取常见用例和代码示例。
