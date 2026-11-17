# check_server.ps1 - Windows Server 状态检查
# 输出：CPU / 内存 / 磁盘 / 网络 / 系统信息的结构化报告

$ErrorActionPreference = "Continue"

function Get-Section($title) {
    Write-Output ""
    Write-Output "===== $title ====="
}

# 系统基本信息
Get-Section "系统信息"
$os = Get-WmiObject Win32_OperatingSystem
$cs = Get-WmiObject Win32_ComputerSystem
Write-Output "主机名: $($cs.Name)"
Write-Output "系统: $($os.Caption) $($os.Version)"
Write-Output "架构: $($os.OSArchitecture)"
Write-Output "启动时间: $($os.LastBootUpTime)"
$uptime = (Get-Date) - $os.ConvertToDateTime($os.LastBootUpTime)
Write-Output "运行时间: $([int]$uptime.TotalHours) 小时 $($uptime.Minutes) 分钟"

# CPU
Get-Section "CPU 使用率"
$cpu = Get-WmiObject Win32_Processor
$cpuLoad = (Get-WmiObject Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
Write-Output "处理器: $($cpu[0].Name)"
Write-Output "核心数: $($cpu.Count)"
Write-Output "CPU 使用率: ${cpuLoad}%"

# 内存
Get-Section "内存使用"
$totalMem = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$freeMem = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$usedMem = [math]::Round($totalMem - $freeMem, 2)
$memPercent = [math]::Round(($usedMem / $totalMem) * 100, 1)
Write-Output "总内存: ${totalMem} GB"
Write-Output "已用内存: ${usedMem} GB"
Write-Output "可用内存: ${freeMem} GB"
Write-Output "内存使用率: ${memPercent}%"

# 磁盘
Get-Section "磁盘使用"
Get-WmiObject Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
    $total = [math]::Round($_.Size / 1GB, 2)
    $free = [math]::Round($_.FreeSpace / 1GB, 2)
    $used = [math]::Round($total - $free, 2)
    $percent = if ($total -gt 0) { [math]::Round(($used / $total) * 100, 1) } else { 0 }
    Write-Output "驱动器 $($_.DeviceID): 总计 ${total}GB | 已用 ${used}GB | 可用 ${free}GB | 使用率 ${percent}%"
}

# 网络
Get-Section "网络适配器"
Get-WmiObject Win32_NetworkAdapterConfiguration -Filter "IPEnabled=True" | ForEach-Object {
    Write-Output "适配器: $($_.Description)"
    Write-Output "  IP: $($_.IPAddress -join ', ')"
    Write-Output "  子网掩码: $($_.IPSubnet -join ', ')"
}

# 关键 Windows 服务状态
Get-Section "关键服务状态"
$services = @("WinRM", "W32Time", "Dnscache", "EventLog", "TermService")
foreach ($svc in $services) {
    $s = Get-Service -Name $svc -ErrorAction SilentlyContinue
    if ($s) {
        Write-Output "$($s.Name): $($s.Status)"
    }
}

# 最近系统事件（Error 级别）
Get-Section "最近系统错误（最近10条）"
Get-EventLog -LogName System -EntryType Error -Newest 10 -ErrorAction SilentlyContinue |
    Select-Object TimeGenerated, Source, Message |
    ForEach-Object { Write-Output "$($_.TimeGenerated) [$($_.Source)] $($_.Message.Substring(0, [Math]::Min(100, $_.Message.Length)))" }

Write-Output ""
Write-Output "===== 检查完成 ====="
exit 0
