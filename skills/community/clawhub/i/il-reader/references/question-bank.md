# 题库格式、匹配边界与贡献方式

本文件说明 `references/question-bank.json` 的结构、运行时如何匹配，以及如何贡献题目。

## 数据规模

| 题型 | 条数 |
|---|---|
| 多选 `multiple` | 400 |
| 单选 `single` | 312 |
| 判断 `judge` | 305 |
| **合计** | **1017** |

题库由用户提供并确认。命中即按库内答案作答，运行时**不再复验**。

> **诚实声明**：题库答案未经 il-reader 独立核验原始出处。若你发现某题答案与官方来源冲突，请开 issue 并附上可核验的原始链接。

## 文件结构

```json
{
  "version": 1,
  "bankRelease": "2026.10",
  "provenance": {
    "file": "question-bank.md",
    "name": "il-radar 题库",
    "sha256": "…",
    "verification": "user_supplied_unverified",
    "answer_policy": "bank_hit_answered_directly",
    "reported_sources": ["…"],
    "sources_detail": { "existing_json": {…}, "internal_xlsx": {…} }
  },
  "entries_sha256": "…",
  "summary": { "total": 1017, "by_type": {…}, "by_reuse_policy": {…}, "flagged_entries": 0 },
  "entries": [ … ]
}
```

| 字段 | 约束 |
|---|---|
| `version` | 必须为 `1`，运行时校验 |
| `entries_sha256` | `sha256(JSON.stringify(entries))`，**必须用 JS 生成**（命令见下文） |
| `entries[].id` | 全局唯一、非空字符串 |
| `entries[].type` | `single` / `multiple` / `judge` |
| `entries[].reuse_policy` | 本项目固定为 `trusted`，表示"命中即直接作答" |
| `entries[].source_kind` | 必须是 `user_supplied_official_sample` 或 `user_supplied_platform_report`（运行时白名单） |
| `entries[].explanation` | 字符串（可为空串） |
| `entries[].urls` | 字符串数组（可为空） |
| `entries[].issues` | 字符串数组；非空会让该题**不再直接作答** |

### 为什么 `entries_sha256` 必须用 JS 生成

运行时的摘要算法是 `sha256(JSON.stringify(entries))`。**Python 的 `json.dumps` 与 JS 的 `JSON.stringify` 对非 ASCII 内容的字节输出不同**，用 Python 算出的摘要一定校验失败。改完题库一律重算：

```bash
node -e "const fs=require('fs'),c=require('crypto');const f='references/question-bank.json';const j=JSON.parse(fs.readFileSync(f,'utf8'));j.entries_sha256=c.createHash('sha256').update(JSON.stringify(j.entries)).digest('hex');fs.writeFileSync(f,JSON.stringify(j,null,2)+'\n')"
```

> **本机实际情况**：本副本只带 `lookup.cjs` 与 `lib/`（`question-bank.cjs`、`asset-cache.cjs`），**没有** `tools/build-digest.cjs`、`tools/validate-bank.cjs`、`tools/list-flagged.cjs`。因此重算摘要用上面的 node 单行命令；改完必须**跑一道已知题**确认不再报"题库不可用"（见 §自检替代做法）。

## 匹配边界

运行时按以下三元组做**精确匹配**（规范化后）：

```
(type, 题干规范化, 全部选项文字排序)
```

规范化会统一：全角/半角括号、全角引号、连续空白。

### 以下变化不影响命中

| 变化 | 原因 |
|---|---|
| 选项整体换序 | 答案按**文字**重映射字母 |
| 题干全角/半角括号差异 | 规范化统一 |
| 题干或选项多/少空格 | 规范化统一 |
| 题干末尾标点差异 | 规范化统一 |

### 以下变化会导致不命中

| 变化 | 说明 |
|---|---|
| 题干被改写 | 增删限定语、换实体、改数字/年份 |
| 任一选项文字不同 | 必须全部选项文字一致 |
| 题型标注错误 | 把 `single` 写成 `multiple` 会直接掉到 27% 命中率 |

**只做安全归一化**：不会为了制造命中而删除否定词、数字、日期、检索式运算符或字段限定词。

## 贡献题目

1. 编辑 `references/question-bank.json`，在 `entries` 中追加条目，遵守上表字段约束
2. 重算摘要（命令见 §为什么 `entries_sha256` 必须用 JS 生成）
3. 自检（本副本无 `tools/`，用真实查库代替）：

   ```bash
   node "<SKILL>/lookup.cjs" --status          # 条数应 +1，且不报"题库不可用"
   node "<SKILL>/lookup.cjs" "<新题的JSON>"     # 应返回 matched
   ```

   `--status` 会加载整份题库并校验摘要，摘要不对会直接报错——等同于"题库能不能用"的回归。想确认某题是否会被排除，用它的 `id` 反查 `entries` 里的 `issues` 字段：**非空即不直接作答**。

4. 判断题必须能从"字母→选项文字"链路确定 `正确`/`错误`
5. 提交 PR，说明题目来源

## 用你自己的题库

题库是可替换的数据层。若你有自己的题库：

- 保持文件名 `references/question-bank.json`（运行时硬编码该路径）
- 遵守上表的字段约束与摘要算法
- 改完先跑 `lookup.cjs --status` + 一道已知题，确认可加载、可命中

`reuse_policy` 用 `trusted` 即可获得"命中即作答"的行为；沿用旧的 `stable`/`dynamic`/`product` 等值也会被接受，但那些值会触发复验理由，不会直接作答。
