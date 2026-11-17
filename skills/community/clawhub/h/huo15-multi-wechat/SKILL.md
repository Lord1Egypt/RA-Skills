---
name: huo15-multi-wechat
displayName: 微信多开
version: 1.1.0
description: >-
  在 macOS 上创建多个独立微信实例，可同时登录不同账号。通过复制官方微信应用并修改
  CFBundleIdentifier + 重命名可执行文件 + 重新签名，绕过微信单实例锁和 Launch Services
  缓存。当用户说"微信多开""开两个微信""多个微信同时登录""multi wechat"等意图时使用。
  支持创建任意数量的微信副本，open 命令和 Dock 点击均可正常多开。
metadata: { "openclaw": { "emoji": "💬" } }
aliases:
  - 微信多开
  - 多开微信
  - 开两个微信
  - 多个微信
  - multi wechat
  - wechat multi instance
---

# 微信多开（macOS）

在 macOS 上创建多个独立微信应用副本，可同时运行并登录不同账号。

## 使用时机

✅ **使用此技能当：** 用户需要在 macOS 上同时运行多个微信实例、登录多个账号、需要多开微信。
❌ **不要用当：** 用户在 Windows/Linux 上需要多开（本技能仅适用 macOS）；用户只需要切换账号而非同时在线。

## ⚠️ 风险与封号概率

| 风险项 | 说明 |
|--------|------|
| **封号概率** | **极低**。本方案不修改微信二进制、不注入代码、不改协议，仅复制应用并改 Bundle ID，与手动复制行为一致。微信客户端本身支持多端登录（手机+电脑+平板），多开只是绕过「同一台电脑单实例」限制。 |
| **可能触发风控的行为** | ⚠️ 多开账号频繁切换、大量群发、自动化操作等**行为本身**可能触发风控，与本方案无关。 |
| **微信更新影响** | 微信更新后副本不会自动更新，需手动重新复制（删旧副本 → 重新跑脚本）。 |
| **签名失效** | 重新签名为 ad-hoc 签名（`-`），首次打开可能被 Gatekeeper 拦截，需在「系统设置 → 隐私与安全性」中点击「仍要打开」。 |
| **数据隔离** | 副本与原版共享同一数据目录，**聊天记录互通**。如需完全隔离需额外配置（见注意事项）。 |

## 前置条件

- macOS 系统
- 已安装微信（`/Applications/WeChat.app`）
- 管理员权限（删除旧的 root 拥有的副本时需要，通过 `osascript` 弹窗获取）

## 原理

微信有**两层锁**需要绕过：

1. **单实例锁（CFBundleIdentifier）** — 微信启动时检查是否已有相同 Bundle ID 的进程在运行，如有则激活旧窗口而非启动新实例。
2. **Launch Services 缓存（可执行文件名）** — macOS 的 `open` 命令通过 Launch Services 启动应用，Launch Services 按可执行文件名做缓存映射。如果副本的可执行文件名与原版相同（都叫 `WeChat`），`open WeChat2.app` 会被重定向到原版 `WeChat.app`，无法启动新实例。

本方案三步绕过：
1. 修改副本的 `CFBundleIdentifier`（如 `com.tencent.xinWeChat2`）→ 绕过单实例锁
2. 重命名副本的可执行文件（`WeChat` → `WeChat2`）并更新 `CFBundleExecutable` → 绕过 Launch Services 缓存
3. 重新签名（ad-hoc）→ 让修改生效

## 核心脚本

使用 `scripts/multi_wechat.sh`：

```bash
# 创建 2 个副本（WeChat2.app + WeChat3.app），加上原版共 3 个
bash scripts/multi_wechat.sh 2

# 创建 1 个副本（WeChat2.app），加上原版共 2 个
bash scripts/multi_wechat.sh 1

# 创建 5 个副本
bash scripts/multi_wechat.sh 5
```

脚本自动完成：复制应用 → 修改 Bundle ID → 重命名可执行文件 → 更新 CFBundleExecutable → 修改显示名 → 重新签名 → 注册 Launch Services → 验证。

## 标准流程

1. **确认环境** — 检查 `/Applications/WeChat.app` 是否存在。
2. **确认数量** — 询问用户需要多开几个（默认 2 个副本，加原版共 3 个）。
3. **清理旧副本** — 如已有 `WeChat2.app` 等副本，先删除（可能需要管理员权限）。
4. **执行脚本** — 运行 `scripts/multi_wechat.sh <数量>`。
5. **刷新启动台** — `killall Dock` + `lsregister` 重新注册。
6. **启动验证** — 依次 `open` 每个微信，确认独立窗口出现。
7. **告知用户** — 说明首次打开可能需在「隐私与安全性」中允许。

## 注意事项

1. **聊天记录共享** — 副本与原版使用相同的数据目录（`~/Library/Containers/com.tencent.xinWeChat`），聊天记录互通。如需完全隔离，需修改副本的容器路径（复杂操作，不推荐普通用户尝试）。
2. **微信更新** — 更新原版微信后，副本不会自动更新。需删除旧副本并重新运行脚本。
3. **Gatekeeper 拦截** — 首次打开副本时 macOS 可能提示「无法验证开发者」。前往「系统设置 → 隐私与安全性」→ 点击「仍要打开」。
4. **不要手动改 Info.plist 后不签名** — 修改了 `CFBundleIdentifier` 或 `CFBundleExecutable` 后必须重新签名，否则无法运行。
5. **副本占用空间** — 每个副本约 300-500MB（完整复制），删除时 `rm -rf` 即可。
6. **必须重命名可执行文件** — 只改 Bundle ID 不改可执行文件名，`open` 命令无法多开（Launch Services 按可执行文件名缓存映射到原版）。这是 v1.1.0 的核心修复。

## 反模式（禁止）

- ❌ 用轻量启动器（脚本调用 `WeChat.app/Contents/MacOS/WeChat`）做多开——微信单实例锁会直接激活旧窗口，**无效**。
- ❌ 只改 `CFBundleIdentifier` 不重命名可执行文件——`open` 命令会被 Launch Services 重定向到原版，**无法多开**。
- ❌ 修改 `CFBundleIdentifier` 或 `CFBundleExecutable` 后不重新签名——应用无法启动。
- ❌ 修改微信二进制文件——可能触发安全检测且无必要。
- ❌ 使用第三方多开工具注入微信——高风险，可能触发风控。

## 核心原则

**复制完整应用 · 改 Bundle ID · 重命名可执行文件 · 重新签名 · 不注入不改协议。** 四步缺一不可——少改可执行文件名则 `open` 命令无效，少改 Bundle ID 则单实例锁无效。
