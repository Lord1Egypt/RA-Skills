#Requires -Version 5.1
<#
.SYNOPSIS
    Windows Terminal / VSCode 配置的「文本级」修改工具（dot-source 用，只定义函数，不执行任何动作）。
.DESCRIPTION
    为什么不用 ConvertFrom-Json -> ConvertTo-Json：
      1. WT 的 settings.json 是 JSONC，默认带 // 注释，ConvertFrom-Json 遇到注释直接抛错；
      2. 即使能解析，走一圈改写也会把用户的注释、空行、字段顺序全部抹掉。
    所以这里只做定点替换/插入；解析只用于「改完之后自检」。
.NOTES
    所有函数都不写系统设置，只动传入的那个文件，便于回归测试。
#>

function ConvertFrom-Jsonc {
    <#
    .SYNOPSIS
        把 JSONC（带 // 与 /* */ 注释、尾逗号）转成对象。仅用于自检。
    #>
    [CmdletBinding()]
    param([Parameter(Mandatory)][AllowEmptyString()][string]$Text)

    $sb = New-Object System.Text.StringBuilder ($Text.Length + 16)
    $inStr = $false; $esc = $false; $i = 0; $n = $Text.Length
    while ($i -lt $n) {
        $ch = $Text[$i]
        $nx = if ($i + 1 -lt $n) { $Text[$i + 1] } else { [char]0 }
        if ($inStr) {
            [void]$sb.Append($ch)
            if ($esc) { $esc = $false }
            elseif ($ch -eq '\') { $esc = $true }
            elseif ($ch -eq '"') { $inStr = $false }
            $i++
            continue
        }
        if ($ch -eq '"') { $inStr = $true; [void]$sb.Append($ch); $i++; continue }
        if ($ch -eq '/' -and $nx -eq '/') {
            while ($i -lt $n -and $Text[$i] -ne "`n") { $i++ }
            continue
        }
        if ($ch -eq '/' -and $nx -eq '*') {
            $i += 2
            while ($i + 1 -lt $n -and -not ($Text[$i] -eq '*' -and $Text[$i + 1] -eq '/')) { $i++ }
            $i += 2
            continue
        }
        [void]$sb.Append($ch)
        $i++
    }

    $clean = $sb.ToString().TrimStart([char]0xFEFF)
    $clean = [regex]::Replace($clean, ',(\s*[\]\}])', '$1')
    return ($clean | ConvertFrom-Json)
}

function Get-JsonStringEscaped {
    <# 转义成可以塞进 JSON 双引号字符串里的文本（路径里的反斜杠） #>
    param([string]$Value)
    if ([string]::IsNullOrEmpty($Value)) { return '' }
    $s = $Value -replace '\\', '\\'
    $s = $s -replace '"', '\"'
    return $s
}

function Find-JsonObjectEnd {
    <# 从 $OpenBraceIndex 处的 '{' 开始，返回配对 '}' 的下标；找不到返回 -1 #>
    param([string]$Text, [int]$OpenBraceIndex)
    $depth = 0; $inStr = $false; $esc = $false
    for ($i = $OpenBraceIndex; $i -lt $Text.Length; $i++) {
        $ch = $Text[$i]
        if ($inStr) {
            if ($esc) { $esc = $false }
            elseif ($ch -eq '\') { $esc = $true }
            elseif ($ch -eq '"') { $inStr = $false }
            continue
        }
        if ($ch -eq '"') { $inStr = $true; continue }
        if ($ch -eq '{') { $depth++ }
        elseif ($ch -eq '}') { $depth--; if ($depth -eq 0) { return $i } }
    }
    return -1
}

function New-ConfigBackup {
    <#
    .SYNOPSIS
        把配置文件复制成 <文件名>.ps7bak，已存在则不覆盖（永远保留最早那份原样）。
    .DESCRIPTION
        即使本次无需修改也会调用，保证任何被本工具碰过的配置文件都留有还原点。
        备份失败（目录只读等）不抛错、返回 $null，不能因为备份不成而让只读路径变成失败。
    #>
    param([Parameter(Mandatory)][string]$Path, [switch]$NoBackup)
    if ($NoBackup) { return $null }
    $bak = $Path + '.ps7bak'
    if (Test-Path -LiteralPath $bak) { return $bak }
    try {
        Copy-Item -LiteralPath $Path -Destination $bak -Force -ErrorAction Stop
        return $bak
    } catch { return $null }
}

function Write-FileKeepingBom {
    <#
    .SYNOPSIS
        按原文件的 BOM 状态写回（原来有 BOM 就保留，没有就不加）。
    .DESCRIPTION
        File.ReadAllText 读的时候会把 BOM 吃掉，如果写回时固定用 UTF8Encoding($false)，
        本来带 BOM 的文件就会被顺手改掉编码——用户只要求改一个字段，不该动这个。
    #>
    param([Parameter(Mandatory)][string]$Path, [Parameter(Mandatory)][AllowEmptyString()][string]$Text)
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $hasBom = ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)
    $enc = New-Object System.Text.UTF8Encoding($hasBom)
    [System.IO.File]::WriteAllText($Path, $Text, $enc)
}

function Update-WtSettings {
    <#
    .SYNOPSIS
        在 Windows Terminal 的 settings.json 里加一条 PowerShell 7 profile，并设为默认。
    .DESCRIPTION
        只做两处定点修改，不重写整个文件：
          1. 若 profiles.list 里没有 name = "PowerShell 7" 的条目，就地插入一条；
          2. 把 defaultProfile 指到那条的 GUID。
        备份成 <文件名>.ps7bak（已存在则不覆盖，保留最初的原样）；即使本次无需修改也会备份，
        这样任何被本工具碰过的配置文件都留有一个「还没被改过」的还原点；
        改写后用 ConvertFrom-Jsonc 自检，解析不了就不落盘（抛错，由调用方决定怎么提示）。
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$PwshPath,
        [string]$Guid = '{9e1b2a44-7c3d-4f8e-b5a1-2d6c9f0e3b71}',
        [switch]$NoBackup
    )

    if (-not (Test-Path -LiteralPath $Path)) { throw "配置文件不存在: $Path" }
    $orig = [System.IO.File]::ReadAllText($Path)
    $text = $orig
    $esc = Get-JsonStringEscaped $PwshPath

    $addedProfile = $false
    $setDefault = $false

    # ---- 1. profiles.list 里补一条 ----
    if ($text -notmatch '"name"\s*:\s*"PowerShell 7"') {
        $m = [regex]::Match($text, '"list"\s*:\s*\[')
        if ($m.Success) {
            $pos = $m.Index + $m.Length
            $rest = $text.Substring($pos)
            $snippet = '{ "commandline": "' + $esc + '", "guid": "' + $Guid + '", "hidden": false, "name": "PowerShell 7", "icon": "ms-appx:///ProfileIcons/pwsh.png" }'
            if ($rest.TrimStart() -match '^\]') {
                # 空列表：不能带尾逗号，否则严格 JSON 解析会挂
                $ins = "`r`n            " + $snippet + "`r`n        "
            } else {
                $ins = "`r`n            " + $snippet + ","
            }
            $text = $text.Substring(0, $pos) + $ins + $rest
            $addedProfile = $true
        }
    }

    # ---- 2. defaultProfile 指过去 ----
    $line = '"defaultProfile": "' + $Guid + '"'
    $m2 = [regex]::Match($text, '"defaultProfile"\s*:\s*"[^"]*"')
    if ($m2.Success) {
        if ($m2.Value.IndexOf($Guid, [StringComparison]::OrdinalIgnoreCase) -lt 0) {
            $text = $text.Substring(0, $m2.Index) + $line + $text.Substring($m2.Index + $m2.Length)
            $setDefault = $true
        }
    } else {
        $mb = [regex]::Match($text, '\{')
        if ($mb.Success) {
            $p = $mb.Index + $mb.Length
            $text = $text.Substring(0, $p) + "`r`n    " + $line + ',' + $text.Substring($p)
            $setDefault = $true
        }
    }

    $result = [pscustomobject]@{
        Changed           = $false
        AddedProfile      = $addedProfile
        SetDefaultProfile = $setDefault
        Backup            = $null
    }
    if ($text -eq $orig) {
        # 无需修改时也留一份最初的还原点：否则一旦哪天要改，备份下来的已经是
        # 「被更早版本重写过」的样子，原始文件再也找不回来。只复制、不写原文件。
        $result.Backup = New-ConfigBackup -Path $Path -NoBackup:$NoBackup
        return $result
    }

    # ---- 3. 自检 -> 备份 -> 落盘（不写 BOM，WT 自己也不写）----
    $null = ConvertFrom-Jsonc -Text $text

    $bak = New-ConfigBackup -Path $Path -NoBackup:$NoBackup
    Write-FileKeepingBom -Path $Path -Text $text

    $result.Changed = $true
    $result.Backup = $bak
    return $result
}

function Update-VsCodeSettings {
    <#
    .SYNOPSIS
        在 VSCode 的 settings.json 里把默认终端指到 PowerShell 7。
    .DESCRIPTION
        VSCode 的 settings.json 同样是 JSONC（几乎人人都有注释），所以同样只做定点修改：
          - terminal.integrated.defaultProfile.windows 改成 "PowerShell 7"；
          - terminal.integrated.profiles.windows 里只加/改 "PowerShell 7" 这一条，
            用户自己配的别的 profile（比如 Ubuntu/WSL）原样保留。
        以前是整对象替换，等于把用户自建的 profile 全删了。
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$PwshPath,
        [switch]$NoBackup
    )

    if (-not (Test-Path -LiteralPath $Path)) { throw "配置文件不存在: $Path" }
    $orig = [System.IO.File]::ReadAllText($Path)
    $text = $orig
    $esc = Get-JsonStringEscaped $PwshPath

    # ---- 1. defaultProfile.windows ----
    $dpName = 'terminal.integrated.defaultProfile.windows'
    $dpLine = '"' + $dpName + '": "PowerShell 7"'
    $m = [regex]::Match($text, '"' + [regex]::Escape($dpName) + '"\s*:\s*"([^"]*)"')
    if ($m.Success) {
        # 值已经就是 PowerShell 7 就别动（否则只因为空格差异也会把文件重写一遍）
        if ($m.Groups[1].Value -ne 'PowerShell 7') {
            $text = $text.Substring(0, $m.Index) + $dpLine + $text.Substring($m.Index + $m.Length)
        }
    } else {
        $mb = [regex]::Match($text, '\{')
        if ($mb.Success) {
            $p = $mb.Index + $mb.Length
            $text = $text.Substring(0, $p) + "`r`n    " + $dpLine + ',' + $text.Substring($p)
        }
    }

    # ---- 2. profiles.windows 里的 "PowerShell 7" 条目 ----
    $pwName = 'terminal.integrated.profiles.windows'
    $entryLine = '"PowerShell 7": { "path": "' + $esc + '", "icon": "terminal-powershell" }'
    $mo = [regex]::Match($text, '"' + [regex]::Escape($pwName) + '"\s*:\s*\{')
    if ($mo.Success) {
        $open = $mo.Index + $mo.Length - 1
        $close = Find-JsonObjectEnd -Text $text -OpenBraceIndex $open
        if ($close -gt $open) {
            $inner = $text.Substring($open + 1, $close - $open - 1)
            $me = [regex]::Match($inner, '"PowerShell 7"\s*:\s*\{')
            if ($me.Success) {
                $eo = $open + 1 + $me.Index + $me.Length - 1
                $ec = Find-JsonObjectEnd -Text $text -OpenBraceIndex $eo
                if ($ec -gt $eo) {
                    # 只改这一条里的 path 值（保留用户自己的排版与其它字段，比如 args/env）
                    $cur = $text.Substring($eo, $ec - $eo + 1)
                    $mp = [regex]::Match($cur, '"path"\s*:\s*"([^"]*)"')
                    if ($mp.Success) {
                        # 值已经对了就别写（否则只因为空格差异也会把文件重写一遍）
                        if ($mp.Groups[1].Value -ne $esc) {
                            $newVal = '"path": "' + $esc + '"'
                            $cur = $cur.Substring(0, $mp.Index) + $newVal + $cur.Substring($mp.Index + $mp.Length)
                        }
                    } else {
                        $cur = $entryLine.Substring($entryLine.IndexOf('{'))
                    }
                    $text = $text.Substring(0, $eo) + $cur + $text.Substring($ec + 1)
                }
            } else {
                if ($inner.Trim().Length -eq 0) {
                    $ins = "`r`n        " + $entryLine + "`r`n    "
                } else {
                    $ins = "`r`n        " + $entryLine + ','
                }
                $text = $text.Substring(0, $open + 1) + $ins + $text.Substring($open + 1)
            }
        }
    } else {
        $mb = [regex]::Match($text, '\{')
        if ($mb.Success) {
            $p = $mb.Index + $mb.Length
            $line = '"' + $pwName + '": { ' + $entryLine + ' },'
            $text = $text.Substring(0, $p) + "`r`n    " + $line + $text.Substring($p)
        }
    }

    $result = [pscustomobject]@{ Changed = $false; Backup = $null }
    if ($text -eq $orig) {
        # 同 Update-WtSettings：无需修改也留一份最初的还原点
        $result.Backup = New-ConfigBackup -Path $Path -NoBackup:$NoBackup
        return $result
    }

    $null = ConvertFrom-Jsonc -Text $text

    $bak = New-ConfigBackup -Path $Path -NoBackup:$NoBackup
    Write-FileKeepingBom -Path $Path -Text $text

    $result.Changed = $true
    $result.Backup = $bak
    return $result
}
