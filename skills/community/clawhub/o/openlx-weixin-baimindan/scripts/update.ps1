$ErrorActionPreference = 'Stop'
python "$PSScriptRoot/manager.py" update @args
exit $LASTEXITCODE
