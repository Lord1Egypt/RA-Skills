---
name: jz-research-target-software-project
description: 调研指定的某一款开源或商业闭源软件项目。
license: MIT
metadata:
  author: johnny-ztsd
  version: "V1.0.5-202608240946"
  my-home-page: https://www.cnblogs.com/know-data
  my-skill-document-specification: https://agentskills.io/specification
tags:
  - software-research
---

# 调研指定的软件项目 Skill

## Role
- 资深软件开发工程师


## Background
- 技术调研

## Task/Goal
- 调研指定的开源或闭源软件项目( softwareProjectId = <softwareProjectId> )，以 Markdown 结构化文档输出。
>> 例如: softwareProjectId = "apache/doris/"
- 参考资料（包括但不限于）:
> - https://github.com/<softwareProjectId>


- 输出文档的关键目录结构、及关键内容为:
```
# 1 概述
## 产品介绍
> 章节内容（包括但不限于）: 产品定位、诞生的背景与原因、解决的核心问题、官方链接（官网URL、Github项目URL）

## 发展历程

## 主要功能

## 核心优势

## 主要短板

## 局限性

## 适用场景

## 同类竞品

## 发展趋势
> 章节内容（包括但不限于）: 
>> - 如果为开源软件，则还需调研: 开源社区的活跃趋势、Star趋势、Fork趋势
>> - 项目发展趋势的一句话总结



# 2 工作原理与架构
## 概念术语

## 架构与运行原理

## ...

# 3 使用指南
> 章节内容（包括但不限于）: 安装部署（Windows、Linux）、关键操作


# Z FAQ
> 章节内容（包括但不限于）: 常见问题。
> 格式要求：每个问题以二级章节`## Q: ` 开头


# Y 推荐文献
> 章节内容（包括但不限于）: 比较推荐的文献、书籍
> 参考格式: [标题 - 来源网站](链接，如果为实体书籍则填`#`符)
- [Doris - Github](https://github.com/<softwareProjectId>)


# X 参考文献 
> 参考格式: [标题 - 来源网站](链接，如果为实体书籍则填`#`符)
- [Doris - Github](https://github.com/<softwareProjectId>)
```

- 提炼标题：用最精炼的语言总结其产品定位与核心特性，作为本调研报告的标题


## Require
- 为确保内容的严谨与正确性，不急于立即输出，请深入思考后，再逐步输出。
- 各级章节内可自主划分子章节；
- 重点文本内容，可加粗；
- 所需图形图像，可直接引用其 URL或使用 mermaid 格式绘制。
> 例如: [doris-architecuture](https://doris.apache.org/assets/images/what-is-doris-new-5c384f030b18178336b8e9beb2a352c5.png)
- 子章节内的多个不同的逻辑段落，可以列表形式输出。