# KingbaseES 错误代码参考

包括错误代码分类、查找表、诊断流程和常见问题。

## 1. 错误代码格式

SQLSTATE 由 5 个字符组成：前 2 位表示大类，后 3 位表示具体错误。

| 前缀 | 大类 | 说明 |
|------|------|------|
| 00 | 成功 | 操作成功完成 |
| 01 | 警告 | 成功但有附加信息 |
| 02 | 无数据 | 无行影响（正常情况） |
| 08 | 连接异常 | 连接建立/维护失败 |
| 09 | 触发器异常 | 触发器处理不恰当 |
| 0A | 不支持的功能 | 调用了不支持的功能 |
| 0B | 特征不存在 | 请求的特征不存在 |
| 0F | 无效的授权规格 | 登录/密码错误或权限不足 |
| 0L | 无效角色指定 | 角色名无效或不存在 |
| 0P | 无效的外部链接 | 外部程序报错 |
| 0Z | 无效的资源规格 | 资源丢失 |
| 20 | 无法建立连接 | 新连接被拒绝 |
| 21 | 内存不足 | 内存分配失败 |
| 22 | 数据相关错误 | 数据值/格式/编码错误 |
| 23 | 完整性约束违反 | 约束冲突 |
| 24 | 无效游标状态 | 游标未打开/已关闭等 |
| 25 | 无效事务状态 | 不在事务块中/事务已中止 |
| 26 | 无效的语句标识符 | 语句名无效 |
| 27 | 触发器异常 | 触发器协议被破坏 |
| 28 | 授权失败 | 密码认证失败 |
| 2D | 无效的语句终止符 | 嵌套事务违规 |
| 34 | 无效的游标名 | 游标名不存在 |
| 3B | 无效的字符集指定 | 字符集相关错误 |
| 3D | 无效的目录规格 | 数据库不存在 |
| 3F | 无效的函数参数 | 函数参数不匹配 |
| 40 | 事务完整性 | 死锁等事务问题 |
| 42 | 语法错误 | SQL 语法/定义错误 |
| 44 | 函数执行违反 | WITH CHECK OPTION 违反 |
| 53 | 资源不足 | 磁盘/内存资源不足 |
| F0 | SQL 例行调用错误 | 存储过程异常 |
| HV | 外外部例程异常 | 外部语言例程错误 |
| 99 | 断言失败 | 内部断言失败 |
| ZZ | 其他错误 | 不属于以上类别 |

## 2. 常见错误代码速查

### 连接类 (08xxx, 28xxx, 3Dxxx)

| SQLSTATE | 错误名 | 现象 | 解决 |
|----------|--------|------|------|
| 08001 | client unable to establish connection | 无法连接数据库 | 检查实例状态、网络、sys_hba.conf |
| 08004 | server rejected the connection | 连接被拒绝 | 检查 max_connections、sys_hba.conf |
| 08006 | connection failure | 连接中途断开 | 检查防火墙、wait_timeout |
| 28000 | invalid authorisation specification | 密码/用户名错误 | 确认 credentials、密码是否过期 |
| 3D000 | invalid catalog name | 数据库不存在 | 确认数据库名、使用 sys_database 查看 |

### 数据类 (22xxx)

| SQLSTATE | 错误名 | 现象 | 解决 |
|----------|--------|------|------|
| 22001 | string data right truncation | 字符串超长 | 增大列宽度、截断数据 |
| 22003 | numeric value out of range | 数值溢出 | 检查数据类型范围 |
| 22004 | null value not allowed | NULL 赋值给 NOT NULL 列 | 检查约束、提供默认值 |
| 22007 | invalid datetime format | 日期格式错误 | 使用正确格式、TO_DATE |
| 22008 | timezone displacement out of range | 时区偏移无效 | 检查时区设置 |
| 22012 | division by zero | 除以零 | 加 NULLIF |
| 22021 | case not found | CASE 无匹配分支 | 加 ELSE 兜底 |
| 22023 | invalid use of escape character | 转义字符错误 | 检查 ESCAPE 语法 |
| 22025 | invalid argument for logarithm | 对数参数无效 | 检查参数 > 0 |
| 22027 | invalid argument for power | 幂函数参数无效 | 检查负数开方 |
| 22P02 | error in assignment | PL/SQL 赋值类型不匹配 | 检查隐式转换 |
| 22P04 | bad copy file format | COPY 文件格式错误 | 检查分隔符、编码 |

### 约束类 (23xxx)

| SQLSTATE | 错误名 | 现象 | 解决 |
|----------|--------|------|------|
| 23505 | duplicate key value | 唯一键冲突 | 检查唯一约束、UPSERT |
| 23503 | foreign key violation | 外键约束违反 | 检查引用值是否存在 |
| 23502 | not null violation | NOT NULL 约束违反 | 检查必填列 |
| 23514 | check violation | CHECK 约束违反 | 检查约束条件 |
| 23P01 | foreign key error on DELETE | 删除时外键冲突 | 先删子记录或 ON DELETE CASCADE |

### 事务类 (25xxx, 40xxx)

| SQLSTATE | 错误名 | 现象 | 解决 |
|----------|--------|------|------|
| 25000 | invalid transaction state | 不在事务中执行 COMMIT/ROLLBACK | 使用 BEGIN |
| 25P02 | transaction rollback | 事务因错误被回滚 | 处理错误后重试 |
| 40001 | serialization failure | 可串行化隔离冲突 | 重放事务 |
| 40P01 | deadlock detected | 检测到死锁 | 调整锁顺序 |

### 语法类 (42xxx)

| SQLSTATE | 错误名 | 现象 | 解决 |
|----------|--------|------|------|
| 42601 | syntax error | SQL 语法错误 | 检查语法、保留字加引号 |
| 42702 | ambiguous column | 列名歧义 | 加表别名限定 |
| 42703 | undefined column | 列不存在 | 检查列名、大小写 |
| 42P01 | undefined table | 表不存在 | 检查表名、search_path |
| 42P07 | duplicate table | 表已存在 | 加 IF NOT EXISTS |
| 42P06 | duplicate column | 列名重复 | 修改列名 |
| 42601 | syntax error at or near | 语法错误 | 检查关键字拼写 |

### 权限类 (42501, 28xxx)

| SQLSTATE | 错误名 | 现象 | 解决 |
|----------|--------|------|------|
| 42501 | insufficient privilege | 权限不足 | GRANT 授权 |
| 28000 | invalid authorisation specification | 认证失败 | 检查密码 |

### 资源类 (53xxx)

| SQLSTATE | 错误名 | 现象 | 解决 |
|----------|--------|------|------|
| 53100 | disk full | 磁盘空间不足 | 清理磁盘、扩展表空间 |
| 53200 | out of memory | 内存不足 | 增大 work_mem、减少并发 |
| 53300 | too many connections | 连接数超限 | 增大 max_connections |
| 57014 | query canceled | 语句超时 | 增大 statement_timeout |

## 3. 错误诊断流程

```
错误发生
  → 读取 SQLSTATE + 错误消息
  → 按前缀定位大类
  → 查速查表定位具体原因
  → 确认上下文（表结构、数据、权限）
  → 应用解决方案
  → 验证修复
```

### 错误信息查询

```sql
-- 查看最后一条错误（需在事务中）
SELECT * FROM sys_last_error();

-- 在 PL/SQL 中捕获错误
BEGIN
    -- 可能出错的语句
EXCEPTION
    WHEN duplicate_value THEN
        RAISE NOTICE '唯一键冲突: %', SQLERRM;
    WHEN foreign_key_violation THEN
        RAISE NOTICE '外键冲突: %', SQLERRM;
    WHEN OTHERS THEN
        RAISE NOTICE '错误代码: %, 消息: %', SQLSTATE, SQLERRM;
END;
```

### 日志中查找错误

```bash
# 查看最近错误
tail -100 $KINGBASE_HOME/data/log/kingbase.log | grep -i "ERROR\|FATAL\|PANIC"

# 按日期查找
grep "2026-06-16" $KINGBASE_HOME/data/log/kingbase.log | grep -i ERROR
```

## 4. 关键原则

1. **SQLSTATE 优先**：错误消息可能因语言设置不同，SQLSTATE 是稳定的
2. **25P02 连锁错误**：事务中一个语句失败后，后续语句都会报 25P02，需 ROLLBACK 重试
3. **40P01 死锁**：不要简单地加大超时，需调整事务锁顺序
### 兼容模式差异

| 兼容模式 | 说明 |
|---------|------|
| Oracle 模式 | 部分错误代码与标准模式不同，错误消息使用Oracle风格编号（ORA-xxxxx） |
| MySQL 模式 | 错误代码映射到MySQL编号，消息格式与MySQL兼容 |
| SQLServer 模式 | 错误代码映射到SQLServer编号，消息格式与SQLServer兼容 |
