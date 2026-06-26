# 正式运行时代码文件清单

以下文件属于**运行时 / UI 正式补丁范围**（来自 `assets/patch/thread-continuity.patch`）：

- `src/agents/pi-embedded-runner/session-manager-init.ts`
- `src/config/sessions/types.ts`
- `src/gateway/server-methods/chat.ts`
- `src/gateway/session-utils.ts`
- `src/gateway/session-utils.types.ts`
- `src/gateway/thread-store.ts`
- `src/gateway/thread-rollover.ts`
- `ui/src/ui/app-view-state.ts`
- `ui/src/ui/app.ts`
- `ui/src/ui/chat-event-reload.ts`
- `ui/src/ui/controllers/chat.ts`
- `ui/src/ui/app-render.ts`
- `ui/src/ui/views/chat.ts`

## source-side 对齐测试

补丁同时包含以下**源码侧验证文件**，用于在匹配源码树里复验运行语义：

- `src/gateway/thread-rollover.test.ts`

这类测试文件可以进入源码树，但**不要**把它们当成 live `dist/` 部署产物手工复制到线上安装目录。

## 不要部署的辅助文件

不要把下面这些一起带上 live：

- 任意 `.bak_*`
- 任意 `.tmp/`
- 验收脚本
- 故障注入脚本
- 浏览器验收脚本
- deploy-backups
- 日志文件
- 真实 workspace 实例数据

典型排除项包括但不限于：
- `run_ui_validation.py`
- `ui_validation_browser.mjs`
- `live_rollover_browser_tmp.mjs`
- 临时 successor-create fault injection 代码

## 为什么要分开

这个 continuity pack 的目标是：
- 让别人能复用正式功能补丁
- 但不把某台机器的验收现场、脏数据、临时辅助物一起拷走
