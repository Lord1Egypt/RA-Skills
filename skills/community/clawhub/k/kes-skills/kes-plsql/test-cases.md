---
name: kes-plsql
description: KingbaseES PL/SQL 编程 — 测试用例
---

# KingbaseES PL/SQL 编程测试用例

## 测试用例 1: 存储过程创建与调用

**场景**：需要创建薪资调整存储过程

**输入问题**："金仓数据库怎么创建存储过程？"

**期望答案要点**：
- `CREATE OR ALTER PROCEDURE` 语法
- `IN`/`OUT`/`INOUT` 参数
- `CALL` 调用方式

**验证方法**：答案包含完整的存储过程创建和调用示例

---

## 测试用例 2: 触发器审计

**场景**：需要对员工表的变更做审计日志

**输入问题**："怎么在金仓数据库上创建审计触发器？"

**期望答案要点**：
- 创建触发器函数 `RETURNS TRIGGER`
- `TG_OP` 判断 INSERT/UPDATE/DELETE
- `OLD`/`NEW` 记录新旧数据
- `CREATE TRIGGER ... AFTER INSERT OR UPDATE OR DELETE`

**验证方法**：答案包含触发器函数和触发器创建语句

---

## 测试用例 3: 动态SQL防注入

**场景**：需要根据参数动态查询不同表和列

**输入问题**："金仓数据库动态SQL怎么写才安全？"

**期望答案要点**：
- 使用 `FORMAT` 的 `%I` 处理标识符
- 使用 `%L` 处理字面量
- 使用 `USING` 传参防止注入
- `quote_ident` / `quote_literal` 手动引用

**验证方法**：答案包含 FORMAT + USING 的安全动态SQL模式
