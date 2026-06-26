---
name: wechat-article-fetcher
description: 抓取微信公众号文章全文内容与图片，支持JSON导出和整页截图
metadata:
  version: 1.0.1
  author: Liuzln
  category: cli-utilities
---

# 微信公众号文章抓取器

抓取任意微信公众号文章 URL，自动提取标题、作者、发布时间与完整正文，下载并本地保存文章内图片，生成整页截图并导出结构化 JSON。

## 使用方式

命令行工具：
- `fetch.py` — 单篇抓取
- `batch_fetch.py` — 批量抓取
- `run_in_venv.py` — Playwright 虚拟环境兼容运行

## 可选参数
- 无头模式（服务器部署）
- 超时控制
- 不保存图片/截图

## 适用场景
内容归档、离线备份、舆情监测、文本/图像数据采集、NLP 数据准备。

## 注意事项
- Cookie 过期需手动更新
- 建议先用少量文章测试确认正常后再批量抓取
