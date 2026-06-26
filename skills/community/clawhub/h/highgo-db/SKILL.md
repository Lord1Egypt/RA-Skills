---
name: highgo-db
description: 通过瀚高数据库（HighGo DB）提供的自定义 psycopg2 驱动连接数据库。该驱动已内置于技能中，支持 Python 2.7 和国密 SM4 安全特性。
---

# 瀚高数据库 (HighGo DB) 连接技能

此技能允许使用瀚高提供的修改版 `psycopg2` 驱动连接瀚高数据库。该驱动已内置在技能的 `assets/driver/` 目录下。

**注意：内置驱动是针对 Python 2.7 编译的，必须在 Python 2.7 环境下运行。**

## 核心功能

1. **执行 SQL 语句**: 在瀚高数据库中运行查询或管理指令。
2. **内置驱动驱动支持**: 自动加载集成在技能内部的瀚高专用 `psycopg2` 驱动。
3. **环境适配**: 脚本已适配 Python 2.7，并能自动处理内部共享库（.so）的加载。

## 运行环境要求

- **Python**: 必须安装 Python 2.7。
- **系统库**: 
  - `libpython2.7.so.1.0`
  - `libldap_r-2.4.so.2` (或兼容版本)
- **Arch Linux 用户**: 如遇到依赖或 PGP 密钥问题，请参阅 [references/driver_info.md](references/driver_info.md) 的安装建议。

## 使用指南

### 1. 执行查询
直接使用 `python2` 调用技能内部的 `execute_query.py`。由于驱动已内置，通常**无需**指定驱动路径。

**示例命令：**
```bash
python2 highgo-db/scripts/execute_query.py \
  --dsn "host=10.238.18.128 port=5866 dbname=ficc user=fic password='PASSWORD' options='-c search_path=system'" \
  --sql "SELECT count(*) FROM sys_user;"
```

### 2. 注意事项
- **DSN 参数**: 瀚高数据库通常需要指定 `options='-c search_path=system'` 来正确访问系统表。
- **驱动覆盖**: 如果需要使用外部驱动，仍可通过 `--driver` 参数手动指定。

## 参考资料
- 关于驱动的详细信息及 Arch Linux 安装建议，请参阅 [references/driver_info.md](references/driver_info.md)。
