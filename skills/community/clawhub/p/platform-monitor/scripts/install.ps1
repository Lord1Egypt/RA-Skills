# Platform Monitor - Windows 一键安装脚本
# 用法: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "🚀 Platform Monitor - Windows 安装向导" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查 Node.js
Write-Host "【1/5】检查 Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "  ✅ Node.js $nodeVersion 已安装" -ForegroundColor Green
} catch {
    Write-Host "  ❌ 未找到 Node.js，请先安装: https://nodejs.org/" -ForegroundColor Red
    Write-Host "  安装后重新运行此脚本" -ForegroundColor Yellow
    pause
    exit 1
}

# 2. 安装依赖
Write-Host ""
Write-Host "【2/5】安装依赖..." -ForegroundColor Yellow
npm install axios cheerio playwright
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ❌ 依赖安装失败" -ForegroundColor Red
    pause
    exit 1
}
Write-Host "  ✅ 依赖安装完成" -ForegroundColor Green

# 3. 生成配置文件
Write-Host ""
Write-Host "【3/5】生成配置文件..." -ForegroundColor Yellow
$configPath = "platform_monitor_config.json"
if (Test-Path $configPath) {
    Write-Host "  ⚠️  配置文件已存在: $configPath" -ForegroundColor Yellow
} else {
    node monitor.js --init
}

# 4. 测试运行
Write-Host ""
Write-Host "【4/5】测试运行..." -ForegroundColor Yellow
node monitor.js
if ($LASTEXITCODE -eq 0 -or $LASTEXITCODE -eq 2) {
    Write-Host "  ✅ 测试运行成功" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  测试运行失败，请检查配置" -ForegroundColor Yellow
}

# 5. 设置定时任务
Write-Host ""
Write-Host "【5/5】设置定时任务..." -ForegroundColor Yellow
$setupCron = Read-Host "是否设置定时任务（每天9:00和21:00运行）？ (Y/n)"
if ($setupCron -ne "n") {
    # 创建定时任务脚本
    $taskScript = @"
# Platform Monitor 定时任务
`$cwd = Get-Location
`$nodePath = (Get-Command node).Source
`$scriptPath = Join-Path `$cwd "monitor.js"

# 创建任务
`$action = New-ScheduledTaskAction -Execute "`$nodePath" -Argument "`$scriptPath" -WorkingDirectory `$cwd
`$trigger1 = New-ScheduledTaskTrigger -Daily -At "09:00"
`$trigger2 = New-ScheduledTaskTrigger -Daily -At "21:00"
Register-ScheduledTask -TaskName "PlatformMonitor-Morning" -Action `$action -Trigger `$trigger1 -Description "平台监控-早班" -Force
Register-ScheduledTask -TaskName "PlatformMonitor-Evening" -Action `$action -Trigger `$trigger2 -Description "平台监控-晚班" -Force

Write-Host "✅ 定时任务已创建"
Write-Host "  早班: 每天 09:00"
Write-Host "  晚班: 每天 21:00"
"@
    
    $taskScriptPath = "setup_cron_temp.ps1"
    $taskScript | Out-File -FilePath $taskScriptPath -Encoding UTF8
    
    Write-Host "  请以管理员身份运行以下命令:" -ForegroundColor Yellow
    Write-Host "  powershell -ExecutionPolicy Bypass -File $taskScriptPath" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✅ 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📝 下一步:" -ForegroundColor Yellow
Write-Host "  1. 编辑 platform_monitor_config.json 填入你的配置"
Write-Host "  2. 运行 node monitor.js 测试"
Write-Host "  3. 运行 node monitor.js --report 查看报告"
Write-Host ""
Write-Host "📚 文档: https://github.com/your-repo/platform-monitor"
Write-Host ""

pause
