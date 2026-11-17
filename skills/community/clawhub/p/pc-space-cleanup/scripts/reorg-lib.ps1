# 云端整理用的函数，点源引用前由调用方设置 $R（云盘根，如 'Z:\123云盘'）和 $LOG。
# 含中文，必须保存为带 BOM 的 UTF-8。函数名别用 Dir —— 别名 dir 优先于函数。
$script:ReorgOk = 0; $script:ReorgFail = 0; $script:ReorgRenamed = 0

function RLog($m) { $l = "{0} {1}" -f (Get-Date -Format 'HH:mm:ss'), $m; Write-Host $l; if ($LOG) { Add-Content -LiteralPath $LOG -Value $l -Encoding UTF8 } }
function MkD($p) { New-Item -ItemType Directory -Force -Path "$R\$p" | Out-Null }

# 把 $src（相对 $R）移进目录 $dstDir（相对 $R），同名时加 _2/_3 后缀，不覆盖
function Into($src, $dstDir) {
  $s = "$R\$src"
  if (-not (Test-Path -LiteralPath $s)) { RLog "  跳过（源不存在）: $src"; return }
  MkD $dstDir
  $item = Get-Item -LiteralPath $s -Force
  $name = $item.Name; $target = "$R\$dstDir\$name"; $i = 2
  while (Test-Path -LiteralPath $target) {
    $base = if ($item.PSIsContainer) { $item.Name } else { [IO.Path]::GetFileNameWithoutExtension($item.Name) }
    $ext  = if ($item.PSIsContainer) { '' } else { $item.Extension }
    $name = "${base}_$i$ext"; $target = "$R\$dstDir\$name"; $i++
  }
  try {
    Move-Item -LiteralPath $s -Destination $target -EA Stop
    $script:ReorgOk++
    if ($name -ne $item.Name) { $script:ReorgRenamed++; RLog "  重名改为 $name : $src → $dstDir" } else { RLog "  OK  $src → $dstDir\" }
  } catch { $script:ReorgFail++; RLog "  失败 $src → $dstDir : $($_.Exception.Message)" }
}

# 把文件夹 $src 的子项全部并入 $dstDir；搬空后原目录移进 _待删除
function Merge($src, $dstDir) {
  if (-not (Test-Path -LiteralPath "$R\$src")) { RLog "  跳过（源不存在）: $src"; return }
  Get-ChildItem -LiteralPath "$R\$src" -Force | ForEach-Object { Into "$src\$($_.Name)" $dstDir }
  if (-not (Get-ChildItem -LiteralPath "$R\$src" -Force)) { Into $src '_待删除' } else { RLog "  注意：$src 未搬空，保留原处" }
}

function Summary { RLog ("===== 成功 {0}，失败 {1}，重名改名 {2} =====" -f $script:ReorgOk, $script:ReorgFail, $script:ReorgRenamed) }
