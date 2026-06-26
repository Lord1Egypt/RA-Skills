---
name: github-trending
description: 查询 GitHub Trending 热门项目，支持按编程语言、日期范围、口语（文档语言）筛选。当用户想了解 GitHub 今日/本周/本月热门项目、特定语言的热门仓库、或中文文档的热门项目时使用此技能。
---

# GitHub Trending 技能

## 何时使用

当用户需要以下任意信息时，请使用本技能：
- 查看 GitHub 当前热门项目（今日/本周/本月）
- 按编程语言筛选热门项目（如 Python、JavaScript、Go 等）
- 按文档口语筛选（如只显示中文文档的项目）
- 查看热门开发者（developers）而非仓库
- 获取趋势项目列表供学习、选型或参考

## 核心能力

1. **构造并返回 GitHub Trending 页面链接**，便于用户直接访问
2. **解释筛选参数**，帮助用户理解如何自定义查询
3. **提供常用筛选值参考**，降低用户使用门槛

## 基础 URL 结构

- **仓库 Trending**：`https://github.com/trending`
- **开发者 Trending**：`https://github.com/trending/developers`

## 筛选参数

GitHub Trending 页面通过 URL 查询参数进行筛选。所有参数均为可选，不指定时使用默认值。

### 1. `l` - 编程语言（Language）

根据项目主要使用的**编程语言**筛选。

| 参数 | 说明 |
|------|------|
| `l` | 语言标识符，小写。如 `python`、`javascript`、`typescript`、`go`、`rust` 等 |

**示例**：只显示 Python 项目 → `?l=python`

**常用语言值**（见 `references/languages.md`）：
- `python` - Python
- `javascript` - JavaScript
- `typescript` - TypeScript
- `go` - Go
- `rust` - Rust
- `java` - Java
- `c` - C
- `cpp` - C++
- `csharp` - C#
- `ruby` - Ruby
- `php` - PHP
- `kotlin` - Kotlin
- `swift` - Swift

### 2. `since` - 日期范围（Date range）

根据**时间窗口**筛选，统计该时间段内的热度。

| 参数值 | 含义 |
|--------|------|
| `daily` | 今日（Today） |
| `weekly` | 本周（This week） |
| `monthly` | 本月（This month） |

**示例**：查看本周热门 → `?since=weekly`

### 3. `spoken_language_code` - 口语/文档语言

根据项目 README/文档的**主要口语**筛选，用于找到特定语言文档的项目。

| 参数 | 说明 |
|------|------|
| `spoken_language_code` | ISO 639-1 语言代码，如 `en`、`zh`、`ja` 等 |

**示例**：只显示中文文档项目 → `?spoken_language_code=zh`

**常用口语代码**（见 `references/spoken-languages.md`）：
- `en` - 英语（English）
- `zh` - 中文（Chinese）
- `ja` - 日语（Japanese）
- `ko` - 韩语（Korean）
- `es` - 西班牙语（Spanish）
- `fr` - 法语（French）
- `de` - 德语（German）
- `ru` - 俄语（Russian）
- `pt` - 葡萄牙语（Portuguese）

## 组合使用示例

多个参数用 `&` 连接：

1. **本周 Python 热门项目**
   ```
   https://github.com/trending?l=python&since=weekly
   ```

2. **本月中文文档的 JavaScript 项目**
   ```
   https://github.com/trending?l=javascript&since=monthly&spoken_language_code=zh
   ```

3. **今日 Rust 热门**
   ```
   https://github.com/trending?l=rust&since=daily
   ```

4. **本周热门开发者**
   ```
   https://github.com/trending/developers?since=weekly
   ```

## 执行步骤

当用户请求 GitHub Trending 相关信息时：

1. **解析用户意图**：确定需要的类型（仓库/开发者）、时间范围、编程语言、口语筛选。
2. **选择合适的参数**：根据用户需求选择 `l`、`since`、`spoken_language_code` 的值。
3. **构造完整 URL**：按 `https://github.com/trending[?参数]` 或 `https://github.com/trending/developers[?参数]` 格式拼接。
4. **返回结果**：给出可点击的链接，并简要说明当前筛选条件。
5. **可选**：如需更丰富的筛选值，可参考 `references/` 目录下的文件。

## 注意事项

- GitHub 官方**不提供** Trending 的 REST API，本技能通过构造网页 URL 实现访问。
- 编程语言值需与 GitHub 语言列表一致，一般为小写英文，部分语言可能使用特殊标识（如 `c%23` 表示 C#，需 URL 编码）。
- 若用户提供的语言名称不明确，可给出常见匹配建议（如 "js" → `javascript`，"ts" → `typescript`）。

## 参考资料

- GitHub Trending 页面：https://github.com/trending
- 编程语言完整列表：`references/languages.md`
- 口语语言代码列表：`references/spoken-languages.md`
