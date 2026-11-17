# 按 JSON 清单分批：拷入 Z:（进 CloudDrive 缓存）→ 等队列和缓存清空 → 等 60s → 逐文件校验
param([Parameter(Mandatory = $true)][string]$Manifest)
. (Join-Path $PSScriptRoot 'common.ps1')
if (-not $env:CD2_TOKEN) { throw '先设置 $env:CD2_TOKEN（CloudDrive API 令牌，找用户要）' }

$m = Read-Manifest $Manifest
Log ("===== 上传开始，清单 {0}，C 盘剩余 {1:N2}GB =====" -f $Manifest, ((Get-PSDrive C).Free / 1GB))
foreach ($b in $m.batches) {
  $files = @(foreach ($it in $b.items) { Expand-Item $it })
  Log ("[{0}] 拷入缓存：{1} 个文件，{2:N2}GB" -f $b.name, $files.Count, (($files | Measure-Object Len -Sum).Sum / 1GB))
  $sw = [Diagnostics.Stopwatch]::StartNew()
  foreach ($it in $b.items) { Copy-Item2Z $it }
  Log ("[{0}] 已进缓存，用时 {1:N0}s，C 盘剩余 {2:N2}GB；等待上传完成" -f $b.name, $sw.Elapsed.TotalSeconds, ((Get-PSDrive C).Free / 1GB))
  Wait-Upload $b.name
  Log ("[{0}] 队列与缓存已清空，用时 {1:N1} 分钟；等 60s 让云端目录列表刷新" -f $b.name, $sw.Elapsed.TotalMinutes)
  Start-Sleep 60
  [void](Test-Files $b.name $files)
}
Log ("===== 上传结束，C 盘剩余 {0:N2}GB =====" -f ((Get-PSDrive C).Free / 1GB))
