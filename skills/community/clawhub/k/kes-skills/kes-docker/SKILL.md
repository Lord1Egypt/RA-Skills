---
name: kes-docker
name_for_command: kes-docker
description: KingbaseES Docker 部署指南。当用户提到 Docker 容器化、docker run、docker-compose、镜像导入、容器启停、Docker License、容器化部署时，必须使用此技能。
---

# KingbaseES Docker 部署指南

本技能指导用户完成 KingbaseES 的 Docker 容器化部署，涵盖镜像获取、容器启动、环境变量配置、数据持久化、License 管理和常见问题。

> **ISO 安装** → 见 `kes-deploy` 技能

## 环境要求

- Docker 20.10.0 及以上版本
- 支持 x86_64、龙芯(LoongArch)、飞腾/鲲鹏(ARM64) 等架构

## 镜像获取与导入

从电科金仓官网或代理商获取镜像文件（如 `kingbase.tar`）。

```bash
# 创建持久化存储路径（root 用户）
mkdir -p /opt/kingbase/data
chmod -R 755 /opt/kingbase/data

# 导入镜像
docker load -i /opt/kingbase/kingbase.tar

# 验证镜像
docker images | grep kingbase
```

> 如果 `docker load -i` 报错，可尝试 `docker import kingbase.tar`。

## 快速启动

```bash
docker run -d --privileged \
  -p 4321:54321 \
  -v /opt/kingbase/data:/home/kingbase/userdata/ \
  --restart=always \
  -e NEED_START=yes \
  -e DB_USER=system \
  -e DB_PASSWORD=12345678ab \
  -e DB_MODE=sqlserver \
  -e ENCODING=utf8 \
  -e ENABLE_CI=yes \
  --name kingbase \
  kingbase:v1 /usr/sbin/init
```

## 环境变量

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `DB_USER` | `system` | 数据库用户名 |
| `DB_PASSWORD` | `12345678ab` | 数据库初始密码 |
| `DB_MODE` | `sqlserver` | 兼容模式（sqlserver/postgres/oracle） |
| `ENCODING` | `utf8` | 字符集 |
| `NEED_START` | `yes` | 启动时自动启动数据库 |
| `ENABLE_CI` | `yes` | 大小写不敏感（sqlserver模式下不生效） |

## 数据持久化

- 容器内数据路径：`/home/kingbase/userdata/`
- 宿主机挂载目录权限必须为 755
- 验证挂载：`docker inspect -f '{{.Mounts}}' kingbase`

## 数据库操作

```bash
# 进入容器
docker exec -it kingbase /bin/bash

# 连接数据库（容器内免密）
ksql

# 指定用户连接
ksql -U SYSTEM -d test -p 54321
```

宿主机远程访问：
```bash
ksql -U SYSTEM -d test -p 4321 -h ${宿主机IP}
```

## 数据库启停

```bash
# 停止
su - kingbase -c "/home/kingbase/install/kingbase/bin/sys_ctl -D /home/kingbase/userdata/data/ stop"

# 启动
su - kingbase -c "/home/kingbase/install/kingbase/bin/sys_ctl -D /home/kingbase/userdata/data/ start"

# 重载配置
su - kingbase -c "/home/kingbase/install/kingbase/bin/sys_ctl reload -D /home/kingbase/userdata/data/"
```

## License 配置

Docker 环境下无网卡 MAC，需申请 Docker 版 License（不与硬件绑定）。

```bash
# 从宿主机复制 License 进容器
docker cp /path/to/license.dat kingbase:/tmp/license.dat

# 容器内操作
docker exec -it kingbase /bin/bash
cp /home/kingbase/userdata/etc/license.dat /home/kingbase/userdata/etc/license.dat.bak
cp /tmp/license.dat /home/kingbase/userdata/etc/license.dat
chown kingbase:kingbase /home/kingbase/userdata/etc/license.dat
chmod 755 /home/kingbase/userdata/etc/license.dat

# 验证
ksql -c "select get_license_validdays();"
```

## 配置文件修改

配置文件随 data 目录持久化（`kingbase.conf`、`sys_hba.conf` 等）。修改后重载：

```bash
su - kingbase -c "/home/kingbase/install/kingbase/bin/sys_ctl reload -D /home/kingbase/userdata/data/"
```

## 卸载

```bash
docker stop kingbase && docker rm kingbase
# 可选：docker rmi ${image_id}
```

> 卸载前请确认数据已备份归档。

## 向量扩展（KES_Vector）

使用带有 KES_Vector 的镜像（如 `kingbase:v1-vector`），容器内直接启用向量能力：

```sql
-- 创建扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- 验证
SELECT extname, extversion FROM sys_extension WHERE extname = 'vector';

-- 创建向量表
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    embedding vector(768)
);

-- 写入并检索
INSERT INTO documents (title, embedding) VALUES ('示例', '[0.1, 0.2, ...]'::vector(768));
SET enable_seqscan = off;
SELECT title, embedding <-> '[0.5, 0.6, ...]'::vector AS distance
FROM documents ORDER BY distance LIMIT 10;
```

> 详细向量类型、索引、距离函数请参考 `kes-vector` 技能。

### 自定义镜像制作

若需将 vector 插件集成到自有镜像：

```bash
# 1. 提取 KES_Vector 插件包
tar -xf KES_Vector-x86_64-*.tar -C /tmp/kes_vector_extract

# 2. 进入运行中的容器
docker exec -it kingbase /bin/bash

# 3. 容器内操作：拷贝 vector.so 和扩展文件
cp /tmp/kes_vector_extract/lib/vector.so /home/kingbase/install/kingbase/lib/
cp /tmp/kes_vector_extract/share/extension/* /home/kingbase/install/kingbase/share/extension/

# 4. 验证
ksql -c "CREATE EXTENSION vector;"
ksql -c "SELECT '[1,2,3]'::vector;"

# 5. 提交为新镜像
docker commit kingbase kingbase:v1-vector
```

## Docker FAQ

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 容器启动后立即退出 | 数据目录权限错误 | 挂载目录权限设为 755 |
| sys_dump 报 exit code 137 | 内存不足 OOM | 增加容器内存 |
| License 绑定失败 | Docker 无网卡 MAC | 申请 Docker 版 License |
| 配置文件修改不生效 | 未重载 | 执行 `sys_ctl reload` |
| 容器外无法访问 | 端口未映射或 sys_hba.conf 限制 | 检查 `-p` 和认证配置 |

## 相关技能

- **kes-deploy** — ISO 安装、开发工具、配置文件详解
- **kes-vector** — KES_Vector 向量扩展
- **kes-mcp** — MCP Server 集成

## 参考文档

```
kes-docker/
├── SKILL.md            # 本文件
├── ref/
│   └── docker-compose-examples.md   # 常见 Docker Compose 部署模板
└── test-cases.md
```
