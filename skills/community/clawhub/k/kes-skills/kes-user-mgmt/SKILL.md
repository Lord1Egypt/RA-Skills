---
name: kes-user-mgmt
name_for_command: kes-user-mgmt
description: KingbaseES 用户权限管理指南。当用户提到用户管理、角色权限、GRANT/REVOKE、表空间配额、资源限制、密码策略时，必须使用此技能。
---

# KingbaseES 用户权限管理指南

本技能指导用户完成 KingbaseES 的用户和权限管理，涵盖角色创建、权限分配、表空间管理和资源配额。

## 管理模块

| 场景 | 操作 | 参考 |
|------|------|------|
| 用户/角色管理 | CREATE/ALTER/DROP | `ref/user-management.md` §1 |
| 权限分配 | GRANT/REVOKE | `ref/user-management.md` §2 |
| 表空间管理 | CREATE TABLESPACE | `ref/user-management.md` §3 |
| 资源配额 | ALTER USER ... QUOTA | `ref/user-management.md` §4 |
| 配置管理 | kingbase.conf | `ref/user-management.md` §5 |

## 权限最小化原则

1. 新建用户默认无权限
2. 按需授予最小权限
3. 定期审计权限分配
4. 及时回收不需要的权限

## 常用操作

```sql
-- 创建用户
CREATE USER app_user WITH PASSWORD 'xxx';

-- 授予连接权限
GRANT CONNECT ON DATABASE test TO app_user;

-- 授予表权限
GRANT SELECT, INSERT, UPDATE ON TABLE users TO app_user;

-- 回收权限
REVOKE DELETE ON TABLE users FROM app_user;

-- 设置表空间配额
ALTER USER app_user QUOTA 1024 MB ON sys_default;
```

## 参考文档

```
kes-user-mgmt/
├── SKILL.md                  # 本文件
├── ref/
│   └── user-management.md    # 完整用户管理指南
└── test-cases.md
```
