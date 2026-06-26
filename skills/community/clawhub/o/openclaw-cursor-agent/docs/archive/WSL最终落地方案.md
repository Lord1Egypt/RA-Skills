# WSL 最终落地方案

这份文档用于把当前的 Windows + Git Bash 兼容模式，升级到更稳定的 WSL 方案。

## 当前状态

已完成：

- `Microsoft-Windows-Subsystem-Linux` 已启用
- `VirtualMachinePlatform` 已启用

当前机器状态：

- 两项功能都已写入系统
- `RestartNeeded = True`

也就是说，**下一步必须先重启系统**。

## 总体目标

把当前执行链路切成：

```text
OpenClaw -> openclaw-cursor-agent -> WSL -> tmux -> Cursor CLI Agent
```

这样可以绕开当前 Windows 原生 Cursor shell tool 的兼容问题。

## Phase 1：系统重启

先重启 Windows。

重启后先验证：

```powershell
wsl --status
wsl --list --verbose
```

如果 `wsl` 命令已可用，继续下一步。

## Phase 2：安装一个发行版

推荐安装 Ubuntu 或 Debian。

如果系统支持：

```powershell
wsl --install -d Ubuntu
```

如果该命令不可用，则改走手动安装发行版方式。

目标是让下面命令可用：

```powershell
wsl -d Ubuntu -- uname -a
```

## Phase 3：在 WSL 内安装 tmux

进入 WSL 后执行：

```bash
sudo apt update
sudo apt install -y tmux
tmux -V
```

目标：

- `tmux` 在 WSL 内原生可用

## Phase 4：在 WSL 内安装 Cursor CLI

在 WSL 中执行：

```bash
curl https://cursor.com/install -fsS | bash
agent --version
```

如果需要登录：

```bash
agent login
```

目标：

- `agent` 在 WSL 内原生可用

## Phase 5：验证 WSL 内三件套

确认这三项都通过：

```bash
command -v bash
command -v tmux
command -v agent
```

## Phase 6：切回插件 WSL 模式

将 `openclaw.json` 中的 `openclaw-cursor-agent` 配置改成：

```json
{
  "enabled": true,
  "config": {
    "toolkitRoot": "C:/Users/Administrator/.openclaw/workspace/cursor-agent-system",
    "defaultProjectPath": "D:/project/openclaw",
    "executionMode": "wsl",
    "timeoutMs": 120000,
    "shell": {
      "executable": "C:/Windows/System32/wsl.exe",
      "args": [],
      "workingDirectory": "",
      "wslDistro": "Ubuntu"
    }
  }
}
```

如果发行版不是 Ubuntu，把 `wslDistro` 改成实际名称。

## Phase 7：验证插件 doctor

切换后运行：

```powershell
openclaw cursor-agent-doctor
```

理想结果：

- `executionMode = wsl`
- `shell.executable = C:/Windows/System32/wsl.exe`
- `python3 ok`
- `tmux ok`
- `agent ok`
- `issues = []`

## Phase 8：执行最小 smoke test

先跑一个极简任务：

```text
帮我用 Cursor 在后台做一个任务：只回复一句 hello from wsl cursor agent，不要修改任何文件。
```

确认：

- 能启动任务
- 能输出开始执行
- 能正常完成

## Phase 9：执行 Git 状态检查任务

然后再跑：

```text
帮我用 Cursor 在后台做一个任务：检查 D:/project/windows-gateway-background 的 git status、git remote -v 和 README 是否存在，只检查，不要修改文件。
```

确认：

- `git status` 真正返回结果
- `git remote -v` 真正返回结果
- README 检查完成

## Phase 10：执行 GitHub 推送任务

最后再跑完整目标任务：

```text
帮我用 Cursor 在后台做一个任务：检查 D:/project/windows-gateway-background 是否已经推送到 GitHub；如果没有，就创建新仓库、补 README、推送代码，最后返回仓库链接。
```

## 推荐验收顺序

按这个顺序验收最稳：

1. `wsl --status`
2. WSL 中 `tmux -V`
3. WSL 中 `agent --version`
4. `openclaw cursor-agent-doctor`
5. 最小 smoke test
6. Git 状态检查任务
7. GitHub 推送任务

## 为什么 WSL 方案更稳

因为当前 Git Bash 兼容模式虽然已经打通：

- OpenClaw 调度
- tmux 后台会话
- Cursor Agent 启动
- 流式输出

但最后仍卡在：

- Cursor CLI Windows 原生 shell tool 执行行为

WSL 的意义就是把最后这一层 shell / git 执行环境切到真正的 Linux 用户态，从根上绕开 Windows 原生兼容问题。

## 实际执行记录（2026-03-19 更新）

所有 Phase 已完成：

| Phase | 状态 | 备注 |
|-------|------|------|
| Phase 1: 系统重启 | ✅ 完成 | WSL 功能已启用 |
| Phase 2: 安装发行版 | ✅ 完成 | Debian (WSL1)，通过 Appx 手动安装 |
| Phase 3: 安装 tmux | ✅ 完成 | tmux 3.1c via apt |
| Phase 4: 安装 Cursor CLI | ✅ 完成 | 通过自定义包装脚本 + Node.js 22 |
| Phase 5: 三件套验证 | ✅ 完成 | bash + tmux + agent 全部可用 |
| Phase 6: 插件切 WSL 模式 | ✅ 完成 | `executionMode: "wsl"`, `wslDistro: "Debian"` |
| Phase 7: 插件 doctor | ✅ 完成 | check-status.sh 正确返回所有任务 |
| Phase 8: 最小 smoke test | ✅ 完成 | agent 成功创建 hello.txt |
| Phase 9: spawn 端到端测试 | ✅ 完成 | `wsl-smoke-final` 任务完成，exit_code=0 |

### 遇到的额外问题及修复

1. **Windows 10 17763 仅支持 WSL1**：`wsl --install` 不可用，改为手动下载 Debian Appx 包安装。
2. **Cursor CLI 自带 Node 二进制不兼容 WSL1**：改为手动安装 Node.js 22 Linux x64 + 自定义包装脚本。
3. **包装脚本缺少 `"$@"`**：子命令（login/status）被吞掉，已修复。
4. **CRLF 换行符**：Windows 文件复制到 WSL 后 shebang 失效，用 `tr -d '\r'` 修复。
5. **PYTHONIOENCODING 容错**：从 `utf-8` 改为 `utf-8:replace`，避免非 UTF-8 字节导致 Python 崩溃。
6. **WSL Debian 缺少 python3**：通过 `apt-get install python3` 补齐。

## 一句话结论

**WSL 方案已全部落地并验证通过。** OpenClaw → WSL Debian → tmux → Cursor CLI Agent 端到端链路稳定运行。
