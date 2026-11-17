$ErrorActionPreference = 'Stop'
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'PYTHON_3_REQUIRED' }
$TaskTemp = Join-Path ([IO.Path]::GetTempPath()) ([Guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $TaskTemp | Out-Null
try {
 $Manager = Join-Path $TaskTemp 'manager.py'
 Invoke-WebRequest 'https://wx.openlx.cn/downloads/openlx-weixin-baimindan/v0.1.1/manager.py' -OutFile $Manager
 if ((Get-FileHash $Manager -Algorithm SHA256).Hash.ToLower() -ne '03b247fff0bbadbc835ad181d3484864649a529dd97bfa034f69858d6327ada9') { throw 'BOOTSTRAP_HASH_MISMATCH' }
 python $Manager install @args
 if ($LASTEXITCODE -ne 0) { throw 'INSTALL_FAILED' }
} finally { Remove-Item $TaskTemp -Recurse -Force }
