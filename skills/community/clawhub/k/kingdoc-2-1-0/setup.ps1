# KingDoc Windows 安装脚本
# 用法: powershell -ExecutionPolicy Bypass -File setup.ps1

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  KingDoc - 金山文档 AI 协作助手 安装向导" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "ERROR: Python not found. Please install Python 3.10+ first." -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Python: $($python.Source)" -ForegroundColor Green

# Check pip
$pip = Get-Command pip -ErrorAction SilentlyContinue
if (-not $pip) {
    Write-Host "ERROR: pip not found." -ForegroundColor Red
    exit 1
}

# Create virtual env
$venvPath = Join-Path $PSScriptRoot ".venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "[..] Creating virtual environment..." -ForegroundColor Gray
    & python -m venv $venvPath
    Write-Host "[OK] venv created" -ForegroundColor Green
}

# Activate venv
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
. $activateScript

# Install dependencies
Write-Host "[..] Installing dependencies..." -ForegroundColor Gray
$deps = @("requests", "mcp", "python-docx", "python-pptx", "pyyaml")
foreach ($dep in $deps) {
    pip install -q $dep
}
Write-Host "[OK] Dependencies installed" -ForegroundColor Green

# Get App credentials
Write-Host ""
Write-Host "请从金山开放平台 (developer.kdocs.cn) 获取以下信息:"
Write-Host ""
$appId = Read-Host "App ID"
$appSecret = Read-Host "App Secret (输入不显示)" -AsSecureString

# Save config
$config = @{
    appName = "kingdoc"
    appId = $appId
    appSecret = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($appSecret)
    )
    scope = "user:file:write user:file:read team:file:write team:file:read"
    environment = "production"
} | ConvertTo-Json -Depth 3

$configPath = Join-Path $PSScriptRoot "config.json"
Set-Content -Path $configPath -Value $config -Encoding UTF8
Write-Host "[OK] Config saved to config.json" -ForegroundColor Green

# Test token
Write-Host ""
Write-Host "[..] Testing API connection..." -ForegroundColor Gray
python $PSScriptRoot\engine\auth.py --config $configPath --test 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Connection test passed!" -ForegroundColor Green
} else {
    Write-Host "[WARN] Connection test failed. Check your credentials." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  安装完成！重启 WorkBuddy 即可使用 KingDoc" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
