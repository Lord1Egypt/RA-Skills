---
name: literature-search-pro
description: [已整合] 专业文献搜索已整合到 search 统一入口技能
argument-hint: "[研究领域] [参数]"
---

# ⚠️ 已整合 - 请使用 search 统一入口

> **本技能保留用于向后兼容，功能已整合到 `search` 统一入口技能**
>
> **推荐使用：** `search scholar [领域] [参数]` 或直接使用本技能（自动转发）

---

# Literature Search Pro（兼容层）

专业级学术文献搜索技能，整合三大数据库（OpenAlex + Semantic Scholar + arXiv）。

## 迁移指南

**新用法：**
```
search scholar 图神经网络 药物发现 max_papers=20
search scholar 振动台子结构试验 year=2023-2026
search scholar 结构损伤识别 深度学习 high_citation
```

**旧用法（仍然可用）：**
```
scholar 图神经网络 药物发现 max_papers=20
```

## 支持的数据库
| 数据库 | 限额 | 特点 | 优先级 |
|--------|------|------|--------|
| OpenAlex | 10K/天 | 最宽松，覆盖广 | 第一 |
| Semantic Scholar | 1K/5 分钟 | 引用数据准确 | 第二 |
| arXiv | 1 次/3 秒 | 最新预印本 | 第三 |

## 核心功能
- ✅ 多源搜索（OpenAlex + Semantic Scholar + arXiv）
- ✅ 智能去重（DOI/arXiv ID/标题模糊匹配）
- ✅ 质量排序（按引用数自动排序）
- ✅ 自动缓存（避免重复请求）
