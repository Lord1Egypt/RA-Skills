---
name: web-content-extractor
version: 1.0.0
description: 从网页URL中提取标题、正文、图片链接等内容
author: MiniMax Agent
tags:
  - utility
  - web
  - content
  - extraction
dependencies:
  - python3
  - requests
  - beautifulsoup4
permissions:
  - network
---

# 网页内容提取器

这是一个实用的网页内容提取技能，可以从任意网页中提取结构化信息。

## 功能特点

- 自动提取网页标题和元数据
- 提取正文内容并清理HTML标签
- 提取所有图片链接
- 提取所有外链
- 支持指定提取元素
- 输出格式化JSON结果

## 使用方法

### 基本用法

```
技能输入：https://example.com
技能输出：{"title": "...", "content": "...", "images": [...], "links": [...]}
```

### 高级用法

- 指定提取特定元素
- 设置内容长度限制
- 自定义输出格式

## 技术规格

- 编程语言：Python 3
- 依赖库：requests, beautifulsoup4
- 网络要求：需要互联网连接
