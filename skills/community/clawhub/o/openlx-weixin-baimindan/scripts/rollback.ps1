$ErrorActionPreference = 'Stop'
python "$PSScriptRoot/manager.py" rollback @args
exit $LASTEXITCODE
