# databases/sqlserver/install.ps1 - SQL Server 数据库层安装入口
# 委托给 os_adapters/windows/install_sqlserver.ps1，此处添加数据库特定配置

param(
    [string]$Edition = "developer",
    [string]$SAPassword = "",
    [string]$DataPath = "C:\SQLData",
    [string]$LogPath = "C:\SQLLogs",
    [string]$BackupPath = "C:\SQLBackup"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$installScript = Join-Path $scriptDir "..\..\os_adapters\windows\install_sqlserver.ps1"

& $installScript `
    -Edition $Edition `
    -SAPassword $SAPassword `
    -DataPath $DataPath `
    -LogPath $LogPath `
    -BackupPath $BackupPath

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# 安装后配置：启用 TCP/IP，设置默认端口
Write-Output "配置 SQL Server TCP/IP..."
$wmiSvc = "ManagedComputer"
try {
    [reflection.assembly]::LoadWithPartialName("Microsoft.SqlServer.SqlWmiManagement") | Out-Null
    $mc = New-Object Microsoft.SqlServer.Management.Smo.Wmi.ManagedComputer
    $tcpProto = $mc.ServerInstances["MSSQLSERVER"].ServerProtocols["Tcp"]
    $tcpProto.IsEnabled = $true
    $tcpProto.Alter()
    $ipAll = $tcpProto.IPAddresses["IPAll"]
    $ipAll.IPAddressProperties["TcpDynamicPorts"].Value = ""
    $ipAll.IPAddressProperties["TcpPort"].Value = "1433"
    $tcpProto.Alter()
    Restart-Service MSSQLSERVER -Force
    Write-Output "SQL Server TCP/IP 已启用，端口：1433"
} catch {
    Write-Warning "TCP/IP 配置跳过（可能需要重启后手动确认）：$_"
}

exit 0
