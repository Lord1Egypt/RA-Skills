$ErrorActionPreference = "Stop"
$script = Join-Path $PSScriptRoot "pan.py"
if (-not (Test-Path -LiteralPath $script)) {
    Write-Error "[pan] 找不到 $script"
    exit 2
}
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $script @args
    exit $LASTEXITCODE
}
if (Get-Command python -ErrorAction SilentlyContinue) {
    & python $script @args
    exit $LASTEXITCODE
}
Write-Error "[pan] 未找到 Python 3；请安装 Python 并把 python.exe 加入 PATH"
exit 127
