# apply_schema.ps1 - 在 SQL Server 上执行建表 DDL
# 参数：
#   -DatabaseName  目标数据库名
#   -SqlFile       SQL 文件路径（由 schema_compiler.py 生成）

param(
    [Parameter(Mandatory=$true)]
    [string]$DatabaseName,

    [Parameter(Mandatory=$true)]
    [string]$SqlFile
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Output "[$(Get-Date -Format 'HH:mm:ss')] $msg" }

if (-not (Test-Path $SqlFile)) {
    Write-Error "SQL 文件不存在：$SqlFile"
    exit 1
}

Write-Step "在数据库 [$DatabaseName] 上执行 Schema..."

# 使用 sqlcmd 执行（Windows 集成验证）
$result = sqlcmd -S localhost -d $DatabaseName -E -i $SqlFile -b 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Error "Schema 执行失败：$result"
    exit 1
}

Write-Step "Schema 执行完成"
Write-Output $result
exit 0
