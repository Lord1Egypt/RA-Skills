# backup.ps1 - 备份 SQL Server 数据库
param(
    [Parameter(Mandatory = $true)]
    [string]$DatabaseName,
    [string]$Dest = "C:\SQLBackup"
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Output "[$(Get-Date -Format 'HH:mm:ss')] $msg" }

if (-not (Test-Path $Dest)) {
    New-Item -ItemType Directory -Path $Dest -Force | Out-Null
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = Join-Path $Dest "$DatabaseName`_$timestamp.bak"

Write-Step "备份数据库 [$DatabaseName] 到 $backupFile..."

$query = @"
BACKUP DATABASE [$DatabaseName]
TO DISK = N'$backupFile'
WITH FORMAT, COMPRESSION, STATS = 10;
"@

sqlcmd -S localhost -E -Q $query
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Step "备份完成：$backupFile"
Write-Output "BACKUP_FILE=$backupFile"
exit 0
