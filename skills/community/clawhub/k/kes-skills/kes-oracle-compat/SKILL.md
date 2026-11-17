---
name: kes-oracle-compat
name_for_command: kes-oracle-compat
description: KingbaseES Oracle 兼容模式指南。当用户提到 Oracle 兼容、oracle_compatible、Oracle 迁移、NVL/DECODE/CONNECT BY、序列 NEXTVAL、ROWNUM、VARCHAR2、数据类型映射、Oracle 系统视图时，必须使用此技能。
---

# KingbaseES Oracle 兼容模式指南

本技能指导用户启用和使用 KingbaseES 的 Oracle 兼容模式，涵盖语法对照、数据类型映射、系统视图兼容和迁移注意事项。

## 兼容模块

| 场景 | 内容 | 参考 |
|------|------|------|
| 模式切换 | oracle_compatible 参数 | `ref/oracle-compat.md` §1 |
| 语法对照 | NVL/DECODE/CONNECT BY/序列 | `ref/oracle-compat.md` §2 |
| 数据类型映射 | VARCHAR2/NUMBER/RAW | `ref/oracle-compat.md` §3 |
| 特殊操作符 | 空值合并/正则/层次 | `ref/oracle-compat.md` §4 |
| 系统视图兼容 | all_tables/user_tab_columns | `ref/oracle-compat.md` §5 |
| 包与程序单元 | DBMS_OUTPUT/游标/异常 | `ref/oracle-compat.md` §6 |
| 迁移注意事项 | 检查清单 + 步骤 | `ref/oracle-compat.md` §7 |
| 常见问题 | 日期/序列/标识符/ROWNUM | `ref/oracle-compat.md` §8 |

## 启用兼容模式

```sql
-- 查看当前状态
SHOW oracle_compatible;

-- 会话级启用
SET oracle_compatible = on;

-- 全局持久化
ALTER SYSTEM SET oracle_compatible = on;
SELECT sys_reload_conf();
```

## 常用语法替换速查

```sql
-- 空值
NVL(x, y)              → COALESCE(x, y)
NVL2(x, a, b)          → CASE WHEN x IS NOT NULL THEN a ELSE b END

-- 条件
DECODE(x, a, b, c)     → CASE WHEN x=a THEN b ELSE c END

-- 层级
START WITH ... CONNECT BY → WITH RECURSIVE ...

-- 序列
seq.NEXTVAL            → nextval('seq')
seq.CURRVAL            → currval('seq')

-- 分页
ROWNUM <= N            → LIMIT N

-- 日期
SYSDATE                → NOW() 或 CURRENT_DATE
ADD_MONTHS(d, n)       → d + (n || ' months')::INTERVAL

-- 连接
e.col(+) = d.col       → LEFT JOIN ... ON

-- 类型
VARCHAR2(n)            → VARCHAR(n)
NUMBER(p,s)            → NUMERIC(p,s)
RAW(n)                 → BYTEA
```

## 迁移步骤

```
1. 启用兼容模式 → ALTER SYSTEM SET oracle_compatible = on
2. 数据类型映射 → VARCHAR2→VARCHAR, NUMBER→NUMERIC
3. 序列迁移 → seq.NEXTVAL → nextval('seq')
4. 层级查询迁移 → CONNECT BY → WITH RECURSIVE
5. 包迁移 → DBMS_OUTPUT.PUT_LINE → RAISE NOTICE
6. 验证 → 检查类型、约束、索引一致性
```

## 关键差异

1. **Oracle DATE** 包含时间，**KES DATE** 仅日期 → 用 TIMESTAMP
2. **空字符串** Oracle `''` = NULL；KES 标准模式 `''` ≠ NULL
3. **标识符大小写** 兼容模式无引号→大写，标准模式→小写
4. **Flashback** Oracle 有，KES 无直接等价

## 参考文档

```
kes-oracle-compat/
├── SKILL.md                 # 本文件
├── ref/
│   └── oracle-compat.md     # 完整 Oracle 兼容参考
└── test-cases.md
```
