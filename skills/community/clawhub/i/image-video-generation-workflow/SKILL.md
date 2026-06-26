---
name: Image Video Generation Workflow
slug: image-video-generation-workflow
version: 2.0.0
description: 基于 ComfyUI / MCP image server / 浏览器审看回路的图片与视频生成工作流技能卡，纳入 YouTube、Bilibili、Flickr 与 GitHub 的 source pack
homepage: https://github.com/jau123/MeiGen-AI-Design-MCP
source: synthesized-from-knowledge-base
capability: 浏览器与执行
---

## When to Use
用户要快速搭一条本地可操作的图片/视频生成工作流，需要把生成引擎、浏览器审看、灵感素材收集和可复用提示词整理成一条稳定回路时使用。

## What It Does
给出一条更接近当前 OpenClaw 采集现实的最小落地路径：
1. 用本地生成引擎产出第一轮图片或视频结果
2. 用浏览器统一审看生成结果
3. 用 YouTube / Bilibili 补工作流演示，用 Flickr 补视觉灵感，用 GitHub 补可执行入口
4. 只把稳定提示词、稳定工作流、稳定素材来源沉淀成可复用资产

## How to Use
1. 先选主生成入口：
   - `ComfyUI / Stable Diffusion`：适合节点式图片和视频工作流
   - `mcp-image`：适合把图片生成与编辑接进 MCP 工具链
   - `MeiGen-AI-Design-MCP`：适合本地多方向并行生成与设计探索
2. 再建立浏览器审看回路：
   - 生成后统一在浏览器里看结果
   - 标记保留、废弃、待重跑
   - 把最稳定的一组提示词和参数回写到工作目录
3. 再按 source pack 补上下文，但不要混用角色：
   - `GitHub`：找真正可接入的仓库与工作流入口
   - `YouTube / Bilibili`：看实际演示、参数思路、回路编排
   - `Flickr`：补视觉灵感与素材方向，不把它当成可执行 workflow 文档
4. 只保留高价值沉淀：
   - 稳定提示词模板
   - 稳定工作流 JSON
   - 稳定素材来源清单
   - 明确的人工筛选规则

## Source Pack Guidance
当前这张技能卡对应的已验证 source pack 是：
- `youtube`
- `bilibili`
- `flickr`
- `github-search`

使用顺序建议：
1. 先从 `GitHub` 选可执行入口
2. 再用 `YouTube / Bilibili` 补实操和审看回路
3. 最后用 `Flickr` 只补视觉参考，不让灵感源反客为主

## Minimal Workflow
1. 选一个主生成入口并固定参数范围
2. 用同一主题跑 3 组图片或视频结果
3. 在浏览器统一审看并标记保留/废弃/待重跑
4. 查一个 GitHub 入口和一个视频演示，补最小执行路径
5. 只把保留下来的提示词、参数、审看结论沉淀成可重复工作流

## Guardrails
- 不把 `Flickr` 这类灵感源当成实施说明书
- 不把单条视频教程当成唯一事实来源
- 先跑最小闭环，再增加模型、风格或后处理复杂度
- 每次只调整一组提示词或参数，避免失去对比性

## References
- https://github.com/shinpr/mcp-image
- https://github.com/iconben/z-image-studio
- https://github.com/jau123/MeiGen-AI-Design-MCP
- https://www.youtube.com/watch?v=7aEQnTsI6zs
- https://www.bilibili.com/video/BV14mrfBSEdq/
- https://www.flickr.com/photos/dianeworland/55055024432/
