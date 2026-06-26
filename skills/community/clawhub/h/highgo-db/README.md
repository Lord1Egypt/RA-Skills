# HighGo DB Skill for Gemini CLI

这是一个为 Gemini CLI 开发的自包含技能，旨在通过瀚高数据库（HighGo DB）提供的自定义 `psycopg2` 驱动连接并操作数据库。

## 特性

- **内置驱动**: 集成了瀚高专用 `psycopg2` 驱动（支持国密 SM4 等安全特性）。
- **Python 2.7 适配**: 核心脚本已完全适配 Python 2.7 环境，解决了旧版驱动在 Python 3 下的兼容性问题。
- **自动环境配置**: 运行时自动配置 `LD_LIBRARY_PATH` 以正确加载驱动依赖的 `.so` 库。
- **SDD 流程支持**: 适用于规范驱动开发流程中的数据库验证和查询。

## 运行环境要求

由于瀚高提供的二进制驱动是针对 Python 2.7 编译的，因此环境必须满足：

- **Python**: 2.7.x
- **系统库**: 
  - `libpython2.7.so.1.0`
  - `libldap_r-2.4.so.2` (或兼容版本)
  - `openssl-1.1` (旧版 OpenSSL 支持)

### Arch Linux 安装建议
```bash
# 导入必要的 PGP 密钥
gpg --keyserver hkps://keyserver.ubuntu.com --recv-keys A21FAB74B0088AA361152586B8EF1A6BA9DA2D5C EFC0A467D613CB83C7ED6D30D894E2CE8B3D79F5 C01E1CAD5EA2C4F0B8E3571504C367C218ADD4FF 8657ABB260F056B1E5190839D9C4D26D0E604491 7953AC1FBC3DC8B3B292393ED5E9E43F7DF9EE8C

# 从 AUR 安装依赖
# 建议使用 yay 或 makepkg 手动安装 python2 和 openssl-1.1
```

## 安装技能

1. 下载或克隆此仓库。
2. 在项目根目录（或技能目录）执行安装：
   ```bash
   gemini skills install highgo-db.skill --scope workspace
   ```
3. 在交互界面执行 `/skills reload`。

## 使用方法

### 执行查询
直接使用 `python2` 调用技能内部的脚本：

```bash
python2 highgo-db/scripts/execute_query.py \
  --dsn "host=[IP] port=[PORT] dbname=[DB] user=[USER] password='[PASS]' options='-c search_path=system'" \
  --sql "SELECT count(*) FROM sys_user;"
```

## 项目结构

- `SKILL.md`: 技能元数据与触发规则。
- `scripts/`: 包含 Python 2.7 兼容的查询执行脚本。
- `assets/driver/`: 内置的瀚高专用驱动文件。
- `references/`: 驱动详细信息与故障排除指南。

## 许可证
基于瀚高数据库提供的 `psycopg2` 修改版，遵循 LGPL 协议。
