<#
.SYNOPSIS
    Email Assistant — 安装后配置脚本 (Windows)
.DESCRIPTION
    首次安装后运行，引导用户完成邮箱账户配置。
#>

$ErrorActionPreference = "Stop"
$SkillDir = Split-Path -Parent $PSScriptRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  🐾 Email Assistant — 配置向导"
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
$PythonPath = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $PythonPath) {
    $PythonPath = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $PythonPath) {
    Write-Host "❌ 未找到 Python。请先安装 Python 3.8+。" -ForegroundColor Red
    Write-Host "   下载: https://www.python.org/downloads/"
    exit 1
}

Write-Host "✅ Python 版本:" -ForegroundColor Green
& $PythonPath.Source --version

Write-Host ""
Write-Host "启动配置向导..." -ForegroundColor Yellow
Write-Host ""

# Run the Python setup wizard
$WizardPath = Join-Path $SkillDir "scripts\setup_wizard.py"
& $PythonPath.Source $WizardPath

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "  🎉 配置完成！"
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "现在你可以使用自然语言操作邮箱了。试试说："
    Write-Host '  "帮我查一下今天的邮件"'
    Write-Host '  "给 xx@qq.com 发一封邮件"'
    Write-Host ""
}
else {
    Write-Host "⚠️  配置未完成，可以稍后重试。" -ForegroundColor Yellow
    Write-Host "   python3 $WizardPath"
}
