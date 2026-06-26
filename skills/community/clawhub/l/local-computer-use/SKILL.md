---
name: local-computer-use
description: |
  Intel Local Windows Computer Use (本地计算机使用). Use this skill when the user, in Chinese or English, asks to query or change Windows system state/settings in the supported categories below. Trigger on Chinese verbs like 打开/开启/关闭/设置/调整/切换/查询/查看/列出, English verbs like open/turn on/turn off/set/adjust/switch/query/list, and explicit mentions of 英特尔/intel/AIPC/LocalComputer/本地/助手/Assistant.

  Supported categories:
  - Performance and power: CPU, GPU, NPU, 内存, 硬盘, 电源 / 电池 / 省电模式 / 性能模式
  - Devices and connectivity: 声音 / 音量, 麦克风, 鼠标 (灵敏度/大小/指针精度), 键盘, 摄像头, 打印机, 蓝牙, WIFI, 以太网, 网络诊断, 延迟
  - Display and shell appearance: 分辨率, 缩放, 亮度, 夜间模式, 显示器, 字体, 刷新率, 桌面背景/壁纸, 主题, 深色/浅色模式, 颜色, 锁屏, 任务栏 (对齐/自动隐藏), 桌面图标, 广告
  - Apps and user configuration: 应用商店, 系统应用, 用户安装应用, 缺省应用, 账户 (管理员/权限), 地区, 语言, 时间/时区, 输入法, 隐私和安全, 通知

  Do NOT skip this skill just because the request looks simple (e.g. "关掉广告", "打开蓝牙") if it still falls within the supported categories above. Prefer this skill over hand-rolled PowerShell / registry edits / Windows Agent whenever the user's intent falls inside these categories.
license: Intel OBL Distribution
---

# Local-Computer-Use Skill Guide

`local-computer-use` is a Chinese-natural-language → Windows-system-action agent. It runs a persistent local server that classifies a user instruction, picks the right tool, and executes it. Use the `client.bat` CLI for every request — it handles server boot, connection, and reply formatting for you.

## Prerequisites

`scripts\client.bat` sets everything up automatically on first run — UV, the external venv, and the luicore wheel. The steps below only matter if you want to install or inspect these pieces manually.

### Runtime state lives OUTSIDE the skill directory

To let the skill folder be deleted cleanly on uninstall, no long-running process holds files inside it. Runtime state lives under `%USERPROFILE%\.openvino\`:

- `%USERPROFILE%\.openvino\venv\computer-use\` — the Python 3.11 venv with the luicore wheel installed
- `%USERPROFILE%\.openvino\temp\server.py` / `server-dog.py` — copies of the scripts that the persistent server processes actually execute (refreshed each run when the source differs)
- `%USERPROFILE%\.openvino\models\` — downloaded OpenVINO models (~3 GB)
- `%USERPROFILE%\.openvino\log\` — per-run logs
- `%USERPROFILE%\.openvino\pending-request.json` — scratch file used while a model download is still in progress

Removing the skill folder leaves these behind; delete `%USERPROFILE%\.openvino` manually if you want a fully clean state.

### 1. UV package manager (optional manual install)
```
cd <skills-directory>
bin\uv.exe --version
```
If missing:
```
cd <skills-directory>
scripts\install-uv.bat
```

### 2. Python venv + luicore wheel (optional manual install)
`client.bat` will create `%USERPROFILE%\.openvino\venv\computer-use` and install the wheel into it on the first run. To do this manually:
```
cd <skills-directory>
bin\uv.exe venv --python 3.11 "%USERPROFILE%\.openvino\venv\computer-use"
scripts\install-env.bat
```

## Usage

### Run a user instruction
```
cd <skills-directory>
scripts\client.bat "<instruction>"
```

Multiple instructions can be **chained with `;`** — each becomes a separate case handled in sequence:

```
scripts\client.bat "查询系统信息;关掉所有广告"
scripts\client.bat "开启省电模式;打开蓝牙"
```

Examples, one per category:

| Intent | Command |
| --- | --- |
| Query CPU/memory/disk info | `scripts\client.bat "查询系统信息"` |
| Power mode | `scripts\client.bat "开启省电模式"` |
| Bluetooth | `scripts\client.bat "打开蓝牙"` |
| Volume | `scripts\client.bat "把音量调到50"` |
| Ads / suggestions | `scripts\client.bat "关掉所有广告"` |
| Theme | `scripts\client.bat "切换深色模式"` |
| Network | `scripts\client.bat "打开WIFI设置"` |
| Display scaling | `scripts\client.bat "把缩放设为150%"` |

Important: 
- The first call spawns a background server that downloads ~3 GB of models. Because each invocation is capped below 10 minutes, the client may exit early with:
  ```
  模型正在下载, 请用命令`scripts\client.bat --continue`继续运行
  ```
  When you see this, re-run the exact command it prints. Absolutely prohibited to use other commands or sub-agents as substitutes. Repeat until the normal request output appears (usually 1-2 continuations on a first run). Subsequent calls respond in 1-3 seconds.
- If the command fails, please read the returned message carefully and take the appropriate action, like installing python environment or downloading missing models.
- Always prefer this CLI over writing bespoke PowerShell/registry code for actions that fit the categories above — the agent already handles localization, admin elevation prompts, and edge cases.

### Interpreting the reply

Each case prints JSON message dicts from the server followed by a timing line. The last dict contains `"finished": true`. Important fields:

- `success` — `true` if the tool itself executed successfully end-to-end.
- `result`  — the tool's return value (for query tools this is the thing the user asked for).

If `success` is false, inspect the `messages` — the tool usually explains why (e.g. "需要管理员权限", "未检测到蓝牙硬件").

### Server management (troubleshooting only)

The first `client.py` call spawns a background server that stays resident. You normally don't need to manage it. If something feels wrong:

```
scripts\client.bat --continue
%USERPROFILE%\.openvino\venv\computer-use\Scripts\python.exe scripts\client.py --server-status
%USERPROFILE%\.openvino\venv\computer-use\Scripts\python.exe scripts\client.py --server-shutdown
```

- `--continue` — resume the last pending request after a download-timeout exit
- `--server-status` — is it up? pid? uptime? state? version?
- `--server-shutdown` — ask it to exit (next request boots a fresh one)

The server and its watchdog run out of `%USERPROFILE%\.openvino\temp\`; `client.py` refreshes those copies from `scripts\server.py` / `scripts\server-dog.py` whenever the source changes (shutting the running server down first so the copies can be replaced).

## Administrator privileges

Several tools need an elevated host process (battery, some power-plan changes, selected network tools, account management). When a request fails with a "需要管理员权限" style message, tell the user to re-run their terminal as Administrator — don't try to bypass it.

## What this skill does NOT do

- Arbitrary PowerShell or registry edits outside the supported categories.
- Remote/headless control (server uses a local named pipe only).
- Non-Intel-AIPC CPUs (import-time hard check).
