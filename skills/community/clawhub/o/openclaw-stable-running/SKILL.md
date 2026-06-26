---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 30460221009cdb3097529c88f77219dcc01d64b15e5cbbf872e4424fb8e4ec052b0ab62408022100b48fe52b42cc75c315de5d1910da49b4d73e29d46bcfe8e646d112e958f6f3ef
    ReservedCode2: 3046022100b44b95cbe6aab8748be573ebe4c8899a359bfc699ea9c207542d7a5f26577a84022100bf965b7cadef1fb9fd0d983cbdd00c97246646ae056edc34959a9280414dd4ba
description: OpenClaw 7×24 小时长稳运行方案 — 进程守护、异常重启、断连重连、断点续跑、资源回收、日志监控。确保 OpenClaw 零崩溃、零断连、零漏执行。无人值守必备。
name: openclaw-stable-running
tags:
    - openclaw
    - 运维
    - 进程守护
    - systemd
    - PM2
    - 监控
    - 稳定性
    - 7x24
---

# OpenClaw 7×24 长稳运行方案

让 OpenClaw 零崩溃、零断连、零漏执行。

## 常见崩溃场景

| 场景 | 危害 |
|------|------|
| 🔴 半夜崩了 | 凌晨 Gateway 挂掉，错过重要消息 |
| 🔴 内存爆了 | 运行一周后内存泄漏，被 OOM Kill |
| 🔴 网络断了 | Wi-Fi/运营商切换，TCP 连接断开 |
| 🔴 任务丢了 | 执行到一半崩溃，重启从头开始 |

---

## 一、进程守护：让 OpenClaw 永远在线

### 推荐方案对比

| 方案 | 崩溃后自启 | 开机自启 | 日志管理 | 资源限制 |
|------|------------|----------|----------|----------|
| nohup | ❌ | ❌ | ❌ 需手动 | ❌ |
| screen | ❌ | ❌ | ❌ | ❌ |
| **systemd** | ✅ | ✅ | ✅ 内置 | ✅ cgroups |
| **PM2** | ✅ | ✅ | ✅ | ✅ |

> ✅ 用 systemd（Linux 推荐）或 PM2，不要用 nohup/screen。

### 方案一：systemd（推荐）

创建服务文件 `/etc/systemd/system/openclaw.service`：

```ini
[Unit]
Description=OpenClaw Gateway Service
Documentation=https://docs.openclaw.ai
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=openclaw
Group=openclaw
WorkingDirectory=/home/openclaw/.openclaw
ExecStart=/usr/local/bin/openclaw gateway start --no-daemon
Restart=always
RestartSec=10
LimitNOFILE=65535
MemoryMax=2G
TasksMax=4096
Environment="NODE_ENV=production"
EnvironmentFile=/home/openclaw/.openclaw/.env
StandardOutput=journal
StandardError=journal
SyslogIdentifier=openclaw

[Install]
WantedBy=multi-user.target
```

**关键参数解释：**
- `Restart=always` — 任何异常退出都自动重启
- `RestartSec=10` — 崩溃后等 10 秒再重启，避免频繁重启
- `MemoryMax=2G` — 内存超限后自动重启，防止 OOM

**启用服务：**
```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl start openclaw
sudo systemctl status openclaw
journalctl -u openclaw -f
```

### 方案二：PM2

```bash
npm install -g pm2
pm2 start "openclaw gateway start --no-daemon" --name openclaw
pm2 save
pm2 startup
```

PM2 配置 `ecosystem.config.js`（见 `scripts/` 目录）：

```js
module.exports = {
  apps: [{
    name: 'openclaw-gateway',
    script: 'openclaw',
    args: 'gateway start --no-daemon',
    max_memory_restart: '1G',   // 内存超 1G 自动重启
    autorestart: true,
    max_restarts: 10,
    restart_delay: 10000,
    node_args: '--expose-gc --max-old-space-size=2048',
  }]
}
```

---

## 二、异常自动重启：崩溃后的自我修复

### 健康检查脚本

每 5 分钟检查一次 Gateway 是否存活，见 `scripts/healthcheck.sh`：

```bash
# crontab -e
*/5 * * * * /home/openclaw/scripts/healthcheck.sh
```

脚本会自动：
1. 检查 Gateway 进程是否存在
2. 检查健康端点是否响应
3. 两者任一失败 → 自动重启
4. 记录日志到 `/var/log/openclaw/healthcheck.log`

### 监控告警（可选）

**Uptime Kuma**（Docker 部署）：
```yaml
# docker-compose.yml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    ports:
      - "3001:3001"
    restart: always
```
监控 `http://localhost:9527/health`，异常时推送通知到飞书/Telegram/Discord。

---

## 三、断连自动重连：网络抖动不是事

### OpenClaw 渠道重连配置

```yaml
# 飞书配置
channels:
  feishu:
    reconnect:
      enabled: true
      maxRetries: 10
      initialDelay: 1000    # 首次重连等待 1s
      maxDelay: 60000       # 最大等待 60s
      backoffMultiplier: 2  # 指数退避

# Discord 配置
channels:
  discord:
    gateway:
      heartbeatInterval: 41250
      reconnect:
        enabled: true
        maxRetries: -1      # 无限重试
```

### LLM API 重试逻辑

```js
async function callLLMWithRetry(prompt, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [{ role: 'user', content: prompt }]
      });
    } catch (error) {
      if (error.status === 429) {
        await sleep((error.headers?.['retry-after'] || 60) * 1000);
      } else if (error.code === 'ECONNRESET' || error.code === 'ETIMEDOUT') {
        await sleep(Math.pow(2, i) * 1000);  // 指数退避
      } else {
        throw error;
      }
    }
  }
  throw new Error('Max retries exceeded');
}
```

---

## 四、任务断点续跑：崩溃后从哪里跌倒从哪里爬起

### 核心思路

```
任务开始 → 记录进度到文件/数据库
         ↓
任务执行中 → 定期更新进度
         ↓
崩溃重启 → 读取进度，从断点继续
```

### 进度持久化（文件方式）

```js
const PROGRESS_FILE = '/home/openclaw/data/task_progress.json';

function saveProgress(taskId, progress) {
  const data = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8') || '{}');
  data[taskId] = { ...progress, updatedAt: Date.now() };
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(data, null, 2));
}

function loadProgress(taskId) {
  const data = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8') || '{}');
  return data[taskId];
}

function clearProgress(taskId) {
  const data = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf8') || '{}');
  delete data[taskId];
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(data));
}
```

### 心跳状态持久化（正确做法）

```js
// ❌ 错误：依赖内存状态
let lastCheckTime = 0;
if (Date.now() - lastCheckTime > 3600000) { /* ... */ }

// ✅ 正确：持久化到文件
const stateFile = '/home/openclaw/data/heartbeat-state.json';
const state = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
if (Date.now() - state.lastCheck > 3600000) {
  state.lastCheck = Date.now();
  fs.writeFileSync(stateFile, JSON.stringify(state));
}
```

### Redis 任务队列（关键任务）

```js
await queue.add('sendNotification', {
  channel: 'feishu', userId: 'ou_xxx', message: 'Task done!'
}, {
  attempts: 3,
  backoff: { type: 'exponential', delay: 2000 }
});
```

---

## 五、资源溢出自动回收：内存不会爆

### PM2 内存监控

```js
// ecosystem.config.js
{
  max_memory_restart: '1G',  // 超 1G 自动重启
}
```

### Node.js 内存监控脚本

```js
const MB = 1024 * 1024;
setInterval(() => {
  const usage = process.memoryUsage();
  const heapUsed = usage.heapUsed / MB;
  console.log(`Memory: ${heapUsed.toFixed(2)}MB`);

  if (heapUsed > 1800) {
    console.error('Memory limit exceeded, exiting...');
    process.exit(1);  // 让 systemd/PM2 重启
  }
}, 60000);
```

启动时开启 GC：`node --expose-gc your-app.js`

### 文件句柄限制

```bash
# 永久提高（/etc/security/limits.conf）
* soft nofile 65535
* hard nofile 65535

# systemd
LimitNOFILE=65535
```

### 定期清理

```bash
# cleanup.sh - 清理 7 天前日志
find /var/log/openclaw -name "*.log" -mtime +7 -delete
find /tmp/openclaw -type f -mtime +1 -delete

# crontab
0 3 * * * /home/openclaw/scripts/cleanup.sh
```

---

## 六、日志与监控

### 日志轮转（logrotate）

```bash
# /etc/logrotate.d/openclaw
/var/log/openclaw/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 openclaw openclaw
}
```

### 检查清单

| 检查项 | 命令 | 预期结果 |
|--------|------|----------|
| 服务状态 | `systemctl status openclaw` | `active (running)` |
| 开机自启 | `systemctl is-enabled openclaw` | `enabled` |
| 日志正常 | `journalctl -u openclaw -n 50` | 无 ERROR |
| 内存使用 | `free -h` | 有余量 |
| 文件句柄 | `ulimit -n` | ≥ 65535 |
| 健康检查 | `curl localhost:9527/health` | `200 OK` |
| 定时任务 | `crontab -l` | 有 healthcheck |

---

## 核心原则

> **没有 100% 稳定的系统，只有 100% 可恢复的系统。**

| 保障层 | 工具 |
|--------|------|
| 进程守护 | systemd / PM2 |
| 异常重启 | healthcheck.sh + crontab |
| 断连重连 | 渠道内置重连 + 指数退避 |
| 断点续跑 | 进度持久化到文件 |
| 资源回收 | 内存监控 + 自动重启 |
| 日志追溯 | logrotate + journalctl |

---

## 脚本目录

- `scripts/healthcheck.sh` — 健康检查 + 自动重启
- `scripts/cleanup.sh` — 日志清理
- `scripts/network_monitor.sh` — 网络监控
- `scripts/ecosystem.config.js` — PM2 配置
- `references/task-resume.md` — 断点续跑详细文档
