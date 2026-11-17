# 被 upload.ps1 / verify.ps1 点源引用。含中文，必须保存为带 BOM 的 UTF-8（PowerShell 5.1）。
# 真实的 python.exe；跳过 WindowsApps 下的商店别名
$PY    = (Get-Command python.exe -All -EA SilentlyContinue | Where-Object { $_.Source -notlike '*\WindowsApps\*' } | Select-Object -First 1).Source
if (-not $PY) { throw '找不到可用的 python.exe（WindowsApps 下的商店别名不算）' }
$CD2   = Join-Path $PSScriptRoot 'cd2.py'
# CloudDrive 本地缓存目录；与 cd2.py GetSystemSettings 字段 4 不一致时以 API 为准改这里
$CACHE = Join-Path $env:LOCALAPPDATA 'CloudDrive.WinUI\temp'
$XF    = '*.baiduyun.p.downloading', '~$*'
$XD    = '.accelerate'

function Read-Manifest($path) {
  $m = Get-Content -LiteralPath $path -Raw -Encoding UTF8 | ConvertFrom-Json
  $script:LOG = $m.log
  $m
}

function Log($msg) {
  $l = "{0} {1}" -f (Get-Date -Format 'MM-dd HH:mm:ss'), $msg
  Write-Host $l   # 走 Host 而不是管道，免得混进 Test-Files 的返回值
  if ($script:LOG) { Add-Content -LiteralPath $script:LOG -Value $l -Encoding UTF8 }
}

# 把清单里的一项展开成 本地文件 → 云端文件 的列表，排除规则与 robocopy 的 /XF /XD 一致
function Expand-Item($it) {
  switch ($it.type) {
    'dir' {
      Get-ChildItem -LiteralPath $it.src -Recurse -File -Force |
        Where-Object { $_.Name -notlike '*.baiduyun.p.downloading' -and $_.Name -notlike '~$*' -and $_.FullName -notmatch '\\\.accelerate\\' } |
        ForEach-Object { [pscustomobject]@{ Src = $_.FullName; Dst = Join-Path $it.dst $_.FullName.Substring($it.src.TrimEnd('\').Length).TrimStart('\'); Len = $_.Length } }
    }
    'file' {
      $f = Get-Item -LiteralPath $it.src -Force
      [pscustomobject]@{ Src = $f.FullName; Dst = Join-Path $it.dst $f.Name; Len = $f.Length }
    }
    'files' {
      Get-ChildItem -LiteralPath $it.src -File -Force -Filter $it.filter |
        ForEach-Object { [pscustomobject]@{ Src = $_.FullName; Dst = Join-Path $it.dst $_.Name; Len = $_.Length } }
    }
    default { throw "未知的清单项类型: $($it.type)" }
  }
}

function Copy-Item2Z($it) {
  switch ($it.type) {
    'dir'   { robocopy $it.src $it.dst /E /COPY:DAT /DCOPY:T /R:3 /W:10 /NP /NFL /NDL /NJH /NJS /XF $XF /XD $XD | Out-Null }
    'file'  { robocopy (Split-Path $it.src) $it.dst (Split-Path $it.src -Leaf) /COPY:DAT /R:3 /W:10 /NP /NFL /NDL /NJH /NJS | Out-Null }
    'files' { robocopy $it.src $it.dst $it.filter /COPY:DAT /R:3 /W:10 /NP /NFL /NDL /NJH /NJS | Out-Null }
  }
  if ($LASTEXITCODE -ge 8) { Log ("  robocopy 失败 exit={0}: {1}" -f $LASTEXITCODE, $it.src) }
}

function Get-Queue {
  $o = & $PY -I $CD2 GetUploadFileList 0801 2>$null
  $n = $o | Select-String '^1: (\d+)'; $t = $o | Select-String '^4: (\d+)'; $d = $o | Select-String '^5: (\d+)'
  [pscustomobject]@{
    Count = $(if ($n) { [int]$n.Matches.Groups[1].Value } else { 0 })
    Total = $(if ($t) { [double]$t.Matches.Groups[1].Value } else { 0 })
    Done  = $(if ($d) { [double]$d.Matches.Groups[1].Value } else { 0 })
  }
}

function Get-CacheCount { @(Get-ChildItem -LiteralPath $CACHE -File -Force -EA SilentlyContinue).Count }

# 等 CloudDrive 上传队列和本地缓存都清空；每 5 分钟记一次进度
function Wait-Upload($name) {
  $last = Get-Date
  while ($true) {
    $q = Get-Queue; $c = Get-CacheCount
    if ($q.Count -eq 0 -and $c -eq 0) { return }
    if (((Get-Date) - $last).TotalMinutes -ge 5) {
      Log ("  [{0}] 上传中：队列 {1} 个文件，已传 {2:N2}/{3:N2}GB，缓存 {4} 个" -f $name, $q.Count, ($q.Done / 1GB), ($q.Total / 1GB), $c)
      $last = Get-Date
    }
    Start-Sleep 30
  }
}

# 逐文件比对云端是否存在、大小是否一致
function Test-Files($name, $files) {
  $miss = @(); $diff = @()
  foreach ($f in $files) {
    $d = Get-Item -LiteralPath $f.Dst -Force -EA SilentlyContinue
    if (-not $d) { $miss += $f.Dst } elseif ($d.Length -ne $f.Len) { $diff += "$($f.Dst) 本地=$($f.Len) 云端=$($d.Length)" }
  }
  Log ("[{0}] 校验：{1} 个文件 {2:N2}GB，缺失 {3}，大小不一致 {4}" -f $name, $files.Count, (($files | Measure-Object Len -Sum).Sum / 1GB), $miss.Count, $diff.Count)
  $miss | Select-Object -First 20 | ForEach-Object { Log "  缺失 $_" }
  $diff | Select-Object -First 20 | ForEach-Object { Log "  不一致 $_" }
  [pscustomobject]@{ Missing = $miss.Count; Different = $diff.Count }
}
