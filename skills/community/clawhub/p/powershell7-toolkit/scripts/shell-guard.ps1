#Requires -Version 5.1
<#
.SYNOPSIS
    反引号 / 特殊字符守卫（shell-guard）。
.DESCRIPTION
    同一个反引号，在两个 shell 里是两种危险：
      - bash（含 Git Bash / MSYS2）：反引号 = 命令替换。`` `date` `` 会被先执行，
        再把输出塞回命令行；落单的反引号会报 unmatched 或把后半段整个吞掉。
      - pwsh：反引号 = 转义符。会吞掉后面一个字符，行尾的反引号是续行。
    AI 生成的命令只要带上反引号，就会被吃掉、误执行，或者写出缺字少符的文件。

    本脚本做三件事：
      1. 诊断一段命令（或一个脚本文件）里的反引号风险，顺带检查：引号外的 Windows
         反斜杠路径（bash 会吃掉反斜杠）、5.1 的 curl 别名 / && / 写文件默认编码等高频坑；
      2. 给出改写后的安全形式与建议；
      3. 可选：诊断通过才真正执行（有风险默认拒绝，加 -Force 才放行）。

    只定义函数、不碰系统任何设置，因此回归测试可以 dot-source 后逐个调用。
.PARAMETER Text
    待检查的命令原文。注意参数名是 -Text 而不是 -Command：后者会撞上 powershell.exe
    自身的 -Command 开关，导致通过 powershell -File 方式调用时参数被截获错位。
    从 bash 传入时必须用单引号包裹，否则反引号在到达本脚本之前
    就已经被 bash 吃掉了，再厉害的守卫也救不回来。
.PARAMETER Shell
    按哪个 shell 的规则诊断：bash（默认）或 pwsh。
.PARAMETER File
    检查一个脚本文件里的反引号，而不是 -Command。
.PARAMETER Execute
    诊断通过后用 pwsh 执行该命令。
.PARAMETER Force
    有风险也照跑（后果自负）。
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\shell-guard.ps1 -Text 'echo `date`'
    （推荐用 & .\shell-guard.ps1 直接调用，可避免 powershell.exe 转发参数时吃引号）
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\shell-guard.ps1 -File .\build.ps1
#>
[CmdletBinding()]
param(
    [string]$Text,
    [ValidateSet('bash', 'pwsh')]
    [string]$Shell = 'bash',
    [string]$File,
    [switch]$Execute,
    [switch]$Force
)

$ErrorActionPreference = 'Continue'

# ---------------------------------------------------------------- 内部：定位「未加引号的 Windows 反斜杠路径」
# bash 在引号外把 \ 当转义符吃掉：cd C:\Users\x 实际执行的是 cd C:Usersx。
# 单引号里原样保留（安全）；bash 双引号里 \U 不属特殊序列也原样保留，但为稳妥起见
# 双引号内不算「裸」——本检查只针对引号外的路径。
function Get-BareBackslashPathIndex {
    param([string]$Command)
    $idx = @()
    $inSingle = $false
    $inDouble = $false
    for ($i = 0; $i -lt $Command.Length; $i++) {
        $c = $Command[$i]
        if ($inSingle) { if ($c -eq "'") { $inSingle = $false }; continue }
        if ($inDouble) { if ($c -eq '"') { $inDouble = $false }; continue }
        if ($c -eq "'") { $inSingle = $true; continue }
        if ($c -eq '"') { $inDouble = $true; continue }
        # 盘符路径：字母 + 冒号 + 反斜杠（引号外）
        if (
            [char]::IsLetter($c) -and
            $i + 2 -lt $Command.Length -and
            $Command[$i + 1] -eq ':' -and
            $Command[$i + 2] -eq '\'
        ) {
            # 前一个字符是字母或数字时说明这是单词中间，不算盘符开头（如 D2:\ 少见，忽略）
            if ($i -eq 0 -or -not [char]::IsLetterOrDigit($Command[$i - 1])) { $idx += $i }
        }
    }
    return $idx
}

# ---------------------------------------------------------------- 内部：定位「裸反引号」
# 单引号里的反引号两个 shell 都当字面量，安全；双引号里则不然：
#   bash 仍然做命令替换，pwsh 仍然当转义符 —— 所以双引号内的反引号也要算「裸」。
function Get-BareBacktickIndex {
    param(
        [string]$Command,
        [ValidateSet('bash', 'pwsh')]
        [string]$Shell = 'bash'
    )
    $idx = @()
    $inSingle = $false
    $inDouble = $false
    for ($i = 0; $i -lt $Command.Length; $i++) {
        $c = $Command[$i]
        if ($inSingle) {
            if ($c -eq "'") { $inSingle = $false }
            continue
        }
        if ($inDouble) {
            # bash 双引号里反斜杠可以转义下一个字符
            if ($Shell -eq 'bash' -and $c -eq '\') { $i++; continue }
            if ($c -eq '"') { $inDouble = $false; continue }
            if ($c -eq '`') { $idx += $i; continue }
            continue
        }
        if ($c -eq "'") { $inSingle = $true; continue }
        if ($c -eq '"') { $inDouble = $true; continue }
        if ($c -eq '`') { $idx += $i; continue }
    }
    return $idx
}

# ---------------------------------------------------------------- 诊断
function Get-ShellQuoteDiagnosis {
    param(
        [string]$Command,
        [ValidateSet('bash', 'pwsh')]
        [string]$Shell = 'bash'
    )
    $idx = Get-BareBacktickIndex -Command $Command -Shell $Shell
    $findings = @()
    $advice   = @()
    $risky    = $false

    if ($idx.Count -gt 0) {
        $risky = $true
        $n = $idx.Count
        if ($Shell -eq 'bash') {
            if ($n % 2 -eq 0) {
                $findings += ('发现 ' + $n + ' 个裸反引号（' + ($n / 2) + ' 对）：bash 会先把反引号里的内容当命令执行，再把输出塞回命令行。')
                $advice   += '要命令替换就写成 $() ：$(date)，不要写 `date`。'
                $advice   += '要字面反引号，就把那一段放进单引号：''...`...''；或把整条命令写进 .ps1 文件用 -File 跑。'
            } else {
                $findings += ('发现 ' + $n + ' 个裸反引号（奇数个）：bash 报 unmatched 反引号，或把后半段直接吞掉，命令静默变形。')
                $advice   += '字面反引号请用单引号包住那一段字符串：''...`...''。'
            }
        } else {
            $findings += ('发现 ' + $n + ' 个裸反引号：pwsh 里反引号是转义符，会吞掉后面一个字符（`n 变成换行，行尾 ` 是续行）。')
            $advice   += '字面反引号放单引号里 ''...`...''，或写两个反引号 `` 表示一个。'
        }
        $advice += "最稳的做法：把命令写成 .ps1 文件（用 cat <<'EOF' 这种带引号的 heredoc），再用 pwsh -File 跑，全程不让 bash 碰。"
    }

    # heredoc 分隔符没加引号：就算一个反引号都没有也要提醒，$ 变量同样会被 bash 展开
    if ($Shell -eq 'bash' -and $Command -match '<<' -and $Command -notmatch "<<[-~]*\s*'") {
        $risky = $true
        $findings += '检测到 heredoc 分隔符没加引号：正文里的 $ 和反引号会被 bash 先展开再写进文件，落盘内容跟你想的不一样。'
        $advice   += "写成 cat <<'EOF' ... EOF（分隔符加单引号），正文才会原样落盘。"
    }

    # bash：引号外的 Windows 反斜杠路径，\ 会被当转义符吃掉
    if ($Shell -eq 'bash') {
        $bs = Get-BareBackslashPathIndex -Command $Command
        if ($bs.Count -gt 0) {
            $risky = $true
            $findings += ('发现 ' + $bs.Count + ' 处引号外的 Windows 路径（含反斜杠）：bash 会把反斜杠当转义符吃掉，C:\Users\x 实际变成 C:Usersx，命令拿着错误路径去跑。')
            $advice   += '整段路径放进单引号：cd ''C:\Users\x''，或改成正斜杠 cd C:/Users/x（Windows 程序也认）。'
        }
    }

    # pwsh：5.1 特有坑，只提醒不判风险（pwsh 7 下这些都正常）
    if ($Shell -eq 'pwsh') {
        if ($Command -match '(^|[\s;&|(])curl\s' -and $Command -notmatch 'curl\.exe') {
            $advice += '提醒：Windows PowerShell 5.1 里 curl 是 Invoke-WebRequest 的别名，参数跟真 curl 完全不同。要用真 curl 就写 curl.exe（pwsh 7 无此问题）。'
        }
        if ($Command -match '&&|\|\|') {
            $advice += '提醒：&& / || 只有 PowerShell 7 支持，5.1 会直接报「token && 不是有效的语句元素」。请确认用 pwsh 7 执行，或写成 cmd1; if ($LASTEXITCODE -eq 0) { cmd2 }。'
        }
        if ($Command -match 'Out-File|Set-Content|Add-Content|Export-Csv' -and $Command -notmatch '-Encoding') {
            $advice += '提醒：5.1 写文件默认 UTF-16（Out-File）或 ANSI，bash/python 读到就是乱码。显式加 -Encoding utf8，或用 pwsh 7（默认 UTF-8）。'
        }
    }

    $safe = $null
    if ($risky) { $safe = ConvertTo-SafeCommand -Command $Command -Shell $Shell }

    return [pscustomobject]@{
        Shell     = $Shell
        Command   = $Command
        Backticks = $idx.Count
        Risky     = $risky
        Findings  = $findings
        Advice    = $advice
        SafeForm  = $safe
    }
}

# ---------------------------------------------------------------- 改写
function ConvertTo-SafeCommand {
    param(
        [string]$Command,
        [ValidateSet('bash', 'pwsh')]
        [string]$Shell = 'bash'
    )
    $idx = Get-BareBacktickIndex -Command $Command -Shell $Shell
    if ($idx.Count -eq 0) { return $Command }

    # bash + 成对反引号：`cmd` -> $(cmd)。这是唯一能确定意图（就是想做命令替换）的情况。
    if ($Shell -eq 'bash' -and $idx.Count % 2 -eq 0) {
        # 保真检查：反引号之间若含单引号或 $（如 'it''s'、"$env:FOO"），改写可能改变语义，
        # 只给建议不做自动改写 —— 猜错比不猜更危险。
        for ($k = 0; $k -lt $idx.Count; $k += 2) {
            $seg = $Command.Substring($idx[$k] + 1, $idx[$k + 1] - $idx[$k] - 1)
            if ($seg.Contains("'") -or $seg.Contains('$')) { return $null }
        }
        $out  = ''
        $prev = 0
        for ($k = 0; $k -lt $idx.Count; $k += 2) {
            $open  = $idx[$k]
            $close = $idx[$k + 1]
            $out += $Command.Substring($prev, $open - $prev)
            $out += '$('
            $out += $Command.Substring($open + 1, $close - $open - 1)
            $out += ')'
            $prev = $close + 1
        }
        $out += $Command.Substring($prev)
        return $out
    }

    # 其余情况（奇数个 / pwsh 转义符）无法判断作者想要命令替换还是字面量，
    # 不做自动改写 —— 猜错比不猜更危险，交给 Advice 给人看。
    return $null
}

# ---------------------------------------------------------------- 执行（有风险默认拒绝）
function Get-GuardHostExe {
    $g = Get-Command pwsh -ErrorAction SilentlyContinue
    if ($g) { return $g.Source }
    $fallback = Join-Path $env:LOCALAPPDATA 'ps7-toolkit\ps7\pwsh.exe'
    if (Test-Path $fallback) { return $fallback }
    return 'powershell'
}

# 执行宿主命令：必须走 -EncodedCommand（Base64 UTF-16LE）。
# 实测（DeepSeek 二轮报告）：任何 -Command 式跨进程转发都会丢内层双引号 ——
# Write-Output "hello  world  spaced" 会被拆成 3 个参数输出 3 行，5.1 与 pwsh 7 均如此，
# argv 层根本不转义内层引号。EncodedCommand 不经过引号重解析，完全保真。
#
# 输出分两路（DeepSeek 三轮报告的两个缺陷都在这里）：
#   1. 默认把子进程输出写宿主（Write-Host），函数才「只返回 int」，不会变成 [输出..., 退出码] 数组；
#      要拿输出请加 -Capture，此时输出走管道、退出码留在 $script:GuardLastExitCode。
#   2. stderr 不与 stdout 混流：加 [stderr] 前缀并压成单行（ErrorRecord 展开会带
#      CategoryInfo / FullyQualifiedErrorId / caret 定位，脚本侧没法解析）。
function Invoke-GuardHost {
    param(
        [string]$Command,
        [switch]$Capture
    )
    $enc = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($Command))
    $errBefore = $Error.Count
    $raw = & (Get-GuardHostExe) -NoLogo -NoProfile -EncodedCommand $enc 2>&1
    foreach ($item in $raw) {
        if ($item -is [System.Management.Automation.ErrorRecord]) {
            $line = (($item.ToString() -split "`r?`n") | Where-Object { $_.Trim().Length -gt 0 } | Select-Object -First 1)
            if (-not $line) { $line = '' }
            $text = '[stderr] ' + $line.Trim()
            if ($Capture) { $text } else { Write-Host $text -ForegroundColor DarkYellow }
        } else {
            $s = "$item"
            if ($Capture) { $s } else { Write-Host $s }
        }
    }
    $script:GuardLastExitCode = $LASTEXITCODE
    if ($null -eq $script:GuardLastExitCode) {
        # 纯 PS 命令失败时个别宿主不留原生退出码：用错误流增量兜底，报错不报成功
        $script:GuardLastExitCode = if ($Error.Count -gt $errBefore) { 1 } else { 0 }
    }
}

# 契约（DeepSeek 三轮报告：返回值曾被输出污染，$rc 变成 Object[] 使判断恒真）：
#   默认      子进程输出显示在宿主，返回值**只有 int 退出码**
#             $rc = Invoke-SafeCommand -Command '...'; if ($rc -ne 0) { ... }   ← 可靠
#   -Capture  子进程输出走管道（可赋值），退出码在 $script:GuardLastExitCode，函数不返回值
#             $out = Invoke-SafeCommand -Command '...' -Capture
#             if ($script:GuardLastExitCode -ne 0) { ... }
# 两种模式互斥，输出与退出码绝不会混进同一个返回流。
function Invoke-SafeCommand {
    param(
        [string]$Command,
        [switch]$Force,
        [switch]$Capture
    )
    $d = Get-ShellQuoteDiagnosis -Command $Command -Shell 'pwsh'
    if ($d.Risky -and -not $Force) {
        Write-Host '[shell-guard] 拒绝执行：命令里有裸反引号，执行结果多半不是你想要的。' -ForegroundColor Yellow
        foreach ($f in $d.Findings) { Write-Host ('  现象: ' + $f) -ForegroundColor Yellow }
        foreach ($a in $d.Advice)   { Write-Host ('  建议: ' + $a) -ForegroundColor DarkYellow }
        Write-Host '  确认没问题就加 -Force。' -ForegroundColor Yellow
        if ($Capture) { $script:GuardLastExitCode = 2; return }
        return 2
    }

    # 不要写 exit (函数调用)：括号会把输出吞进表达式（1.1.6 内测「执行结果消失」的根因）。
    Invoke-GuardHost -Command $Command -Capture:$Capture
    if ($Capture) { return }
    return $script:GuardLastExitCode
}

# ---------------------------------------------------------------- 命令行入口
# dot-source 且不传参数时（回归测试就是这么用的）只定义函数，什么都不做。
if ($File) {
    if (-not (Test-Path $File)) { Write-Host ('[shell-guard] 文件不存在: ' + $File) -ForegroundColor Red; exit 3 }
    $Text = [System.IO.File]::ReadAllText($File)
}

if ($Text) {
    $d = Get-ShellQuoteDiagnosis -Command $Text -Shell $Shell
    if (-not $d.Risky) {
        Write-Host ('[shell-guard] 安全：在 ' + $Shell + ' 里没有发现裸反引号等硬风险。') -ForegroundColor Green
        if ($d.Advice.Count -gt 0) {
            foreach ($a in $d.Advice) { Write-Host ('  提醒: ' + $a) -ForegroundColor DarkYellow }
        }
    } else {
        if ($d.Backticks -gt 0) {
            Write-Host ('[shell-guard] 有风险：' + $Shell + ' 里发现 ' + $d.Backticks + ' 个裸反引号。') -ForegroundColor Yellow
        } else {
            Write-Host ('[shell-guard] 有风险：' + $Shell + ' 口径下发现其它硬风险（见下）。') -ForegroundColor Yellow
        }
        foreach ($f in $d.Findings) { Write-Host ('  现象: ' + $f) -ForegroundColor Yellow }
        foreach ($a in $d.Advice)   { Write-Host ('  建议: ' + $a) -ForegroundColor DarkYellow }
        if ($d.SafeForm) { Write-Host ('  改写: ' + $d.SafeForm) -ForegroundColor Cyan }
    }

    if ($Execute) {
        # 拒绝逻辑按 pwsh 口径（与 Invoke-SafeCommand 一致）；不在此处写 exit (函数调用)，
        # 避免括号把内层输出吞进表达式 —— 这是 1.1.6 内测发现的「执行结果消失」根因。
        $dp = Get-ShellQuoteDiagnosis -Command $Text -Shell 'pwsh'
        if ($dp.Risky -and -not $Force) {
            Write-Host '[shell-guard] 拒绝执行：命令里有裸反引号，执行结果多半不是你想要的。' -ForegroundColor Yellow
            foreach ($f in $dp.Findings) { Write-Host ('  现象: ' + $f) -ForegroundColor Yellow }
            foreach ($a in $dp.Advice)   { Write-Host ('  建议: ' + $a) -ForegroundColor DarkYellow }
            Write-Host '  确认没问题就加 -Force。' -ForegroundColor Yellow
            exit 2
        }
        # CLI 的 -Execute 用 -Capture 让 stdout 留在管道上（可被 > 重定向、被调用方捕获），
        # 退出码仍从 $script:GuardLastExitCode 取。
        Invoke-GuardHost -Command $Text -Capture
        exit $script:GuardLastExitCode
    }

    if ($d.Risky) { exit 1 } else { exit 0 }
}
