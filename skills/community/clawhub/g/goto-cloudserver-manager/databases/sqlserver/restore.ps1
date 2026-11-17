# restore.ps1 - 从 .bak 文件恢复 SQL Server 数据库
param(
    [Parameter(Mandatory = $true)]
    [string]$DatabaseName,
    [Parameter(Mandatory = $true)]
    [string]$Source,
    [string]$DataPath = "C:\SQLData",
    [string]$LogPath = "C:\SQLLogs"
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Output "[$(Get-Date -Format 'HH:mm:ss')] $msg" }

if (-not (Test-Path $Source)) {
    Write-Error "备份文件不存在：$Source"
    exit 1
}

Write-Step "从 $Source 恢复数据库 [$DatabaseName]..."

# 查询备份文件内的逻辑文件名，重新映射到目标数据路径
$fileListQuery = "RESTORE FILELISTONLY FROM DISK = N'$Source';"
$fileList = sqlcmd -S localhost -E -Q $fileListQuery -h -1 -s "," -W

$moveClauses = @()
foreach ($line in $fileList) {
    if (-not $line.Trim()) { continue }
    $cols = $line.Split(",")
    $logicalName = $cols[0].Trim()
    $fileType = $cols[2].Trim()
    if ($fileType -eq "D") {
        $moveClauses += "MOVE N'$logicalName' TO N'$DataPath\$DatabaseName.mdf'"
    } elseif ($fileType -eq "L") {
        $moveClauses += "MOVE N'$logicalName' TO N'$LogPath\${DatabaseName}_log.ldf'"
    }
}
$moveSql = $moveClauses -join ",`n    "

$query = @"
ALTER DATABASE [$DatabaseName] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO
RESTORE DATABASE [$DatabaseName]
FROM DISK = N'$Source'
WITH $moveSql,
    REPLACE, STATS = 10;
GO
ALTER DATABASE [$DatabaseName] SET MULTI_USER;
GO
"@

sqlcmd -S localhost -E -Q $query
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Step "恢复完成：[$DatabaseName]"
exit 0
