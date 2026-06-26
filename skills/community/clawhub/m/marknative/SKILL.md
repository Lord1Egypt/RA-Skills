---
name: marknative
description: Render Markdown into paginated PNG/SVG without a browser using marknative.
allowed-tools:
  - Bash
  - Read
  - Write
---

# marknative

把 Markdown 渲成分页 PNG / SVG，不走浏览器。

## 适用场景

- Markdown 转图片
- 批量导出文章、笔记、文档
- 服务端渲染，不想依赖 Chromium

## 先决条件

```bash
npm ls marknative skia-canvas
```

如果没装：

```bash
npm install marknative
```

## 最小示例

```ts
import { renderMarkdown } from 'marknative'
import { writeFile } from 'node:fs/promises'

const markdown = `
# Hello, marknative

- item 1
- item 2
`

const pages = await renderMarkdown(markdown, { format: 'png' })

for (const [i, page] of pages.entries()) {
  await writeFile(`page-${i + 1}.png`, page.data)
}
```

## 常见参数

- `format: 'png' | 'svg'`
- `painter`：自定义绘制器，一般先不用

## 调试顺序

1. 先跑最小示例
2. 确认能输出 1 页
3. 再加表格、引用、代码块
4. 有排版问题就先看字体、换行和内容长度

## 注意点

- 这是一个 ESM / TypeScript 友好的库
- 直接 import 源码时，要注意运行器是否支持 TS/ESM
- 没有 Bun 的环境里，用 `tsx` 或兼容 Node TS 的方式更稳
- `skia-canvas` 是绘制后端，安装失败先看系统架构和 Node 版本
