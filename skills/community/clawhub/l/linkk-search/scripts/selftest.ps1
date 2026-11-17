# selftest.ps1 — Windows PowerShell 自检（等价于 scripts/selftest.sh）
# 用法: powershell -ExecutionPolicy Bypass -File selftest.ps1   （默认端口 8888，$env:SXP_PORT 可改）
$ErrorActionPreference = 'Stop'
$port = if ($env:SXP_PORT) { $env:SXP_PORT } else { 8888 }
$base = "http://127.0.0.1:$port"
$fail = 0

Write-Host "== SearXNG 自检 (端口 $port) =="

# 1) 存活
try {
  $r = Invoke-WebRequest -Uri "$base/" -TimeoutSec 5 -UseBasicParsing
  Write-Host "[PASS] 实例存活 (HTTP $($r.StatusCode))"
} catch {
  Write-Host "[FAIL] 实例无响应 → 先确认 Docker Desktop 引擎在跑、容器已启动：docker ps"
  $fail = 1
}

# 2) JSON API + 3) 结果数
try {
  $j = Invoke-WebRequest -Uri "$base/search?q=test&format=json" -TimeoutSec 15 -UseBasicParsing
  $n = ([regex]::Matches($j.Content, '"url"')).Count
  if ($j.Content -match '"query"') {
    Write-Host "[PASS] JSON API 可用"
    if ($n -ge 3) { Write-Host "[PASS] 实测返回 $n 条结果，上游引擎正常" }
    else { Write-Host "[WARN] 仅返回 $n 条 → 见 TROUBLESHOOT 第 1、6 条" }
  } else {
    Write-Host "[FAIL] JSON API 异常 → settings.yml 的 search.formats 缺 json（第 4 条）"
    $fail = 1
  }
} catch {
  Write-Host "[FAIL] JSON 请求出错: $($_.Exception.Message)（第 4 条）"
  $fail = 1
}

Write-Host ""
if ($fail -eq 0) { Write-Host "SELFTEST PASS - 把 http://localhost:$port 填进 OpenClaw" }
else { Write-Host "SELFTEST FAIL - 按上方提示查 docs/TROUBLESHOOT.md"; exit 1 }
