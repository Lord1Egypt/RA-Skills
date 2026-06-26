# MQL 语法规范参考

> **重要：`workitem query` 的 `--search-mql` 参数必须是完整的 SQL 查询语句**
> - 必须包含 `SELECT` 和 `FROM` 子句
> - 不接受 JSON 对象、简写条件或不完整片段
> - 正确: `` SELECT `工作项ID`, `名称` FROM `空间名`.`需求` WHERE `状态` = '进行中' ``
> - 错误: `{"status": "进行中"}` / `status = '进行中'` / `WHERE status = '进行中'`

## 基础语法

```sql
SELECT fieldList                            -- 指定查询的字段列表
FROM `空间名`.`工作项类型名`                   -- 指定数据来源
WHERE conditionExpression                    -- 查询条件（可选）
[ORDER BY fieldOrderByList [{ASC|DESC}]]     -- 排序（可选）
[LIMIT [offset,] row_count]                  -- 分页（可选）
```

**标识符规则**：
- 所有字段名和表名必须使用反引号包裹，如 `` `工作项ID` ``、`` `空间名`.`需求` ``
- SELECT/FROM/WHERE/ORDER BY 中既可使用 key 也可使用名称。**优先使用 key**，从 `workitem meta-fields` 返回值中获取：系统字段 key 为单词（如 `priority`、`status`），自定义字段 key 为 `field_x23bd` 格式，工作项类型 key 如 `story`、`issue`。名称是用户自定义的 UGC 内容（语言不定），仅作为找不到 key 时的兜底
- **禁止** `count()`、`SUM()`、`GROUP BY`。总数从返回结果的 `count` 字段读取

---

## 数据类型

| MQL 类型 | 说明 | 对应的工作项字段类型 |
|-----------|------|-------------------|
| bool | 真假值，取值 TRUE/FALSE/1/0 | bool |
| bigint | 整数类型 | number 类型下的 work_item_id 和 auto_number |
| double | 浮点数类型 | 除 work_item_id/auto_number 外的其他 number |
| varchar | 字符串类型 | text、multi-pure-text、multi-text、select、tree-select、radio、user、link、signal、workitem_related_select |
| date | 日期类型，格式 `YYYY-MM-DD` 或 `YYYY-MM-DD+TZD`（如 `2025-12-24+08:00`） | date |
| datetime | 日期时间类型，格式 `YYYY-MM-DDThh:mm:ss` 或 `YYYY-MM-DDThh:mm:ssTZD` | schedule、precise_date |
| array(varchar) | 字符串数组 | multi-select、tree-multi-select、multi-user、link_cloud_doc、workitem_related_multi_select、multi-file |
| array(struct) | 结构体数组 | compound_field |
| lambda expression | 返回 bool 的函数表达式，写法：`x -> x > 10`、`x -> x in ('a', 'b')` | — |

---

## 常用运算符

### BETWEEN ... AND ...

标准 SQL 区间查询，适用于日期和数值字段：

```sql
WHERE `创建时间` BETWEEN '2025-01-01' AND '2025-10-01'
```

### LIKE / NOT LIKE

模糊匹配，`%` 匹配任意字符：

```sql
WHERE `缺陷名` LIKE '%性能问题%'
WHERE `缺陷名` NOT LIKE '%后端性能问题%'
```

---

## 常用函数

### 数组函数

| 函数 | 说明 |
|------|------|
| `array_cardinality(array_col)` | 获取数组长度 |
| `array_contains(array_col, element [, element2, ...])` | 数组是否包含某元素（多值表示包含其中之一） |
| `any_match(array_col, predicate)` | 是否有任一元素满足条件 |
| `all_match(array_col, predicate)` | 是否所有元素满足条件 |
| `none_match(array_col, predicate)` | 是否所有元素都不满足条件 |
| `array_filter(array_col, predicate)` | 根据条件过滤数组，返回新数组 |

**示例**：
```sql
-- 当前负责人包含张三
array_contains(`当前负责人`, '张三')

-- 优先级包含 P0 或 P1
array_contains(`优先级`, 'P0', 'P1')

-- 当前负责人包含当前登录用户或李四
any_match(`当前负责人`, x -> x in (current_login_user(), '李四'))

-- 所有处理人都在后端团队中
all_match(`处理人`, usr -> usr in team(true, '后端开发团队'))

-- 标签数组为空
array_cardinality(`标签`) = 0
```

### 时间函数

支持的函数：`RELATIVE_DATETIME_EQ`、`RELATIVE_DATETIME_GT`、`RELATIVE_DATETIME_GE`、`RELATIVE_DATETIME_LT`、`RELATIVE_DATETIME_LE`、`RELATIVE_DATETIME_BETWEEN`

函数签名：`RELATIVE_DATETIME_*(col_name, 'date_para', ['days'])`

**date_para 枚举值**：

| 枚举 | 含义 | 是否支持 days 参数 |
|------|------|-------------------|
| today | 当天 | 支持（正值向后偏移，负值向前偏移） |
| tomorrow | 明天 | 不支持 |
| yesterday | 昨天 | 不支持 |
| current_week | 当周 | 不支持 |
| next_week | 下周 | 不支持 |
| last_week | 上周 | 不支持 |
| current_month | 当月 | 不支持 |
| next_month | 下月 | 不支持 |
| last_month | 上月 | 不支持 |
| future | 从今天起的未来范围 | 支持 |
| past | 从今天起的过去范围 | 支持 |

**days 参数**：仅 `today`、`future`、`past` 支持。格式为 `'Nd'` 或 `'-Nd'`。

**示例**：
```sql
-- 今天创建的工作项
RELATIVE_DATETIME_EQ(`创建时间`, 'today')

-- 3天内到期的工作项
RELATIVE_DATETIME_LE(`截止时间`, 'future', '3d')

-- 上周创建的需求
RELATIVE_DATETIME_BETWEEN(`创建时间`, 'last_week')

-- 本月更新的任务
RELATIVE_DATETIME_BETWEEN(`更新时间`, 'current_month')

-- 今天后 3 天
RELATIVE_DATETIME_EQ(`创建时间`, 'today', '3d')

-- 今天前 3 天
RELATIVE_DATETIME_EQ(`创建时间`, 'today', '-3d')

-- 排期开始时间在过去 30 天内
RELATIVE_DATETIME_BETWEEN(`__需求排期_开始时间`, 'past', '30d')
```

### 人员与角色函数

| 函数 | 说明 |
|------|------|
| `current_login_user()` | 返回当前登录用户的 userkey |
| `team(include_manager, '团队名')` | 返回团队成员 userkey 数组（第一个参数 true 表示包含管理者） |
| `all_participate_persons()` | 返回所有参与当前工作项的人员 userkey 数组 |
| `participate_roles()` | 返回所有参与角色的 rolekey 数组（如 RD、QA、PM） |

**示例**：
```sql
-- 当前负责人是当前登录用户
array_contains(`当前负责人`, current_login_user())

-- 指派给产品团队（含管理者）
any_match(`当前负责人`, x -> x in team(true, '产品团队'))

-- 查询有 RD 和 QA 角色参与的工作项
WHERE array_contains(participate_roles(), 'RD', 'QA')
```

---

## 名称消歧（`<id:xxxx>` 语法）

当人名、团队名等存在重复时，MQL 会因无法唯一标识而报错。此时使用 `<id:xxxx>` 语法指定唯一 ID：

```sql
-- 人名消歧：张三对应多人时，指定 userkey
WHERE `创建人` = '张三<id:1234>'

-- 团队名消歧：指定团队唯一 key
WHERE any_match(`负责人`, x -> x in (team(true, '开放平台团队<id:3455>')))
```

遇到 MQL 返回"名称重复"类错误时，需获取对应的唯一 ID 后使用此语法重试。

---

## 特殊字段查询规则

### 日期区间类型字段

日期区间类型（如"需求排期"）不能直接查询，必须拆分为子字段，格式：`` `__排期名_开始时间` `` / `` `__排期名_结束时间` ``

```sql
-- 正确：使用子字段
WHERE `__开发周期_开始时间` > '2025-01-01' AND `__开发周期_结束时间` < '2025-01-31'
WHERE RELATIVE_DATETIME_BETWEEN(`__需求排期_开始时间`, 'past', '30d')

-- 错误：直接查询日期区间字段
WHERE RELATIVE_DATETIME_BETWEEN(`需求排期`, 'past', '30d')
```

### 角色字段

角色可作为 MQL 属性查询，使用 `__角色名` 格式（加 `__` 前缀以区分普通自定义字段）：

```sql
-- 查询 RD 包含某人的工作项
WHERE array_contains(`__RD`, '张三')

-- 查询多个角色条件
WHERE array_contains(`__RD`, '张三') AND array_contains(`__PM`, '李四')
```

---

## 完整查询示例

> 以下示例优先使用字段 key。字段 key 从 `workitem meta-fields` 返回值获取；找不到 key 时可用中文字段名兜底。

### 示例 1：查询空间下我参与的 P0 需求

```sql
SELECT `work_item_id`, `name`, `priority`, `current_owners`, `status`
FROM `空间名`.`story`
WHERE array_contains(`priority`, 'P0')
  AND array_contains(all_participate_persons(), current_login_user())
```

### 示例 2：查询最近一周创建的缺陷

```sql
SELECT `work_item_id`, `name`, `created_by`, `created_at`, `status`
FROM `空间名`.`issue`
WHERE RELATIVE_DATETIME_BETWEEN(`created_at`, 'past', '7d')
```

### 示例 3：查询逾期未完成的任务

```sql
-- __需求排期_结束时间 为排期子字段，名称因空间配置而异，需从 workitem meta-fields 确认
SELECT `work_item_id`, `name`, `current_owners`, `__需求排期_结束时间`, `status`
FROM `空间名`.`task`
WHERE RELATIVE_DATETIME_LT(`__需求排期_结束时间`, 'today')
  AND `status` != '已完成'
```

### 示例 4：查询某团队 RD 负责的需求

```sql
SELECT `work_item_id`, `name`, `__RD`, `status`
FROM `空间名`.`story`
WHERE any_match(`__RD`, x -> x in (team(true, '开放平台团队')))
```

### 示例 5：查询我创建的进行中的需求（带排序和分页）

```sql
SELECT `work_item_id`, `name`, `priority`, `status`
FROM `空间名`.`story`
WHERE `created_by` = current_login_user()
  AND `status` = '进行中'
ORDER BY `created_at` DESC
LIMIT 20
```

### 示例 6：模糊匹配 + 当前登录用户

```sql
SELECT `work_item_id`, `name`
FROM `空间名`.`issue`
WHERE `name` NOT LIKE '%后端性能问题%'
  AND array_contains(all_participate_persons(), '李四')
  AND `assigned_to` = current_login_user()
ORDER BY `created_at` ASC
LIMIT 10
```
