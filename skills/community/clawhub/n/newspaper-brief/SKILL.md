---
name: newspaper-brief
description: Create mobile-first newspaper-style brief images from raw content or existing summaries. Use when the user says `报纸模式`, `做成报纸图`, `按报纸样式输出`, asks for a 报纸图/简报图/报纸样式总结, or wants notes/chats/articles rendered as a newspaper-style HTML/PNG long image. Supports two flows: (1) raw article/chat/link/notes -> extract and structure key points -> render, (2) existing summary/bullets -> render directly.
---

# Newspaper Brief

把整理结果从“聊天流”切成“版面流”，先产出适合手机阅读的报纸风长图。

## 默认工作方式

优先使用这套流程：

1. 读用户给的原始材料（文章、聊天记录、链接摘要、会议纪要）
2. 先整理成结构化要点
3. 再渲染成报纸风长图

如果用户已经给了现成摘要/要点，也可以直接跳到第 3 步。

## 触发词

以下中文说法都应直接进入本技能：

- `报纸模式`
- `做成报纸图`
- `按报纸样式输出`

也兼容这些自然说法：

- `整理成简报图`
- `做成报纸样式`
- `用报纸风输出`
- `给我一张报纸风长图`

## v1 范围

- 仅做 *手机版长图*
- 先输出 **HTML**，再截图为 **PNG**
- 默认风格：黑白报纸 + 轻米色纸张背景 + 少量强调线
- 适合 Telegram 直接查看，不追求打印排版

## 数据准备

优先整理成下面这种结构，再交给脚本：

```json
{
  "paper_name": "紫音简报",
  "issue": "2026-03-07",
  "title": "AI 输出界面值得重做",
  "subtitle": "把聊天流改造成版面流，比单纯堆更长回答更有效",
  "summary": "一句导语，放在标题下方。",
  "highlights": [
    "先给 3-5 条 TL;DR",
    "正文使用 2-4 个版块分栏",
    "手机端版式必须优先保证可读性"
  ],
  "quote": "AI 时代，真正该重做的可能不是模型，而是输出界面。",
  "sections": [
    {
      "heading": "核心判断",
      "body": "这里放正文段落。支持多段文本。"
    },
    {
      "heading": "产品建议",
      "bullets": ["建议一", "建议二", "建议三"]
    }
  ],
  "footer_note": "来源：群聊讨论｜整理：紫音"
}
```

### 原始材料模式

当用户只给原文/聊天记录时，先由代理自己完成提炼：

- 先写标题
- 再写一句导语
- 提炼 3-5 条 highlights
- 拆成 2-4 个 sections
- 最后补一句 footer

### 标题规则（v1.1）

- 标题最多两行
- 不允许用 `...` / `……` 省略截断
- 默认优先 **重写成更短、更像报纸标题的表达**
- 只有在仍然接近边界时，才轻微缩小字号

不要把未经整理的大段原文直接硬塞进模板，除非用户明确要求“原汁原味”。

## 脚本

### 1) 生成 HTML

```bash
python skills/newspaper-brief/scripts/render_newspaper.py \
  --input skills/newspaper-brief/examples/ai-interface-sample.json \
  --html output/newspaper-brief/demo.html \
  --normalized output/newspaper-brief/demo.normalized.json
```

### 2) 可选：顺手导出 PNG（本地浏览器兜底）

```bash
python skills/newspaper-brief/scripts/render_newspaper.py \
  --input skills/newspaper-brief/examples/ai-interface-sample.json \
  --html output/newspaper-brief/demo.html \
  --png output/newspaper-brief/demo.png
```

脚本会尝试寻找本机 Edge/Chrome 进行 headless screenshot，并在导出后自动裁掉底部多余空白。若 PNG 失败，HTML 仍然可用。

## 推荐截图方式

### 首选：OpenClaw browser 工具

当 browser 工具可用时：

1. 打开生成后的本地 HTML
2. 使用全页截图
3. 导出 PNG

优点：比纯命令行截图更稳，尤其是长图。

### 兜底：脚本内置浏览器截图

适合快速 smoke test，但超长页面可能截断。遇到特别长的内容时：

- 缩短单张图内容
- 或后续扩展为分页输出

## 版面建议

v1 保持固定结构：

- 报头（刊名 / 期号 / 日期）
- 大标题
- 导语
- 左侧主内容区
- 右侧速览栏（highlights + quote）
- 页脚（来源 / 整理说明）

## 质量检查

完成前至少检查：

- 标题是否够像“报纸标题”，不要像聊天句子
- highlights 是否是短句，不要过长
- section 数量是否控制在 2-4 个
- 正文是否有明显层次
- 手机上是否一眼能看到重点

## 样例

直接参考：

- `skills/newspaper-brief/examples/ai-interface-sample.json`

先用样例跑通，再替换成真实内容。