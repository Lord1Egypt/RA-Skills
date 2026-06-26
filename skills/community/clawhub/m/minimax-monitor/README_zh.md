# MiniMax 套餐监控中心

[English](./README.md)

实时仪表盘，监控 MiniMax API 套餐使用情况，支持配额、速率探针、本周用量追踪，以及 24 小时历史趋势。

> **当前版本：v1.5.0** | [更新日志](#更新日志) | [安全说明](#安全与数据流)

![Dashboard](demo.png)

![License](https://img.shields.io/badge/License-MIT-blue)

---

## v1.5.0 新增

- 🆕 **24 小时用量历史端点**（`GET /api/history`）—— 每次配额查询自动写入 `history.jsonl` 环形 buffer，保留 24h
- 🆕 **响应式布局** —— 主面板高度 `min(560px, 100vh - 150px)`，小屏笔记本不再触发竖向滚动
- 🆕 **双语 README** —— `README.md`（英文）+ `README_zh.md`（本文件）互相跳转
- 🔒 v1.4.0 已落地的 CORS 严格化、header key 默认拒绝、localStorage 默认不加载 —— 详见 [安全与数据流](#安全与数据流)

## 更新日志

### v1.5.0（2026-06-25）
- 🆕 **`/api/history` 端点**：server 每次 `fetchQuota` 时把 `(timestamp, usedPct, modelSnapshot)` 追加到 `history.jsonl`，保留最近 24h；通过 `GET /api/history?hours=24` 暴露给前端画趋势线
- 🆕 **主面板响应式高度**：`min(560px, 100vh - 150px)`。小屏笔记本不再硬切滚动
- 🆕 **双语 README**：本文件 + 英文 `README.md` 互相跳转

### v1.4.0（2026-06-25）
- 🔒 **CORS 严格化**：`Access-Control-Allow-Origin: *` 改为 `127.0.0.1 / localhost / file://` 白名单。恶意网页无法再调用本机 server 消耗你的 MiniMax 配额
- 🔒 **Header API key 默认拒绝**：server 默认忽略 `X-MMX-API-Key` request header，需要时显式加 `--allow-header-key` flag。避免本机服务被当成"凭据代理"
- 🔒 **localStorage 默认不自动加载**：API key 不再自动从 localStorage 复用。增加"记住 24 小时"勾选框，勾选后临时写入，到期自动清除
- 🔒 **`--no-probe` flag**：关闭 `/api/probe` 端点（返回 403），避免真实推理请求消耗配额
- 📄 **SKILL.md / README 加 Security & Data Flow 章节**

### v1.3.0（2026-06-24）
- 🆙 **Video 模型"套餐未启用"识别**：与真正的"无限额"区分，海螺视频卡片变宽内嵌升级面板
- 🆙 **套餐对比 banner**：Plus / Max / Ultra 三档视频权益对比
- 🆙 **无周限账号识别**：`current_weekly_status=3` 的模型展示"无周限"
- 🐛 **大圆环 dasharray bug**：原硬编码 `515`（= 2πr）实际是半圆（πr ≈ 257.6），改用 `pathLength="100"` 归一化
- 🐛 **流式响应解析错误**：burst 探测改用 `data.trimStart().startsWith('data:')` 判定成功
- 🔧 **端口 9876 → 9877**：避让 minimax-embedding-adapter

### v1.2.0（2026-06-23）
- 🆙 **适配官方 Token Plan 新格式**：`/v1/token_plan/remains` 不再返回 `*_usage_count` / `*_total_count`，改为只返 `*_remaining_percent`。Server 推导已用%，前端契约保持不变
- 🆙 **飞书卡片文案同步**：5小时配额 / 模型明细 / 本周配额全部展示"已用 X% / 剩余 Y%"

### v1.1.0（2026-05-02）
- 🆕 **标签页自动刷新**：切换回浏览器标签时，自动触发一次配额和速率数据刷新，不再依赖定时轮询

### v1.0.0（2026-04-26）
- 初始版本，支持配额仪表盘 + 速率探针 + 飞书推送

---

## 功能特性

- 📊 **实时配额仪表盘** — 5小时窗口用量环形图 + 各模型明细
- ⏱️ **重置倒计时** — 自动计算距离窗口重置的剩余时间
- 📈 **API 速率探针** — TTFT、P50、Token 速度实测
- 📅 **本周配额追踪** — 有周限的模型显示本周已用/总额
- 📜 **24 小时用量历史**（v1.5.0）— 本地 `history.jsonl` 环形 buffer，前端可画趋势线
- 🔔 **飞书推送（可选）** — 查询后推送到飞书群

---

## 快速开始

### 前置要求

- Node.js ≥ 18（运行后端服务）
- Python 3（飞书推送可选）

### 安装

```bash
# 克隆或下载后进入目录
cd minimax-monitor

# 无需 npm install，纯 Node.js 标准库零依赖
```

### 启动

```bash
# 1. 启动后端服务
node mmx-monitor-server.js

# 2. 打开监控页面（macOS 自动唤起浏览器）
open mmx-monitor.html
# Windows: start mmx-monitor.html
# Linux: xdg-open mmx-monitor.html
```

### 查询配额

页面打开后，点击输入框上方的 **查询** 按钮（API Key 会自动读取本地 mmx 配置），或手动粘贴 Key 后查询。

---

## 安全与数据流（v1.4.0+）

**本服务默认会**：

1. **读取本地凭证**：从 `~/.mmx/config.json` 读取 `api_key`（MiniMax Token Plan key）
2. **每 60s 调 MiniMax API**：调 `https://www.minimaxi.com/v1/token_plan/remains` 拿配额数据
3. **每 60s 主动探测 MiniMax 推理性能**（默认开启）：发真实 streaming + 并发请求到 `api.minimaxi.com/v1/text/chatcompletion_v2`，计入会产生 token 费用
4. **可选推送到飞书**（需手动运行 `mmx_quota_feishu.py`，默认不开启）

**本服务不会**：

- 不会把 API key 上传到任何远程
- 不会把 MiniMax API key 推到 Feishu；推送的是**配额查询结果**（百分比数字）
- 不会允许跨源网页调用本机 server（CORS allowlist 限定 `127.0.0.1 / localhost / file://`）

### 启动选项

```bash
# 默认配置（推荐）
node mmx-monitor-server.js

# 关闭主动探测（节省配额）
node mmx-monitor-server.js --no-probe

# 启用 header API key 透传（高级用户，自负责）
node mmx-monitor-server.js --allow-header-key
```

### 浏览器中的 API Key

v1.4.0 起，**默认不会**从 localStorage 自动加载 API Key。如果想 24 小时内免输入：

- 页面顶部"记住 24 小时"勾选后输入 Key
- 到期后自动清除

---

## 配置文件

### 环境变量（飞书推送，可选）

```bash
# 复制模板
cp .env.example .env

# 填写以下变量
MINIMAX_API_KEY=sk-cp-…here      # MiniMax API Key（Token Plan 类型）
FEISHU_APP_ID=your-app-id                 # 飞书应用 App ID
FEISHU_APP_SECRET=***        # 飞书应用 App Secret
FEISHU_CHAT_ID=your-chat-id               # 飞书群 ID
```

### mmx 本地配置（自动读取）

后端服务会自动读取 `~/.mmx/config.json` 中的 API Key，无需手动配置。

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `mmx-monitor.html` | 监控页面（纯前端，单文件 HTML） |
| `mmx-monitor-server.js` | 本地代理服务（Node.js，端口 9877） |
| `mmx_quota_feishu.py` | 飞书推送脚本（可选） |
| `history.jsonl` | 24h 用量历史（v1.5.0+，自动生成） |
| `CHANGELOG.md` | 完整更新日志（带版本对比链接） |
| `demo.png` | 监控页面截图 |
| `README.md` | 英文 README |
| `README_zh.md` | 本文件（中文） |
| `LICENSE` | MIT 开源协议 |

---

## API 接口

后端提供以下 REST 接口：

| 接口 | 说明 |
|------|------|
| `GET /api/token_plan` | 从 MiniMax 官方获取配额（推荐） |
| `GET /api/probe` | 实时 API 延迟探针（`--no-probe` 时返回 403） |
| `GET /api/history?hours=24` | 24h 用量历史（v1.5.0） |
| `GET /health` | 健康检查 |

> `/api/quota` 已在 v1.3.0 移除（被 `/api/token_plan` 取代）。

---

## 飞书推送（可选）

### 方式一：命令行推送

```bash
python3 mmx_quota_feishu.py <api_key>
```

### 方式二：配合定时任务

设置 cron 定时推送，结合 `.env` 中的飞书配置。

---

## 常见问题

**Q: 点查询后显示"连接失败"？**
A: 请确认后端服务已启动（`node mmx-monitor-server.js`）。服务未运行时前端会提示"请先启动后端服务"。

**Q: 端口 9877 被占用？**
A: 停止占用该端口的进程，或修改 `mmx-monitor-server.js` 中的 `PORT` 常量。

**Q: 飞书推送失败？**
A: 确认 `.env` 中 `FEISHU_APP_ID`、`FEISHU_APP_SECRET`、`FEISHU_CHAT_ID` 均已填写，且飞书机器人已加入目标群。

---

## 开源协议

MIT License - 详见 [LICENSE](LICENSE) 文件。
