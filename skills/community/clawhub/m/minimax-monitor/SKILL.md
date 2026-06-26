---
name: minimax-monitor
description: MiniMax 套餐监控中心。触发词：打开 minimax 监控、minimax 监控、minimax 仪表盘。
version: 1.5.0
---

# MiniMax 套餐监控中心

> **触发词**：查配额 / 打开配额监控 / 启动 MiniMax 监控
> 当前版本：v1.5.0

## 更新日志

### v1.5.0（2026-06-25）
- 🆕 **`/api/history` 端点**：server 每次 `fetchQuota` 时把 `(timestamp, usedPct, modelSnapshot)` 追加到 `history.jsonl`，保留最近 24h（自动 trim）。`GET /api/history?hours=24` 返回历史采样，供前端画趋势线。
- 🆕 **主面板响应式高度**：`min(560px, vh-150px)`，小屏笔记本（700-800px 高度）不滚动。JS 调 fitMainH() 写 `--main-h` CSS 变量；main-grid `height: var(--main-h, 560px)` + `max-height: calc(100vh - 150px)` 双闸。
- 🆕 **双语 README**：`README.md`（英文）+ `README_zh.md`（中文）互相跳转。
- 🆕 **`.gitignore` 加 `history.jsonl`**：24h 滚动 buffer 不入 git。
- 🔧 **SKILL.md frontmatter version 同步到 1.5.0**。

### v1.4.0（2026-06-25）
- 🔒 **安全加固**（响应 ClawHub security-audit 13 条 finding）：
  - **F5 CORS `*` → 本机白名单**：`Access-Control-Allow-Origin` 从 `*` 改成 `127.0.0.1/localhost/file://` allowlist。恶意网页不再能跨域调本机 server 消耗你的 MiniMax 配额。
  - **F3 header API key 默认拒绝**：server 默认忽略 `X-MMX-API-Key` header，只用本机 `~/.mmx/config.json` 的 key。需要使用 header key 时显式开启 `node mmx-monitor-server.js --allow-header-key`。
  - **F11 凭证读 取明确告知**：启动 banner 列出 “读取 ~/.mmx/config.json” + CORS / header key / probe 状态。
  - **F13 localStorage 默认不加载**：API key 默认每次重启重新输入。加勾选 “记住 24 小时” 后才临时写入 localStorage，过期自动清除。
  - **F4 probe 可关闭**：担心真实 inference 探测消耗配额的话，用 `node mmx-monitor-server.js --no-probe`，`/api/probe` 端点返回 403。
  - **F6/F10 README / SKILL.md 加 Security & Data Flow 章节**（见下文）。

### v1.3.0（2026-06-24）
- 🆙 **识别 `current_interval_status === 3` 的“套餐未启用”场景**：官方 API 在视频额度上会返 status=3 但实际调 API 被拒“用量上限”。这跟真正的“无限额”（语音/音乐/图像）同码，元数据无法区分。后端加 `interval_unlimited: true` 字段，前端模型卡片显示“套餐未启用 · 不可调用”（红字 + 灰底 + bar 灰调），不参与顶部 4h 聚合。
- 🆙 **套餐对比 banner**：检测到 video 未启用时，海螺视频卡片变宽（`grid-column: 1 / -1`）内嵌升级面板，列出三档套餐视频权益（Plus ¥49 不支持 / Max ¥119 3 条/日 + “推荐”标 / Ultra ¥469 5 条/日，数据来源官方订阅页 2026-06-24 截图），含“查看官方套餐”跳转链接。设计思路：与在顶部单独挂 banner 比，升级信息与“不可调用”卡片合一，用户视线从“为什么红了”直接跳到“怎么解锁”。
- 🔧 **端口 9876 → 9877**：避让 minimax-embedding-adapter（监听 127.0.0.1:9876 IPv4）。两个服务撞端口会随机抢答。

### v1.2.0（2026-06-23）
- 🆙 **适配官方 Token Plan 新格式**：官方 `/v1/token_plan/remains` 不再返回 `current_interval_usage_count` / `current_interval_total_count`，改为只返 `*_remaining_percent`（剩余百分比）。Server 把 `used` 推导成"已用%"、`total` 恒 100，前端契约保持不变。
- 🆙 **飞书卡片文案同步**：5小时配额 / 模型明细 / 本周配额全部展示"已用 X% / 剩余 Y%"，不再打印"0/100"基数。
- 🐛 **大圆环 dasharray bug**：原代码 `stroke-dasharray="(pct/100*515) 515"` 硬编码 515（= 2πr），但实际路径是半圆（πr ≈ 257.6），导致 pct ≥ 50% 时圆环已填满但数字还显示 60% 多。改用 `pathLength="100"` 归一化，dasharray 直接 `pct 100`。
- 🆙 **stat 数字加 % 后缀**：5小时/本周所有 stat 数字（已用、剩余、总、每周已用、每周总额）都加上 `%`，让单位语义清晰。
- 🆙 **无周限账号识别**：根据官方 `current_weekly_status=3` 判定模型本周无配额上限，前端 stat 与模型卡片、飞书卡片均展示"无周限"字样，不再误显"已用 0% / 100%"。
- 🔧 `buildModels` 增加 `clampPct()` 守卫，防止 `remaining_percent` 越界或缺失。

### v1.1.0（2026-05-02）
- 🆕 **标签页自动刷新**：切换回浏览器标签时，自动触发一次配额和速率数据刷新，不再依赖定时轮询

### v1.0.0（2026-04-26）
- 初始版本，支持配额仪表盘 + 速率探针 + 飞书推送

# MiniMax 套餐监控中心

> **触发词**：打开 minimax 监控 / minimax 监控 / minimax 仪表盘
> 启动后 **自动用 `open` 命令打开 HTML 页面**（macOS 直接唤起浏览器），无需手动拖入。

## Security & Data Flow（v1.4.0）

本技能默认会：

1. **读取本地凭证**：从 `~/.mmx/config.json` 读取 `api_key`（MiniMax Token Plan key）。
2. **定时调用 MiniMax API**：每 60s 调 `https://www.minimaxi.com/v1/token_plan/remains` 拿配额数据。
3. **主动探测 MiniMax 推理性能**（v1.4.0 默认开启）：每 60s 发真实 streaming / concurrent 请求到 `api.minimaxi.com/v1/text/chatcompletion_v2`，计入会产生 token 费用。
4. **可选推送到飞书**（需手动运行 `mmx_quota_feishu.py`，默认不开启）。

**不会做**：

- 不会把 API key 上传到任何远程（仅本地使用）。
- 不会把 MiniMax API key 推到 Feishu；推送的是**配额查询结果**（百分比数字）。
- 不会允许跨源网页调用本机 server（CORS allowlist 限定 `127.0.0.1/localhost/file://`）。

**想关闭主动探测**（节省配额）：`node mmx-monitor-server.js --no-probe`
**想使用 header 透传 key**（高级用户，需要自负责）：`node mmx-monitor-server.js --allow-header-key`

## 技能简介

MiniMax API 套餐使用情况实时监控，支持**网页端**和**飞书端**两种查询方式。

## 文件说明

| 文件 | 说明 |
|------|------|
| `mmx-monitor.html` | 监控页面（前端，单文件 HTML，三栏仪表盘） |
| `mmx-monitor-server.js` | 本地代理服务（Node.js，连接 MiniMax API，端口 9877） |
| `mmx_quota_feishu.py` | 飞书推送脚本（查询配额后推送到飞书） |

## 使用方式

### 方式一：网页端（实时仪表盘）

1. 启动后端服务（如未运行）：
   ```bash
   node ~/.openclaw/workspace/skills/minimax-monitor/mmx-monitor-server.js
   ```
2. 我会自动执行 `open` 命令打开 `mmx-monitor.html`，浏览器自动加载

### 方式二：飞书端（问"查配额"时触发）

直接对我说**查配额**，我运行脚本把当前配额以飞书卡片形式推给你。

手动运行：
```bash
python3 ~/.openclaw/workspace/skills/minimax-monitor/mmx_quota_feishu.py <api_key>
```

## 飞书卡片内容

- 5小时总体配额使用率 + 已用/总额/剩余
- 重置倒计时
- 各模型明细（颜色标记：🟢<75% 🟡75-94% 🔴95%+）
- 本周配额（如有）

## 环境变量

| 变量 | 说明 |
|------|------|
| `MINIMAX_API_KEY` | MiniMax API Key（Token Plan 类型） |
| `FEISHU_APP_ID` | 飞书机器人 App ID |
| `FEISHU_APP_SECRET` | 飞书机器人 App Secret |
| `FEISHU_CHAT_ID` | 默认推送群 ID |

## 注意事项

- 后端服务需在页面之前启动，端口 9877（v1.3.0 起避开 9876 的 minimax-embedding-adapter）
- 页面刷新间隔：配额 60s，速率 60s
- API Key 类型必须是 `sk-cp-` 开头（Token Plan）
