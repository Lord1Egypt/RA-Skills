# Notion 记账财务分析

> 通过 Notion API 全自动读取记账数据，生成专业财务分析报告。

---

## 🎯 这是什么

一个专注于 **Notion 记账用户** 的数据分析技能。只需提供 Notion Integration Token，即可自动：
- ✅ 全量读取支出/收入流水表（自动处理翻页，不漏任何记录）
- ✅ 100% 解析 relation 类别字段（解决 Notion 记账数据无法正确分类的核心痛点）
- ✅ 多维分析：年/月/类别/标签/大额 TOP
- ✅ 生成 Markdown 财务报告，自动保存到 `/workspace/`

---

## 💡 核心价值

| 痛点 | 本技能解决方案 |
|------|--------------|
| Notion relation 类别全是 ID，看不懂 | 先收集所有 ID，再批量查名称，100% 解析 |
| 数据量大，翻页容易漏 | 自动翻页循环直到抓完所有页 |
| 类别和标签重复计算 | 规范字段优先级，一个类别只取一个字段 |
| 手动汇总费时易错 | 一键分析，报告秒生成 |

---

## 📋 前置要求

- **Notion Integration Token**：在 [notion.so/my-integrations](https://www.notion.so/my-integrations) 创建
- **支出/收入流水表**的 data_source_id（可搜索获取）
- Token 需要对目标页面有访问权限（在 Notion 页面右上角 `...` → `Add connections`）

---

## 🚀 使用方式

在 MaxClaw 中直接说：
```
分析我的 Notion 记账数据
生成2026年财务报告
查看我的收支趋势
```

或者使用内置分析脚本：
```bash
node analyze.mjs <NOTION_TOKEN> <EXPENSE_DATA_SOURCE_ID> [INCOME_DATA_SOURCE_ID] [YEAR]
```

---

## 📊 分析维度

- **收支总览**：总收入、总支出、净结余、月均支出、储蓄率
- **月度趋势**：柱状图 + 每月明细
- **类别分析**：relation 字段 100% 解析，含真实类别名称
- **标签分析**：select 字段交叉验证
- **TOP 大额**：逐笔溯源，追踪大额支出
- **优化建议**：基于数据结构的个性化财务建议

---

## 🔧 技术亮点

- **自动翻页**：`has_more` → `next_cursor` 循环，不漏数据
- **批量并发查询**：所有 relation ID 只查一次，网络效率最优
- **YAML frontmatter 规范**：符合 ClawHub skill 标准格式
- **生产级脚本**：含异常处理、未解析 ID 主动提示

---

## 📂 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能触发逻辑 + 踩坑经验 + 执行流程文档 |
| `analyze.mjs` | 可独立运行的分析脚本，Node.js ESM 格式 |
| `README.md` | 本文件，ClawHub 市场展示页面 |

---

*适用于已有 Notion 记账系统的个人/家庭用户*
