# 只校验不上传：中断后、换网回来后、或删本地前再确认一遍
param([Parameter(Mandatory = $true)][string]$Manifest)
. (Join-Path $PSScriptRoot 'common.ps1')

$m = Read-Manifest $Manifest
if ($env:CD2_TOKEN) {
  $q = Get-Queue; $c = Get-CacheCount
  if ($q.Count -gt 0 -or $c -gt 0) { Log ("注意：CloudDrive 还有 {0} 个文件在队列、缓存 {1} 个，校验结果里的缺失可能只是还没传完" -f $q.Count, $c) }
} else {
  Log '注意：没设 $env:CD2_TOKEN，无法确认上传队列是否已清空'
}
$bad = 0
foreach ($b in $m.batches) {
  $files = @(foreach ($it in $b.items) { Expand-Item $it })
  $r = Test-Files $b.name $files
  $bad += $r.Missing + $r.Different
}
Log ("===== 校验结束：问题文件共 {0} 个 =====" -f $bad)
