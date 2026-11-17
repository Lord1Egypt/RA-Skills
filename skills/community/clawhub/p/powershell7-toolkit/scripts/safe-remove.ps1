<#
.SYNOPSIS
    safe-remove.ps1 —— 安全删除：默认进回收站，删错了能还原。

.DESCRIPTION
    为什么需要这个脚本：

    在部分 AI 客户端里，「运行时编译 .NET 代码」和「实例化 COM 对象」这两类操作会被
    工具层安全规则直接拦住，报错大意是「运行时编译 .NET 代码属于高风险操作」，
    于是删除操作连一个文件都没动，整条清理流程卡死。

    本脚本只用「已编译好的程序集里现成的类型」完成回收站删除：
    全程不做运行时编译，不实例化 COM 对象，因此在受限环境下同样可用。

    安全优先的默认行为：
      1. 只处理存在、且不在保护名单里的路径（系统目录、用户目录本身、盘根一律拒绝）
      2. 删除目录必须显式加 -Recurse
      3. 目标所在磁盘没有回收站（网络盘 / 移动盘 / 未启用）时，默认中止而不是永久删
      4. 只有显式加 -Permanent 才永久删除，且输出会明确标注不可恢复

.PARAMETER Path
    要删除的路径，支持通配符，可以传多个，也可以从管道传入。

.PARAMETER Recurse
    允许删除目录（目录会整体进回收站，不是逐个文件删）。

.PARAMETER Permanent
    永久删除，不进回收站。不可恢复，慎用。

.PARAMETER Force
    只读 / 隐藏属性的目标也删。

.PARAMETER PassThru
    输出结构化结果对象，供上层脚本消费；此时人读信息改走信息流。

.EXAMPLE
    pwsh -NoProfile -File scripts\safe-remove.ps1 -Path "C:\temp\old" -Recurse

.EXAMPLE
    pwsh -NoProfile -File scripts\safe-remove.ps1 -Path "C:\temp\*.log" -WhatIf

.EXAMPLE
    pwsh -NoProfile -File scripts\safe-remove.ps1 -Path "D:\build\out" -Recurse -Permanent

.NOTES
    退出码：
      0  全部成功
      1  有失败项
      2  没有可删目标（路径都不存在，或全被保护规则跳过）
      3  目标位置回收站不可用，需要显式加 -Permanent 才能继续
#>
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
    [Parameter(Mandatory = $true, ValueFromPipeline = $true, Position = 0)]
    [string[]] $Path,

    [switch] $Recurse,
    [switch] $Permanent,
    [switch] $Force,
    [switch] $PassThru
)

begin {
    $script:VbFs = $null
    $script:NeedPermanent = $false
    $script:Results = [System.Collections.ArrayList]::new()
    $script:Count = @{ recycled = 0; permanent = 0; skipped = 0; failed = 0 }

    function Say {
        param([string] $Text)
        if ($PassThru) { Write-Host $Text } else { Write-Output $Text }
    }

    function Add-Result {
        param([string] $Target, [string] $Kind, [string] $Message)
        $tag = switch ($Kind) {
            'recycled'  { '[recycle]   ' }
            'permanent' { '[permanent] ' }
            'skip'      { '[skip]      ' }
            'fail'      { '[fail]      ' }
        }
        Say ("{0} {1}  {2}" -f $tag, $Target, $Message)
        # 注意别直接 Count[$Kind]++：Kind 是 skip/fail，计数键是 skipped/failed，
        # 直接自增会往哈希表里塞出 skip、fail 两个新键，汇总行永远显示 0。
        switch ($Kind) {
            'recycled'  { $script:Count.recycled++ }
            'permanent' { $script:Count.permanent++ }
            'skip'      { $script:Count.skipped++ }
            'fail'      { $script:Count.failed++ }
        }
        $null = $script:Results.Add([pscustomobject]@{
            Path    = $Target
            Result  = $Kind
            Message = $Message
        })
    }

    # 取回收站删除所需的类型。只做类型引用 + 已编译程序集加载，
    # 不做运行时编译，也不创建 COM 对象。
    function Get-VbFileSystem {
        if ($script:VbFs) { return $script:VbFs }
        $t = $null
        try { $t = [Microsoft.VisualBasic.FileIO.FileSystem] } catch { }
        if (-not $t) {
            try {
                $null = [System.Reflection.Assembly]::LoadWithPartialName('Microsoft.VisualBasic')
                $t = [Microsoft.VisualBasic.FileIO.FileSystem]
            } catch { }
        }
        if ($t) { $script:VbFs = $t }
        return $script:VbFs
    }

    function Test-RecycleAvailable {
        param([string] $FullPath)

        if ($FullPath.StartsWith('\\')) { return $false }   # UNC 路径没有回收站

        $root = [System.IO.Path]::GetPathRoot($FullPath)
        if (-not $root) { return $false }

        $drive = $root.TrimEnd('\')
        $type = 'Unknown'
        try { $type = ([System.IO.DriveInfo]::new($drive)).DriveType.ToString() } catch { return $false }

        # 只认本地固定盘；移动盘/U 盘/NETWORK/CDROM 一律视为不可靠
        if ($type -ne 'Fixed') { return $false }

        $sid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
        $candidates = @(
            "$root`$Recycle.Bin\$sid",
            "$root`$Recycle.Bin"
        )
        foreach ($c in $candidates) {
            if (Test-Path -LiteralPath $c) { return $true }
        }
        return $false
    }

    function Test-ProtectedPath {
        param([string] $FullPath)

        $p = $FullPath.TrimEnd('\')

        if ($p -match '^[A-Za-z]:$') { return $true }              # 盘根 C:\
        if ($p -match '^\\\\[^\\]+\\[^\\]+$') { return $true }     # \\server\share

        $guards = @(
            $env:SystemRoot,
            $env:ProgramFiles,
            ${env:ProgramFiles(x86)},
            $env:ProgramData,
            $env:USERPROFILE,
            $env:LOCALAPPDATA,
            $env:APPDATA,
            "$env:SystemDrive\Users",
            "$env:SystemDrive\Windows"
        ) | Where-Object { $_ } | ForEach-Object { $_.TrimEnd('\') }

        foreach ($g in $guards) {
            if ($p -ieq $g) { return $true }
            # 目标是被保护路径的父级（例如删 C:\Users 会连带端掉所有用户目录）
            if ($g.StartsWith($p + '\', [System.StringComparison]::OrdinalIgnoreCase)) { return $true }
        }
        return $false
    }

    function Resolve-Target {
        param([string] $InputPath)
        if ($InputPath -match '[*?\[]') {
            return @(Get-Item -Path $InputPath -Force -ErrorAction SilentlyContinue |
                     ForEach-Object { $_.FullName })
        }
        $one = Get-Item -LiteralPath $InputPath -Force -ErrorAction SilentlyContinue
        if ($one) { return @($one.FullName) }
        return @()
    }
}

process {
    foreach ($raw in $Path) {

        $targets = Resolve-Target $raw
        if ($targets.Count -eq 0) {
            Add-Result $raw 'skip' '路径不存在'
            continue
        }

        foreach ($full in $targets) {

            if (Test-ProtectedPath $full) {
                Add-Result $full 'skip' '受保护路径（系统目录/用户目录/盘根），拒绝删除'
                continue
            }

            $item = Get-Item -LiteralPath $full -Force -ErrorAction SilentlyContinue
            if (-not $item) {
                Add-Result $full 'skip' '无法读取该路径'
                continue
            }

            $isDir = [bool] $item.PSIsContainer
            if ($isDir -and -not $Recurse) {
                Add-Result $full 'skip' '是目录，需显式加 -Recurse'
                continue
            }

            if ($full.Length -ge 240) {
                Write-Warning "路径长度 $($full.Length) 字符，超过 240 时部分文件 API 会失败"
            }

            if ($Permanent) {
                if (-not $PSCmdlet.ShouldProcess($full, '永久删除')) { continue }
                try {
                    Remove-Item -LiteralPath $full -Recurse:$isDir -Force -ErrorAction Stop
                    Add-Result $full 'permanent' '已永久删除，不可恢复'
                } catch {
                    Add-Result $full 'fail' $_.Exception.GetBaseException().Message
                }
                continue
            }

            # ---- 默认：进回收站 ----
            if (-not (Test-RecycleAvailable $full)) {
                Add-Result $full 'fail' '该位置没有可用回收站（网络盘/移动盘/未启用），需显式加 -Permanent'
                $script:NeedPermanent = $true
                continue
            }

            $vb = Get-VbFileSystem
            if (-not $vb) {
                Add-Result $full 'fail' '回收站通道不可用（程序集加载失败），需显式加 -Permanent'
                $script:NeedPermanent = $true
                continue
            }

            if (-not $PSCmdlet.ShouldProcess($full, '移入回收站')) { continue }

            try {
                if ($isDir) {
                    $vb::DeleteDirectory($full, 'OnlyErrorDialogs', 'SendToRecycleBin')
                } else {
                    $vb::DeleteFile($full, 'OnlyErrorDialogs', 'SendToRecycleBin')
                }
                Add-Result $full 'recycled' '已移入回收站，可从回收站还原'
            } catch {
                Add-Result $full 'fail' $_.Exception.GetBaseException().Message
            }
        }
    }
}

end {
    $done = $script:Count.recycled + $script:Count.permanent
    $total = $done + $script:Count.skipped + $script:Count.failed

    Say ''
    Say ("总计 {0}：进回收站 {1}，永久删除 {2}，跳过 {3}，失败 {4}" -f `
        $total, $script:Count.recycled, $script:Count.permanent, $script:Count.skipped, $script:Count.failed)

    if ($PassThru) {
        $script:Results | ForEach-Object { Write-Output $_ }
    }

    # -WhatIf 只是预览，没有真的删任何东西，不算「没有可删目标」
    if ($PSBoundParameters.ContainsKey('WhatIf')) { exit 0 }

    if ($script:NeedPermanent -and $done -eq 0) { exit 3 }
    if ($script:Count.failed -gt 0) { exit 1 }
    if ($done -eq 0) { exit 2 }
    exit 0
}
