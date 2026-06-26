---
name: pans-case-writer
description: |
  自动将客户成功案例包装为 Case Study（案例研究）。支持背景 / 挑战 / 方案 /
  成果四段式结构化模板，支持 Markdown / PDF / HTML 多种格式导出，
  提供交互式创建模式逐步引导输入关键信息。
  触发词：案例研究, case study, 客户案例, 成功案例, 案例包装,
  客户故事, 销售案例, 案例撰写
---

# pans-case-writer

自动将客户成功案例包装为 Case Study（案例研究）。

## 功能

- 将零散的客户信息转化为结构化的 Case Study
- 支持背景 / 挑战 / 方案 / 成果四段式模板
- 支持 Markdown / PDF / HTML 多种格式导出
- 交互式创建模式，逐步引导输入关键信息

## Case Study 结构

```
# [客户名称] 案例研究

## 客户背景
[行业 / 规模 / 核心业务]

## 面临挑战
[业务痛点 / 技术难点 / 约束条件]

## 解决方案
[产品选型 / 实施路径 / 关键技术]

## 成果与价值
[量化指标 / 业务提升 / 客户评价]
```

## CLI 用法

```bash
# 交互式创建
python3 case.py --create

# 导出指定格式
python3 case.py --export input.md --format pdf
python3 case.py --export input.md --format html

# 查看帮助
python3 case.py --help

# 列出支持的模板
python3 case.py --list
```

## 快速开始

1. 运行 `python3 case.py --create` 进入交互模式
2. 回答提示，依次输入客户名称、行业、挑战、方案、成果
3. 生成 Markdown 文件后，使用 `--export` 导出为 PDF 或 HTML
