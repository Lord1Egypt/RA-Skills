---
name: linkfox-keyword-library
description: 查询用户的词库列表和词条内容。用户说"查词库"、"看我的词库"、"词库里有什么词"、"查词库内容"、"keyword library"、"我的关键词词库"时触发。支持库、按词库ID或名称获取词条详情。
---

# 词库查询

查询当前用户的关键词词库列表和词条内容，用于在 Agent 对话中引用用户自建的关键词资产。

## 参数概览

### 查询词库列表

- **必填字段**：`uid`（用户ID，由系统自动注入）
- **可选字段**：`name`（词库名称模糊搜索）

### 查询词条内容

- **必填字段**：`uid`（用户ID）、`libraryId` 或 `libraryName`（二选一）
- **可选字段**：`limit`（返回词条数量上限，默认 500，最大 500）

完整参数与响应结构见 [`references/api.md`](references/api.md)。

## 调用方式

- **Python 脚本**：`python scripts/keyword_library.py '<JSON 参数>'`

**子命令**（通过 JSON 中的 `action` 字段区分）：

| action | 说明 |
|--------|------|
| `listLibraries` | 查询用户词库列表 |
| `getWords` | 查询指定词库的词条内容 |

**输出策略（脚本默认行为）**：
- **始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-keyword-library-<timestamp>.json`
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段的长度 + 前 3 条样本）
- 加 `--inline` 强制全量打印到 stdout（同样落盘）

## 使用指引

1. **先列词库**：不确定用户有哪些词库时，先调用 `listLibraries` 获取清单。
2. **再取词条**：拿到词库 ID 或名称后，调用 `getWords` 获取具体词条。
3. **模糊搜索**：用户只记得大概名字时，传 `name` 做模糊匹配。
4. **词条上限**：单次最多返回 500 条词条，大词库建议在对话中告知用户总数。

### 示例

**1. 查看所有词库**
```json
{"action": "listLibraries", "uid": "自动注入"}
```

**2. 按名称搜索词库**
```json
{"action": "listLibraries", "uid": "自动注入", "name": "品牌"}
```

**3. 按词库ID查询词条**
```json
{"action": "getWords", "uid": "自动注入", "libraryId": "abc123"}
```

**4. 按词库名称查询词条**
```json
{"action": "getWords", "uid": "自动注入", "libraryName": "品牌风险词"}
```

## 展示规则

- 词库列表：表格展示名称、类型、渠道、词条数量、描述
- 词条内容：表格展示词、标签、渠道、备注
- 若用户要把词库内容用于 listing 或广告，直接提取 `word` 字段作为关键词素材

## 限制

- 仅能查询当前用户自己的词库（按 uid 隔离）
- 单次最多返回 500 条词条
- 词库名称搜索为模糊匹配（包含即命中）

## 与其他 skill 的关系

- 本 skill 查询的是用户手动维护的词库（品牌风险词、敏感词、违禁词、自定义词等）
- 与 `linkfox-sif-asin-keywords`（SIF 流量词反查）、`linkfox-aba-intelligent-query`（ABA 搜索词）是互补关系
- Agent 可结合词库内容做 listing 合规检查、广告词筛选等
