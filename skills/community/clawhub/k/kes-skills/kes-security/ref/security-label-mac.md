# KingbaseES 标签与MAC强制访问控制

通过 sysmac 插件实现标记和强制访问控制，按密级和分类保护用户数据，防止未授权访问。

## 1. sysmac 插件概述

KingbaseES 通过 sysmac 插件实现强制访问控制功能。

### 加载方法

```sql
# kingbase.conf
shared_preload_libraries = 'sysmac'
```

修改后重启数据库加载插件。

### 配置参数

| 参数名 | 取值范围 | 默认值 | 描述 |
|--------|---------|--------|------|
| sysmac.enable_mac | on/off | off | 控制强制访问控制是否打开 |
| sysmac.enable_col_mac | on/off | off | 控制列级强制访问控制是否打开 |

```sql
-- 开启行级和对象级强访
ALTER SYSTEM SET sysmac.enable_mac = on;
SELECT sys_reload_conf();

-- 开启列级强访（需先开启 mac）
ALTER SYSTEM SET sysmac.enable_col_mac = on;
SELECT sys_reload_conf();
```

## 2. 标记元素

标记包含两个元素：等级（level）和范围（compartment）。

- **等级**：代表数据敏感度，数值越大级别越高。例如：普通、秘密、机密
- **范围**：用于数据分类。例如：陆军、海军、空军

### 标记语法

```
<等级>:[<范围>{,<范围>}]
```

示例：
- `机密:` -- 仅包含等级
- `秘密:空军,陆军` -- 包含等级和范围集合

### 标记比较

| 关系 | 形式化定义 |
|------|-----------|
| A = B | LEVEL(A) = LEVEL(B) AND COMPARTMENT(A) = COMPARTMENT(B) |
| A > B | LEVEL(A) > LEVEL(B) AND COMPARTMENT(A) >= COMPARTMENT(B)，或 LEVEL(A) = LEVEL(B) AND COMPARTMENT(A) > COMPARTMENT(B) |
| A 支配 B | A = B OR A > B |
| A, B 不可比较 | COMPARTMENT(A) 和 COMPARTMENT(B) 互不包含 |

等级比较依据 levid 数值大小，范围比较依据集合包含关系。

## 3. 策略管理

所有强访操作以策略（policy）为单位管理。不同策略彼此独立，不同策略下的标记无法比较。

### 创建策略

```sql
-- sysmac.create_policy(policy_name, column_name, hide_column)
-- policy_name: 策略名称（数据库内唯一）
-- column_name: 策略列名称（应用于表时自动添加）
-- hide_column: true=隐藏策略列, false=不隐藏

SELECT sysmac.create_policy('p1', 'p1_column', true);
```

### 禁用/启用策略

```sql
-- 禁用策略（不删除，仅停止执行访问控制）
SELECT sysmac.disable_policy('p1');

-- 启用策略
SELECT sysmac.enable_policy('p1');
```

### 删除策略

```sql
-- sysmac.drop_policy(policy_name, drop_column)
-- 删除策略及其下所有数据标记和用户会话标记
-- drop_column: true=同时删除表中的策略列

SELECT sysmac.drop_policy('p1', true);
```

## 4. 等级/范围/标记 CRUD

### 创建等级

```sql
-- sysmac.create_level(policy_name, level_name, levid)
-- levid 取值范围 [1,9999]，数值越大级别越高，策略下唯一

SELECT sysmac.create_level('p1', 'general', 10);
SELECT sysmac.create_level('p1', 'privacy', 20);
SELECT sysmac.create_level('p1', 'secret', 30);
```

### 删除等级

```sql
SELECT sysmac.drop_level('p1', 'general');
SELECT sysmac.drop_level('p1', 10);
```

### 创建范围

```sql
-- sysmac.create_compartment(policy_name, comp_name, comp_id)
-- comp_id 取值范围 [1,9999]，策略下唯一

SELECT sysmac.create_compartment('p1', 'manager', 40);
SELECT sysmac.create_compartment('p1', 'qa', 30);
SELECT sysmac.create_compartment('p1', 'rd', 20);
```

### 删除范围

```sql
SELECT sysmac.drop_compartment('p1', 'manager');
SELECT sysmac.drop_compartment('p1', 40);
```

### 创建标记

```sql
-- sysmac.create_label(policy_name, label, labelid)
-- labelid 取值范围 [1,99999999]，数据库下唯一

SELECT sysmac.create_label('p1', 'general:rd', 11);
SELECT sysmac.create_label('p1', 'privacy:qa,rd', 21);
SELECT sysmac.create_label('p1', 'secret:manager,qa', 31);
```

### 修改标记

```sql
SELECT sysmac.alter_label('p1', 'general:rd', 'general:rd,qa');
SELECT sysmac.alter_label('p1', 11, 'general:rd,qa');
```

### 删除标记

```sql
SELECT sysmac.drop_label('p1', 'general:rd');
SELECT sysmac.drop_label('p1', 11);
```

### 标记 ID 与字符串转换

```sql
-- ID 转标记字符串
SELECT sysmac.label_to_char(11);
-- general:rd

-- 标记字符串转 ID
SELECT sysmac.char_to_label('p1', 'general:rd');
-- 11
```

### 标记比较

```sql
-- sysmac.mac_label_compare(policy_name, label_string1, label_string2)
-- 返回值：EQUAL / STRICTLY_DOMINATES / STRICTLY_DOMINATED_BY / NON_COMPARABLE

SELECT sysmac.mac_label_compare('p1', 'privacy:rd', 'privacy:qa,rd');
-- STRICTLY_DOMINATED_BY（privacy:rd 被 privacy:qa,rd 支配）

SELECT sysmac.mac_label_compare('p1', 'privacy:rd', 'privacy:rd');
-- EQUAL
```

## 5. 用户标签配置

### 授予用户等级

```sql
-- sysmac.set_levels(policy_name, username, max_level, min_level, def_level, row_level)
-- max_level: 读写访问最高等级
-- min_level: 写访问最低等级（必须 <= max_level）
-- def_level: 默认会话等级（必须 <= row_level）
-- row_level: 写入等级（必须 <= max_level）

SELECT sysmac.set_levels('p1', 'u1', 'secret', 'general', 'privacy', 'privacy');
```

### 授予用户范围

```sql
-- sysmac.set_compartments(policy_name, username, read_compartments, max_write_compartments, default_compartments, row_compartments, min_write_compartments)
-- 必须先授予等级再授予范围

SELECT sysmac.set_compartments('p1', 'u1',
    'manager,qa,rd',       -- 读范围
    'manager,qa',          -- 最大写范围
    'manager',             -- 默认范围
    'manager,qa',          -- 写入范围
    'manager'              -- 最小写范围
);
```

### 授予用户标记（推荐）

通过标记同时设置等级和范围：

```sql
-- sysmac.set_user_labels(policy_name, username, max_read_label, max_write_label, min_write_label, def_label, row_label)

SELECT sysmac.set_user_labels('p1', 'u1',
    'secret:manager,qa,rd',     -- 最大读标记
    'secret:manager,qa',        -- 最大写标记
    'general:',                 -- 最小写标记
    'privacy:manager',          -- 默认会话标记
    'privacy:manager,qa'        -- 写入标记
);
```

### 设置用户默认标记

```sql
-- sysmac.set_default_label(policy_name, username, label)

SELECT sysmac.set_default_label('p1', 'u1', 'privacy:manager');
```

### 设置用户默认写入标记

```sql
-- sysmac.set_def_row_label(policy_name, username, label)

SELECT sysmac.set_def_row_label('p1', 'u1', 'privacy:manager,qa');
```

### 回收用户所有权限

```sql
SELECT sysmac.drop_user_access('p1', 'u1');
```

## 6. 策略特权

| 特权 | 说明 |
|------|------|
| READ | 读取策略保护的所有数据，仍按标记仲裁写 |
| FULL | 读写策略保护的所有数据，不受 MAC 限制 |
| WRITEUP | 提升数据标记等级（只能提升到用户最大等级），不能修改范围 |
| WRITEDOWN | 降低数据标记等级（只能降低到用户最小等级），不能修改范围 |
| WRITEACROSS | 修改数据标记范围（新范围必须是用户最大写范围的子集），不能修改等级 |

```sql
-- 授予特权
SELECT sysmac.set_user_privs('p1', 'u1', 'READ');
SELECT sysmac.set_user_privs('p1', 'u1', 'FULL,WRITEUP');

-- 回收所有特权
SELECT sysmac.set_user_privs('p1', 'u1', NULL);
```

## 7. 行级 MAC 完整示例

以下为例演示行级强访的完整流程：

```sql
-- Step 1: sso 开启强访
\c - sso
ALTER SYSTEM SET sysmac.enable_mac = on;
SELECT sys_reload_conf();

-- Step 2: sso 创建策略、等级、范围
SELECT sysmac.create_policy('p1', 'p1_column', true);
SELECT sysmac.create_level('p1', 'general', 10);
SELECT sysmac.create_level('p1', 'privacy', 20);
SELECT sysmac.create_level('p1', 'secret', 30);
SELECT sysmac.create_compartment('p1', 'manager', 40);
SELECT sysmac.create_compartment('p1', 'qa', 30);
SELECT sysmac.create_compartment('p1', 'rd', 20);
SELECT sysmac.create_compartment('p1', 'unimportant', 10);

-- Step 3: system 创建用户
\c - system
CREATE USER urd_manager WITH PASSWORD '12345678ab';
CREATE USER uqa_manager WITH PASSWORD '12345678ab';
CREATE USER ugeneral_manager WITH PASSWORD '12345678ab';

-- Step 4: sso 设置用户标记
\c - sso
SELECT sysmac.set_user_labels('p1', 'ugeneral_manager',
    'secret:manager,qa,unimportant', 'secret:manager,qa', 'secret:', 'secret:', 'secret:manager,qa');
SELECT sysmac.set_user_labels('p1', 'uqa_manager',
    'privacy:rd,unimportant', 'privacy:rd', 'privacy:rd', 'privacy:rd', 'privacy:rd');
SELECT sysmac.set_user_labels('p1', 'urd_manager',
    'privacy:qa,rd,unimportant', 'privacy:qa,rd', 'privacy:qa,rd', 'privacy:qa,rd', 'privacy:qa,rd');

-- Step 5: system 创建表并授权
\c - system
CREATE TABLE tu_info(id INT, name CHAR(10));
GRANT ALL ON tu_info TO uqa_manager;
GRANT ALL ON tu_info TO urd_manager;
GRANT ALL ON tu_info TO ugeneral_manager;

-- Step 6: sso 将策略应用于表
\c - sso
SELECT sysmac.apply_table_policy('p1', 'public', 'tu_info');

-- Step 7: sso 创建数据标记
CALL sysmac.create_label('p1', 'general:unimportant', 11);
CALL sysmac.create_label('p1', 'privacy:qa', 21);
CALL sysmac.create_label('p1', 'privacy:rd', 22);
CALL sysmac.create_label('p1', 'privacy:qa,rd', 25);

-- Step 8: uqa_manager 写入数据
\c - uqa_manager
INSERT INTO tu_info VALUES (1, 'wang');
-- 该行自动获得 uqa_manager 的写入标记 privacy:rd (labelid=22)

-- Step 9: urd_manager 写入数据
\c - urd_manager
INSERT INTO tu_info VALUES (2, 'zhang');
-- 该行自动获得 urd_manager 的写入标记 privacy:qa,rd (labelid=25)

-- Step 10: urd_manager 查询数据
SELECT p1_column, * FROM tu_info;
-- p1_column | id | name
-- 22        |  1 | wang     -- 可读（privacy:rd 被 urd_manager 标记支配）
-- 25        |  2 | zhang    -- 可读（标记相等）

-- Step 11: urd_manager 尝试修改 uqa_manager 的数据
UPDATE tu_info SET name = 'wang1' WHERE id = 1;
-- ERROR:  对于策略p1没有写访问权限

-- Step 12: urd_manager 修改自己的数据
UPDATE tu_info SET name = 'zhang1' WHERE id = 2;
-- UPDATE 1

-- Step 13: 清理环境
\c - sso
CALL sysmac.remove_table_policy('p1', 'public', 'tu_info', true);
CALL sysmac.drop_user_access('p1', 'urd_manager');
CALL sysmac.drop_user_access('p1', 'uqa_manager');
CALL sysmac.drop_user_access('p1', 'ugeneral_manager');
CALL sysmac.drop_policy('p1', true);

\c - system
DROP TABLE tu_info;
DROP USER urd_manager;
DROP USER uqa_manager;
DROP USER ugeneral_manager;
```

## 8. 对象级 MAC 示例

对象级强访支持：table、view、index、procedure、function、package、sequence、trigger、synonym。

```sql
-- sso 创建策略和标记
\c - sso
CALL sysmac.create_policy('p1', 'p1_column', false);
CALL sysmac.create_level('p1', 'l1', 10);
CALL sysmac.create_level('p1', 'l2', 20);
CALL sysmac.create_level('p1', 'l3', 30);
CALL sysmac.create_compartment('p1', 'c1', 100);
CALL sysmac.create_label('p1', 'l1:c1', 50);
CALL sysmac.create_label('p1', 'l2:c1', 60);
CALL sysmac.create_label('p1', 'l3:c1', 70);

-- system 创建用户、表和授权
\c - system
CREATE USER u_mac1 WITH PASSWORD '12345678ab';
CREATE USER u_mac2 WITH PASSWORD '12345678ab';
CREATE TABLE t_mac1(a INT);
GRANT ALL ON t_mac1 TO u_mac1;
GRANT ALL ON t_mac1 TO u_mac2;

-- sso 设置用户标记和对象标记
\c - sso
CALL sysmac.set_user_labels('p1', 'u_mac1', 'l3:c1', 'l3:c1', 'l3:c1', 'l3:c1', 'l3:c1');
CALL sysmac.set_user_labels('p1', 'u_mac2', 'l1:c1', 'l1:c1', 'l1:c1', 'l1:c1', 'l1:c1');

-- 对表设置对象级标记 l2:c1（高于 u_mac2 的 l1:c1，低于 u_mac1 的 l3:c1）
CALL sysmac.apply_obj_policy('p1', 'table', 'public', 't_mac1', 'l2:c1');

-- u_mac1 操作成功（标记 l3:c1 支配对象标记 l2:c1）
\c - u_mac1
INSERT INTO t_mac1 VALUES (1);
SELECT * FROM t_mac1;

-- u_mac2 操作失败（标记 l1:c1 被对象标记 l2:c1 支配）
\c - u_mac2
SELECT * FROM t_mac1;
-- ERROR:  table未经许可访问策略p1

-- 删除对象标记
\c - sso
CALL sysmac.drop_obj_policy('p1', 'table', 'public', 't_mac1');
```

## 9. 列级 MAC 示例

列级强访需开启 `sysmac.enable_col_mac` 参数，仅支持普通表。

```sql
-- sso 开启列级强访
\c - sso
ALTER SYSTEM SET sysmac.enable_mac = on;
ALTER SYSTEM SET sysmac.enable_col_mac = on;
SELECT sys_reload_conf();

-- sso 创建策略、等级、范围、标记
CALL sysmac.create_policy('p1', 'p1_column', false);
CALL sysmac.create_level('p1', 'l1', 10);
CALL sysmac.create_level('p1', 'l2', 20);
CALL sysmac.create_level('p1', 'l3', 30);
CALL sysmac.create_compartment('p1', 'c1', 100);
CALL sysmac.create_label('p1', 'l1:c1', 50);
CALL sysmac.create_label('p1', 'l2:c1', 60);

-- system 创建用户和表
\c - system
CREATE USER u_mac1 WITH PASSWORD '12345678ab';
CREATE USER u_mac2 WITH PASSWORD '12345678ab';
CREATE TABLE t_mac2(a INT, b VARCHAR(10));
GRANT ALL ON t_mac2 TO u_mac1;
GRANT ALL ON t_mac2 TO u_mac2;

-- sso 设置用户标记
\c - sso
CALL sysmac.set_user_labels('p1', 'u_mac1', 'l3:c1', 'l3:c1', 'l2:c1', 'l2:c1', 'l2:c1');
CALL sysmac.set_user_labels('p1', 'u_mac2', 'l1:c1', 'l1:c1', 'l1:c1', 'l1:c1', 'l1:c1');

-- sso 设置列级标记（b 列标记为 l2:c1）
CALL sysmac.set_column_label('p1', 'public', 't_mac2', 'b', 'l2:c1');

-- u_mac1 操作成功（写入标记 l2:c1 >= 列标记 l2:c1）
\c - u_mac1
INSERT INTO t_mac2 VALUES (1, 'hello');
SELECT * FROM t_mac2;

-- u_mac2 访问 b 列失败（标记 l1:c1 < 列标记 l2:c1）
\c - u_mac2
SELECT * FROM t_mac2;
-- ERROR:  策略p1的未授权读访问
SELECT a FROM t_mac2;
-- 成功（a 列无标记限制）

-- u_mac2 只操作 a 列
INSERT INTO t_mac2(a) VALUES (2);
UPDATE t_mac2 SET a = 3;

-- 清理
\c - sso
CALL sysmac.drop_column_label('p1', 'public', 't_mac2', 'b');
CALL sysmac.drop_user_access('p1', 'u_mac1');
CALL sysmac.drop_user_access('p1', 'u_mac2');
CALL sysmac.drop_policy('p1', true);
ALTER SYSTEM SET sysmac.enable_col_mac = off;
SELECT sys_reload_conf();
```

## 10. 读写访问仲裁规则

KingbaseES 强访遵循"向下读，区间写"模型：

### 读访问规则

- 数据标记等级 <= 用户当前读标记等级
- 用户会话读标记必须包含数据标记中的所有范围

即用户只能读取等级相同或更低的数据，且必须具备数据所在的所有范围权限。

### 写访问规则（上写模型）

- 数据标记等级 <= 用户当前写标记等级
- 数据标记等级 >= 用户最小等级
- 用户会话写标记必须包含数据标记中的所有范围

即用户只能写入等级在自己最小和最大等级之间的数据。信息流向总是向上（从低密级到高密级），防止高密级信息被降级泄露。

### 标记检查顺序

表上有强制访问控制策略时，依次检查：表级强访 -> 列级强访 -> 行级强访。

## 11. 常见问题

### 问题1：用户无法读取数据

**排查**：
```sql
-- 检查用户标记
-- 检查数据标记
-- 确认用户标记支配数据标记
SELECT sysmac.mac_label_compare('p1', '数据标记', '用户标记');
-- 应返回 EQUAL 或 STRICTLY_DOMINATES
```

### 问题2：写入被拒绝

**原因**：用户写入等级不在数据标记的等级区间内。

**解决**：
- 调整用户的最小/最大写入等级
- 使用 WRITEUP 特权允许提升标记等级

### 问题3：策略列名称冲突

**原因**：同一数据库下策略列名称必须唯一。创建策略时指定的 column_name 不可重复。

**解决**：为每个策略使用不同的列名，如 p1_column、p2_column。

### 问题4：行级策略不适用于分区表

行级强访仅支持普通表，不支持分区表、系统表、临时表、外部表、物化视图。

## 最佳实践

1. 由 sso 用户统一管理策略、等级、范围和标记
2. 使用 set_user_labels 一次性设置用户所有标记
3. 生产环境策略列建议隐藏（hide_column=true）
4. 标记 ID 规划预留充足空间
5. 清理时先移除表策略，再回收用户权限，最后删除策略
6. 列级强访仅对特定敏感列使用，避免全表启用
