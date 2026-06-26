---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3046022100a3d8183ddf0d0db1ba9846eee5764c57cb679d3767cf83777c8d2e8713a3b88b022100ac09929b3886c34c2be9c8378391e30dbf34f4e95ba8bbeda1821f18c53aec23
    ReservedCode2: 3045022100dc8c6fcb3a3a234c9b91c572561e8453f1040a098be4a5104c8b1147920b2f2a0220528d8ca3d0f2db47cd33f1e24ce3e273ad5259f4e167fdf1cef2b75866478b56
description: |-
    将网页内容转换为 Markdown 格式。
    当需要获取网页内容并转换为可读 Markdown 时使用此 Skill。
    优先级：markdown.new > defuddle.md > r.jina.ai > Scrapling
name: markdown-fetcher
---

# Markdown Fetcher

将网页内容转换为 Markdown 格式的 Skill。

## 使用场景

- 需要抓取网页内容进行阅读或分析
- 将网页文章转为 Markdown 进行整理
- 提取网页数据

## 转换优先级

按以下顺序尝试，直到成功：

1. **首选**：`https://markdown.new/{原URL}`
   - 适用于 Cloudflare 托管的网站
   - 示例：`https://markdown.new/https://www.nature.com/nathumbehav/`

2. **备选1**：`https://defuddle.md/{原URL}`
   - 如果 markdown.new 不支持
   - 示例：`https://defuddle.md/https://www.nature.com/nathumbehav/`

3. **备选2**：`https://r.jina.ai/{原URL}`
   - 通用网页抓取服务
   - 示例：`https://r.jina.ai/https://www.nature.com/nathumbehav/`

4. **备选3**：Scrapling
   - 如果以上都不行，使用 GitHub 上的 Scrapling 工具
   - 仓库：https://github.com/D4Vinci/Scrapling
   - 安装：`pip install scrapling`
   - 使用：`scrapling -u "URL"`

## 最佳实践

1. 先尝试 `markdown.new/`
2. 如果失败，尝试 `r.jina.ai/`（最稳定）
3. 仅在其他方法都失败时考虑 Scrapling

## 示例

```
原始URL: https://www.nature.com/articles/s41586-026-01234-x

尝试顺序:
1. https://markdown.new/https://www.nature.com/articles/s41586-026-01234-x
2. https://r.jina.ai/https://www.nature.com/articles/s41586-026-01234-x
```
