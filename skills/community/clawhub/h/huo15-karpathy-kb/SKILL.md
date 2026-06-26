---
name: huo15-knowledge-base
displayName: 火一五知识库技能
description: 【青岛火一五信息科技有限公司】基于 Karpathy LLM Knowledge Base 三层架构（Data Ingest → Compilation → Active Maintenance）的知识捕获与管理技能。将知识点写入 memory/ 目录并同步到公司 Odoo 知识库。
version: 1.0.0
aliases:
  - 卡帕西知识库
  - 知识库技能
  - karpathy
dependencies:
  python-packages:
    - python-docx
---

# 火一五知识库技能 v1.0

> 基于 Karpathy LLM Knowledge Base 三层架构 — 青岛火一五信息科技有限公司

## 一、核心概念

Karpathy LLM Knowledge Base 三层架构：

| 层次 | 名称 | 功能 |
|------|------|------|
| **Data Ingest** | 数据摄入 | 原始知识点捕获（对话/文档/邮件） |
| **Compilation** | 编译整理 | 提取关键实体、关系、引用，建档入库 |
| **Active Maintenance** | 主动维护 | 定期检查知识 drift，淘汰过时内容 |

## 二、触发词

- 知识库 / 入库 / 存入知识库
- 卡帕西知识库 / Karpathy 知识库
- 同步知识库 / 更新知识库
- 记一下 / 这个记到知识库
- capture knowledge / save to knowledge base

## 三、知识写入流程

### 3.1 知识点文件命名规范

```
memory/
├── knowledge/
│   ├── {category}/{YYYY-MM-DD}_{slug}.md
│   └── categories: odoo / business / technical / product / feedback
```

### 3.2 知识点文件格式

```markdown
# {标题}

## 摘要
{2-3句话总结}

## 详细说明
{核心内容}

## 关键要点
- {要点1}
- {要点2}

## 引用来源
- {来源1}
- {来源2}

## 相关知识点
- {related_topic_1}
- {related_topic_2}

---
**入库时间：** YYYY-MM-DD
**来源：** {对话/文档/其他}
**标签：** {tag1}, {tag2}
```

## 四、同步到 Odoo 知识库

### 4.1 写入 Odoo 知识库

使用 `odoo_knowledge_create` 工具：

```python
title = "{标题}"
content = """<div class="knowledge-article">
<h2>摘要</h2>
<p>{摘要}</p>
<h2>详细说明</h2>
<p>{详细说明}</p>
<h2>关键要点</h2>
<ul>
<li>{要点1}</li>
<li>{要点2}</li>
</ul>
</div>"""
category = "技术"  # 或 "业务" / "产品" / "客户反馈"
```

### 4.2 Odoo 知识库分类

| category | Odoo 知识库分类 |
|----------|---------------|
| odoo | Odoo 技术 |
| business | 业务知识 |
| technical | 技术积累 |
| product | 产品知识 |
| feedback | 客户反馈 |

## 五、KARPATHY 三层执行

### 5.1 Data Ingest（摄入）
- 对话/文档 → 提取核心知识点
- 去重检查（grep 已有 knowledge 目录）
- 生成标准文件

### 5.2 Compilation（编译）
- 提取实体：人名/公司名/产品名/功能名
- 建立关联：相关知识点双向链接
- 打标签：odoo / business / technical 等

### 5.3 Active Maintenance（维护）
- 同一话题新知识 → 合并更新而非新建
- 超过 90 天未更新的知识点 → 标记 `{{drift}}`
- 删除重复/过时内容

## 六、版本历史

- **v1.0.0（当前）**
  - 初始版本
  - 支持知识点文件生成 + Odoo 知识库同步
  - Karpathy 三层架构落地

---

**技术支持：** 青岛火一五信息科技有限公司
