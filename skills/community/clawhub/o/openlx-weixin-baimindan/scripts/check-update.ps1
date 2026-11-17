$ErrorActionPreference = 'Stop'
python "$PSScriptRoot/manager.py" check-update @args
exit $LASTEXITCODE
