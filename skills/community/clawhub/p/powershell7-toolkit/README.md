# PowerShell 7 工具链（ps7-toolkit）

[![检查](https://github.com/yujianyu/ps7-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/yujianyu/ps7-toolkit/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/yujianyu/ps7-toolkit)](https://github.com/yujianyu/ps7-toolkit/releases/latest)
[![License](https://img.shields.io/github/license/yujianyu/ps7-toolkit)](LICENSE)

> Windows 上一键把 PowerShell 5.1 换成 PowerShell 7，顺带装上 6 个 Rust 高性能命令行工具，并根治中文乱码。

不需要管理员权限，不需要 Python，不写死盘符，断网也能装。重复执行是安全的——只补缺失项，不会重复安装。

---

## 这个工具是干什么的

现在你在 WorkBuddy、DeepSeek DSH、豆包、千问这些 AI 客户端里让它跑个命令、处理批文件、搜点东西，它在 Windows 上调的是系统自带的 **Windows PowerShell 5.1** —— 一个 2009 年的老引擎。于是就经常出现这些情况：

- 脚本里带中文注释，直接报「字符串缺少终止符」
- 输出满屏 `鐗堟湰` 这种乱码，AI 自己也读不懂在返回什么
- 内联命令的引号被外层解析拆散，明明写对了却执行失败
- 想连 GitHub 下载点东西，超时 —— 因为 5.1 默认用老 TLS
- 想用 `&&` 串联命令、用 `?:` 写个判断，语法直接不支持

这些看起来像「AI 出错了」，其实九成是 shell 太老。AI 在 5.1 上每走一步都要绕坑，绕不过去就报错，报了错就重试，token 就这样白白烧掉。

换成 PowerShell 7 之后，这一整类问题会一次性消失：UTF-8 是默认的，TLS 是新的，语法是现代的，速度还快一倍。AI 不用再猜、不用再绕，把精力放回真正要做的事上。

**所以它做的事，一句话：把 Windows 自带的 PowerShell 5.1 换成 PowerShell 7，再补上 6 个 Rust 写的命令行工具，顺手把中文乱码根治掉。**

装完之后你会得到三样东西：

- **PowerShell 7（`pwsh`）** —— 新的主力 shell。UTF-8 默认、支持 `&&` / `??` / `?:`、实测比 5.1 快约 2 倍
- **六个 Rust 命令行工具** —— `ripgrep`（检索）/ `fd`（找文件）/ `fzf`（模糊跳转）/ `bat`（带高亮的 cat）/ `delta`（diff 美化）/ `jq`（处理 JSON）
- **一整套已经配好的默认** —— profile 编码、`.ps1` 双击关联、Windows Terminal 与 VSCode 的默认终端、开始菜单快捷方式

这些不是可有可无的锦上添花。如果你在 Windows 上用过命令行——或者让 AI 帮你用过——下面这些坑大概率都踩过：

| 症状 | 原因 | 装完之后 |
|---|---|---|
| AI 执行脚本时报「字符串缺少终止符」 | 脚本含中文，5.1 按 ANSI/GBK 读 | 7 默认 UTF-8，不再误判 |
| 中文输出变成 `鐗堟湰` 一堆乱码 | 5.1 默认编码是 ANSI/GBK | UTF-8 全局打通，所有调用 PowerShell 的软件都不乱码 |
| 连不上 GitHub / 下载总是失败 | 5.1 默认用老 TLS，握手被拒 | 7 内置 TLS 1.2+，直连正常 |
| 脚本里不能用 `&&`、`??`、`?:` | 5.1 不支持这些语法 | 全部可用 |
| 处理大文件、大目录慢得离谱 | 5.1 跑在 .NET Framework 上 | 实测约快 1.9 倍 |
| 搜代码用 `Select-String` 等到花儿谢 | 纯 PowerShell 实现 | 换 `rg`，实测快 11 倍 |

---

## 使用教程

### 第一步：先自己装好 PowerShell 7（推荐）

**官方下载地址：<https://github.com/PowerShell/PowerShell/releases>**

打开上面的链接，翻到最新版本，在 **Assets** 里挑一个下载：

| 选这个 | 适合谁 | 怎么装 |
|---|---|---|
| `PowerShell-7.x.x-win-x64.msi` | 大多数人 | 双击一路下一步。会自动装进 `Program Files` 并加好 PATH |
| `PowerShell-7.x.x-win-x64.zip` | 不想装、要便携版 | 解压到任意目录（比如 `D:\Tools\ps7`），再把这个目录加进 PATH |

> 不确定自己什么架构？Windows 10/11 绝大多数是 **x64**。ARM 设备（如骁龙本）选 `win-arm64`。

装完**新开一个终端**验证：

```powershell
pwsh -v
```

能看到 `7.x.x` 就成功了。

**装好之后再回来跑下面的脚本** —— 它会检测到你已经装了 PowerShell 7，直接复用，不会重复下载，只给你补上 Rust 工具和那些默认化配置。

> 实在不想手动折腾？也可以跳过这一步，直接跑下面的安装脚本，它会自动把 PowerShell 7 下载并装好（内置了国内镜像加速，连不上 GitHub 也能装）。

---

### 第二步：装 Rust 工具链与默认配置

打开 **PowerShell**（开始菜单搜 PowerShell 就行，5.1 也可以），执行：

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\install.ps1"
```

装完**重启终端**（让 PATH 生效），然后验证：

```powershell
pwsh -v          # 应显示 7.x
rg --version     # 应显示 ripgrep
```

#### 已经装好 PowerShell 7 了？

不用做任何额外操作。安装器会探测到已有版本并直接复用，只补 Rust 工具和默认配置。

想把已经下好但还没装的 zip 交给它处理（跳过自动搜索）：

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\install.ps1" -ZipPath "D:\下载\PowerShell-7.6.7-win-x64.zip"
```

---

## 安装器是怎么找安装包的

它不会傻等你在某个固定目录放文件，而是按这个顺序找：

1. **先探测系统里已装的 pwsh** —— 扫 `Program Files\PowerShell\7`、用户目录、注册表 App Paths、PATH、scoop、chocolatey、Microsoft Store 版。
   **找到就直接复用，绝不重复安装**（如果你已经用 MSI 装过，它只会补 Rust 工具和默认化配置）。
2. 没找到，才找**本地 zip** —— Downloads / 桌面 / 下载 / 迅雷下载 / Documents / TEMP 都会翻一遍。
3. 本地也没有，才**自动下载** ——
   查 GitHub API 拿最新版本 → 三个国内镜像依次回退 → 微软官方 `aka.ms` 短链 → 内置版本表兜底（这一层保证**断网也能装**）。

---

## 常用参数

| 参数 | 说明 |
|---|---|
| `-ZipPath <路径>` | 指定本地安装包，跳过自动搜索 |
| `-ToolsRoot <路径>` | 自定义安装根目录，默认 `%LOCALAPPDATA%\ps7-toolkit` |
| `-Mirror <URL>` | 自定义下载镜像，会插到内置镜像列表最前 |
| `-SkipDefaults` | 只装不配，不动系统默认（不写 profile、不改注册表、不建快捷方式） |
| `-SkipRustTools` | 只装 PowerShell 7，不装那 6 个 Rust 工具 |
| `-CheckOnly` | 只体检，不做任何改动 |
| `-Force` | 强制在 `-ToolsRoot` 下放一份完整的 pwsh。本机已装就直接复制（约 5 秒），没装才联网下载 |

> 有一点容易误会：不加 `-Force` 时，如果本机已经装了 PowerShell 7，安装器会**复用**那一份，
> 不会复制到 `-ToolsRoot`（省 300MB 磁盘）。所以想让 pwsh 也落到 `D:\Tools\ps7` 这种自定义目录，
> 要加 `-Force`。安装时会明确打印「未复制到 …」，不会让你蒙在鼓里。

例子——装到别的盘、只装主程序：

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\install.ps1" -ToolsRoot "D:\Tools\ps7" -SkipRustTools
```

例子——把 pwsh 真正搬到 D 盘（本机已有安装则复制，不下载）：

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\install.ps1" -ToolsRoot "D:\Tools\ps7" -Force
```

---

## 装完怎么用

### pwsh —— 主力 shell

开始菜单里会有「PowerShell 7」。命令行里直接敲：

```powershell
pwsh
```

右击 `.ps1` 文件也会用 PowerShell 7 打开。Windows Terminal 和 VSCode 的默认终端也会被切成 PS7。

### rg —— 极速内容检索（最值钱的一个）

```powershell
rg -n "关键词" .                          # 当前目录递归搜，显示行号
rg -n -e "关键词" -g "*.py" C:\某目录     # 只搜 .py
rg -i "关键词"                            # 忽略大小写
rg -l "关键词"                            # 只列文件名
rg --files -g "*.log" | rg -v "temp"     # 管道配合
```

自带 `.gitignore` 规则，不会去翻 `node_modules` 或 `.git`。

### fd —— 找文件

```powershell
fd 关键词                      # 文件名模糊匹配
fd -e py                       # 所有 .py
fd -H -I "config"              # 包含隐藏文件和 gitignore 里的
fd -x rm {}                    # 对结果逐个执行命令
```

### fzf —— 模糊查找

```powershell
fd | fzf                       # 从文件列表里模糊挑
history | fzf                  # 翻历史命令
```

### bat —— 带语法高亮的 cat

```powershell
bat README.md                  # 高亮 + 行号 + git 改动标记
bat -p file.py                 # 纯净输出，不要行号
```

### delta —— git diff 变好看

配好 git 后自动生效：

```
git config --global core.pager delta
git config --global interactive.diffFilter "delta --color-only"
```

### jq —— 处理 JSON

```powershell
curl.exe -s https://api.github.com/repos/PowerShell/PowerShell | jq .tag_name
Get-Content data.json | jq ".[] | .name"
```

> **中文键名注意**：jq 的裸字段名只支持 ASCII。中文键必须写 `jq '.["名称"]'`，
> 直接写 `.名称` 会报 `INVALID_CHARACTER`。中文**值**不受影响，只有键名要注意。

---

## 验证与排错

跑一遍体检：

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\verify.ps1"
```

它会分 6 段检查并给出报告：PowerShell 7 / Rust 工具 / profile 编码设置 / 注册表与文件关联 / 应用层配置 / PATH。

加 `-Json` 可以输出机器可读结果。

## 反引号与特殊字符（AI 执行前必读）

反引号在 **bash（Git Bash / MSYS2）里是命令替换**，在 **pwsh 里是转义符**——同一个字符，两种危险：

```bash
echo `date`        # bash：date 被真的执行，输出塞回命令行
Write-Host "a`nb"  # pwsh：反引号吞掉 n，"a`nb" 变成换行
cat <<EOF ... EOF  # 未加引号的 heredoc：正文里的 ` 和 $ 会被展开后再落盘
```

**规则**：命令替换写 `$(date)`；字面反引号放单引号 `'...`...'`；写文件用 `cat <<'EOF'`；
长命令 / 嵌套引号写成 `.ps1` 文件再用 `pwsh -File` 跑。

**拿不准就先过守卫**（只读诊断，不改系统）：

```powershell
& ".\scripts\shell-guard.ps1" -Text 'echo 今天是 `date`'      # 会话内直调，引号保真
pwsh -NoProfile -ExecutionPolicy Bypass -File ".\scripts\shell-guard.ps1" -File .\build.ps1 -Shell pwsh
```

退出码：`0` 安全 / `1` 发现风险 / `2` 有风险拒绝执行（配合 `-Execute`）/ `3` 文件不存在。
加 `-Execute` 先诊断再执行，有风险默认拒绝，`-Force` 放行。

> **退出码的归一说明**：`-Execute` 里原生命令的非零退出码统一归一为 `1`（不精确透传原值）。
> 原因是精确透传要靠残余的 `$LASTEXITCODE`，会把上一条命令的码带进判断里，得不偿失。
> 需要精确码就直接自己跑：`& <命令>; $LASTEXITCODE`。

守卫还会顺带检查高频坑：bash 引号外的 Windows 路径（`C:\Users` 的反斜杠被吃掉，判硬风险）；
pwsh 口径下提醒 5.1 的 curl 别名（写 `curl.exe`）、`&&` 不支持、`Out-File` 默认 UTF-16。

> **调用方式**：参数名是 `-Text`（不是 `-Command`，避免撞上 powershell.exe 自身开关）。
> 引号保真实测结论：会话内 `&` 直调保真；守卫 `-Execute` 内部走 `-EncodedCommand` 保真；
> **任何 `-Command` 式跨进程转发一律丢内层双引号（5.1 与 pwsh 7 实测均丢，
> `git commit -m "a  b"` 会变成另一条命令）**，别当兜底；跨进程调守卫用 pwsh 7 的 `-File`。

> 从 bash 调守卫时 `-Text` 后面必须**用单引号**，否则反引号在到达守卫前就被 bash 吃掉了。

**在脚本里调用守卫函数**（dot-source 后可用，两种模式互斥，输出和退出码不会混在一起）：

```powershell
. .\scripts\shell-guard.ps1

# 默认：输出直接显示在控制台，返回值只有 int 退出码
$rc = Invoke-SafeCommand -Command 'Get-Content a.txt | Measure-Object -Line'
if ($rc -ne 0) { '失败了' }

# -Capture：输出走管道（可赋值），退出码在 $GuardLastExitCode
$out = Invoke-SafeCommand -Command 'git status --porcelain' -Capture
if ($GuardLastExitCode -ne 0) { '失败了' }
```

> 子进程的 stderr 会加 `[stderr] ` 前缀并压成单行，不会和 stdout 混在一起。
> 注意别写 `exit (Invoke-SafeCommand ...)`——括号会把输出吞进表达式。

### 自己跑回归测试

安装器改过之后，可以跑一遍冒烟测试确认没弄坏东西：

```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\smoke-test.ps1"
```

60 项断言，约 1~2 分钟，全程在临时目录里跑、**不碰你的系统配置**（用 `-SkipDefaults`），跑完自动清理。
覆盖：只读体检、隔离安装、6 个工具是否真能跑、幂等（连跑两次二进制一致）、
`-Force` 是否走复制而不是下载、中文 + 空格路径、错误参数处理、卸载是否干净，
以及反引号守卫的 20 项（诊断口径、引号保真、stderr 前缀、返回值契约、拒绝执行）。

退出码 `0` 表示全过，`1` 表示有失败——所以它也能直接塞进 CI。

**开发者备注（改守卫的人必看）**：测引号保真时，跨进程一律用 `-File` + 文件承载命令串，
或 `-EncodedCommand`；**千万别拿 `-Command "<含内层双引号的字符串>"` 当对照组**——
对照组自己就会走 argv 层把引号切散，于是「被测组和对照组都坏」，看起来像「都没问题」。
这个坑我们在 1.1.6 里真踩过两次。

更多踩坑记录见 [references/troubleshooting.md](references/troubleshooting.md)，涵盖：装完 `pwsh` 找不到、中文还是乱码、双击 `.ps1` 提示没有关联、镜像下载卡住、Windows Terminal 没跟着切等。

---

## 卸载

```powershell
# 1. 删安装目录（默认在 %LOCALAPPDATA%\ps7-toolkit；装的时候用了 -ToolsRoot 就删那个目录）
#    想留退路就把 Remove-Item 换成 scripts\safe-remove.ps1 -Recurse（移进回收站，可还原）
Remove-Item -Recurse -Force "$env:LOCALAPPDATA\ps7-toolkit"

# 2. 删这几个注册表项
Remove-Item -Recurse "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\pwsh.exe"
Remove-Item -Recurse "HKCU:\Software\Microsoft\Classes\.ps1"
# 这两项是「默认终端程序」的全局设置，删掉等于恢复系统自动选择
Remove-ItemProperty "HKCU:\Console\%%Startup" -Name DelegationConsole -ErrorAction SilentlyContinue
Remove-ItemProperty "HKCU:\Console\%%Startup" -Name DelegationTerminal -ErrorAction SilentlyContinue
```

再从用户 PATH 里去掉 `%LOCALAPPDATA%\ps7-toolkit\ps7` 和 `%LOCALAPPDATA%\ps7-toolkit\bin`，最后删掉两个 profile 文件里本工具追加的段落。

---

## 这个工具会改动什么

所有改动都在**当前用户**范围内，不需要管理员权限，**不写 `HKEY_LOCAL_MACHINE`**。

| 改动 | 位置 |
|---|---|
| 写入可执行文件 | `%LOCALAPPDATA%\ps7-toolkit`（可用 `-ToolsRoot` 改） |
| 追加用户 PATH | `HKCU\...\Environment` 的 `Path` |
| 写入 profile | `Documents\PowerShell\...profile.ps1`（7.x）<br>`Documents\WindowsPowerShell\...profile.ps1`（5.1） |
| 注册 pwsh 路径 | `HKCU\...\App Paths\pwsh.exe` |
| 关联 `.ps1` 双击行为 | `HKCU\Software\Microsoft\Classes\.ps1\shell\open\command` |
| 默认控制台 | `HKCU\Console\%%Startup` 的 `DelegationConsole` / `DelegationTerminal`（仅当检测到 Windows Terminal） |
| 开始菜单快捷方式 | `%APPDATA%\Microsoft\Windows\Start Menu\Programs` |
| 配置备份 | `settings.json.ps7bak`（WT / VSCode 各一份；生成后不再覆盖，保留最初原样） |

不想动系统默认就加 `-SkipDefaults`，或先跑 `-CheckOnly` 只看不改。

**网络访问**：仅在需要下载时访问 `api.github.com`、`github.com`、`gh-proxy.com` / `ghfast.top` / `ghproxy.net`（国内加速镜像）、`aka.ms`。不收集任何数据，不上报统计，不需要任何 API Key。

---

## 设计上故意不做的事

| 没做的事 | 原因 |
|---|---|
| 改 `HKLM\...\Nls\CodePage\ACP = 65001` | 会让老的 GBK 程序（部分国产软件、游戏）全部乱码，风险远大于收益 |
| 把 `powershell.exe` 劫持成指向 pwsh | 系统组件和大量安装脚本硬依赖 `C:\Windows\System32\WindowsPowerShell\v1.0\`，改了会导致装软件失败 |
| 用 `Add-Type` 编译 .NET 代码 | 部分 AI 客户端的安全策略会直接拦截（需要等价能力时看下方「安全删除」） |

正确姿势是习惯敲 `pwsh`，或用开始菜单里的「PowerShell 7」。5.1 留着不碍事，老脚本还能跑。

> 1.1.8 起开始菜单入口不再建 `.lnk`（建快捷方式只能调 COM 或运行时编译，受限环境会被拦），
> 改为放一个 `PowerShell 7.cmd`；机器上已经存在 `.lnk` 的不会被改动。

---

## 安全删除（默认进回收站）

`Remove-Item` 是**永久删除，不进回收站**，`-Force` 更是直接抹掉。要删得能还原，用自带封装：

```powershell
# 默认移入回收站
pwsh -NoProfile -File .\scripts\safe-remove.ps1 -Path "C:\temp\old" -Recurse

# 先看会删什么
pwsh -NoProfile -File .\scripts\safe-remove.ps1 -Path "C:\temp\*.log" -WhatIf
```

| 行为 | 说明 |
|---|---|
| 默认 | 移入回收站，可从回收站还原 |
| `-Permanent` | 永久删除，输出明确标注不可恢复 |
| `-Recurse` | 删目录必需；不带时目录直接拒绝 |
| `-WhatIf` | 只预览不执行 |
| 受保护名单 | 盘根、系统目录、用户目录本身一律拒绝 |
| 回收站检测 | 网络盘 / 移动盘 / 未启用回收站 → 中止并提示，**不会偷偷改成永久删** |

退出码：`0` 成功 / `1` 有失败 / `2` 无可删目标 / `3` 无回收站需 `-Permanent`。

实现上只用已编译好的 `Microsoft.VisualBasic.FileIO.FileSystem`，不做运行时编译、不创建 COM 对象，
所以在前述受限环境里也能跑；5.1 下该类型不会自动加载，脚本内部已用反射补载。

---

## 作为 AI 技能使用

**最省事的方式：把下面这句话直接丢给你的 AI 助手。**

```text
帮我把 https://github.com/yujianyu/ps7-toolkit 装成技能，然后按它的 SKILL.md 用起来
```

只要这个 AI 助手能联网、能读写文件（Claude Code / WorkBuddy / 豆包 / 千问 / DeepSeek DSH / Cursor 都算），它就能自己把仓库拉下来、放进对应的技能目录。

仓库根目录的 `SKILL.md` 就是给它们读的执行说明书，里面写好了什么时候该触发、怎么调用、装完之后必须遵守的规范，以及几条硬禁忌（比如别去改 `HKLM` 的代码页、别劫持 `powershell.exe`）。

各客户端的技能目录：

| 客户端 | 放哪里 |
|---|---|
| WorkBuddy | 「添加技能 → 导入技能」，拖文件夹或 zip 进去 |
| Claude Code | `~/.claude/skills/ps7-toolkit/` |
| 千问 | `~/.qwenworkcn/skills/ps7-toolkit/` |
| 豆包 | `%LOCALAPPDATA%\DoubaoWork\User Data\Default\.doubaowork\agent_mode\workspace\.user_skills\ps7-toolkit\` |
| DeepSeek DSH | 在该客户端 skills 目录建同名文件夹，或把要点追加到 `~/.dsh/AGENTS.md` |
| 其他 | 整个目录丢进该客户端的 skills 目录即可，认 `SKILL.md` |

> 本技能也已提交到 ClawHub（WorkBuddy 技能市场的 SkillHub 分区），审核放行后可直接 `clawhub install yujianyu/powershell7-toolkit` 安装。目前仍处于平台审核队列中，所以上面那个「丢仓库地址给 AI」的方式最稳妥。

---

## 目录结构

```
ps7-toolkit/
├── SKILL.md                      给 AI 助手读的执行说明书
├── README.md                     本文件
├── CHANGELOG.md                  版本记录
├── assets/icon.png               512x512 图标
├── scripts/
│   ├── install.ps1               主安装器（探测优先 + 自动下载兜底）
│   ├── setup-defaults.ps1        默认化（profile / 注册表 / 关联 / 快捷方式 / 终端）
│   ├── verify.ps1                六段体检
│   ├── wt-config.ps1             WT/VSCode 配置的文本级改写（保留注释）
│   └── smoke-test.ps1            38 项回归测试（隔离沙箱，不碰系统配置）
└── references/
    └── troubleshooting.md        踩坑与排错
```

---

## 环境要求

- Windows 10 / 11（Server 亦可）
- Windows PowerShell 5.1（系统自带）或 PowerShell 7+
- 无需管理员权限（如勾选「为所有用户安装」MSI 版才需要）

---

## 更新记录

- **v1.1.5**（最新）—— 换环境复查又收到 3 条反馈，全部成立：体检把「全 0 GUID」当成已指定；
  默认终端的注册表写入被 Windows Terminal 配置（JSONC，带 `//` 注释）解析失败连带跳过；
  改写 WT/VSCode 配置会把用户的注释、空行、自定义 profile 全抹掉（只在「第一次跑」触发，
  之后自愈，所以自己测不出来）。这一版把配置改写改成文本级定点修改 + 自动备份 + 改后自检，
  内测又修掉 3 处：独立运行 `setup-defaults.ps1` 会往 PATH 加一条死链、
  VSCode 配置「值已经对了」也会重写一次、落盘会丢掉原文件的 UTF-8 BOM。
  回归测试从 23 项扩到 38 项。细节见 [CHANGELOG.md](CHANGELOG.md)。
- **v1.1.4** —— 换环境实测（用另一个 AI 客户端独立装一遍、跑一遍回归测试）发现的 5 个问题：
  空的下载缓存目录永远清不掉、「默认终端程序」写到了系统不读的注册表位置等于空跑、
  体检只做字符串包含所以会谎报 PATH 正常、换目录重装会留下死的 PATH 项、以及一条恒假的测试断言。
  细节见 [CHANGELOG.md](CHANGELOG.md)。
- **v1.1.3** —— 第一轮回归测试修掉 6 个真 bug：安装器退出码「假成功」、GitHub 限流时
  6 个工具静默装不上、PowerShell 5.1 下进度条刷屏、体检脚本硬编码了开发机路径、
  `-ZipPath` 输了不存在的文件会偷偷改成联网下载、复用 choco shim 导致「装上但跑不起来」。
- **v1.1.2** —— 技能市场重发布，代码与 1.1.1 完全一致，无需重装。
- **v1.1.1** —— 技能描述改为「症状驱动」，让 AI 在撞到具体报错时更容易想起调用它。
- **v1.1.0** —— 首个公开版本。

每个版本的安装包都在 [Releases](https://github.com/yujianyu/ps7-toolkit/releases) 里。

---

## 许可证

[MIT](LICENSE)
