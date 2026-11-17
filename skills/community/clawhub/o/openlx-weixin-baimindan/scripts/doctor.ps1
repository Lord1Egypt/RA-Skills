$ErrorActionPreference = 'Stop'
python "$PSScriptRoot/manager.py" doctor @args
exit $LASTEXITCODE
