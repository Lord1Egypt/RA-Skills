# configure_winrm.ps1 - 启用并配置 WinRM（HTTPS），用于云助手首次推送初始化备用通道
param(
    [int]$Port = 5986,
    [string]$CertThumbprint = ""
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Output "[$(Get-Date -Format 'HH:mm:ss')] $msg" }

Write-Step "启用 WinRM 服务..."
Enable-PSRemoting -Force -SkipNetworkProfileCheck | Out-Null

if (-not $CertThumbprint) {
    Write-Step "未指定证书，生成自签名证书..."
    $cert = New-SelfSignedCertificate -DnsName $env:COMPUTERNAME -CertStoreLocation Cert:\LocalMachine\My
    $CertThumbprint = $cert.Thumbprint
}

Write-Step "清理同端口旧 HTTPS Listener..."
Get-ChildItem WSMan:\localhost\Listener |
    Where-Object { $_.Keys -match "Transport=HTTPS" } |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Step "创建 HTTPS Listener（端口 $Port）..."
New-Item -Path WSMan:\localhost\Listener -Transport HTTPS -Address * `
    -CertificateThumbPrint $CertThumbprint -Port $Port -Force | Out-Null

winrm set winrm/config/service/auth '@{Basic="true"}' | Out-Null
winrm set winrm/config/service '@{AllowUnencrypted="false"}' | Out-Null

Write-Step "配置防火墙规则（仅内网可访问 WinRM HTTPS 端口）..."
Remove-NetFirewallRule -DisplayName "GotoCloudServerManager-WinRM-HTTPS" -ErrorAction SilentlyContinue
New-NetFirewallRule `
    -DisplayName "GotoCloudServerManager-WinRM-HTTPS" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort $Port `
    -RemoteAddress "10.0.0.0/8" `
    -Action Allow `
    -Profile Any `
    -Enabled True | Out-Null

Write-Step "WinRM 配置完成（端口：$Port，证书指纹：$CertThumbprint）"
exit 0
