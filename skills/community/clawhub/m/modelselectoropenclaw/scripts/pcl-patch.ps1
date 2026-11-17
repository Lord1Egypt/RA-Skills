# PCL Model Picker — OpenClaw Control UI 增强补丁（幂等）
# 把「左列供应商导航 + 右列该供应商模型」的双列选择器注入 OpenClaw Control UI，
# 并隐藏菜单内官方「此聊天使用的账户」账号控件。
# 重复运行安全；OpenClaw 升级覆盖安装目录后重新运行一次即可恢复。
# 适用于 Windows PowerShell 5.1+ / PowerShell 7+。
#
# 用法：
#   powershell -ExecutionPolicy Bypass -File pcl-patch.ps1                # 安装/修复
#   powershell -ExecutionPolicy Bypass -File pcl-patch.ps1 -Remove        # 卸载
#   powershell -ExecutionPolicy Bypass -File pcl-patch.ps1 -Dist "<...>\dist\control-ui"
#
# 修改范围（就这两处，其余一切不动）：
#   1) dist\control-ui\index.html           —— 末尾追加/替换一行 <script> 标签（首次运行自动备份 .bak-pcl）
#   2) dist\control-ui\assets\pcl-model-picker.v*.js —— 新增增强脚本，清理时保留最近两版

param(
    [switch]$Remove,
    [string]$Dist = ''
)

$ErrorActionPreference = 'Stop'
$srcDir = Split-Path -Parent $MyInvocation.MyCommand.Path
# 自动选用版本号最大的增强脚本，以后升级脚本无需改这里
$jsFile = Get-ChildItem $srcDir -Filter 'pcl-model-picker.v*.js' -ErrorAction SilentlyContinue |
    Sort-Object { [int]([regex]::Match($_.Name, 'v(\d+)\.js$').Groups[1].Value) } -Descending |
    Select-Object -First 1
if (-not $jsFile) { throw "缺少增强脚本 pcl-model-picker.v*.js（应与 pcl-patch.ps1 同目录）" }
$jsName = $jsFile.Name
$marker = 'pcl-model-picker'
# 兼容任意历史版本号（以及带/不带内容指纹）的注入标签，升级脚本时自动原位替换
$tagPattern = '<script defer src="\./assets/pcl-model-picker\.v\d+\.js(\?h=[0-9a-f]{8})?"></script><!-- pcl-model-picker -->'

function Find-ControlUiDir {
    param([string]$Explicit)
    if ($Explicit) {
        if (Test-Path (Join-Path $Explicit 'index.html')) { return $Explicit }
        throw "指定的 -Dist 下没有 index.html: $Explicit"
    }
    $candidates = New-Object System.Collections.Generic.List[string]
    # 1) npm 全局 root（覆盖任意 npm prefix）
    try {
        $npmRoot = (& npm root -g 2>$null)
        if ($npmRoot) { $candidates.Add((Join-Path $npmRoot 'openclaw\dist\control-ui')) }
    } catch {}
    # 2) 常见 npm 全局前缀
    $candidates.Add('C:\npm-global\node_modules\openclaw\dist\control-ui')
    if ($env:APPDATA) { $candidates.Add((Join-Path $env:APPDATA 'npm\node_modules\openclaw\dist\control-ui')) }
    $candidates.Add('/usr/local/lib/node_modules/openclaw/dist/control-ui')
    $candidates.Add('/usr/lib/node_modules/openclaw/dist/control-ui')
    # 3) 从 PATH 里的 openclaw CLI 反推安装目录
    try {
        $cmd = Get-Command openclaw -ErrorAction SilentlyContinue
        if ($cmd -and $cmd.Source) {
            $dir = Split-Path -Parent $cmd.Source
            for ($i = 0; $i -lt 6 -and $dir; $i++) {
                $candidates.Add((Join-Path $dir 'node_modules\openclaw\dist\control-ui'))
                $dir = Split-Path -Parent $dir
            }
        }
    } catch {}
    foreach ($c in $candidates) {
        if ($c -and (Test-Path (Join-Path $c 'index.html'))) { return $c }
    }
    throw "未找到 OpenClaw Control UI 目录。请显式指定：-Dist '<npm全局目录>\node_modules\openclaw\dist\control-ui'"
}

$dist   = Find-ControlUiDir $Dist
$index  = Join-Path $dist 'index.html'
$assetDst = Join-Path $dist "assets\$jsName"
Write-Host "[PCL] Control UI 目录: $dist"

if ($Remove) {
    $html = [System.IO.File]::ReadAllText($index)
    if ($html -match $tagPattern) {
        $html = [regex]::Replace($html, $tagPattern, '')
        [System.IO.File]::WriteAllText($index, $html, (New-Object System.Text.UTF8Encoding($false)))
        Write-Host '[PCL] 已从 index.html 移除注入标签'
    } else {
        Write-Host '[PCL] index.html 中没有补丁标记，无需移除'
    }
    Get-ChildItem (Join-Path $dist 'assets') -Filter 'pcl-model-picker.v*.js' -ErrorAction SilentlyContinue |
        Remove-Item -Force
    Write-Host '[PCL] 已清理 assets 中的增强脚本'
    exit 0
}

if (-not (Test-Path (Join-Path $srcDir $jsName))) { throw "缺少增强脚本 $jsName（应与 pcl-patch.ps1 同目录）" }

# 内容指纹：Control UI 的 Service Worker 对 /assets/ 是 cache-first、HTTP 缓存 immutable，
# 同名改内容会被旧缓存永久钉死（v4 就是这样静默失效的）。把内容哈希放进 URL 查询串后，
# 内容一变缓存键就变，浏览器立即取到新脚本，不必再靠人工升文件名。
$fingerprint = (Get-FileHash (Join-Path $srcDir $jsName) -Algorithm SHA256).Hash.Substring(0, 8).ToLower()
$tag = '<script defer src="./assets/' + $jsName + '?h=' + $fingerprint + '"></script><!-- ' + $marker + ' -->'

# 1) 拷贝增强脚本到 assets（带版本号文件名：Control UI 的 Service Worker 对 /assets/ 是
#    cache-first，内容变更必须换新文件名，否则浏览器永远吃旧缓存）
Copy-Item (Join-Path $srcDir $jsName) $assetDst -Force
Write-Host "[PCL] 脚本已复制 -> $assetDst"

# 2) 注入 index.html（首次运行先备份；已有旧版本标签则原位替换）
$html = [System.IO.File]::ReadAllText($index)
$bak = Join-Path $dist 'index.html.bak-pcl'
if (-not (Test-Path $bak)) {
    [System.IO.File]::WriteAllText($bak, $html, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host "[PCL] 已备份原始 index.html -> $bak"
}
if ($html -match $tagPattern) {
    if ($html.Contains($tag)) {
        Write-Host '[PCL] index.html 已是当前版本，跳过注入'
    } else {
        $html = [regex]::Replace($html, $tagPattern, $tag)
        [System.IO.File]::WriteAllText($index, $html, (New-Object System.Text.UTF8Encoding($false)))
        Write-Host '[PCL] 已替换为当前版本的注入标签'
    }
} else {
    if ($html -match '</body>') {
        $html = $html -replace '</body>', "  $tag`r`n</body>"
    } else {
        $html = $html + "`r`n$tag"
    }
    [System.IO.File]::WriteAllText($index, $html, (New-Object System.Text.UTF8Encoding($false)))
    Write-Host '[PCL] 已注入 index.html'
}

# 3) 清理 assets 中的历史版本脚本：保留最近两版（当前 + 上一版），
#    防止浏览器缓存着旧 HTML 时请求已被删除的旧脚本而 404（布局退回默认）。
Get-ChildItem (Join-Path $dist 'assets') -Filter 'pcl-model-picker.v*.js' |
    ForEach-Object {
        $ver = [int]([regex]::Match($_.Name, 'v(\d+)\.js$').Groups[1].Value)
        [pscustomobject]@{ File = $_; Ver = $ver }
    } |
    Sort-Object Ver -Descending |
    Select-Object -Skip 2 |
    ForEach-Object { Remove-Item $_.File.FullName -Force }

Write-Host '[PCL] 完成。浏览器 Ctrl+F5 强制刷新 Control UI 即可生效。'
