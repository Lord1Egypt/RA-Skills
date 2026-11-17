---
name: kes-oracle-compat
description: KingbaseES Oracle 兼容模式 — 测试用例
---

# KingbaseES Oracle 兼容模式测试用例

## 测试用例 1: 启用 Oracle 兼容模式

**场景**：从 Oracle 迁移，需要启用兼容模式

**输入问题**："金仓数据库怎么开启 Oracle 兼容模式？"

**期望答案要点**：
- `SHOW oracle_compatible;` 查看当前状态
- `ALTER SYSTEM SET oracle_compatible = on;` 全局启用
- `SELECT sys_reload_conf();` 重载配置
- 配置文件中 `oracle_compatible = on`

**验证方法**：答案包含启用步骤和配置重载

---

## 测试用例 2: Oracle 语法替换

**场景**：Oracle SQL 需要改写为金仓语法

**输入问题**："Oracle 的 NVL、DECODE、CONNECT BY 在金仓里怎么写？"

**期望答案要点**：
- `NVL(x, y)` → `COALESCE(x, y)`
- `DECODE(x, a, b, c)` → `CASE WHEN x=a THEN b ELSE c END`
- `START WITH ... CONNECT BY` → `WITH RECURSIVE ...`
- 兼容模式下 NVL/DECODE 可直接使用

**验证方法**：答案提供正确的语法映射

---

## 测试用例 3: 数据类型映射

**场景**：Oracle 表结构迁移到金仓

**输入问题**："Oracle 的 VARCHAR2、NUMBER、RAW 对应金仓什么类型？"

**期望答案要点**：
- `VARCHAR2(n)` → `VARCHAR(n)`（兼容模式可直接用 VARCHAR2）
- `NUMBER(p,s)` → `NUMERIC(p,s)`
- `RAW(n)` → `BYTEA`
- Oracle `DATE` 含时间 → KES 用 `TIMESTAMP`

**验证方法**：答案包含完整的数据类型对照表
