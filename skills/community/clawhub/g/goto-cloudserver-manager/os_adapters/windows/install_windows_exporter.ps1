# install_windows_exporter.ps1 - 安装 Windows Exporter（Prometheus 监控代理）
# 版本：windows_exporter 0.24.0

param(
    [string]$Version = "0.24.0",
    [int]$Port = 9182,
    [string]$Collectors = "cpu,cs,logical_disk,memory,net,os,service,system,tcp"
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Output "[$(Get-Date -Format 'HH:mm:ss')] $msg" }

# 检查是否已安装
$existing = Get-Service -Name "windows_exporter" -ErrorAction SilentlyContinue
if ($existing) {
    Write-Step "windows_exporter 已安装（状态：$($existing.Status)），跳过"
    exit 0
}

Write-Step "下载 windows_exporter v$Version..."
$downloadUrl = "https://github.com/prometheus-community/windows_exporter/releases/download/v${Version}/windows_exporter-${Version}-amd64.msi"
$msiPath = "$env:TEMP\windows_exporter.msi"

Invoke-WebRequest -Uri $downloadUrl -OutFile $msiPath -UseBasicParsing

Write-Step "静默安装 windows_exporter..."
$proc = Start-Process msiexec.exe `
    -ArgumentList "/i `"$msiPath`" /quiet ENABLED_COLLECTORS=$Collectors LISTEN_PORT=$Port" `
    -Wait -PassThru -NoNewWindow

if ($proc.ExitCode -ne 0) {
    Write-Error "windows_exporter 安装失败，退出码：$($proc.ExitCode)"
    exit $proc.ExitCode
}

# 配置防火墙（仅内网监控系统访问）
New-NetFirewallRule `
    -DisplayName "GotoCloudServerManager-WindowsExporter-$Port" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort $Port `
    -RemoteAddress "10.0.0.0/8" `
    -Action Allow -Enabled True -ErrorAction SilentlyContinue | Out-Null

# 验证服务
$svc = Get-Service -Name "windows_exporter" -ErrorAction SilentlyContinue
if ($svc -and $svc.Status -eq "Running") {
    Write-Step "windows_exporter 安装成功，监听端口 $Port"
} else {
    Write-Error "windows_exporter 服务未正常运行"
    exit 1
}

Remove-Item $msiPath -Force -ErrorAction SilentlyContinue
Write-Step "Windows Exporter 安装完成"
exit 0
