---
name: openclaw-browser-recover
description: "Diagnose and recover OpenClaw browser tool timeouts (browser.status/tabs/snapshot) involving gateway ports 18789/18791 and Chrome CDP 9222 conflicts. Use when browser tool says timed out/restart gateway, MCP Connection closed, port 9222 in use, cannot start openclaw browser, or user asks to fix browser control." 
---

# OpenClaw Browser Recover

目标：在 **不瞎重试** 的前提下，快速恢复 browser 工具可用性，并给用户一句话的“下一步动作”。

## 关键事实（先记住）
- `browser` 工具依赖 gateway 的 browser-control（通常监听 **18791**）
- `profile="user"` 依赖本机 Chrome 的 **CDP 9222**（必须有 Chrome 正在跑且 9222 可用）
- `profile="openclaw"` 也默认使用 9222；如果 9222 已被本机 Chrome 占用，会出现 **PortInUse**
- 看到 `timed out... Do NOT retry`：说明链路卡死，重复调用 browser 工具只会更糟。

## 标准恢复流程（按顺序，做到哪步好就停）

### 0) 先等一下（处理偶发卡顿）
- 等 20~30 秒后再进行下一步检查。

### 1) 端口与服务体检（exec）
运行：
```bash
openclaw gateway status
ss -lntp | egrep '(:18789|:18791|:9222)' || true
```
判读：
- 18789/18791 不在 → gateway 侧问题，优先重启 gateway。
- 9222 不在 → user profile 无法用，需要用户开启带 9222 的 Chrome。

### 2) 轻量 browser 侧探测（browser）
依次：
- `browser.status profile="user"`
- `browser.tabs profile="user" limit=5`

如果仍 timeout / MCP Connection closed → 进入第 3 步。

### 3) 修复动作（最短优先）
A. **只做一次** gateway 重启：
- `openclaw gateway restart`

B. 仍然 Connection closed：
- 让用户 **完全退出 Chrome** → 重新打开 Chrome → 重新打开目标页面
- 然后再执行 `browser.status profile="user"`

C. 需要 openclaw profile 但 9222 被占：
- 让用户关掉占用 9222 的 Chrome（或改用 user profile）。

> 同一轮最多：一次 restart；不要 stop+start 连击，除非用户明确要求。

## 给用户的“下一步一句话”模板
- 如果 9222 不在：
  - “请先打开带 9222 的 Chrome（或把推文截图发我），我才能接管浏览器。”
- 如果 browser timeout：
  - “browser-control 卡住了：请执行 `openclaw gateway restart`，我再继续。”
- 如果 Connection closed：
  - “控制通道断开：请把 Chrome 完全退出再重开，然后回我‘Chrome 重开了’。”

## 附：脚本（可选）
如果需要一键体检，运行：
```bash
bash skills/openclaw-browser-recover/scripts/healthcheck.sh
```
