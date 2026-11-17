# install_sqlserver.ps1 - SQL Server 2022 静默安装
# 参数：
#   -Edition    developer (默认) / standard / enterprise
#   -SAPassword  SA 账号密码（若为空则使用 Windows 集成验证）
#   -InstallPath 安装路径（默认 C:\Program Files\Microsoft SQL Server）
#   -DataPath    数据文件路径（默认 C:\SQLData）

param(
    [string]$Edition = "developer",
    [string]$SAPassword = "",
    [string]$InstallPath = "C:\Program Files\Microsoft SQL Server",
    [string]$DataPath = "C:\SQLData",
    [string]$LogPath = "C:\SQLLogs",
    [string]$BackupPath = "C:\SQLBackup"
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Output "[$(Get-Date -Format 'HH:mm:ss')] $msg" }

Write-Step "开始 SQL Server 2022 安装（版本：$Edition）"

# 检查是否已安装
$existing = Get-Service -Name "MSSQLSERVER" -ErrorAction SilentlyContinue
if ($existing) {
    Write-Step "SQL Server 已安装（状态：$($existing.Status)），跳过安装"
    exit 0
}

# 检查磁盘空间（至少需要 10GB）
$drive = Split-Path -Qualifier $DataPath
$disk = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='$drive'"
$freeGB = [math]::Round($disk.FreeSpace / 1GB, 2)
if ($freeGB -lt 10) {
    Write-Error "磁盘 $drive 剩余空间不足 10GB（当前：${freeGB}GB），安装中止"
    exit 1
}

# 创建数据目录
@($DataPath, $LogPath, $BackupPath) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
        Write-Step "创建目录：$_"
    }
}

# 生成配置文件
$configFile = "$env:TEMP\sql_install_config.ini"
$saAuth = if ($SAPassword) {
    "SECURITYMODE=SQL`nSAPWD=$SAPassword"
} else {
    "SECURITYMODE=Windows"
}

@"
[OPTIONS]
ACTION=Install
FEATURES=SQLENGINE,FullText
INSTANCENAME=MSSQLSERVER
INSTANCEDIR=$InstallPath
SQLUSERDBDIR=$DataPath
SQLUSERDBLOGDIR=$LogPath
SQLBACKUPDIR=$BackupPath
SQLSYSADMINACCOUNTS=BUILTIN\Administrators
IACCEPTSQLSERVERLICENSETERMS=True
QUIET=True
INDICATEPROGRESS=False
TCPENABLED=1
$saAuth
"@ | Set-Content -Path $configFile -Encoding UTF8

Write-Step "配置文件已生成：$configFile"

# 下载 SQL Server 2022（Developer 版免费）
$isoUrl = "https://download.microsoft.com/download/3/8/d/38de7036-2433-4207-8eae-06e247e17b25/SQLServer2022-DEV-x64-ENU.exe"
$installer = "$env:TEMP\SQLServer2022Setup.exe"

if (-not (Test-Path $installer)) {
    Write-Step "下载 SQL Server 2022 安装程序..."
    Invoke-WebRequest -Uri $isoUrl -OutFile $installer -UseBasicParsing
}

Write-Step "开始静默安装（预计 10-20 分钟）..."
$proc = Start-Process -FilePath $installer `
    -ArgumentList "/ConfigurationFile=`"$configFile`" /IACCEPTSQLSERVERLICENSETERMS" `
    -Wait -PassThru -NoNewWindow

if ($proc.ExitCode -ne 0 -and $proc.ExitCode -ne 3010) {
    Write-Error "SQL Server 安装失败，退出码：$($proc.ExitCode)"
    exit $proc.ExitCode
}

# 启动服务
Write-Step "启动 SQL Server 服务..."
Start-Service MSSQLSERVER -ErrorAction SilentlyContinue
Start-Sleep 5

# 设置 SQL Server Browser 自动启动
Set-Service -Name SQLBrowser -StartupType Automatic -ErrorAction SilentlyContinue
Start-Service SQLBrowser -ErrorAction SilentlyContinue

# 验证安装
$sqlSvc = Get-Service -Name "MSSQLSERVER" -ErrorAction SilentlyContinue
if ($sqlSvc -and $sqlSvc.Status -eq "Running") {
    Write-Step "SQL Server 安装成功并正在运行"
} else {
    Write-Error "SQL Server 服务未能启动，请检查安装日志"
    exit 1
}

# 清理临时文件
Remove-Item $configFile -Force -ErrorAction SilentlyContinue

Write-Step "SQL Server 2022 安装完成"
exit 0
