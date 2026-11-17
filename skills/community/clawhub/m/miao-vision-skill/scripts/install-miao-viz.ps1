$ErrorActionPreference = "Stop"
$Compatibility = Get-Content (Join-Path $PSScriptRoot "../cli-compatibility.json") -Raw | ConvertFrom-Json
& npm.cmd install -g "@miao-vision/cli@$($Compatibility.recommendedCliVersion)"
if ($LASTEXITCODE -ne 0) { throw "Global npm installation failed. Check npm prefix permissions or use a user-managed Node installation; no elevation was attempted." }
& node (Join-Path $PSScriptRoot "check-miao-viz.mjs") --require-recommended --print-path
if ($LASTEXITCODE -ne 0) { throw "Installed global CLI failed version or capability verification. Check PATH." }
