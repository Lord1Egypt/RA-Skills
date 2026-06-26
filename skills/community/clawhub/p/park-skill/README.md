# 园区智能运营助手 (Park Smart Operations Assistant)

为产业园区、科技园区、工业园区打造的智能化运营助手技能。

[English Version](#english)

---

## 功能特性

### 🎯 五大核心模块

| 模块 | 功能 |
|------|------|
| **园区概况** | 基础信息、交通配套、生活配套、核心优势 |
| **招商服务** | 政策解读、房源管理、入驻流程、资质要求 |
| **企业服务** | 工商注册、政策申报、人才服务、融资对接 |
| **运营管理** | 物业服务、安全管理、环保合规、投诉处理 |
| **数据看板** | 入驻率统计、产业分布、税收贡献、企业成长 |

### 🌍 多语言支持

- 🇨🇳 中文 (zh-CN)
- 🇺🇸 English (en-US)

### 📊 数据输出格式

- 结构化 JSON 数据
- Markdown 表格呈现
- Excel/PDF 文档导出

---

## 快速开始

### 基础查询

```
查询园区概况
查看招商政策
了解入驻流程
获取物业服务
```

### 场景对话示例

**中文场景:**
- "园区有哪些优惠政策？"
- "我想了解厂房租金"
- "如何申请高新企业认定？"
- "查询本月入驻率数据"

**English Scenarios:**
- "What are the lease terms for office space?"
- "Tell me about the tax incentives"
- "How to apply for high-tech enterprise certification?"
- "Show me the occupancy rate statistics"

---

## 目录结构

```
park-skill/
├── SKILL.md              # 技能定义文件
├── README.md             # 使用说明
├── clawhub.yaml          # 发布配置
├── config/
│   └── park-config.yaml  # 园区数据配置
├── i18n/
│   ├── zh-CN.yaml        # 中文语言包
│   └── en-US.yaml        # 英文语言包
└── examples/
    ├── example-query.md  # 查询示例
    └── example-output.md # 输出示例
```

---

## 配置说明

### 1. 园区数据配置

编辑 `config/park-config.yaml` 文件配置园区信息：

```yaml
park:
  name: "示例园区"
  location: "城市名"
  area: 500000  # 平方米
  industry: "科技创新"
```

### 2. 语言切换

通过对话指令切换语言：
- 中文模式：`使用中文`
- English mode：`Use English`

---

## 使用场景

| 场景 | 适用角色 | 功能 |
|------|---------|------|
| 招商接待 | 招商专员 | 政策解读、房源推荐 |
| 企业服务 | 服务管家 | 工商注册、申报指导 |
| 物业管理 | 物业经理 | 报修处理、安全管理 |
| 数据分析 | 运营总监 | 入驻率统计、产值分析 |

---

## 扩展定制

如需自定义园区数据或功能模块，请联系开发团队。

---

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| 1.0.0 | 2025-01 | 初始版本发布 |

---

## 许可证

MIT License

---

# English

## Overview

**Park Smart Operations Assistant** is an intelligent skill designed for industrial parks, technology parks, and business parks. It covers core scenarios including business recruitment, enterprise services, operations management, and data dashboards.

## Features

- **5 Core Modules**: Park Overview, Recruitment, Enterprise Services, Operations, Data Dashboard
- **Multilingual**: Chinese (zh-CN) and English (en-US)
- **Structured Output**: JSON, Markdown tables, Excel/PDF export

## Quick Start

```markdown
# Query park overview
Query park overview

# Check recruitment policies
View recruitment policies

# Get property services
Property services inquiry
```

## Support

For questions or customization needs, please contact support.

---

*Last updated: 2025-01*
