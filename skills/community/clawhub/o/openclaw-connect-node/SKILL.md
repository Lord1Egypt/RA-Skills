# OpenClaw Connect Enterprise — Node 节点

**版本**: 0.1.5

子节点是 OpenClaw Connect Enterprise 的分布式执行单元，通过 WebSocket 长连接注册到 Hub，接收并执行 Hub 下发的任务。

## 快速安装

```bash
# 1. 解压包
unzip openclaw-connect-enterprise-node.zip
cd openclaw-connect-enterprise

# 2. 安装依赖
cd node/server && npm install && cd ../..
cd node/frontend && npm install && cd ../..

# 3. 启动（生产环境）
cd node/server
HUB_URL=http://你的Hub地址:3100 \
APP_ID=你的APP_ID \
APP_KEY=你的APP_KEY \
APP_TOKEN=你的APP_TOKEN \
npx tsx src/index.ts

# 4. 启动（开发环境）
npm run dev
```

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `HUB_URL` | ✅ | Hub 服务器地址，如 `http://YOUR_HUB_IP:3100` |
| `APP_ID` | ✅ | 节点唯一标识，在 Hub 后台创建节点获得 |
| `APP_KEY` | ✅ | 节点密钥，在 Hub 后台创建节点获得 |
| `APP_TOKEN` | ✅ | 节点令牌，在 Hub 后台创建节点获得 |
| `NODE_NAME` | 否 | 节点显示名称，默认取主机名 |
| `NODE_PORT` | 否 | 节点本地端口，默认 `3100` |
| `OPENCLAW_GATEWAY_PORT` | 否 | 本地 OpenClaw Gateway 端口，默认 `18789` |

## 凭证持久化

首次注册成功 后，凭证会自动保存到 `~/.openclaw-node/node.json`。重启后会自动恢复连接，无需重新配置。

## 前端界面

```bash
cd node/frontend && npm run build
# 访问 http://节点地址:3100
```

## API 端点

### Hub → Node（节点本地）

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/status` | 节点运行状态 |
| `GET` | `/api/agents` | 本地 Agent 列表 |
| `GET` | `/api/tasks` | 同步的任务列表 |
| `POST` | `/api/tasks/:id/start` | 标记任务开始 |
| `POST` | `/api/tasks/:id/complete` | 标记任务完成 |
| `POST` | `/api/tasks/:id/fail` | 标记任务失败 |

### Node → Hub（Hub 端点）

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/api/nodes/register` | 注册到 Hub |
| `POST` | `/api/nodes/:id/heartbeat` | 心跳（30秒/次） |
| `GET` | `/api/nodes/:id/tasks` | 拉取分配的任务 |
| `POST` | `/api/nodes/:id/agents/register` | 注册 Agent |
| `POST` | `/node/api/tasks/:id/complete` | 上报任务完成 |
| `POST` | `/node/api/tasks/report` | 上报本地任务到 Hub |

## 任务执行流程

1. 节点每 30 秒向 Hub 拉取新任务（`fetchTasks`）
2. 任务进入执行队列，按优先级依次执行
3. 执行方式（按优先级）：
   - **本地 OpenClaw Gateway**（`POST /tools/invoke`）
   - **Hub Execute API**（代理执行）
   - **OpenClaw CLI**（`openclaw agent`）
4. 完成后自动上报结果到 Hub

## 目录结构

```
node/
├── package.json           # 节点总包管理
├── install-node.sh        # 安装脚本
├── uninstall-node.sh      # 卸载脚本
├── README.md              # 英文说明
├── SKILL.md               # 本文档
├── server/
│   ├── src/
│   │   └── index.ts       # 节点服务端主程序
│   ├── package.json
│   └── tsconfig.json
└── frontend/
    ├── src/               # 节点前端页面源码
    ├── package.json
    └── tailwind.config.js
```

## 与 Hub 的连接架构

```
┌─────────────────────────────────────────────────┐
│  Hub (YOUR_HUB_IP:3100)                        │
│  • 任务调度与分发                                 │
│  • 节点管理                                       │
│  • Agent 同步                                    │
│  • 记忆汇聚                                       │
└──────────────┬──────────────────────────────────┘
               │  HTTP REST + WebSocket
               │  心跳 30s / 任务拉取 30s
┌──────────────▼──────────────────────────────────┐
│  Node (各服务器)                                 │
│  • 本地 OpenClaw Gateway (18789)                 │
│  • 任务执行（CLI / REST / Hub Execute）           │
│  • 凭证持久化 (~/.openclaw-node/node.json)        │
└─────────────────────────────────────────────────┘
```

## 升级

从 Hub 后台获取新的节点包，解压后：

```bash
# 备份旧配置（凭证已持久化，通常不需要）
cp ~/.openclaw-node/node.json ~/.openclaw-node/node.json.bak

# 替换代码
rm -rf openclaw-connect-enterprise
unzip new-package.zip
cd openclaw-connect-enterprise/node/server && npm install

# 重启（凭证自动恢复）
pkill -f "tsx src/index"
nohup npm start &
```
