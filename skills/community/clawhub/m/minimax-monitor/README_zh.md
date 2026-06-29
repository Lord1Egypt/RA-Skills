# MiniMax 套餐监控中心

[English](./README.md)

实时本地仪表盘，监控 MiniMax API 套餐使用情况，支持配额、按需速率测试、本周用量追踪、24 小时历史趋势。

> **当前版本：v1.6.2** | [更新日志](CHANGELOG.md) | [许可证](LICENSE)

![Dashboard](demo.png)

![License](https://img.shields.io/badge/License-MIT-blue)

---

## v1.6.2 功能

### 配额监控

- 📊 **4 小时 / 24 小时 / 本周** 三档用量追踪 — 主圆环按用户当前 Token Plan 套餐的实际周期动态显示
- 🎯 **模型卡片** 区分 4h 限额 / 24h 限额 / 周无限额 / 套餐未启用(视频模型 status=3 元数据不可区分时显示"套餐未启用 · 不可调用"提示并排除出 4h 聚合)
- 📈 **24 小时趋势线** — 本地 `history.jsonl` 滚动 buffer 记录每次 `token_plan` 调用的用量快照

### 速率测试(按需)

- ⚡ **TTFT / P50 / 突发并发 / token·s** 四项指标,基于真实 chat completion 请求
- ⚠️ **UI 红字 + confirm() 二次确认** — 每次测试消耗约 180 token,需用户主动确认,不点不动

### 安全

- 🔒 **本地凭证按需加载** — Server 启动**不读** `~/.mmx/config.json`。用户在仪表盘顶部点 "加载本地凭证" 按钮 + `confirm()` 二次确认后,才通过 `POST /api/load_cred` 读取 API key,存入 server 进程内存(不写磁盘、不写浏览器、不上传)
- 🔒 **`/api/load_cred` 响应不含完整 API key** — 只回 `keyLength` + `keyPrefix`(前 6 字符,用于视觉确认 `sk-cp-` 前缀)
- 🔒 **`/api/load_cred` 拒绝空 Referer** — 强制 `Referer` 是本机白名单 `127.0.0.1 / localhost / file://` 之一
- 🔒 **CORS 严格** — `Access-Control-Allow-Origin` 仅放行 `127.0.0.1 / localhost / file://`
- 🔒 **不向远程传输 key** — API key 永不离开本机

---

## 快速开始

### 前置条件

- Node.js ≥ 18

### 运行

```bash
# 1. 启动后端服务
node mmx-monitor-server.js

# 2. 打开浏览器(macOS 自动唤起 http://127.0.0.1:9877/)
open http://127.0.0.1:9877/
# Windows / Linux: 手动访问 http://127.0.0.1:9877/
```

### 加载 API Key

页面打开后,点击顶部 **"加载本地凭证"** 按钮 → 确认 → 从 `~/.mmx/config.json` 读取 key 存入 server 进程内存。或直接在输入框粘贴 key。

---

## 启动选项

```bash
# 默认
node mmx-monitor-server.js

# 启用 X-MMX-API-Key header 透传(高级)
node mmx-monitor-server.js --allow-header-key

# 关闭 /api/probe 端点(完全不发起推理调用)
node mmx-monitor-server.js --no-probe
```

---

## 配置

### mmx 本地配置(按需加载)

后端服务**不**自动读取 `~/.mmx/config.json`。需要时点仪表盘顶部的 **"加载本地凭证"** 按钮,触发 `confirm()` 二次确认后才会调用 `POST /api/load_cred` 读取 API key,存入 server 进程内存(不写磁盘、不出现在 HTTP 响应里)。Server 重启后 key 丢失,需要重新点击按钮加载;未加载时所有需要 key 的端点返 401。

### 环境变量(备选)

如果 `~/.mmx/config.json` 不存在:

```bash
# 复制模板
cp .env.example .env

MINIMAX_API_KEY=sk-cp-…here           # MiniMax API Key(Token Plan 类型)
```

---

## 安全与数据流

**本服务默认会**:

1. **按需加载本地凭证** — 仪表盘"加载本地凭证"按钮触发 `POST /api/load_cred`,从 `~/.mmx/config.json` 读取 API key 到 server 进程内存(不写浏览器 / 不写文件 / server 重启后丢失)。未加载时所有需要 key 的端点返 401。
2. **每 60s 调 MiniMax API** — `https://www.minimaxi.com/v1/token_plan/remains` 拿配额数据。
3. **写入本地用量采样** — 每次配额拉取后追加到 `<skill-dir>/history.jsonl`(24h 滚动 buffer,只含用量百分比,不含凭证)。
4. **速率测试需用户主动触发** — 仪表盘按钮 + `confirm()` 才发起 5 次 chat completion 请求(约 180 token)。

**本服务不会**:

- 启动时自动读取 `~/.mmx/config.json`
- 在任何 HTTP 响应中返回完整 API key
- 接受空 Referer 调凭证加载端点
- 允许跨源网页调用本机 server
- 自动或定时运行速率测试

---

## API 端点

| 端点 | 说明 |
|------|------|
| `POST /api/load_cred` | 从 `~/.mmx/config.json` 加载 API key(用户点按钮 + confirm) |
| `GET /api/token_plan` | 从 MiniMax 官方拉取配额(需已加载 key) |
| `GET /api/probe` | 按需 API 延迟探测(用户点按钮 + confirm,需已加载 key) |
| `GET /api/history?hours=24` | 24h 用量历史(本地滚动 buffer) |
| `GET /health` | 健康检查 |

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `mmx-monitor.html` | 监控页面(单文件 HTML 前端) |
| `mmx-monitor-server.js` | 本地代理服务(Node.js,端口 9877) |
| `history.jsonl` | 24h 用量历史滚动 buffer(自动生成,不入 git) |
| `SKILL.md` | 技能定义 |
| `CHANGELOG.md` | 完整版本历史 |
| `demo.png` | 仪表盘截图 |
| `LICENSE` | MIT 许可证 |

---

## 常见问题

**Q: 点击查询后提示"连接失败"?**
A: 确认后端服务在跑(`node mmx-monitor-server.js`)。

**Q: 端口 9877 被占用?**
A: 停掉占用该端口的进程,或修改 `mmx-monitor-server.js` 中的 `PORT` 常量。

---

## 许可证

MIT License — 见 [LICENSE](LICENSE)。