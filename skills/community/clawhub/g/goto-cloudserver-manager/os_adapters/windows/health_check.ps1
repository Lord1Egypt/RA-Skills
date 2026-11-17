# health_check.ps1 - Windows Server 健康检查（快速版，用于定期巡检）
# 输出结果供 report_generator.py 解析

$ErrorActionPreference = "Continue"
$result = @{}

# CPU
$cpu = (Get-WmiObject Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
$result["cpu_percent"] = $cpu

# 内存
$os = Get-WmiObject Win32_OperatingSystem
$totalMem = $os.TotalVisibleMemorySize
$freeMem = $os.FreePhysicalMemory
$memPercent = [math]::Round((($totalMem - $freeMem) / $totalMem) * 100, 1)
$result["memory_percent"] = $memPercent
$result["memory_total_gb"] = [math]::Round($totalMem / 1MB, 2)
$result["memory_free_gb"] = [math]::Round($freeMem / 1MB, 2)

# 磁盘（C 盘）
$disk = Get-WmiObject Win32_LogicalDisk -Filter "DeviceID='C:'"
$diskPercent = [math]::Round((($disk.Size - $disk.FreeSpace) / $disk.Size) * 100, 1)
$result["disk_c_percent"] = $diskPercent
$result["disk_c_free_gb"] = [math]::Round($disk.FreeSpace / 1GB, 2)

# SQL Server 服务状态
$sqlSvc = Get-Service -Name "MSSQLSERVER" -ErrorAction SilentlyContinue
$result["sqlserver_status"] = if ($sqlSvc) { $sqlSvc.Status.ToString() } else { "NotInstalled" }

# 整体健康状态判断
$healthy = $true
$warnings = @()

if ($cpu -gt 90) { $healthy = $false; $warnings += "CPU 使用率过高：${cpu}%" }
if ($memPercent -gt 90) { $healthy = $false; $warnings += "内存使用率过高：${memPercent}%" }
if ($diskPercent -gt 85) { $warnings += "C 盘使用率较高：${diskPercent}%" }
if ($result["sqlserver_status"] -ne "Running" -and $result["sqlserver_status"] -ne "NotInstalled") {
    $healthy = $false
    $warnings += "SQL Server 服务异常：$($result['sqlserver_status'])"
}

$result["healthy"] = $healthy
$result["warnings"] = $warnings -join "; "

# 以 JSON 格式输出供 Python 解析
$result | ConvertTo-Json -Compress
exit 0
