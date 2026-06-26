# Changelog

All notable changes to MiniMax Monitor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.5.0] - 2026-06-25

### ✨ Features

- **`/api/history` 端点（24h 滚动 buffer）**。每次 `fetchQuota` 把 `(ts, used, total, models[])` 追加到 `history.jsonl`，超过 24h 的行自动 trim。`GET /api/history?hours=24` 返回历史采样供前端画趋势线。典型场景：想看到今天配额从早到晚是稳步上升还是被某次 batch 快速消耗。
- **主面板响应式高度**。`min(560px, 100vh-150px)`，小屏笔记本（700-800px 高度）不再触发竖向滚动。JS 调 `fitMainH()` 写 `--main-h` CSS 变量；main-grid `height: var(--main-h, 560px)` + `max-height: calc(100vh - 150px)` 双闸。
- **双语 README**。`README.md`（英文）+ `README_zh.md`（中文）互相跳转。
- **`.gitignore` 加 `history.jsonl`**。24h 滚动 buffer 是运行产物，不入版本控制。
- **SKILL.md frontmatter version 同步到 1.5.0**。

## [1.4.0] - 2026-06-25

### 🔒 Security（响应 ClawHub security-audit 13 条 finding）

- **CORS 严格化**（F5，97% confidence）。`Access-Control-Allow-Origin: *` 改为 `127.0.0.1/localhost/file://` allowlist。任何跨域网页不再能调用本机 server，防止恶意站点消耗你的 MiniMax 配额。
- **Header API key 默认拒绝**（F3，94%）。server 默认忽略 `X-MMX-API-Key` request header，不再变成"凭据代理"。需要使用 header key 时显式开启：`node mmx-monitor-server.js --allow-header-key`。
- **凭证读取明确告知**（F11，87%）。启动 banner 列出 CORS 策略、header key 状态、probe 状态、以及会读取的 `~/.mmx/config.json` 路径。
- **localStorage 默认不自动加载**（F13，94%）。API key 不再自动从 localStorage 加载复用。增加"记住 24 小时"勾选框，勾选后临时写入 localStorage，到期自动清除。
- **Probe endpoint 可关闭**（F4，92%）。担心真实 inference 探测消耗配额的话，用 `node mmx-monitor-server.js --no-probe`，`/api/probe` 端点返回 403。
- **Security & Data Flow 文档**（F1/F6/F10）。SKILL.md 顶部新增章节，列出会读什么（`~/.mmx/config.json`）、会发什么（`api.minimaxi.com`、`open.feishu.cn`）、不会做什么（不上传 key、不推 key 到 Feishu）。
- **触发词收窄**（F7/F8）。"查配额" 这个泛词被替换为更明确的 "打开 minimax 监控" / "minimax 监控" / "minimax 仪表盘"，减少误触。

## [1.3.0] - 2026-06-24

### ✨ Features

- **Video 模型"套餐未启用"识别**。官方 `/v1/token_plan/remains` 在 video 额度上会返回 `current_interval_status=3`，但实际调 API 被拒"用量上限"。这跟真正的"无限额"（语音/音乐/图像）同码，元数据无法区分。后端加 `interval_unlimited: true` 字段，前端模型卡片显示"套餐未启用 · 不可调用"（红字 + 灰底 + bar 灰调），不参与顶部 4h 聚合。
- **套餐对比 banner**。检测到 video 未启用时，海螺视频卡片变宽（`grid-column: 1 / -1`）内嵌升级面板，列出三档套餐视频权益（Plus ¥49 不支持 / Max ¥119 3 条/日 + "推荐"标 / Ultra ¥469 5 条/日，数据来源官方订阅页 2026-06-24 截图），含"查看官方套餐"跳转链接。
- **官方 Token Plan 新格式适配**。`/v1/token_plan/remains` 不再返回 `current_interval_usage_count` / `current_interval_total_count`，改为只返 `*_remaining_percent`（剩余百分比）。server 把 `used` 推导成"已用%"、`total` 恒 100，前端契约保持不变。
- **飞书卡片文案同步**。5小时配额 / 模型明细 / 本周配额全部展示"已用 X% / 剩余 Y%"，不再打印"0/100"基数。
- **无周限账号识别**。根据官方 `current_weekly_status=3` 判定模型本周无配额上限，前端 stat 与模型卡片、飞书卡片均展示"无周限"字样，不再误显"已用 0% / 100%"。
- **端口 9876 → 9877**。避让 minimax-embedding-adapter（监听 `127.0.0.1:9876` IPv4）。两个服务撞端口会随机抢答。

### 🐛 Bug Fixes

- **大圆环 dasharray bug**。原代码 `stroke-dasharray="(pct/100*515) 515"` 硬编码 515（= 2πr），但实际路径是半圆（πr ≈ 257.6），导致 pct ≥ 50% 时圆环已填满但数字还显示 60% 多。改用 `pathLength="100"` 归一化，dasharray 直接 `pct 100`。
- **流式响应解析错误**。SSE 流式响应是多行 `data: {...}\n\n...` 格式，`parseJson` 整块会失败。`burst` 探测改用 `data.trimStart().startsWith('data:')` 判定成功。
- **MODEL_NAME_MAP 修正**。`MiniMax-Hailuo-2.3-6s-768p` 之前错写为 `2.0-Pro-HD`，改为正确的 `Hailuo-2.3-768P`。新增 `'video': '海螺视频'` 映射。
- **删 p99 编造字段**。原 `p99` 字段是 `latency * 1.4` 写死的，不是真实测量，删除。
- **删 /api/quota endpoint**。被 v1.2.0 协议变更后已经空跑，删除。
- **buildModels 增加 clampPct() 守卫**，防止 `remaining_percent` 越界或缺失。

## [1.2.0] - 2026-06-23

### ✨ Features

- **官方 Token Plan 新格式适配**（同 v1.3.0 修复项，已记录于此）。
- **stat 数字加 % 后缀**。5小时/本周所有 stat 数字（已用、剩余、总、每周已用、每周总额）都加上 `%`，让单位语义清晰。

### 🐛 Bug Fixes

- **大圆环 dasharray bug**（同 v1.3.0 修复项，已记录于此）。

## [1.1.0] - 2026-04-26

### ✨ Features

- **标签页自动刷新**。切换回浏览器标签时，自动触发一次配额和速率数据刷新，不再依赖定时轮询。

## [1.0.0] - 2026-04-26

### ✨ Initial Release

- 实时配额仪表盘（5h 重置倒计时、模型明细、本周配额）
- API 速率探针（SEQ-10 顺序、BURST-3 并发、TTFT、延迟、Tokens/s）
- 飞书推送（可选）
- 双层卡片布局（glass-card 玻璃质感）

[Unreleased]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.5.0...HEAD
[1.5.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.0.0...v1.1.0
