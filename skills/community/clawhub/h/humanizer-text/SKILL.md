---
name: humanizer
version: 2.1.1
description: |
  Remove signs of AI-generated writing from text. Detects and fixes: inflated symbolism,
  promotional language, superficial -ing analyses, vague attributions, em dash overuse,
  rule of three, AI vocabulary words, negative parallelisms, excessive conjunctive phrases.
  Makes AI text sound natural and human-written.
---

# Humanizer — 去除AI写作痕迹

## 功能概述

将 AI 生成的文本改写成自然、人类书写风格的文本。检测并修复以下常见 AI 写作特征：

## AI 写作痕迹清单

| 痕迹类型 | 识别特征 | 修复方向 |
|---|---|---|
| 夸张修辞 | 过度使用"无与伦比""史诗级"等 | 降低调性，客观陈述 |
| 推销语言 | 频繁出现"难以置信""绝对推荐" | 改为中性推荐语气 |
| 浅层-ing 分析 | "通过XXX，我们可以看到…" | 直接陈述观点 |
| 模糊归因 | "研究表明""专家说"无具体来源 | 补充具体来源或删除 |
| 破折号滥用 | 连续使用"——" | 改用逗号或句号 |
| 三重规则 | 习惯性三连排比 | 改为单点或两点论述 |
| AI 词汇 | "首先/其次/最后"固定搭配 | 自然过渡词 |
| 负面排比 | "既不…也不…"过度使用 | 直接表达 |
| 连接词堆砌 | "然而/但是/因此/并且"连用 | 简化句子结构 |

## 使用方式

直接发送需要改写的 AI 生成文本，输出改写后的自然版本。

## 参考文档
- `README.md` — 详细的 AI 痕迹分类与修复示例
