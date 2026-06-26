---

name: concept-research
description: |
  调查某个概念是否已被实现及实现现状。使用多语言关键词、多引擎交叉验证、多维度搜索。
  当用户提出一个想法或概念时，通过系统化的搜索流程调研其现有解决方案。
  触发条件：用户询问"有没有人做过"、"查一下xxx的现状"、"调研xxx"等。
---

# Concept Research - 概念现状调研

> **ClawHub**: https://clawhub.ai/leeshunee/kinema-concept-research | `clawhub install kinema-concept-research`
> **GitHub**: https://github.com/KinemaClawWorkspace/kinema-concept-research

调查一个概念是否已被实现、做成什么样子。彻底搜索，输出摘要清单。

## 工作流

### 阶段 1: 概念澄清（对话）

通过多轮对话明确：
- 用户想做什么
- 核心功能是什么
- 目标用户是谁
- 差异化期望是什么

**产出**: 一句话概念定义

### 阶段 2: 关键词拆解

基于概念定义，拆解为多组关键词：

1. 核心词变体 - 同义词、近义词、不同表述
2. 技术栈词 - 涉及的技术、框架、协议
3. 场景词 - 使用场景、解决的问题
4. 组合词 - 核心词 + 技术/场景

每组生成中英文版本。

### 阶段 3: 广度搜索

使用 searxng-search 逐批搜索：

1. 每组关键词搜索 1-2 页结果
2. 记录所有相关链接
3. 根据标题/摘要初步标记相关性

时间过滤（如搜索引擎支持）:
- 五年之前、两年之前、一年之前、三个月之前、最近三个月

### 阶段 4: 深度探索

从高相关性结果中挑选 3-5 个进行深度探索：

1. Web 页面: 使用 web_fetch 抓取内容
2. GitHub Repo: 克隆到本地，阅读 README
3. PDF/论文: 下载阅读

探索内容记录：
- 核心功能
- 技术实现
- 优缺点
- 与用户概念的异同

### 阶段 5: 输出报告

生成摘要清单：

| 字段 | 说明 |
|------|------|
| 链接 | 原始 URL |
| 概述 | 是什么，做了什么 |
| 基本思路 | 核心技术方案 |
| 相同点 | 与用户概念的共性 |
| 不同点 | 与用户概念的差异 |
| 分析 | 机会点、改进空间 |

## 项目目录

所有文件保存在：`projects/research-{uuid}/`

```
projects/research-{uuid}/
├── concepts/
│   └── definition.md
├── keywords/
│   └── keywords.md
├── search/
│   ├── broad/
│   └── deep/
├── repos/
├── papers/
└── report.md
```

## 搜索工具

优先使用 searxng-search。如 SearXNG 未部署，可使用 ddg-search。

---

## 相关文档

- searxng-search skill
- skill-creator skill
