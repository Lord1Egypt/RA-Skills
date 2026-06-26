---
name: setup-postgres-mcp
description: |
  安装部署 postgres-mcp 服务并配置 MCP 连接，引导用户完成从零到可用的全流程。
  当用户第一次使用 PostgreSQL 功能、提到安装/部署/配置 postgres-mcp、环境搭建、MCP 服务连接失败时使用。
---

项目仓库：https://github.com/crystaldba/postgres-mcp

## 执行流程

### 1. 检测服务状态

检查 postgres-mcp 是否已在运行。询问用户是否已经部署了 postgres-mcp 服务。

- 已部署 → 询问连接方式（stdio 或 SSE），跳到步骤 3
- 未部署 → 进入步骤 2

### 2. 部署服务

确认操作系统（macOS / Linux / Windows）和是否已安装 Docker 或 Python 3.12+。

#### 数据库连接字符串注意事项

**重要**：如果密码包含特殊字符，必须进行 URL 编码，否则会导致连接失败。

**常见特殊字符编码对照表**：

| 字符 | URL 编码 | 示例 |
|------|----------|------|
| `@` | `%40` | `Pass@123` → `Pass%40123` |
| `#` | `%23` | `Pass#123` → `Pass%23123` |
| `%` | `%25` | `Pass%123` → `Pass%25123` |
| `/` | `%2F` | `Pass/123` → `Pass%2F123` |
| `?` | `%3F` | `Pass?123` → `Pass%3F123` |
| `&` | `%26` | `Pass&123` → `Pass%26123` |
| `=` | `%3D` | `Pass=123` → `Pass%3D123` |
| `:` | `%3A` | `Pass:123` → `Pass%3A123` |
| ` ` (空格) | `%20` | `Pass 123` → `Pass%20123` |

**完整示例**：

```bash
# 原始信息
用户名：postgres
密码：pass@1
主机：192.168.1.100
端口：5432
数据库：mydb

# 错误的连接字符串（会失败）
postgresql://postgres:pass@1@192.168.1.100:5432/mydb

# 正确的连接字符串（@ 编码为 %40）
postgresql://postgres:pass%401@192.168.1.100:5432/mydb
```

#### 方式一：Docker（推荐）

Docker 方式最简单，无需配置 Python 环境。

**使用 Docker 运行（stdio 模式）**：

```bash
docker run -i --rm \
  ghcr.io/crystaldba/postgres-mcp:latest \
  "postgresql://user:pass@host:5432/dbname"
```

**使用 Docker 运行（SSE 模式）**：

```bash
docker run -d -p 8000:8000 \
  ghcr.io/crystaldba/postgres-mcp:latest \
  --transport sse \
  --port 8000 \
  "postgresql://user:pass@host:5432/dbname"
```

注意：
- 替换 `user:pass@host:5432/dbname` 为实际的数据库连接信息
- 如果数据库在本机，host 使用 `host.docker.internal`（Mac/Windows）或 `172.17.0.1`（Linux）
- 可以添加 `--read-only` 参数启用只读模式

#### 方式二：Python + uv

适合 Python 开发者或需要从源码安装的场景。

**安装 uv**：

推荐使用以下任一方法（更安全）：

**方法1：Homebrew（macOS/Linux）**
```bash
brew install uv
```

**方法2：pip（跨平台）**
```bash
pip install uv
```

**方法3：pipx（隔离安装）**
```bash
pipx install uv
```

**安装 postgres-mcp**：

```bash
# 从 PyPI 安装
uv pip install postgres-mcp

# 或从源码安装
git clone https://github.com/crystaldba/postgres-mcp.git
cd postgres-mcp
uv pip install -e .
uv sync
```

**运行服务（stdio 模式）**：

```bash
uv run postgres-mcp "postgresql://user:pass@host:5432/dbname"
```

**运行服务（SSE 模式）**：

```bash
uv run postgres-mcp \
  --transport sse \
  --port 8000 \
  "postgresql://user:pass@host:5432/dbname"
```

#### 方式三：pipx

适合全局安装。

```bash
pipx install postgres-mcp
postgres-mcp "postgresql://user:pass@host:5432/dbname"
```

### 3. 配置 MCP 连接

根据用户使用的客户端和传输方式配置连接。

#### Claude Desktop（stdio 模式）

编辑配置文件：
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**Docker 方式**：

```json
{
  "mcpServers": {
    "postgres": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "ghcr.io/crystaldba/postgres-mcp:latest",
        "postgresql://user:pass@host.docker.internal:5432/dbname"
      ]
    }
  }
}
```

**Python 方式**：

```json
{
  "mcpServers": {
    "postgres": {
      "command": "uv",
      "args": [
        "run",
        "postgres-mcp",
        "postgresql://user:pass@localhost:5432/dbname"
      ]
    }
  }
}
```

#### Cursor（stdio 模式）

编辑 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "postgres": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "ghcr.io/crystaldba/postgres-mcp:latest",
        "postgresql://user:pass@host.docker.internal:5432/dbname"
      ]
    }
  }
}
```

#### SSE 模式（任何客户端）

如果使用 SSE 模式，配置 HTTP 端点：

```json
{
  "mcpServers": {
    "postgres": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

### 4. 验证与提示

1. **提示用户重启客户端** — MCP 配置变更后需重启才能加载新的 MCP 工具
2. 重启后检查可用的 MCP 工具列表，确认 postgres-mcp 工具已加载
3. 验证成功 → 可以开始使用其他 postgres skills

## 配置选项

### 只读模式

添加 `--read-only` 参数启用只读模式，只允许 SELECT 查询：

```bash
postgres-mcp --read-only "postgresql://..."
```

### 环境变量

- `DATABASE_URL` — 数据库连接字符串
- `POSTGRES_MCP_READ_ONLY` — 设置为 `true` 启用只读模式
- `POSTGRES_MCP_QUERY_TIMEOUT` — 查询超时时间（秒）

## 失败处理

| 场景 | 处理 |
|---|---|
| Docker 未安装 | 建议安装 Docker 或改用 Python 方式 |
| Python 版本过低 | 需要 Python 3.12+，建议升级或使用 Docker |
| 数据库连接失败 | 检查连接字符串、网络、防火墙、数据库权限 |
| 密码包含特殊字符导致连接失败 | 使用 URL 编码（如 `@` → `%40`），参考上方编码对照表 |
| 配置写入后工具仍不可用 | 提示重启客户端会话 |
| Docker 无法访问本机数据库 | 使用 `host.docker.internal` 或 `172.17.0.1` |

## 常见错误示例

### 错误 1：密码特殊字符未编码

**错误日志**：
```
WARNING  error connecting in 'pool-1': failed to resolve host '1@192.168.22.113'
```

**原因**：密码 `pass@1` 中的 `@` 被误认为是主机分隔符

**解决**：将密码编码为 `pass%401`

### 错误 2：端口被占用

**错误日志**：
```
ERROR: [Errno 98] error while attempting to bind on address ('0.0.0.0', 8001): address already in use
```

**解决**：
```bash
# 查找占用进程
lsof -i :8001

# 终止进程
kill <PID>

# 或使用其他端口
postgres-mcp --sse-port 8002 "postgresql://..."
```

### 错误 3：数据库拒绝连接

**错误日志**：
```
WARNING  Could not connect to database: Connection refused
```

**检查清单**：
- [ ] 数据库服务是否运行
- [ ] 防火墙是否允许连接
- [ ] PostgreSQL `pg_hba.conf` 是否允许远程连接
- [ ] 用户名和密码是否正确
