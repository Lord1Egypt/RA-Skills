---
name: kes-plsql
name_for_command: kes-plsql
description: KingbaseES PL/SQL 编程指南。当用户提到存储过程、函数、触发器、游标、包(Package)、PL/SQL、匿名块、动态SQL、异常处理时，必须使用此技能。
---

# KingbaseES PL/SQL 编程指南

本技能指导用户完成 KingbaseES 的过程化 SQL 编程，涵盖存储过程、函数、触发器、游标、包和异常处理。

**重要**：PL/SQL 函数始终使用金仓原生语法，与 Oracle 兼容模式无关。

## 管理模块

| 场景 | 操作 | 参考 |
|------|------|------|
| 匿名块 | DO $$ ... $$ | `ref/plsql.md` §1 |
| 控制结构 | IF/LOOP/CASE | `ref/plsql.md` §2 |
| 存储过程 | CREATE PROCEDURE | `ref/plsql.md` §3 |
| 函数 | CREATE FUNCTION | `ref/plsql.md` §4 |
| 触发器 | CREATE TRIGGER | `ref/plsql.md` §5 |
| 游标 | CURSOR/REFCURSOR | `ref/plsql.md` §6 |
| 包 | PACKAGE | `ref/plsql.md` §7 |
| 异常处理 | EXCEPTION/RAISE | `ref/plsql.md` §8 |
| 动态SQL | EXECUTE/FORMAT | `ref/plsql.md` §9 |
| 日志调试 | RAISE/LOG | `ref/plsql.md` §10 |

## 快速入门

```sql
-- 匿名块
BEGIN
    DECLARE v_count INT;
    SELECT count(*) INTO v_count FROM sys_tables;
    RAISE NOTICE '表数量: %', v_count;
END;

-- 存储过程
CREATE OR ALTER PROCEDURE update_salary(IN p_id INT, IN p_rate DECIMAL)
AS
BEGIN
    UPDATE employees SET salary = salary * (1 + p_rate / 100) WHERE id = p_id;
END;
CALL update_salary(1, 10.00);

-- 函数
CREATE OR ALTER FUNCTION calc_bonus(p_salary DECIMAL, p_grade CHAR)
RETURNS DECIMAL
AS
BEGIN
    RETURN p_salary * CASE p_grade
        WHEN 'S' THEN 0.30 WHEN 'A' THEN 0.20 ELSE 0.10
    END;
END;
SELECT calc_bonus(15000, 'A');
```

## 命名规范

```
v_  - 局部变量    p_  - 参数    c_  - 常量
g_  - 全局变量    r_  - 记录    cur_ - 游标
fn_   - 函数      proc_ - 过程  trg_  - 触发器  pkg_ - 包
```

## 安全提醒

1. 使用 `USING` 参数防止 SQL 注入
2. 动态表名/列名用 `quote_ident`
3. `SECURITY DEFINER` 慎用，明确权限边界

## 参考文档

```
kes-plsql/
├── SKILL.md           # 本文件
├── ref/
│   └── plsql.md       # 完整 PL/SQL 编程参考
└── test-cases.md
```
