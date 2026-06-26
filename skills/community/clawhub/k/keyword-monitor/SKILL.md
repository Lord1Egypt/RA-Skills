---
name: keyword-monitor
description: 关键词监控与内容采集自动化工具 — 多关键词并行监控、全网爆款内容自动抓取，每日生成结构化报告推送到飞书群。适用于内容运营、竞品监控、热点追踪、线索收集等场景。
version: 1.3.0
author: yesong-Hue
homepage: https://clawhub.ai/yesong-Hue/keyword-monitor
tags: [关键词监控, 内容采集, 飞书推送, 自动化, 内容运营, 竞品监控]
readme: |
  # 关键词监控系统
  
  专为内容运营者和竞品监控设计的自动化工具。通过多关键词并行监控，自动抓取全网爆款内容，每日生成结构化数据报告并推送到飞书群。
  
  ## 核心功能
  
  ### 1. 多关键词并行监控
  支持同时监控数十个关键词，每个关键词独立采集最新热门内容。支持配置关键词权重和平台偏好。
  
  ### 2. 全网爆款内容采集
  基于 Tavily AI 搜索 API，自动抓取各大平台（抖音、微博、知乎、小红书等）的热门内容。
  
  ### 3. 结构化数据报告
  自动生成 Markdown 格式表格报告，字段包括：排名、标题、平台、热度评分、发布时间、原文链接。
  
  ### 4. 飞书群自动推送
  每日报告自动推送到飞书群，支持自定义推送时间和群组。
  
  ### 5. 本地数据存储
  所有报告保存在本地，支持历史查询和趋势分析。
  
  ## 安装
  
  通过OpenClaw Skills安装：
  
  ```
  openclaw skills install keyword-monitor
  ```
  
  安装后配置关键词和飞书Webhook即可使用。
  
  ## 配置说明
  
  - 关键词列表：编辑配置文件，每行一个关键词
  - 飞书推送：在配置中设置Webhook地址（可选）
  - API配置：需要Tavily API Key（免费注册：https://tavily.com）
  
  ## 适用场景
  
  - 内容矩阵运营：追热点、找选题
  - 竞品监控：实时追踪竞品动态
  - 热点追踪：第一时间捕捉行业热点
  - 销售线索收集：自动采集潜在客户信息
  
  ## 隐私说明
  
  - 所有数据存储在本地，不会上传到第三方
  - 飞书Webhook仅用于推送报告
  
  ## 相关资源
  
  - AI技能包集合：AI智造工坊 http://ai.qnitgroup.com
  - Tavily API：https://tavily.com
  
  ## 作者
  
  yesong-Hue
---

# 关键词监控

> 多关键词并行监控 + 全网爆款内容采集 + 每日报告推送到飞书群

## 核心功能

1. 多关键词并行监控
2. 全网爆款内容采集（Tavily AI搜索）
3. 结构化数据报告
4. 飞书群自动推送
5. 本地数据存储

## 安装使用

通过OpenClaw安装后，配置关键词和飞书Webhook即可。

## 相关资源

- AI技能包集合：http://ai.qnitgroup.com
- ShadowAI API：https://referer.shadowai.xyz/r/1056448