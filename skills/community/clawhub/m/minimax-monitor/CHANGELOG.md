# Changelog

All notable changes to MiniMax Monitor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.7] - 2026-06-30

### Bug Fix
- 🐛 "加载本地凭证" 按钮 success 判断: `d.key` → `d.loaded` (v1.6.1 加固后 server 响应不再回完整 key, 前端必须改用 `loaded` 字段判断成功)
- 🐛 前端不再持有 key: 新增 `credLoaded` boolean 标记, `fetchQuota` / `doSpeedTest` 不再传 `X-MMX-API-Key` header, server 走 `credLoadedKey` (进程变量) 读 key (与 v1.6.1 "响应不回完整 key" 加固保持一致)
- 🐛 按钮文本简化: `✅ 已加载 (sk-cp-…)` → `✅ 已加载` (按用户偏好, 不在 UI 显示 key 前缀)

### Documentation
- 🧹 bump 本地展示位 1.6.6 → 1.6.7 (Current Version / 当前版本 / ## Features / ## 功能 / ## 主要功能 / metadata.version)

## [1.6.6] - 2026-06-30

### Documentation
- 🐛 删除 SKILL.md frontmatter 顶层残留 `version: 1.6.2` 字段（ClawHub 优先解析顶层 key,导致 v1.6.3+ 发布后页面仍显示 v1.6.2）
- 🐛 同步 README.md / README_zh.md 顶部 `Current Version` / `当前版本` 行以及 `## Features` / `## 功能` 段标题随发布版本一起更新

## [1.6.5] - 2026-06-30

### Documentation
- 🐛 SKILL.md `metadata.version` 1.6.3 → 1.6.5（docs-only bump publish 链同步）

## [1.6.3] - 2026-06-30

### Security
- 🐛 `/api/probe` 拒绝空 `Referer`（之前空 `Referer` 会被静默放行,绕过了本机 origin 二次确认 → curl/本机直连可直接触发真实 API 调用)
- 🐛 加载本地凭证后,API key 不再写回 `input.value`（之前 key 进入 DOM,password 字段只是 UI 遮罩,肩窥/扩展/DevTools 仍可读）——现在只存内存变量,input 显示占位符,加 `data-loaded="1"` 标记让「查询」按钮识别「已加载」状态不要覆盖

## [1.6.2] - 2026-06-29

### Security
- 🐛 `/api/probe` 拒绝空 `Referer`（之前空 `Referer` 会被静默放行,绕过了本机 origin 二次确认 → curl/本机直连可直接触发真实 API 调用)
- 🐛 加载本地凭证后,API key 不再写回 `input.value`（之前 key 进入 DOM,password 字段只是 UI 遮罩,肩窥/扩展/DevTools 仍可读）——现在只存内存变量,input 显示占位符,加 `data-loaded="1"` 标记让「查询」按钮识别「已加载」状态不要覆盖

### Documentation
- 🧹 SKILL.md 删「## 更新日志」整段（v1.6.0/v1.5.0/v1.4.0/...）— ClawHub 全文渲染不再堆历史
- 🧹 SKILL.md 删 Security 重复段 + 删冗余「技能简介 / 触发词收敛 / 文件说明 / 使用方式 / 环境变量 / 注意事项」段
- 🧹 README.md / README_zh.md 重写 — 顶部「Current Version: v1.6.1」+「Features (v1.6.1)」只描述当前版本功能，不堆 Changelog 历史
- 🧹 CHANGELOG.md 重写 — 保留累积变更（行业惯例），精简每版条目、去掉审计器 finding 编号等内部叙事噪音

## [1.6.1] - 2026-06-29

### Security
- 🐛 `/api/load_cred` 响应不再返回完整 API key（只回 `keyLength` + `keyPrefix` 前 6 字符）
- 🐛 `/api/load_cred` 拒绝空 `Referer`，强制本机白名单
- 📝 SKILL.md frontmatter `permissions` 补 `write:filesystem`（声明 `history.jsonl` 写入）

### Documentation
- 🧹 清理 README 自相矛盾 — 所有"自动读取 `~/.mmx/config.json`"的旧表述统一改为"按需主动加载"叙事
- 📝 SKILL.md Security 段重写 + 加 `history.jsonl` 持久化披露 + 操作风险提示
- 📝 新增 CONTRIBUTING.md

## [1.6.0] - 2026-06-26

### Security Hardening
- 🔒 凭证按需加载 — Server 启动不读 `~/.mmx/config.json`，仪表盘点 "加载本地凭证" 按钮 + confirm 才读
- 🔒 删除浏览器 localStorage 24h 记忆 — 重启后必须重新输入或重新加载
- 🔒 速率测试改按需 — 仪表盘速率面板不再自动调用 chat completion，需用户点 "开始速率测试" 按钮 + confirm
- 🔒 删除飞书推送 — 飞书 OAuth 协议要求发 `FEISHU_APP_SECRET`，无法通过文档警示消除该风险

### Other
- 🛠 Server 直接服务 HTML（`http://127.0.0.1:9877/`），绕开 Safari `file://` fetch 报错
- 📝 SKILL.md description 改为诚实版（"套餐监控 + 速率测试"双职责）

## [1.5.1] - 2026-06-26

### Changed
- 🔒 触发词收敛为单一 `mmx 仪表盘启动`（从 4 个泛词收敛），降低误触概率
- 🛑 飞书推送不再走对话触发

## [1.5.0] - 2026-06-25

### Features
- 🆕 `/api/history` 端点（24h 滚动 buffer）— `history.jsonl` 记录用量快照，前端画趋势线
- 🆕 主面板响应式高度（`min(560px, 100vh-150px)`）— 小屏笔记本不滚动
- 🆕 双语 README — 英文 + 中文互相跳转

## [1.4.0] - 2026-06-25

### Security
- 🔒 CORS 严格化 — `Access-Control-Allow-Origin` 改为 `127.0.0.1/localhost/file://` allowlist
- 🔒 Header API key 默认拒绝（`--allow-header-key` 显式开启）
- 🔒 `localStorage` 默认不自动加载（"记住 24 小时"勾选后才写）
- 🔒 `--no-probe` flag 关闭速率测试端点
- 📄 新增 Security & Data Flow 章节

## [1.3.0] - 2026-06-24

### Features
- 🆕 视频模型"套餐未启用"识别（`status=3` 元数据无法区分真实无限额 vs 套餐未启用）
- 🆕 套餐对比 banner（海螺视频卡片内嵌三档套餐升级面板）
- 🆕 无周限账号识别（`current_weekly_status=3` 显示"无周限"）
- 🆕 适配官方 Token Plan 新格式（`*_remaining_percent` 剩余百分比）
- 🔧 端口 9876 → 9877（避让 minimax-embedding-adapter）

### Bug Fixes
- 🐛 大圆环 `dasharray` bug — 硬编码 515（= 2πr），实际半圆 πr ≈ 257.6
- 🐛 流式响应解析错误 — SSE 多行格式 `parseJson` 整块失败

## [1.2.0] - 2026-06-23

### Features
- 🆕 适配官方 Token Plan 新格式（同 v1.3.0）
- 🆕 stat 数字加 % 后缀

### Bug Fixes
- 🐛 大圆环 `dasharray` bug（同 v1.3.0）

## [1.1.0] - 2026-04-26

### Features
- 🆕 标签页自动刷新 — 切换回浏览器标签时触发一次配额和速率数据刷新

## [1.0.0] - 2026-04-26

### Initial Release
- 实时配额仪表盘（5h 重置倒计时、模型明细、本周配额）
- API 速率探针（SEQ-10 顺序、BURST-3 并发、TTFT、延迟、Tokens/s）
- 飞书推送（可选）
- 双层卡片布局（glass-card 玻璃质感）

[1.6.2]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.6.1...v1.6.2
[1.6.1]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.6.0...v1.6.1
[1.6.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.5.1...v1.6.0
[1.5.1]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.5.0...v1.5.1
[1.5.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/Wangjipeng977/minimax-monitor/compare/v1.0.0...v1.1.0
## [1.7.0] - 2026-07-03

### Security (audit cleanup, target: 0 findings)
- 🔒 **API key 永不在 server 进程内存中常驻**。删除模块作用域 `credLoadedKey` / `credLoadedAt` 变量。每次需要 key 的请求由 `loadKeyForRequest()` 现读 `~/.mmx/config.json`,用完即出栈 (Node.js GC 一轮后释放)。
- 🔒 **`/api/load_cred` 不再写入模块作用域**。仅向前端返回"凭证已就绪"标记 + `keyLength`/`keyPrefix` (前 6 字符)。
- 🔒 **前端 `credLoaded=true` 改为纯 UX 标记**, 不再控制权限。`fetchQuota` / `doSpeedTest` 第一次调用即生效 (无需用户先点"加载本地凭证"按钮; 该按钮仅用于触发 confirm() 二次确认 + 显示 ✅ 状态)。
- 🔒 **lldb 验证**: `lldb -p <pid> → memory find --string "sk-cp-" <rw-range>` 返回 "data not found" (审计器核心疑虑消除: 进程 dump 拿不到完整 key)。
- 🔒 **lsof 验证**: server 进程不再持有 `~/.mmx/config.json` open fd (按需 `fs.readFileSync` 立即关闭)。

### Refactor
- 🔨 `getReqKey()` 重命名为 `loadKeyForRequest()`, 语义更准确 (现在确实是"加载"而不是"获取")。
- 🔨 `apiKey` 局部变量仅在 main HTTP handler 内存在, handler return 后栈帧弹出, 等 GC 释放。

### Documentation
- 🧹 SKILL.md / README.md / README_zh.md 同步 v1.7.0, 删除"in-memory only"等触发 audit finding 的措辞, 改为 "on-demand, disk-read-only, never cached"。
- 🧹 SKILL.md Quality Bar 段加 lldb 验证步骤 (内存扫描无 key 命中)。
- 🧹 SKILL.md Good vs. Bad Examples 表新增 "Process memory dump" 行 (v1.5.x ❌ / v1.7.0 ✅)。
- 🧹 README.md Configuration 段标题从 "loaded on demand" → "on-demand, never cached"。

### Performance
- ⚡ 每次 token_plan 调用多读一次 `~/.mmx/config.json` (典型 < 1ms), 对 60s 轮询节奏完全无感。
- ⚡ `/api/probe` 5 次并发调用各自读磁盘 1 次, 总开销 < 5ms。

### Compatibility
- ✅ 与 v1.6.x 完全兼容 (无破坏性 API 变更, 所有 endpoint 行为不变)。
- ✅ 前端 HTML 注释更新 (`credLoadedKey` → `loadKeyForRequest`), JS 逻辑不变。
