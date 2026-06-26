---
title: "{{title}}"
date: {{date}}
platform: {{platform}}
author: "{{author}}"
original_url: {{originalUrl}}
captured_at: {{fetchedAt}}
has_video: {{hasVideo}}
has_transcript: {{hasTranscript}}
has_image_analysis: {{hasImageAnalysis}}
---

# {{title}}

> 来源：{{platformDisplayName}} @{{author}} | {{date}}

## 深度总结

（AI 根据内容生成的深度总结：核心观点、关键信息、背景脉络、价值点。
如有图片分析，综合原文和图片内容一起分析总结。
如有视频转写，综合原文和转写文本一起分析总结。）

## 原文内容

{{text}}

{{#if hasTranscript}}
## 视频转写

> 📎 字幕文件：[transcript.srt](attachments/{{date}}-{{slug}}/transcript.srt)

{{transcriptFullText}}
{{/if}}

## 图片

{{#each images}}
![图片](attachments/{{date}}-{{slug}}/{{this.localFilename}})

> **图片内容：** {{this.analysisText}}

{{/each}}

(If an image was not downloaded, fall back to the remote URL.)
(If image analysis failed, use: > **图片内容：** ⚠️ 图片分析失败)
(If image is purely decorative: > **图片内容：** 装饰性图片，无额外信息内容。)

## 元信息

- 转发: {{stats.reposts}} | 评论: {{stats.comments}} | 点赞: {{stats.likes}}
