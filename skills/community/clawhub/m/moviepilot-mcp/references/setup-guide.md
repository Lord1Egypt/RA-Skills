# MoviePilot 配置指南

## 获取 API 密钥（API_TOKEN）

MoviePilot 的 MCP API 使用 `API_TOKEN` 作为认证密钥。

### 方法 1：Web UI（推荐）

1. 浏览器打开 MoviePilot 网页（如 `http://192.168.x.x:3001`）
2. 进入 **系统设定**
3. 找到 **API_TOKEN** 字段
4. 复制该值

### 方法 2：容器环境变量

如果使用 Docker 部署：

```bash
# 查看容器环境变量
docker inspect <容器名> | grep API_TOKEN

# 或查看 docker-compose.yml
grep API_TOKEN docker-compose.yml
```

### 方法 3：容器启动日志

MoviePilot 在启动时会打印 API_TOKEN：

```bash
docker logs <容器名> 2>&1 | grep -i "api.token\|apikey\|API_TOKEN"
```

### 方法 4：容器内配置文件

```bash
# 进入容器
docker exec -it <容器名> cat /config/env | grep API_TOKEN
# 或
docker exec -it <容器名> cat /app/config/env | grep API_TOKEN
```

### 方法 5：NAS 文件系统

如果 MoviePilot 部署在 NAS 上（群晖/威联通等），在 Docker 映射的配置目录中查找 `env` 文件。

---

## 版本差异

| 版本 | API_TOKEN 要求 |
|------|---------------|
| V1 | 默认值 `moviepilot`，可自定义 |
| V2 | 必须 ≥16 个字符；不符合要求会强制重新生成 |

如果 V2 填入的 API_TOKEN 不符合要求（长度不足），MoviePilot 会生成一个新值并在日志中打印。此时需要去日志中查找新值。

---

## 确认服务器地址

默认端口为 **3001**，MCP 端点路径为 `/api/v1/mcp`。

```
完整地址示例：
http://your-server:3001/api/v1/mcp
http://nas.local:3001/api/v1/mcp
https://your-domain.com:3001/api/v1/mcp
```

### 验证连接

```bash
curl "http://<地址>:3001/api/v1/mcp/tools?apikey=<你的key>"
```

成功时返回工具列表 JSON。401 表示 API Key 错误，连接超时表示地址/端口不对或服务未运行。

---

## 配置本技能

```bash
# 方式 1：交互式
python3 scripts/setup.py

# 方式 2：命令行
python3 scripts/setup.py '{"base_url":"http://your-server:3001","apikey":"your-api-key"}'
```

配置保存到 `config.json`，调用脚本自动读取。修改配置可重新运行 setup.py 或直接编辑 `config.json`。

---

## 排错

| 症状 | 可能原因 | 检查 |
|------|---------|------|
| HTTP 401 | API Key 错误 | 确认复制的 API_TOKEN 无多余空格 |
| 连接超时 | 服务未运行或端口不对 | `docker ps` 确认容器在运行 |
| 连接拒绝 | 防火墙或网络不通 | 同网段内 `ping` 测试 |
| 返回空/tools 列表为空 | V2 自动重置了 key | 查容器日志找新 API_TOKEN |
