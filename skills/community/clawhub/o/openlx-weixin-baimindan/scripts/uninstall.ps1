$ErrorActionPreference = 'Stop'
python "$PSScriptRoot/manager.py" uninstall @args
exit $LASTEXITCODE
