---
name: kes-user-mgmt
description: KingbaseES 用户权限管理 — 测试用例
---

# KingbaseES 用户权限管理测试用例

## 测试用例 1: 用户创建与权限分配

**场景**：为新应用创建数据库用户并授予最小权限

**输入问题**："金仓数据库怎么创建用户并授予表访问权限？"

**期望答案要点**：
- `CREATE USER app_user WITH PASSWORD 'xxx'`
- `GRANT CONNECT ON DATABASE test TO app_user`
- `GRANT SELECT, INSERT, UPDATE ON TABLE users TO app_user`
- 遵循最小权限原则

**验证方法**：答案包含 CREATE USER 和 GRANT 语句

---

## 测试用例 2: 权限回收

**场景**：用户不再需要 DELETE 权限

**输入问题**："怎么撤销某个用户对表的删除权限？"

**期望答案要点**：
- `REVOKE DELETE ON TABLE users FROM app_user`
- 验证权限已回收：查询 `sys_role_privileges` 或 `sys_table_privileges`

**验证方法**：答案包含 REVOKE 语句和验证方法

---

## 测试用例 3: 表空间配额设置

**场景**：限制用户在某个表空间的使用量

**输入问题**："怎么限制金仓数据库用户的表空间配额？"

**期望答案要点**：
- `ALTER USER app_user QUOTA 1024 MB ON sys_default`
-  unlimited quota: `ALTER USER app_user QUOTA UNLIMITED ON sys_default`
- 查看使用情况的 SQL

**验证方法**：答案包含 ALTER USER QUOTA 语法
