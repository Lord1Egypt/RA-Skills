---
name: kes-perl
description: KingbaseES Perl 连接 — 测试用例
---

# KingbaseES Perl 测试用例

## 测试用例 1: DBI 基础连接

**场景**：Perl 项目需要连接 KingbaseES

**输入问题**："Perl 怎么连接金仓数据库？"

**期望答案要点**：
- 使用 `DBD::KB` 驱动
- DSN 格式：`DBI:KB:dbname=TEST;host=127.0.0.1;port=54321`
- `DBI->connect()` 标准调用

**验证方法**：答案包含 DBI:KB 驱动标识和连接方法

---

## 测试用例 2: 事务操作

**场景**：Perl 脚本需要事务控制

**输入问题**："Perl DBI 怎么在金仓数据库做事务？"

**期望答案要点**：
- `$dbh->{AutoCommit} = 0`
- `$dbh->commit()` / `$dbh->rollback()`
- 使用 eval 块捕获异常

**验证方法**：答案包含 AutoCommit 设置和 commit/rollback 调用

---

## 测试用例 3: Schema 查询

**场景**：需要查询表结构和元数据

**输入问题**："Perl 怎么查询金仓数据库的表信息？"

**期望答案要点**：
- `$dbh->tables()` 获取表列表
- `$dbh->column_info()` 获取列信息
- `$dbh->primary_key_info()` 获取主键

**验证方法**：答案使用 DBI 标准 Schema 方法
