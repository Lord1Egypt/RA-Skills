param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [string[]]$CommandArguments
)

$ErrorActionPreference = 'Stop'
$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$NodeBin = & (Join-Path $ScriptDirectory 'bootstrap.ps1') -PrintNode
& $NodeBin (Join-Path $ScriptDirectory 'legal-skill.mjs') @CommandArguments
exit $LASTEXITCODE
