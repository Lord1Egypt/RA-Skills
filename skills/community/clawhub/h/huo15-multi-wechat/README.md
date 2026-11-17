# 微信多开（macOS）

> 青岛火一五信息科技有限公司 · huo15-skills

在 macOS 上创建多个独立微信实例，可同时运行并登录不同账号。

## 原理

微信有**两层锁**需要绕过：

1. **单实例锁（CFBundleIdentifier）** — 微信启动时检查是否已有相同 Bundle ID 的进程在运行，如有则激活旧窗口而非启动新实例。
2. **Launch Services 缓存（可执行文件名）** — macOS 的 `open` 命令通过 Launch Services 启动应用，Launch Services 按可执行文件名做缓存映射。如果副本的可执行文件名与原版相同（都叫 `WeChat`），`open WeChat2.app` 会被重定向到原版 `WeChat.app`，无法启动新实例。

本方案三步绕过：
1. 修改副本的 `CFBundleIdentifier`（如 `com.tencent.xinWeChat2`）→ 绕过单实例锁
2. 重命名副本的可执行文件（`WeChat` → `WeChat2`）并更新 `CFBundleExecutable` → 绕过 Launch Services 缓存
3. 重新签名（ad-hoc）→ 让修改生效

## 使用方法

```bash
# 创建 2 个副本（默认），加上原版共 3 个微信
bash scripts/multi_wechat.sh 2

# 创建 1 个副本，加上原版共 2 个
bash scripts/multi_wechat.sh 1
```

脚本会自动：
1. 复制 `/Applications/WeChat.app` 到 `WeChat2.app`、`WeChat3.app`...
2. 修改每个副本的 `CFBundleIdentifier`（`com.tencent.xinWeChat2`、`com.tencent.xinWeChat3`...）
3. 重命名每个副本的可执行文件（`WeChat` → `WeChat2`、`WeChat3`...）并更新 `CFBundleExecutable`
4. 修改显示名
5. 重新签名（ad-hoc）
6. 重新注册到 Launch Services + 刷新 Dock
7. 验证签名

## ⚠️ 封号风险评估

### 封号概率：极低

| 分析维度 | 说明 |
|----------|------|
| **技术原理** | 本方案不修改微信二进制、不注入代码、不修改通信协议，仅复制应用并改 Bundle ID。与用户手动复制应用行为一致。 |
| **微信多端策略** | 微信官方支持多端同时在线（手机 + 电脑 + 平板），多开只是绕过「同一台电脑单实例」限制，不违反多端策略。 |
| **服务端检测** | 微信服务端无法检测客户端是否为副本（Bundle ID 是本地标识，不上报服务端）。 |
| **历史经验** | 此方法在 macOS 社区广泛使用多年，未见因多开本身导致封号的案例。 |

### 可能触发风控的行为（与多开方案无关）

以下**行为本身**可能触发风控，无论是否多开：

- ⚠️ 频繁切换账号登录/退出
- ⚠️ 大量群发消息、自动回复
- ⚠️ 使用自动化脚本操作微信
- ⚠️ 发送大量好友请求
- ⚠️ 涉及违规内容

**结论**：只要正常使用，多开本身不会导致封号。

## 注意事项

1. **聊天记录共享** — 副本与原版使用相同的数据目录（`~/Library/Containers/com.tencent.xinWeChat`），聊天记录互通。如需完全隔离，需额外配置容器路径。
2. **微信更新** — 更新原版微信后，副本不会自动更新。需删除旧副本并重新运行脚本。
3. **Gatekeeper 拦截** — 首次打开副本时 macOS 可能提示「无法验证开发者」。前往「系统设置 → 隐私与安全性」→ 点击「仍要打开」。
4. **磁盘占用** — 每个副本约 300-500MB（完整复制），删除时 `rm -rf` 即可。
5. **旧副本删除** — 如果之前的副本是 `root` 用户创建的（如通过 `sudo` 签名），删除时需要管理员密码。脚本通过 `osascript` 弹窗自动处理。
6. **v1.0.0 副本升级** — 如果用 v1.0.0 脚本创建过副本（只改了 Bundle ID 没改可执行文件名），`open` 命令无法多开。重新运行 v1.1.0 脚本即可修复。

## 为什么不用轻量启动器？

轻量启动器（用 shell 脚本调用 `WeChat.app/Contents/MacOS/WeChat`）**无法多开**——微信单实例锁会检测到已有进程在运行，直接激活旧窗口。

必须复制完整应用并修改 `CFBundleIdentifier` + 重命名可执行文件，才能真正绕过两层锁。

## v1.1.0 修复：为什么只改 Bundle ID 不够？

v1.0.0 只修改了 `CFBundleIdentifier`，`open` 命令仍然无法多开。原因：macOS Launch Services 按可执行文件名做缓存映射，副本的可执行文件名与原版相同（都叫 `WeChat`），`open WeChat2.app` 被重定向到原版。

v1.1.0 新增：重命名副本的可执行文件（`WeChat` → `WeChat2`）并更新 `CFBundleExecutable`，同时注册到 Launch Services，使 `open` 命令和 Dock 点击都能正常多开。

## 版本历史

见 [docs/changelog.md](docs/changelog.md)
