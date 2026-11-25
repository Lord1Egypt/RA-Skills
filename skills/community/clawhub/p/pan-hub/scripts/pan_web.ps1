# pan_web.ps1 — Windows 一键「网页下载助手」：启动本机 serve + 全局剪贴板监听 + 打开 Web UI
# 用法：powershell -ExecutionPolicy Bypass -File scripts\pan_web.ps1 [port]
$ErrorActionPreference = "SilentlyContinue"
param([int]$Port = 17890)

$root = Split-Path -Parent $PSScriptRoot
$py = $null
foreach ($cmd in @("py.exe", "python.exe", "python3.exe")) {
    $res = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($res) { $py = $cmd; break }
}
if (-not $py) {
    Write-Host "[pan_web] 未找到 Python 3；请先安装 Python 并勾选 Add python.exe to PATH" -ForegroundColor Red
    exit 127
}

$status = "http://127.0.0.1:$Port/api/status"
if (-not (Test-Path "$root\scripts\pan.py")) {
    Write-Host "[pan_web] 找不到 scripts\pan.py" -ForegroundColor Red
    exit 2
}

# 常驻下载服务（后台）
$serveUp = $false
try { $null = Invoke-WebRequest -Uri $status -UseBasicParsing -TimeoutSec 2; $serveUp = $true } catch {}
if (-not $serveUp) {
    Write-Host "[pan_web] 启动本机下载服务 :$Port"
    Start-Process -WindowStyle Hidden -FilePath $py -ArgumentList "$root\scripts\pan.py","serve","--port","$Port" -RedirectStandardOutput (Join-Path $env:TEMP "pan_web_serve.log") -RedirectStandardError (Join-Path $env:TEMP "pan_web_serve.err.log")
    Start-Sleep -Seconds 1
}

# 剪贴板监听（后台，自动把当前/后续剪贴板里的链接投递）
Write-Host "[pan_web] 启动全局剪贴板监听（可在操作中心里结束）"
Start-Process -WindowStyle Hidden -FilePath $py -ArgumentList "$root\scripts\clipboard_monitor.py","--port","$Port","--once"
Start-Process -WindowStyle Hidden -FilePath $py -ArgumentList "$root\scripts\clipboard_monitor.py","--port","$Port","--interval","2"

# 打开网页
$url = "http://127.0.0.1:$Port/"
try { Start-Process $url } catch {}
Write-Host "[pan_web] Web 首页：$url" -ForegroundColor Green
Write-Host "[pan_web] 实时进度：http://127.0.0.1:$Port/live" -ForegroundColor Cyan
Write-Host "[pan_web] 提示：关闭本窗口不影响后台下载服务；停止服务请关闭 python 进程。"
exit 0
