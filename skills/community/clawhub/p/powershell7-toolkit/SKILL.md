---
name: powershell7-toolkit
version: "1.1.8"
display_name: "PowerShell 7 工具链"
display_name_en: "PowerShell 7 Toolkit"
author: "欣欣 (YUJIANYU)"
agent_created: true
category: development
description: "在 Windows 上部署 PowerShell 7 与 Rust 高性能命令行工具链（ripgrep / fd / fzf / bat / delta / jq），根治中文输出乱码，并把 pwsh 设为系统默认 shell。当 AI 助手在 Windows 上执行命令时遇到以下情况，应主动调用本技能：报「字符串缺少终止符」、中文输出乱码、内联命令的引号被拆散、连接 GitHub 下载超时、脚本里不能用 && 或 ?: 三元运算、Select-String 检索太慢。这些多半是系统自带的 PowerShell 5.1 太老所致。跨机器自包含、幂等、免管理员、断网可装。"
description_zh: "在 Windows 上部署 PowerShell 7 与 Rust 高性能命令行工具链（ripgrep / fd / fzf / bat / delta / jq），根治中文输出乱码，并把 pwsh 设为系统默认 shell。当 AI 助手在 Windows 上执行命令时遇到以下情况，应主动调用本技能：报「字符串缺少终止符」、中文输出乱码、内联命令的引号被拆散、连接 GitHub 下载超时、脚本里不能用 && 或 ?: 三元运算、Select-String 检索太慢。这些多半是系统自带的 PowerShell 5.1 太老所致。跨机器自包含、幂等、免管理员、断网可装。"
description_en: "Deploys PowerShell 7 and the Rust CLI toolchain (ripgrep / fd / fzf / bat / delta / jq) on Windows, fixes Chinese mojibake, and makes pwsh the default shell. Use this skill when an AI assistant on Windows hits errors such as 'string is missing the terminator', garbled Chinese output, mangled inline quotes, GitHub download timeouts, missing && or ternary operators, or slow Select-String searches - these usually mean the built-in Windows PowerShell 5.1 is too old. Self-contained, idempotent, no admin rights required, works offline."
tags: ["powershell", "pwsh", "ripgrep", "rust", "utf8", "编码", "命令行", "windows", "工具链", "developer"]
requires: []
metadata:
  label: PowerShell 7 工具链
  openclaw:
    os: ["windows"]
    emoji: "⚡"
---

# PowerShell 7 工具链

一套**自包含、幂等、跨机器**的部署包。任何 AI 助手都可以照着本文件执行，无需联网查资料。

## 一、什么时候用这个技能

- 要装 / 升级 PowerShell 7（pwsh）
- 中文在 PowerShell / cmd / 第三方工具输出里乱码
- 想用 ripgrep 等 Rust 工具加速检索
- 要把 pwsh 设为系统默认 shell
- AI 生成的命令里带反引号，在 bash 或 pwsh 里被吃掉、误执行、或写出的文件缺字少符（见第六节）

## 二、安装（一条命令）

```powershell
powershell -ExecutionPolicy Bypass -File "<技能目录>\scripts\install.ps1"
```

**它的策略是「探测优先 → 自动下载兜底」：**

1. **先探测**系统里已装的 pwsh —— 扫 `Program Files\PowerShell\7`、用户目录、注册表 App Paths、PATH、scoop/chocolatey、Store 版（WindowsApps）。**找到就直接复用，绝不重复安装**
2. 找不到才找**本地 zip**（Downloads / 桌面 / 下载 / 迅雷下载 / Documents / TEMP）
3. 本地也没有才**自动下载**：官方 API 查最新版 → 三个国内镜像依次回退 → 微软 aka.ms 官方短链 → 内置固定版本表兜底（**断网也能装**）

常用参数：

| 参数 | 说明 |
|---|---|
| `-ZipPath "D:\xxx\PowerShell-7.6.7-win-x64.zip"` | 指定安装包（跳过自动搜索） |
| `-ToolsRoot "D:\Tools\ps7"` | 安装根目录（默认 `%LOCALAPPDATA%\ps7-toolkit`） |
| `-Mirror "https://your.mirror/"` | 自定义下载镜像（会插到内置列表最前） |
| `-SkipDefaults` | 只装不配（不改系统默认） |
| `-SkipRustTools` | 只装 PowerShell 7 |
| `-Force` | 强制在 `-ToolsRoot` 下放一份完整 pwsh：本机已装则复制（约 5 秒），没装才下载 |
| `-CheckOnly` | 只体检，不做任何改动 |

**特性**：幂等（重复跑只补缺失项）、免管理员权限、不依赖 Python、不写死盘符、断网可用、卸载只需删目录 + 3 个注册表项。

## 三、日常使用规范（装完之后必须遵守）

1. **执行命令优先用 pwsh**。**不要写死路径**——用户可能用 `-ToolsRoot` 装到别的盘：
   ```powershell
   # 从 App Paths 拿真实位置（setup-defaults 会写，指向实际安装的 pwsh）
   $pwsh = (Get-ItemProperty 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pwsh.exe').'(default)'
   & $pwsh -NoProfile -File script.ps1
   ```
   拿不到就直接敲 `pwsh`（装完在 PATH 里）。只有在必须写死时才用默认位置
   `%LOCALAPPDATA%\ps7-toolkit\ps7\pwsh.exe`，而且要先 `Test-Path` 确认存在。
2. **复杂脚本写成 `.ps1` 文件再用 `-File` 跑**，不要用 `-Command` 内联 —— 内联时嵌套引号会被外层解析拆散。
3. **给 PowerShell 5.1 跑的 .ps1 文件必须存成 UTF-8 with BOM**；给 pwsh 跑的用普通 UTF-8 即可。
   - 原因：5.1 读 .ps1 按 ANSI(GBK) 解析，脚本里含中文注释会报"字符串缺少终止符"。
4. **文本检索用 rg，不用 Select-String**（实测快 11 倍）：
   ```powershell
   rg -n --no-heading -e "关键词" -g "*.py" C:\path
   ```
5. **输出乱码时**先查 `[Console]::OutputEncoding` 和 `$OutputEncoding` 是否为 UTF-8（profile 已自动设置）。
6. **命令里有反引号时先过守卫**（`shell-guard.ps1`，见第六节），或写成 `.ps1` 文件用 `-File` 跑。
   反引号在 bash 里是命令替换、在 pwsh 里是转义符，内联执行十有八九会变形。

## 四、绝对不要做的事

| 禁止 | 原因 |
|---|---|
| 改 `HKLM\...\Nls\CodePage\ACP = 65001` | 会让老的 GBK 程序（部分国产软件/游戏）全部乱码，风险远大于收益 |
| 劫持 `powershell.exe` 指向 pwsh | 系统组件与大量安装脚本硬依赖 `C:\Windows\System32\WindowsPowerShell\v1.0\`，改了会导致装软件失败 |
| 用 `Add-Type` 编译 .NET 代码 | 部分 AI 客户端的安全策略会直接拦截（替代见下方「被拦时的替代路径」） |
| 在 Bash 里直接调 `powershell` | 某些客户端策略会拦（"Invoking PowerShell from Bash bypasses security checks"），改写成脚本文件执行 |

### 被拦时的替代路径

部分 AI 客户端会对即将执行的命令做关键字扫描，命中就直接拒绝，命令一个字都跑不了。
这类拦截不要去想办法绕（换写法骗过扫描既不可靠、也会让技能过不了市场审核），
正确做法是换成不触发规则的等价实现：

| 被拦的操作 | 典型报错大意 | 可用替代 |
|---|---|---|
| 运行时编译 .NET 代码 | 属于运行时编译，不允许 | 用现成 cmdlet（`Expand-Archive`）；或用已编译程序集里现成的类型（见下） |
| 实例化 COM 对象 | COM 可执行任意代码 | 用 .NET 原生 API；建 `.lnk` 改为 `.cmd` 入口 |
| 从 bash 直接调 `powershell` | 绕过安全检查 | 写 `.ps1` 再用 `pwsh -File` 跑 |
| 内联 `-Command` 带嵌套引号 | 引号被拆散 / 参数错位 | 写 `.ps1` 用 `-File`，或先过 `shell-guard.ps1` |

**删文件进回收站（最常踩的一条）：**

`Remove-Item` 是**永久删除，不进回收站**。要删得能还原，用本技能自带的封装：

```powershell
# 默认移入回收站，能从回收站还原
pwsh -NoProfile -File "<技能目录>\scripts\safe-remove.ps1" -Path "C:\temp\old" -Recurse

# 先预览，不动手
pwsh -NoProfile -File "<技能目录>\scripts\safe-remove.ps1" -Path "C:\temp\*.log" -WhatIf
```

- 默认进回收站；`-Permanent` 才永久删（输出会标注不可恢复）
- `-WhatIf` 预览，`-Recurse` 才允许删目录
- 盘根、系统目录、用户目录本身一律拒绝；网络盘/移动盘没有回收站时默认中止，不偷偷永久删
- 底层只用**已编译好的** `Microsoft.VisualBasic.FileIO.FileSystem`，不做运行时编译、不碰 COM，
  所以受限环境同样可用（5.1 下该类型不会自动加载，脚本内部已用反射补载）

退出码：`0` 全部成功 / `1` 有失败项 / `2` 没有可删目标 / `3` 目标位置无回收站，需显式 `-Permanent`。

## 五、能力清单（安装后可用）

| 工具 | 用途 | 替代 |
|---|---|---|
| pwsh 7.x | 主力 shell（UTF-8 默认、&& 链、三元 `?:`、`??`、`ForEach-Object -Parallel`，性能约 2 倍） | Windows PowerShell 5.1 |
| rg (ripgrep) | 极速递归检索，自带 .gitignore 规则 | Select-String / findstr |
| fd | 极速文件名查找 | Get-ChildItem |
| fzf | 模糊查找（可接管 Ctrl+R 历史搜索） | — |
| bat | 带语法高亮的 cat（配 delta 更好看） | cat / type |
| delta | git diff 高亮 | — |
| jq | JSON 处理 | ConvertFrom-Json |

> jq 中文键名注意：裸字段名只支持 ASCII。中文键必须写 `jq '.["名称"]'`，
> 直接写 `.名称` 会报 `INVALID_CHARACTER`（中文键名/含空格键名都要走 `["..."]` 写法）。

## 六、反引号与特殊字符（AI 执行前必读）

Windows 上 AI 生成的命令要经过两个 shell，反引号在两边都是雷，而且含义相反：

| shell | 反引号的含义 | 后果 |
|---|---|---|
| bash / Git Bash / MSYS2 | 命令替换 | 反引号里的内容先执行，输出再塞回命令行；落单的反引号报 unmatched，或把后半段整个吞掉 |
| pwsh 7.x | 转义符 | 吞掉后面一个字符（`n 变成换行），行尾的反引号是续行 |

**规则（照抄即可）：**

| 你要做的事 | 别这么写 | 这么写 |
|---|---|---|
| 命令替换 | `` echo `date` `` | `echo $(date)` |
| 字面反引号 | `` echo "a`b" `` | `echo 'a`b'`（单引号里两个 shell 都当字面量） |
| 写含反引号的文件（markdown / 脚本） | `cat <<EOF ... EOF` | `cat <<'EOF' ... EOF`（分隔符加单引号） |
| 把命令交给 pwsh | `pwsh -Command "...`..."` | `pwsh -Command '...`...'`（单引号），或写成 .ps1 后用 `-File` |
| 长命令 / 引号嵌套 | `-Command` 内联 | 写成 `.ps1` 文件再 `pwsh -File`（同第三节第 2 条） |

**拿不准就先过一遍守卫**（只读诊断，不改系统任何东西）：

```powershell
# 首选：会话内直调（任何父进程下引号都完全保真）
& "<技能目录>\scripts\shell-guard.ps1" -Text '要检查的命令'
# 跨进程：在 pwsh 7 会话里转发，或由外部直接启动 pwsh（引号保真）
pwsh -NoProfile -ExecutionPolicy Bypass -File "<技能目录>\scripts\shell-guard.ps1" -Text '要检查的命令'
pwsh -NoProfile -ExecutionPolicy Bypass -File "<技能目录>\scripts\shell-guard.ps1" -File .\build.ps1
```

**参数是 `-Text` 而不是 `-Command`**：后者会撞上 powershell.exe 自身的 `-Command` 开关，
转发时参数被截获错位。

**引号保真的硬结论（实测，5.1 与 pwsh 7 均验证）：**

- 会话内 `&` 直调：**保真**（首选，任何父进程都成立）
- 守卫的 `-Execute`：内部走 `-EncodedCommand`（Base64），**保真**
- **任何 `-Command` 式跨进程转发一律丢内层双引号**（5.1 与 pwsh 7 实测均丢）——
  `Write-Output "hello  world  spaced"` 会被拆成 3 个参数输出 3 行，`git commit -m "a  b"`
  会变成另一条命令。这不是「次优但可用」的兜底，是失真路径
- 5.1 做父进程转发时连守卫参数本身都会被切散 → 跨进程调用守卫一律用 pwsh 7 的 `-File`

退出码：`0` 安全 / `1` 发现风险 / `2` 有风险拒绝执行（配合 `-Execute`）/ `3` 文件不存在。
加 `-Execute` 会「先诊断再执行」，有风险默认拒绝，`-Force` 才放行；`-Shell pwsh` 可切换诊断口径。
`-Execute` 里原生命令的非零退出码统一**归一为 1**（不精确透传，避免残余 `$LASTEXITCODE` 污染判断）。

> 关键：从 bash 调守卫时 `-Text` 后面必须**用单引号**，否则反引号在到达守卫之前就被 bash 吃掉了。
> 同理，任何含反引号的内容想原样落盘，都用带引号的 heredoc（`<<'EOF'`）。

**在脚本里调用守卫函数**（dot-source 后可用）：默认 `$rc = Invoke-SafeCommand -Command '...'`
返回**只有 int 退出码**（输出显示在控制台）；要拿输出用 `-Capture`，此时输出走管道、
退出码在 `$GuardLastExitCode`。两种模式互斥，不会把输出和退出码混成一个数组。
子进程 stderr 形如 `[stderr] 原文`（单行，不掺 stdout）。别写 `exit (Invoke-SafeCommand ...)`。

**其他高频坑（守卫诊断时也会顺带提醒）：**

| 坑 | 现象 | 正确写法 |
|---|---|---|
| bash 里写 Windows 路径 | `cd C:\Users\x` 的反斜杠被当转义符吃掉，实际执行 `cd C:Usersx` | `cd 'C:\Users\x'`（单引号）或 `cd C:/Users/x`（正斜杠 Windows 也认） |
| 5.1 里用 curl | `curl https://...` 实际是 Invoke-WebRequest 的别名，参数全对不上 | 写 `curl.exe`（pwsh 7 无此问题） |
| 5.1 里用 `&&` / `\|\|` / 三元 | 直接报「token && 不是有效的语句元素」 | 用 pwsh 7 执行；或 `cmd1; if ($LASTEXITCODE -eq 0) { cmd2 }` |
| 5.1 里写文件 | `Out-File` / `>` 默认 UTF-16，bash、python 读到全是乱码 | 显式加 `-Encoding utf8`，或用 pwsh 7（默认 UTF-8） |
| 判断上一条命令成败 | `$?` 是布尔不是退出码；`$LASTEXITCODE` 会残留上一次的值 | 用 `$LASTEXITCODE` 判断原生 exe；用前先 `$LASTEXITCODE = 0` 清零 |

## 七、文件清单

```
SKILL.md                          本文件
assets/icon.png                   512x512 图标
scripts/install.ps1               主安装器（幂等，跨机器）
scripts/setup-defaults.ps1        默认化（profile/注册表/文件关联/开始菜单入口/终端/VSCode）
scripts/verify.ps1                体检脚本，输出诊断报告
scripts/safe-remove.ps1           安全删除：默认进回收站，带保护路径与 -WhatIf
scripts/wt-config.ps1             WT/VSCode 配置的文本级改写（保留注释，可被测试单独调用）
scripts/shell-guard.ps1           反引号/特殊字符守卫（bash 命令替换与 pwsh 转义符诊断 + 安全改写 + 执行拦截）
scripts/smoke-test.ps1            回归测试（隔离沙箱，不碰系统配置，退出码可接 CI）
references/troubleshooting.md     踩坑与排错
CHANGELOG.md                      版本记录
```

遇到报错或结果不符合预期时，先读 @references/troubleshooting.md，里面有逐条现象与处置办法
（`pwsh` 找不到、中文仍乱码、双击 `.ps1` 没反应、镜像下载卡住、Windows Terminal 没跟着切等）。

## 八、给终端用户的三步说明

1. 打开 PowerShell，执行：
   `powershell -ExecutionPolicy Bypass -File "脚本路径\install.ps1"`
2. 重启终端 / 常用应用（PATH 才会刷新）
3. 验证：`pwsh -v` 应显示 7.x；`rg --version` 应显示 ripgrep

## 九、这个技能会改动什么（知情同意）

安装过程全部在**当前用户**范围内，不需要管理员权限，不触碰 `HKEY_LOCAL_MACHINE`，也不会改动系统区域设置（不改 `ACP`）。

会做的改动：

| 改动 | 位置 | 如何撤销 |
|---|---|---|
| 写入可执行文件 | `%LOCALAPPDATA%\ps7-toolkit`（或 `-ToolsRoot` 指定目录） | 删除该目录 |
| 追加用户 PATH | `HKCU\...\Environment` 的 `Path` | 删掉该项里的 `ps7-toolkit` 路径 |
| 写入 profile | `%USERPROFILE%\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`（7.x）<br>`%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`（5.1） | 删除该文件或去掉本技能追加的段落 |
| 注册 pwsh 路径 | `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pwsh.exe` | 删除该键 |
| 关联 .ps1 双击行为 | `HKCU\Software\Microsoft\Classes\.ps1\shell\open\command` | 删除该键 |
| 默认控制台 | `HKCU\Console\%%Startup` 的 `DelegationConsole` / `DelegationTerminal`（仅当检测到 Windows Terminal 时） | 删掉这两个值 |
| 建开始菜单入口 | `%APPDATA%\Microsoft\Windows\Start Menu\Programs` 下的 `PowerShell 7.cmd`（已有 `.lnk` 时保持不动） | 删除该文件 |

网络行为：仅在需要下载时访问 `api.github.com`（查版本与真实下载地址）、`github.com`（下载安装包）、`gh-proxy.com` / `ghfast.top` / `ghproxy.net`（国内加速镜像）、`aka.ms`（微软官方短链）。不收集任何用户数据、不上报统计、不请求 API Key。

只读体检（`verify.ps1`）与只装不改（`-SkipDefaults`）不产生任何持久化改动。
