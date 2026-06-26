<p align="center">
  <img src="./src/humancanhelp.png" alt="HumanCanHelp logo" width="720">
</p>

# HumanCanHelp (HCL)

> English + 中文双语说明 / Bilingual documentation in English and Chinese

HumanCanHelp is a local human-in-the-loop handoff tool for visual or interactive tasks that AI cannot finish alone.

HumanCanHelp 是一个本地运行的人机接手工具，适用于 AI 无法单独完成的视觉类或交互类任务。

It starts a short-lived help session, gives you a URL, and lets a human open that page to see and interact with either:

它会启动一个短时协助会话，生成一个 URL，让真人打开页面后查看并操作以下任一内容：

- a live browser tab through Chrome DevTools Protocol (CDP), or
- a full desktop session through VNC.

- 通过 Chrome DevTools Protocol（CDP）共享实时浏览器标签页，或
- 通过 VNC 共享完整桌面会话。

Challenge or verification steps are only one example. HCL is for any moment where an agent needs a real person to briefly look at a screen, click something, type something, or complete a blocked step.

验证或挑战步骤只是其中一种用法。只要 AI 需要真人临时看一眼屏幕、点一下、输一点内容，或帮忙把卡住的步骤走完，HCL 都能派上用场。

No accounts, no cloud dashboard, no API keys. It runs on your machine.

不需要账号，不需要云端控制台，也不需要 API Key。它直接运行在你的本地机器上。

## What HCL is for

## HCL 适合做什么

HCL is useful when an automated workflow reaches a human-only step such as:

当自动化流程走到必须由真人接手的一步时，HCL 会很有用，例如：

- slider, click, or visual confirmation flows
- browser steps that require a human eye or judgment
- “please look at this screen and finish this step” handoffs
- remote help during Playwright or Puppeteer sessions
- desktop-only interactions when browser-tab sharing is not enough

- 滑块、点击或视觉确认类流程
- 需要人工判断的浏览器步骤
- 普通登录页、登录表单，或其他可以由远程协助者代为完成的登录相关步骤
- “请看一下这个页面并帮我完成这一步” 的接手场景
- Playwright 或 Puppeteer 会话中的远程人工协助
- 浏览器标签页共享不够时的桌面级交互

The core model is simple:

核心模型很简单：

1. Start HCL locally.
2. HCL prints a local URL, and optionally a public URL.
3. A human opens the page and sees the shared browser tab or desktop.
4. The human interacts directly.
5. The human clicks **Done**, **Owner action required**, or **Cannot solve**.
6. Your CLI exits with success or failure.

1. 在本地启动 HCL。
2. HCL 打印一个本地 URL，必要时也可以打印一个公共 URL。
3. 真人打开页面后，就能看到共享的浏览器标签页或桌面。
4. 真人直接进行操作。
5. 真人点击 **Done**、**Owner action required** 或 **Cannot solve**。
6. CLI 以成功或失败状态退出。

## Current status

## 当前状态

This project currently runs from a local checkout.

目前更推荐直接以本地仓库方式运行这个项目。

```bash
npm install
npm run build
node dist/index.js start
```

The package metadata and CLI names are already in place, but this README should treat the local checkout flow as the real installation path for now.

虽然 package metadata 和 CLI 名称都已经就位，但当前 README 仍然把“本地仓库运行”作为主要安装方式。

## How it works

## 工作方式

HumanCanHelp supports two session modes.

HumanCanHelp 目前支持两种会话模式。

### 1. CDP mode: share a browser tab

### 1. CDP 模式：共享浏览器标签页

If Chrome or another Chromium-based browser is running with remote debugging enabled, HCL can connect through CDP and share a live browser tab.

如果 Chrome 或其他基于 Chromium 的浏览器已经开启远程调试，HCL 就可以通过 CDP 连接并共享实时浏览器标签页。

This is the recommended mode for:

这是推荐模式，适用于：

- browser automation recovery
- blocked steps inside a web page that need a human eye or action
- short human intervention during Playwright or Puppeteer runs

- 浏览器自动化恢复
- 网页内部需要人工观察或操作的受阻步骤
- 普通登录流程里需要人工代点、代填的页面步骤
- Playwright 或 Puppeteer 执行过程中的短时人工介入

In CDP mode, the helper can:

在 CDP 模式下，协助者可以：

- see the live page
- click
- type
- drag sliders

- 查看实时页面
- 点击
- 输入
- 拖动滑块

### 2. VNC mode: share a full desktop

### 2. VNC 模式：共享完整桌面

If CDP is unavailable, HCL can connect to a VNC server and share a full desktop session instead.

如果 CDP 不可用，HCL 可以改为连接 VNC 服务并共享完整桌面会话。

This is useful when:

这种模式适用于：

- the blocked step is not inside a browser tab
- you need access to a native desktop app
- browser-only sharing is too limited

- 受阻步骤不在浏览器标签页中
- 你需要访问原生桌面应用
- 仅共享浏览器标签页不够用

## Quick start

## 快速开始

### Auto-detect mode

### 自动检测模式

If you do not pass `--cdp` or `--vnc`, HCL will:

如果你没有传 `--cdp` 或 `--vnc`，HCL 会：

1. try CDP at `localhost:9222`
2. fall back to VNC at `localhost:5900`

1. 先尝试 `localhost:9222` 上的 CDP
2. 如果不行，再回退到 `localhost:5900` 上的 VNC

HCL starts its own helper HTTP server automatically. You do **not** need to install a separate HTTP service first.

HCL 会自动启动自己的 helper HTTP 服务。你**不需要**额外再装一个 HTTP 服务。

What you do need is at least one usable local session source:

你真正需要的是至少一个可用的本地会话来源：

- a Chromium browser with remote debugging enabled for CDP mode, or
- a reachable VNC server for VNC mode.

- 一个为 CDP 模式开启了远程调试的 Chromium 浏览器，或
- 一个可连通的 VNC 服务，用于 VNC 模式。

If neither is available, HCL now fails early with setup guidance instead of starting a session that cannot connect.

如果两者都不可用，HCL 现在会直接提前失败，并给出设置提示，而不是先启动一个实际上根本连不上的会话。

```bash
node dist/index.js start
```

Example output:

```text
HumanCanHelp started

Local:   http://<your-local-ip>:6080
Mode:    CDP (Chrome DevTools Protocol)
Target:  ws://localhost:9222/devtools/page/XXXX
Timeout: 600s
```

### Explicit CDP mode

### 显式 CDP 模式

Start Chrome with remote debugging enabled:

先用远程调试参数启动 Chrome：

```bash
chrome --remote-debugging-port=9222
```

Then start HCL:

然后启动 HCL：

```bash
node dist/index.js start --cdp localhost:9222
```

If HCL can reach the CDP endpoint but no page target is open, it will ask you to open the page you want to share before starting.

如果 HCL 能连到 CDP 端点，但没有打开可共享的页面，它会提示你先打开目标页面再启动。

### Explicit VNC mode

### 显式 VNC 模式

```bash
node dist/index.js start --vnc localhost:5900
```

If no VNC server is reachable, HCL will stop and tell you to start one first.

如果没有可连接的 VNC 服务，HCL 会直接停止并提示你先启动 VNC。

Example output:

```text
HumanCanHelp started

Local:   http://<your-local-ip>:6080
Mode:    VNC
VNC:     localhost:5900
Timeout: 600s
```

### Remote helper mode

### 远程协助模式

If the helper is not on the same network, you can ask HCL to create a public tunnel URL.

如果协助者不在同一个网络里，你可以让 HCL 创建一个公共隧道 URL。

Install the optional tunnel dependency first:

请先安装可选的隧道依赖：

```bash
npm install localtunnel
```

```bash
node dist/index.js start --public --password "use-a-long-random-password"
```

Only use `--public` when you intentionally want to expose the live help session outside your local network.

只有在你明确要把这次实时协助会话暴露到本地网络之外时，才建议使用 `--public`。

That public URL can expose a live browser tab or desktop session to anyone who can reach it, so always set a strong, unique password and share it through a trusted channel.

这个公共 URL 可能会把实时浏览器标签页或桌面会话暴露给任何能访问它的人，因此务必设置一个强且唯一的密码，并通过可信渠道单独发送。

Example output:

```text
HumanCanHelp started

Local:    http://<your-local-ip>:6080
Public:   https://abc123.lhr.life
Mode:     CDP (Chrome DevTools Protocol)
Timeout:  600s
Password: yes
```

## Session lifecycle

## 会话生命周期

When a helper opens the page, HCL serves a live interaction UI.

协助者打开页面后，HCL 会提供一个可实时交互的界面。

The helper can:

协助者可以：

- interact with the shared screen or tab
- click **Done** when the task is complete
- continue helping through ordinary login screens or sign-in steps when a remote helper can legitimately complete them through CDP/VNC
- click **Owner action required** only when the real account owner must continue personally, such as owner-bound MFA, SSO approval, or another owner-only sign-in step
- click **Cannot solve** if they cannot finish it

- 与共享的屏幕或标签页交互
- 在任务完成后点击 **Done**
- 如果远程协助者可以通过 CDP/VNC 合理完成普通登录页面、登录表单或其他常规登录步骤，就继续协助处理
- 只有当必须由真实账号持有者本人继续时，例如 owner 绑定的 MFA、SSO 批准或其他仅限账号主人完成的登录动作，才点击 **Owner action required**
- 如果无法完成则点击 **Cannot solve**

Session behavior:

会话行为如下：

- **Done** → CLI exits with success
- **Owner action required** → CLI exits with a dedicated login-required failure so the calling workflow can escalate the session to the actual account owner
- **Cannot solve** → CLI exits with failure
- **Timeout** → session expires, the page shows an expired state, and HCL starts a fresh session with the same config

- **Done** → CLI 成功退出
- **Owner action required** → CLI 以专门的 login-required 失败状态退出，方便调用方把当前会话升级给真正的账号持有者处理
- **Cannot solve** → CLI 失败退出
- **Timeout** → 当前会话过期，旧页面会显示过期状态并失效，同时 HCL 会用相同配置立即重新开启一个新会话

## CLI reference

## CLI 参考

### Commands

```bash
node dist/index.js start [options]
node dist/index.js stop
node dist/index.js status
```

### Options

| Option | Default | Description |
|---|---|---|
| `--port` | `6080` | HTTP port for the helper page |
| `--cdp` | auto | CDP endpoint, for example `localhost:9222` |
| `--vnc` | auto | VNC endpoint, for example `localhost:5900` |
| `--timeout` | `600` | Session expiry time in seconds; when it expires, HCL immediately starts a fresh session with the same config |
| `--public` | off | Create a public tunnel URL for remote helpers |
| `--password` | none | Require a password before the helper can access the session |
| `--mask` | none | Apply helper-side black mask regions like `x,y,w,h;x,y,w,h` and block pointer input inside them |

### Status

### Status / 状态

`status` reports whether a server is running, which mode it is in, and whether a public URL exists.

`status` 会报告当前是否有服务在运行、正在使用哪种模式，以及是否存在公共 URL。

### Stop

### Stop / 停止

`stop` shuts down the running local HCL server on the selected port.

`stop` 会关闭指定端口上当前正在运行的本地 HCL 服务。

## Privacy and security notes

## 隐私与安全说明

What exists today:

当前已经具备：

- local-first workflow
- optional password protection
- optional public tunnel only when explicitly requested and the optional `localtunnel` package is installed

- 本地优先的工作方式
- 可选密码保护
- 只有在显式请求并安装可选 `localtunnel` 依赖后，才会启用公共隧道

Important limitation:

重要限制：

- `--mask` now renders black helper-side overlays and blocks helper pointer interactions inside those regions, but it does **not** rewrite or sanitize the underlying CDP/VNC transport stream itself.

- `--mask` 现在会在协助者界面中渲染黑色遮罩，并阻止协助者在这些区域内进行指针操作，但它**不会**改写或清洗底层 CDP/VNC 传输流本身。

So the honest current privacy story is:

所以当前更准确的隐私描述是：

- password protection works
- sharing is opt-in
- public tunnel support is optional and currently depends on a separately installed tunnel package
- helper-side masking is available for visual redaction and click blocking, but transport-level sanitization is still out of scope for the current architecture

- 密码保护是有效的
- 共享必须由你显式开启
- 公共隧道支持是可选能力，并且依赖单独安装的隧道包
- 当前已提供协助者界面的可视遮罩与点击阻止能力，但底层传输级脱敏仍超出当前架构范围

## VNC setup

## VNC 设置

### macOS

### macOS

System Settings → General → Sharing → Screen Sharing → enable

### Linux

### Linux

```bash
sudo apt install x11vnc
x11vnc -display :0 -forever
```

### Windows

### Windows

Install [TightVNC](https://www.tightvnc.com/) or UltraVNC.

## What HCL does not claim yet

## HCL 目前不宣称具备的能力

The current codebase is intentionally small and local.

当前代码库有意保持小而本地化。

It does **not** currently claim to be:

它**目前并不宣称**自己是：

- a hosted service
- a polished remote desktop platform
- a full MCP runtime
- a complete transport-level privacy-masking system
- a fully polished npm-published product you can install globally without caveats today

- 一个托管式在线服务
- 一个打磨完善的远程桌面平台
- 一个完整的 MCP runtime
- 一个完整的隐私遮罩系统
- 一个今天就能无条件全局安装并即刻使用的成熟 npm 产品

The safest way to think about HCL right now is:

当前最稳妥的理解方式是：

> a lightweight local handoff tool for short human assistance sessions during blocked AI workflows

> 一个轻量级、本地优先的人类接手工具，用于 AI 工作流受阻时的短时人工协助

## Why this is broader than a single use case

## 为什么它不只是单一用途工具

Verification or challenge steps are a common use case because they are a clear example of “AI is blocked, a human needs to take over briefly.”

验证或挑战类步骤是一个常见用例，因为它非常典型地体现了“AI 被卡住，需要真人短暂接手”这种情况。

But the product itself is broader:

但这个产品本身的能力范围更广：

- it can share a browser tab
- it can share a desktop session
- it supports arbitrary clicking and typing
- it supports success / failure handoff semantics
- it works for any short visual or interactive blocker, not just verification challenges

- 它可以共享浏览器标签页
- 它可以共享桌面会话
- 它支持任意点击和输入
- 它支持成功 / 失败的接手语义
- 它适用于任何短时视觉或交互阻塞场景，而不只是验证类挑战

If a workflow reaches a point where a person needs to look, decide, click, type, drag, or confirm something on a live screen, HCL is the handoff layer.

只要一个工作流走到需要真人查看、判断、点击、输入、拖动，或在实时屏幕上确认某件事的步骤，HCL 就可以作为这个接手层。

## License

MIT
