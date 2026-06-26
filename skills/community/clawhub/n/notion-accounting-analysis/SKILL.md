---
name: notion-accounting-analysis
description: Notion记账财务数据分析技能，自动读取支出收入流水表，全量翻页获取数据，100%解析relation类别字段，按年月类别标签多维分析并生成Markdown财务报告。
tags:
  - notion
  - finance
  - accounting
  - analysis
version: 1.0.4
---

# Notion 记账数据分析 Skill

> 适用场景：用户说"分析我的 Notion 记账数据"、"生成财务报告"、"查看收支趋势"时触发。
> 前置条件：用户提供 Notion Integration Token（secret_xxx 格式）和 data_source_id。

---

## 核心能力

1. **全量数据获取** — 自动翻页（处理 Notion API `has_more`），不漏任何记录
2. **relation 字段 100% 解析** — 先收集所有 relation ID，再批量并发查询对应名称，零遗漏
3. **多维分析** — 按年/月/类别/标签/大额 TOP 多角度剖析
4. **智能报告生成** — 自动输出 Markdown 报告到 `/workspace/`，带优化建议
5. **异常主动提示** — 若 relation ID 无法解析，会列出 ID 并提示如何修复

---

## 已知 relation ID → 类别名称（已验证）

| relation ID（前8位） | 对应类别 |
|---|---|
| `2e1bd123...817c` | 房租 |
| `2e1bd123...80e8` | 旅游娱乐 |
| `2e1bd123...8081` | 房贷 |
| `2e1bd123...815a` | 餐饮 |
| `2e1bd123...8004` | 总记账 |
| `2e1bd123...806f` | 医疗 |
| `2e1bd123...8059` | 购物 |
| `2e1bd123...80d4` | 所得税 |
| `2e1bd123...817f` | 交通 |
| `2e1bd123...81dd` | 人情往来 |
| `2e1bd123...8084` | 专项 |
| `2e1bd123...810d` | 运动 |
| `2e1bd123...8054` | 公司额外 |
| `2e1bd123...81de` | 日用 |

> 💡 若发现新的 relation ID 查不到名称：在 Notion 中打开该记录页面 → 右上角 `...` → `Add connections` → 添加 Integration 即可。

---

## 字段识别规范（重要踩坑记录）

支出流水表通常有两个分类字段，优先级：

| 字段 | 类型 | 处理方式 |
|------|------|---------|
| `支出类别` | **relation** | 通过 API 查询名称，**必须** |
| `标签` | select | 直接存储名称，**可用** |

**错误**：只用 select，忽略 relation → 类别大量丢失。
**正确**：relation 用 ID 查表，select 直接用，两者结合覆盖 100% 类别。

---

## 执行流程

### 第 1 步：确认数据源

用户未提供 data_source_id 时，用搜索接口查找：

```bash
curl -s -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_API_TOKEN" \
  -H "Notion-Version: 2025-09-03" \
  -d '{"query": "支出", "page_size": 20}' \
  | jq '.results[] | {id, title: .properties.Name.title[0].plain_text}'
```

### 第 2 步：全量获取数据（必须翻页）

```javascript
// 错误：只查第一页 → 数据不完整
const page = await fetch('/v1/data_sources/{id}/query', {page_size: 100});

// 正确：循环直到 has_more = false
let cursor = null;
do {
  const body = cursor ? {page_size:100, start_cursor:cursor} : {page_size:100};
  const page = await fetch('/v1/data_sources/{id}/query', body);
  results.push(...page.results);
  cursor = page.has_more ? page.next_cursor : null;
} while (cursor);
```

### 第 3 步：relation ID 批量解析（必须）

```javascript
// 第一步：收集所有 relation IDs（不重复）
const allIds = [...new Set(results.flatMap(r =>
  (r.properties['支出类别']?.relation || []).map(rel => rel.id)
))];

// 第二步：并发查询所有 ID（每个只查一次）
const relMap = Object.fromEntries(
  await Promise.all(allIds.map(async id => [id, await resolvePageName(id)]))
);
```

### 第 4 步：分析并输出报告

```bash
# 可直接使用附带的分析脚本
node analyze.mjs <token> <expense_data_source_id> [income_data_source_id] [year]
```

---

## 常见错误处理

| 现象 | 原因 | 解决方案 |
|------|------|---------|
| 类别全是"未分类" | 只用了 select，relation 全部丢失 | 改用 relation ID 查表 |
| 总支出比预期少 | 只查了第一页（100条），还有后续页 | 循环翻页直到 has_more=false |
| relation ID 查不到名称 | 记录不在 integration 可见范围内 | Notion 页面 → Add connections |
| 金额对不上 | select 和 relation 重复计算了同一笔 | select 和 relation 只取一个字段 |

---

## 分析报告模板

```markdown
# {年份} 年度财务分析报告

> 数据来源：Notion 支出流水表 & 收入流水表
> 分析范围：{年}年（{n}笔支出，{n}笔收入）

## 一、收支总览
## 二、月度趋势
## 三、类别分析（relation 100% 解析）
## 四、标签分析
## 五、TOP N 大额支出
## 六、优化建议
```
