# MiniMax 套餐监控中心

[English](./README.md)

实时本地仪表盘，监控 MiniMax API 套餐使用情况，支持配额、按需速率测试、本周用量追踪、24 小时历史趋势。

> **当前版本：v1.7.0** | [更新日志](CHANGELOG.md) | [许可证](LICENSE)

![Dashboard](demo.png)

![License](https://img.shields.io/badge/License-MIT-blue)

---

## v1.7.0 功能(v1.6.7 → v1.7.0 增量)

### v1.7.0 安全加固

- 🔒 **凭证不在 server 进程内存中常驻** — 每次需要 API key 的请求由 `loadKeyForRequest()` 现读 `~/.mmx/config.json`,用完即出栈,Node.js GC 一轮后释放。**进程内存 dump 拿不到完整 key**(lldb 验证: `memory find --string "sk-cp-"` 在 rw 段无命中)。
- 🔒 **`/api/load_cred` 不再写入模块作用域** — 仅向前端返回"凭证已就绪"标记 + `keyLength`/`keyPrefix`(前 6 字符)。前端 `credLoaded=true` 现在是 UX 标记,不再控制权限。
- 🔒 **lsof 验证** — server 进程不再持有 `~/.mmx/config.json` open fd,按需 `fs.readFileSync` 立即关闭。

### 配额监控

- 📊 **4 小时 / 24 小时 / 本周** 三档用量追踪 — 主圆环按用户当前 Token Plan 套餐的实际周期动态显示
- 🎯 **模型卡片** 区分 4h 限额 / 24h 限额 / 周无限额 / 套餐未启用(视频模型 status=3 元数据不可区分时显示"套餐未启用 · 不可调用"提示并排除出 4h 聚合)
- 📈 **24 小时趋势线** — 本地 `history.jsonl` 滚动 buffer 记录每次 `token_plan` 调用的用量快照

### 速率测试(按需)

- ⚡ **TTFT / P50 / 突发并发 / token·s** 四项指标,基于真实 chat completion 请求
- ⚠️ **UI 红字 + confirm() 二次确认** — 每次测试消耗约 180 token,需用户主动确认,不点不动

### 安全(v1.6.x 累计)

- 🔒 **本地凭证按需加载** — Server 启动**不读** `~/.mmx/config.json`。用户在仪表盘顶部点 "加载本地凭证" 按钮 + `confirm()` 二次确认后,才通过 `POST /api/load_cred` 读取 API key。Server 重启后 key 丢失(v1.7.0 起 key 也从不进 server 内存,仅磁盘上原生存在的 `~/.mmx/config.json`)。
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

页面打开后,点击顶部 **"加载本地凭证"** 按钮 → 确认 → server 被授权按需读 `~/.mmx/config.json`。每次 `/api/token_plan` / `/api/probe` 调用时现读磁盘、用完即丢弃(不缓存到 server 进程内存)。或在输入框直接粘贴 key 走 `--allow-header-key` 模式。

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

### mmx 本地配置(按需读取,从不缓存)

后端服务**不**自动读取 `~/.mmx/config.json`,也**不**把 key 缓存到 server 进程内存。需要时点仪表盘顶部的 **"加载本地凭证"** 按钮,触发 `confirm()` 二次确认后 server 会被授权按需读 `~/.mmx/config.json`(每次需要 key 的请求现读一次,用完即出栈)。key 永不写磁盘、永不出现在 HTTP 响应里、永不进 server 进程内存(v1.7.0 起)。

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

1. **按需读取本地凭证(v1.7.0: 不进内存)** — 仪表盘"加载本地凭证"按钮触发 `POST /api/load_cred`,server 获得按需读 `~/.mmx/config.json` 的授权。**v1.7.0 起**:key 不写进 server 进程内存,每次需要时由 `loadKeyForRequest()` 现读磁盘、用完即出栈。不写浏览器 / 不写文件 / 不出现在 HTTP 响应里。`lldb memory find` 在 server 进程 rw 段无 key 命中。
2. **每 60s 调 MiniMax API** — `https://www.minimaxi.com/v1/token_plan/remains` 拿配额数据。
3. **写入本地用量采样** — 每次配额拉取后追加到 `<skill-dir>/history.jsonl`(24h 滚动 buffer,只含用量百分比,不含凭证)。
4. **速率测试需用户主动触发** — 仪表盘按钮 + `confirm()` 才发起 5 次 chat completion 请求(约 180 token)。

**本服务不会**:

- 启动时自动读取 `~/.mmx/config.json`
- 把 key 缓存到 server 进程内存(v1.7.0 起);每次现读磁盘用完即出栈
- 在任何 HTTP 响应中返回完整 API key
- 接受空 Referer 调凭证加载端点
- 允许跨源网页调用本机 server
- 自动或定时运行速率测试

---

## API 端点

| 端点 | 说明 |
|------|------|
| `POST /api/load_cred` | 授权 server 按需读 `~/.mmx/config.json`(用户点按钮 + confirm;不缓存 key 到内存) |
| `GET /api/token_plan` | 从 MiniMax 官方拉取配额(每次现读磁盘 key) |
| `GET /api/probe` | 按需 API 延迟探测(用户点按钮 + confirm,每次现读磁盘 key) |
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
