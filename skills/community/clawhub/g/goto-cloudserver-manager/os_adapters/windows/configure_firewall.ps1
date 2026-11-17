# configure_firewall.ps1 - Windows 防火墙配置
# 仅允许内网段访问数据库端口，禁止直接对公网开放

param(
    [int[]]$Ports = @(1433),           # 要开放的端口列表
    [string]$SourceCIDR = "10.0.0.0/8", # 允许的来源 IP 段（仅内网）
    [string]$RulePrefix = "GotoCloudServerManager"
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Output "[$(Get-Date -Format 'HH:mm:ss')] $msg" }

# 安全检查：禁止对 0.0.0.0/0 开放数据库端口
if ($SourceCIDR -eq "0.0.0.0/0" -or $SourceCIDR -eq "Any") {
    Write-Error "安全策略禁止将数据库端口对公网（0.0.0.0/0）开放。请指定内网 CIDR。"
    exit 1
}

Write-Step "配置 Windows 防火墙规则（来源：$SourceCIDR）"

foreach ($port in $Ports) {
    $ruleName = "$RulePrefix-TCP-$port-Inbound"

    # 删除同名旧规则
    Remove-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

    # 创建新规则
    New-NetFirewallRule `
        -DisplayName $ruleName `
        -Direction Inbound `
        -Protocol TCP `
        -LocalPort $port `
        -RemoteAddress $SourceCIDR `
        -Action Allow `
        -Profile Any `
        -Enabled True | Out-Null

    Write-Step "已开放端口 $port（来源：$SourceCIDR）"
}

# 确保 WinRM (5986) 仅对内网开放
$winrmRule = "$RulePrefix-WinRM-5986"
Remove-NetFirewallRule -DisplayName $winrmRule -ErrorAction SilentlyContinue
New-NetFirewallRule `
    -DisplayName $winrmRule `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 5986 `
    -RemoteAddress "10.0.0.0/8" `
    -Action Allow `
    -Profile Any `
    -Enabled True | Out-Null
Write-Step "WinRM 端口 5986 已配置（仅限内网）"

Write-Step "防火墙规则配置完成"
exit 0
