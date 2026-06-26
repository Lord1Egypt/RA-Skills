# OpenClaw Connect Node - 子节点

OpenClaw Connect Enterprise 的子节点服务，可独立部署在任何服务器上，通过 Hub 进行统一管理。

## 功能特性

- 🔗 自动注册到 Hub 并维持心跳连接
- 💓 30秒心跳间隔 + 指数退避自动重连
- 📊 系统监控（CPU/内存/磁盘）
- 🧠 本地记忆管理（短期/中期/长期）
- 📋 任务同步与执行
- 🤖 Agent 自动注册
- 🌐 Web 管理界面
- 🏥 健康检查端点
- 🔄 systemd 守护进程

## 一键安装

### 从 Git 仓库安装

```bash
bash install-node.sh \
  --hub-url http://your-hub:3100 \
  --app-id YOUR_APP_ID \
  --app-key YOUR_APP_KEY \
  --token YOUR_TOKEN \
  --node-name "我的节点" \
  --from-git
```

### 从本地代码安装

先将代码上传到服务器，然后在项目根目录执行：

```bash
cd /path/to/OpenClaw-Connect
bash node/install-node.sh \
  --hub-url http://your-hub:3100 \
  --app-id YOUR_APP_ID \
  --app-key YOUR_APP_KEY \
  --token YOUR_TOKEN \
  --node-name "我的节点" \
  --from-local
```

### 安装参数

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `--hub-url` | ✅ | - | Hub 服务器地址 |
| `--app-id` | ✅ | - | 应用 ID（从 Hub 管理界面获取） |
| `--app-key` | ✅ | - | 应用 Key |
| `--token` | ✅ | - | 认证 Token |
| `--node-name` | ❌ | hostname | 节点名称 |
| `--port` | ❌ | 3200 | 监听端口 |
| `--install-dir` | ❌ | /opt/openclaw-node | 安装目录 |
| `--from-git` | ❌ | auto | 从 Git 仓库 clone |
| `--from-local` | ❌ | auto | 使用当前目录代码 |
| `--service-name` | ❌ | openclaw-node | systemd 服务名 |

## 手动安装

如果不使用一键脚本，可以手动安装：

### 1. 环境要求

- Node.js >= 18
- npm
- Linux (systemd)

### 2. 安装依赖

```bash
cd node/server && npm install
cd ../frontend && npm install && npx vite build
```

### 3. 配置环境变量

创建 `.env` 文件：

```bash
# Hub 连接配置
HUB_URL=http://your-hub:3100
NODE_APP_ID=your_app_id
NODE_APP_KEY=your_app_key
NODE_TOKEN=your_token

# 节点配置
NODE_NAME=my-node
NODE_PORT=3200
DATA_DIR=/opt/openclaw-node/data
NODE_ENV=production
```

### 4. 启动服务

```bash
# 开发模式
cd node/server && npx tsx src/index.ts

# 或用 systemd（参考 install-node.sh 中的配置）
```

## 管理命令

安装完成后，使用 `openclaw-node` 命令管理节点：

```bash
openclaw-node start      # 启动节点
openclaw-node stop       # 停止节点
openclaw-node restart    # 重启节点
openclaw-node status     # 查看状态
openclaw-node logs       # 查看日志（持续跟踪）
openclaw-node logs 50    # 查看最近50行日志
openclaw-node config     # 查看配置
openclaw-node update     # 更新代码并重启
openclaw-node health     # 健康检查
```

## API 端点

### 健康检查

```bash
curl http://localhost:3200/health
curl http://localhost:3200/api/health
```

返回：
```json
{
  "status": "ok",
  "nodeId": "node-xxx",
  "nodeName": "my-node",
  "hubUrl": "http://your-hub:3100",
  "connected": true,
  "uptime": 12345,
  "version": "0.0.1"
}
```

### 节点状态
```bash
curl http://localhost:3200/api/status
```

### 系统监控
```bash
curl http://localhost:3200/api/monitor
```

## 卸载

```bash
# 保留数据目录
bash uninstall-node.sh

# 完全删除（包括数据）
bash uninstall-node.sh --purge
```

## 故障排查

### 1. 服务启动失败

```bash
# 查看详细日志
journalctl -u openclaw-node -n 100 --no-pager

# 手动启动测试
cd /opt/openclaw-node
source .env
cd node/server && npx tsx src/index.ts
```

### 2. 无法连接到 Hub

```bash
# 检查网络连通性
curl -v http://your-hub:3100/health

# 检查配置
openclaw-node config

# 查看连接日志
openclaw-node logs | grep -i "connect\|register\|heartbeat"
```

### 3. 端口被占用

```bash
# 查看端口占用
ss -tlnp | grep :3200

# 修改端口
vim /opt/openclaw-node/.env  # 修改 NODE_PORT
openclaw-node restart
```

### 4. 前端页面空白

```bash
# 重新构建前端
cd /opt/openclaw-node/node/frontend
npm install
npx vite build
openclaw-node restart
```

### 5. 内存不足

```bash
# 检查内存使用
free -h

# 调整 systemd 内存限制
# 编辑 /etc/systemd/system/openclaw-node.service
# 修改 MemoryMax=1G
systemctl daemon-reload
openclaw-node restart
```

### 6. 心跳断连

节点内置自动重连机制：
- 心跳间隔：30秒
- 失败后指数退避：30s → 60s → 120s → 240s → 300s (上限)
- 连续失败会记录错误日志但不会停止重试

如果持续断连，检查：
- Hub 服务是否正常运行
- 网络是否通畅
- 防火墙是否放行

## 目录结构

```
node/
├── install-node.sh        # 一键安装脚本
├── uninstall-node.sh      # 一键卸载脚本
├── package.json           # 节点总 package.json
├── README.md              # 本文档
├── server/                # 后端服务
│   ├── src/
│   │   └── index.ts       # 主入口（Fastify 服务）
│   ├── package.json
│   └── tsconfig.json
└── frontend/              # 前端管理界面
    ├── src/
    ├── package.json
    ├── vite.config.ts
    └── dist/              # 构建产物
```

## 环境变量说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `HUB_URL` | Hub 服务器地址 | 空（不连接） |
| `NODE_APP_ID` | 应用 ID | 空 |
| `NODE_APP_KEY` | 应用 Key | 空 |
| `NODE_TOKEN` | 认证 Token | 空 |
| `NODE_NAME` | 节点名称 | hostname |
| `NODE_PORT` | 监听端口 | 3200 |
| `DATA_DIR` | 数据存储目录 | ./data |
| `NODE_ENV` | 运行环境 | development |

> 💡 兼容旧版变量名：`APP_ID`, `APP_KEY`, `APP_TOKEN` 也可使用，新版变量优先。
