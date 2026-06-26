# Himalaya 邮件查询使用指南

## 概述

Himalaya 的 `envelope list` 和 `envelope thread` 命令支持一套专门设计的查询 DSL（领域特定语言），用于**筛选**和**排序**邮件。你的查询字符串会被 Himalaya 解析成 AST，最终转换为 IMAP `SEARCH` / `SORT` 命令发送给邮件服务器。

> **注意**：Himalaya 的查询语法是高层封装，并非直接使用 IMAP 原始关键字，但底层会映射为 IMAP 搜索条件。

---

## 查询语法结构

一条完整查询由 **过滤条件** 和 **排序条件** 组成，两者可选：

```
[filter-query] [order by sort-query]
```

- `filter-query`：指定筛选条件（可选）
- `sort-query`：指定排序规则（可选）
- 若两者同时存在，**过滤条件必须写在 `order by` 前面**

---

## 过滤条件语法

### 基本形式

过滤条件由**条件**和**运算符**组合而成，支持使用括号 `()` 改变优先级。

### 可用的条件

| Himalaya 语法 | 含义 | 对应 IMAP 搜索键 | 示例 |
|--------------|------|-----------------|------|
| `date <yyyy-mm-dd>` | 日期精确匹配 | `SENTON` | `date 2025-04-12` |
| `before <yyyy-mm-dd>` | 日期严格小于 | `SENTBEFORE` | `before 2025-04-01` |
| `after <yyyy-mm-dd>` | 日期严格大于 | `SENTSINCE` (+1天) | `after 2025-04-01` |
| `from <pattern>` | 发件人匹配 | `FROM` | `from alice@example.com` |
| `to <pattern>` | 收件人匹配 | `TO` | `to bob@example.com` |
| `subject <pattern>` | 主题匹配 | `SUBJECT` | `subject "会议通知"` |
| `body <pattern>` | 正文内容匹配 | `BODY` | `body 项目进度` |
| `flag <flag>` | 邮件标志匹配 | 对应状态标志 | `flag seen` |

### 可用的运算符

| 运算符 | 优先级 | 含义 | 示例 |
|--------|--------|------|------|
| `not` | 最高 | 取反 | `not from spam@example.com` |
| `and` | 中 | 两者都必须满足 | `from boss and subject 周报` |
| `or` | 最低 | 满足其一即可 | `from alice or from bob` |

**优先级规则**：`not` > `and` > `or`，复杂查询建议用括号明确优先级。

### 模式匹配中的空格与引号

- **引号**：用双引号包裹含空格的字符串，如 `subject "foo bar"`
- **转义**：无引号模式下可用反斜杠转义空格和括号，如 `subject foo\ bar`
- 引号内可转义 `\"` 和 `\\`

---

## 排序条件语法

使用关键字 `order by` 开头，后跟一个或多个排序字段，每个字段可指定 `asc` 或 `desc`。

### 可用的排序字段

| 字段 | 排序依据 |
|------|---------|
| `date` | 邮件日期 |
| `from` | 发件人 |
| `to` | 收件人 |
| `subject` | 主题 |

### 默认顺序

- 不指定时默认为 **升序** (`asc`)
- 多字段排序时按声明顺序依次应用

---

## 组合查询示例

### 纯过滤
```bash
# 主题包含"周报"且正文包含"进度"
himalaya envelope list subject 周报 and body 进度

# 来自老板或 CEO 的邮件
himalaya envelope list from boss@example.com or from ceo@example.com

# 不是已删除的邮件（假设服务器支持相关标志）
himalaya envelope list not flag deleted
```

### 纯排序
```bash
# 按日期降序排列（最新的在前）
himalaya envelope list order by date desc

# 先按发件人升序，再按主题降序
himalaya envelope list order by from asc subject desc
```

### 过滤 + 排序
```bash
# 查找未读邮件，按日期降序排列
himalaya envelope list not flag seen order by date desc

# 查找4月以来的重要邮件，先按发件人排序再按日期排序
himalaya envelope list after 2025-04-01 and subject 重要 order by from date desc
```

---

## 常见场景命令示例

### 1. 查看未读邮件
```bash
himalaya envelope list not flag seen
himalaya envelope list not flag seen order by date desc
```

### 2. 查看来自特定发件人的邮件
```bash
himaya envelope list from alice@example.com
himalaya envelope list from alice@example.com order by date desc
```

### 3. 按日期范围查找
```bash
# 2025年4月1日至4月10日（before 不包含边界）
himalaya envelope list after 2025-03-31 and before 2025-04-11

# 2025年4月12日当天的邮件
himalaya envelope list date 2025-04-12
```

### 4. 主题搜索
```bash
# 简单关键词
himalaya envelope list subject 项目

# 带空格的短语
himalaya envelope list subject "会议通知"

# 转义空格（等效写法）
himalaya envelope list subject 会议\ 通知
```

### 5. 复杂组合查询
```bash
# （主题含"紧急"或正文含"报错"）且来自运维组
himalaya envelope list "(subject 紧急 or body 报错) and from ops@example.com"

# 来自老板且不是已读的
himalaya envelope list from boss@example.com and not flag seen
```

### 6. 分页浏览
```bash
# 每页 20 封，浏览第 2 页
himalaya envelope list --page 2 --page-size 20 subject 周报 order by date desc
```

### 7. 指定文件夹查询
```bash
# 在 Archives.FOSS 文件夹中查找
himalaya envelope list --folder Archives.FOSS from kernel.org
```

### 8. 线程视图
```bash
# 以线程形式查看包含某查询的邮件
himalaya envelope thread subject "产品需求"
```

---

## Himalaya DSL 到 IMAP 的映射速查

了解映射关系有助于理解服务器侧实际执行的搜索行为：

| Himalaya DSL | IMAP SEARCH 键 | 备注 |
|-------------|----------------|------|
| `date D` | `SENTON D` | 精确匹配发送日期 |
| `before D` | `SENTBEFORE D` | 不包含边界日 |
| `after D` | `SENTSINCE (D+1)` | 为排除边界，Himalaya 会替你加一天 |
| `from P` | `FROM P` | 模糊匹配发件人 |
| `to P` | `TO P` | 模糊匹配收件人 |
| `subject P` | `SUBJECT P` | 模糊匹配主题 |
| `body P` | `BODY P` | 搜索正文，性能较低 |
| `flag F` | 对应状态键 | 如 `flag seen` → `SEEN` |
| `and` | 隐式 `AND`（多个 `SearchKey::And`） | 两者都必须满足 |
| `or` | `OR` | 满足其一 |
| `not` | `NOT` | 取反 |
| `order by date desc` | `SortCriterion { reverse: true, key: Date }` | 需要服务器支持 `SORT` 扩展 |

---

## 性能与兼容性提示

1. **优先使用头部字段搜索**：`from`、`to`、`subject` 比 `body` 搜索速度快得多
2. **避免频繁全文搜索**：`body` 会触发服务器全文扫描，大量邮件时较慢
3. **排序依赖服务器能力**：
   - 若服务器支持 `SORT` 扩展，Himalaya 使用 `UID SORT` 在服务器端排序并分页
   - 若不支持，Himalaya 先 `SEARCH` 获取 UID，然后在客户端内存中排序和分页
4. **日期格式**：Himalaya 支持 `yyyy-mm-dd`、`yyyy/mm/dd`、`dd-mm-yyyy`、`dd/mm/yyyy` 四种日期格式
5. **引号与特殊字符**：查询中包含空格或括号时，请使用双引号包裹或反斜杠转义

---

## 参考文件

- Himalaya CLI 查询解析入口：`src/email/envelope/command/list.rs`
- 底层查询 AST 与 IMAP 映射：`email-lib` 中的 `src/email/envelope/list/imap.rs`
- 查询语法解析器：`email-lib` 中的 `src/email/search_query/parser.rs`
