---
name: humancanhelp
description: Use for a short local human handoff when an AI workflow is blocked on a visual or interactive step / 当 AI 工作流卡在视觉或交互步骤时，可用本工具进行短时本地人工接手
version: 1.1.1
metadata:
  openclaw:
    requires:
      bins:
        - node
---

# HumanCanHelp (HCL) / 人工接手工具

HumanCanHelp is a local human-in-the-loop handoff tool for moments when AI needs a person to briefly see a live screen, click, type, drag, or complete a blocked step. It supports both browser tab sharing (CDP) and full desktop sharing (VNC).

HumanCanHelp 是一个本地运行的人机接手工具，适用于 AI 需要真人临时看一眼实时画面、点击、输入、拖动，或把卡住的步骤继续做完的场景。它同时支持浏览器标签页共享（CDP）和桌面共享（VNC）。

## When to Use / 适用场景

- Visual checks that need a real person to look at the screen
  需要真人查看屏幕的视觉确认步骤
- Short blocked browser or desktop steps during an automated workflow
  自动化流程里短暂卡住的浏览器或桌面步骤
- Ordinary login pages or sign-in steps that a remote helper can legitimately complete
  远程协助者可以合理代为完成的普通登录页面或登录步骤
- Any interactive handoff where AI cannot safely complete the step alone
  任何 AI 无法单独安全完成的交互式接手场景

## How to Use / 使用方式

Use a local checkout as the primary flow right now. If you publish the package into your own environment later, the CLI behavior stays the same: start HCL, send the printed URL to a helper, and wait for the CLI to exit.

当前更推荐直接从本地仓库运行。如果以后你把这个包发布到自己的环境里，CLI 行为也保持一致：启动 HCL，把打印出的 URL 发给协助者，然后等待 CLI 退出。

```bash
npm install
npm run build
npm start
```

Optional published-package flow, only after you have actually published or installed it:

只有在你真的已经发布或安装过这个包之后，才适合使用下面这种已发布包流程：

```bash
npx humancanhelp start
```

If you installed it globally yourself, `hcl start` is equivalent.

如果你是自己全局安装的，那么 `hcl start` 也是等价的。

### Step 1: Start the help server / 第一步：启动帮助服务

HCL starts its own helper HTTP server automatically. You do **not** need to install a separate HTTP server first.

HCL 会自动启动自己的 helper HTTP 服务。你**不需要**先额外安装独立的 HTTP 服务。

What you do need is one of these local session sources:

你真正需要的是以下任意一种本地会话来源：

- a Chromium browser with remote debugging enabled for CDP mode, or
  一个开启远程调试的 Chromium 浏览器，用于 CDP 模式
- a reachable VNC server for desktop mode.
  一个可连通的 VNC 服务，用于桌面模式

```bash
hcl start
```

HCL auto-detects the best mode:
- If Chrome DevTools is running on port 9222 → CDP mode (shares browser tab)
- Otherwise → VNC mode (shares full desktop, requires VNC server)

HCL 会自动检测最合适的模式：
- 如果 9222 端口上的 Chrome DevTools 可用 → 使用 CDP 模式（共享浏览器标签页）
- 否则 → 回退到 VNC 模式（共享完整桌面，但需要 VNC 服务）

If neither source is available, HCL now fails early with setup instructions instead of starting a session that cannot connect.

如果两种来源都不可用，HCL 现在会直接提前失败，并给出设置提示，而不是先启动一个实际上根本连不上的会话。

For explicit mode selection:

如果你想显式指定模式：

```bash
# CDP mode (browser tab only)
# CDP 模式（仅共享浏览器标签页）
hcl start --cdp localhost:9222

# VNC mode (full desktop)
# VNC 模式（共享完整桌面）
hcl start --vnc localhost:5900
```

CDP mode output:

CDP 模式输出示例：

```
  HumanCanHelp started

  Local:   http://<your-local-ip>:6080
  Mode:    CDP (Chrome DevTools Protocol)
  Target:  ws://localhost:9222/devtools/page/XXXX
  Timeout: 600s
```

VNC mode output:

VNC 模式输出示例：

```
  HumanCanHelp started

  Local:   http://<your-local-ip>:6080
  Mode:    VNC
  VNC:     localhost:5900
  Timeout: 600s
```

### For remote helpers (public URL) / 远程协助者访问（公共 URL）

```bash
hcl start --public --password "use-a-long-random-password"
```

If you want `--public`, install the optional tunnel dependency first from your local checkout:

如果你想使用 `--public`，请先在本地仓库里安装可选隧道依赖：

```bash
npm install localtunnel
```

This creates both a local and a public tunnel URL:

这样会同时生成本地地址和公共访问地址：

```
  Local:   http://<your-local-ip>:6080
  Public:  https://abc123.lhr.life
  Mode:    CDP (Chrome DevTools Protocol)
  Timeout: 600s
  Password: yes
```

Only use `--public` when you intentionally want to expose the live help session outside your local network.

只有在你明确希望把实时帮助会话暴露到本地网络之外时，才应使用 `--public`。

If you expose a public URL, always use a strong, unique `--password` so the helper must authenticate before they can access the live session.

如果你暴露公共 URL，请务必使用强且唯一的 `--password`，这样协助者在访问实时会话前必须先认证。

### Step 2: Tell the user to open the URL / 第二步：让用户打开 URL

Say something like:

你可以这样说：

> Please open this URL to help me finish the blocked step: http://<your-local-ip>:6080
> 请打开这个 URL，帮我完成当前受阻的步骤：http://<your-local-ip>:6080

### Step 3: Wait / 第三步：等待

The CLI blocks until:
- The user clicks "Done" on the page → exits with code 0
- The user clicks "Owner action required" only when the real account owner must continue personally → exits with a dedicated login-required failure outcome so the workflow can escalate to the account owner
- The user clicks "Cannot solve" → exits with code 1
- Timeout expires → HCL immediately starts a fresh session with the same config

CLI 会一直阻塞，直到：
- 用户在页面上点击 “Done” → 以退出码 0 结束
- 用户只有在必须由真实账号持有者本人继续时才点击 “Owner action required” → 以专门的 login-required 失败结果结束，方便把流程升级给账号持有者
- 用户点击 “Cannot solve” → 以退出码 1 结束
- 超时 → 当前会话立刻过期，旧页面会失效，而 HCL 会用相同配置立即启动一个新的会话

### Step 4: Continue / 第四步：继续

After the CLI exits with code 0, the human has finished interacting with the screen. Normal login-related help can still complete this way. Continue your task.

当 CLI 以退出码 0 结束后，说明人工已经完成了屏幕交互；普通登录相关协助也同样可以通过这种方式完成。此时你就可以继续原来的任务。

Use the dedicated "Owner action required" outcome only for the narrower case where the real account owner must take over personally, such as owner-bound MFA, SSO approval, or another identity step the helper cannot legitimately complete.

只有在更窄的那类情况——必须由真实账号持有者本人接手，例如 owner 绑定的 MFA、SSO 批准，或其他协助者不能合理代办的身份确认步骤——才使用专门的 “Owner action required” 结果。

## CLI Reference / CLI 参考

```bash
hcl start [options]

Options:
  --cdp <host:port>    Use CDP mode (Chrome DevTools Protocol), e.g. --cdp localhost:9222
  --vnc <host:port>    Use VNC mode, VNC server address (default: localhost:5900)
  --port <number>      HTTP server port (default: 6080)
  --timeout <seconds>  Session expiry in seconds; HCL immediately starts a fresh session after timeout (default: 600)
  --public             Also create a public tunnel URL for remote helpers
  --password <string>  Protect the help URL with a password
  --mask <regions>     Render black helper-side mask regions and block pointer input: "x,y,w,h;x,y,w,h"
```

```bash
hcl start [参数]

参数:
  --cdp <host:port>    使用 CDP 模式（Chrome DevTools Protocol），例如 --cdp localhost:9222
  --vnc <host:port>    使用 VNC 模式，VNC 服务地址（默认：localhost:5900）
  --port <number>      HTTP 服务端口（默认：6080）
  --timeout <seconds>  会话过期时间，单位秒；超时后会按相同配置立即开启新会话（默认：600）
  --public             为远程协助者生成公共访问地址
  --password <string>  为帮助 URL 添加访问密码
  --mask <regions>     渲染黑色协助者侧遮罩并阻止指针输入："x,y,w,h;x,y,w,h"
```

## Modes / 模式

### CDP Mode (recommended) / CDP 模式（推荐）

Shares only the browser tab via Chrome DevTools Protocol. Supports mouse clicks, typing, and slider drag interactions. Best for Playwright, Puppeteer, and browser-based recovery workflows.

通过 Chrome DevTools Protocol 仅共享浏览器标签页。支持鼠标点击、键盘输入和滑块拖动。适合 Playwright、Puppeteer 和其他浏览器自动化恢复场景。

Requires Chrome launched with `--remote-debugging-port=9222`.

要求 Chrome 通过 `--remote-debugging-port=9222` 启动。

### VNC Mode / VNC 模式

Shares the full desktop via VNC. Requires a VNC server running on the machine.

通过 VNC 共享完整桌面。要求机器上已经有 VNC 服务在运行。

## Session Expiry / 会话过期

The help page automatically expires when:
- Timeout is reached → page shows "This session has expired", disconnects
- Helper clicks Done → session ends, CLI exits with code 0
- Helper clicks "Cannot solve" → session ends, CLI exits with code 1

帮助页面会在以下情况自动过期：
- 达到超时时间 → 当前页面显示 “This session has expired” 并断开连接，同时 HCL 会立即按原配置重新拉起一个新会话
- 协助者点击 Done → 会话结束，CLI 以退出码 0 结束
- 协助者点击 “Cannot solve” → 会话结束，CLI 以退出码 1 结束

## Privacy / 隐私说明

Password protection is available now. For password-protected sessions, remote helpers must authenticate before HCL exposes live session metadata or event updates. The `--mask` flag now renders black helper-side mask regions and blocks helper pointer input inside them, but it does not sanitize the underlying CDP/VNC transport stream itself.

当前已经支持密码保护。对于带密码的会话，远程协助者必须先通过认证，HCL 才会暴露实时会话元数据或事件更新。`--mask` 现在会在协助者界面中渲染黑色遮罩，并阻止协助者在这些区域内进行指针操作，但它不会改写底层 CDP/VNC 传输流本身。
