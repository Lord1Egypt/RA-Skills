# 诊断辅助（非门禁）：corpus 锚点 -> kb 覆盖度雷达。
# 运行环境：需 PowerShell 7+（Windows PowerShell 5.1 下崩溃）；从仓库根目录运行。
# 输出解读：missing 高噪——changelog 历史版本/依赖版本未进 kb 不属缺陷，仅作人工排查线索。
$ErrorActionPreference = 'Stop'
$pairs = @{
  'monorepo'      = 'output/full-react-expert/kb/monorepo.md'
  'nestjs'        = 'output/full-react-expert/kb/nestjs.md'
  'nextjs'        = 'output/full-react-expert/kb/nextjs.md'
  'react-admin'   = 'output/full-react-expert/kb/react-admin.md'
  'react-core'    = 'output/full-react-expert/kb/react-core.md'
  'tanstack-query'= 'output/full-react-expert/kb/tanstack-query.md'
  'testing'       = 'output/full-react-expert/kb/testing.md'
  'vite-tooling'  = 'output/full-react-expert/kb/vite-tooling.md'
}
$crossKb = (Get-ChildItem output/full-react-expert/kb -Filter *.md | Get-Content -Raw) -join "`n"

foreach ($sub in $pairs.Keys) {
  $anchorPath = "corpus/react/$sub/docs/_anchors.md"
  if (-not (Test-Path $anchorPath)) { Write-Output "[$sub] no anchors"; continue }
  $raw = Get-Content $anchorPath -Raw
  # 提取 x.y.z 版本号（去重）
  $vers = @{}
  foreach ($m in ([regex]'\b\d+\.\d+\.\d+\b').Matches($raw)) { $vers[$m.Value] = $true }
  # 提取反引号/加粗标记的标识符（特性名）
  $names = @{}
  foreach ($m in ([regex]'`([A-Za-z@/][A-Za-z0-9_@/.\-]{4,40})`').Matches($raw)) {
    $v = $m.Groups[1].Value
    if ($v -match '^https?://' -or $v -match '^\d') { continue }
    $names[$v] = $true
  }
  $kb = Get-Content $pairs[$sub] -Raw
  $missingVers = @($vers.Keys | Where-Object { $kb -notmatch [regex]::Escape($_) -and $crossKb -notmatch [regex]::Escape($_) })
  $missingNames = @($names.Keys | Where-Object { $kb -notmatch [regex]::Escape($_) -and $crossKb -notmatch [regex]::Escape($_) })
  Write-Output "[$sub] versions: $($vers.Count), missing: $($missingVers.Count) [$($missingVers -join ' ')]"
  Write-Output "[$sub] names: $($names.Count), missing: $($missingNames.Count) [$(($missingNames | Select-Object -First 30) -join ' | ')]"
}
