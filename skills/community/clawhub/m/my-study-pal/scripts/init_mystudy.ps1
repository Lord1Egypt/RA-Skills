param(
    [string]$Root = (Get-Location).Path
)

$ErrorActionPreference = "Stop"

$skillRoot = Split-Path -Parent $PSScriptRoot
$templateRoot = Join-Path $skillRoot "assets\mystudy-template"
$studyRoot = Join-Path $Root "mystudy"
$detailRoot = Join-Path $studyRoot "study-detail"

function Copy-TemplateIfMissing {
    param(
        [string]$TemplatePath,
        [string]$DestinationPath
    )

    if (-not (Test-Path -LiteralPath $DestinationPath)) {
        Copy-Item -LiteralPath $TemplatePath -Destination $DestinationPath
        Write-Output "created: $DestinationPath"
    } else {
        Write-Output "exists:  $DestinationPath"
    }
}

New-Item -ItemType Directory -Force -Path $studyRoot | Out-Null
New-Item -ItemType Directory -Force -Path $detailRoot | Out-Null

Copy-TemplateIfMissing `
    -TemplatePath (Join-Path $templateRoot "study-summary.md") `
    -DestinationPath (Join-Path $studyRoot "study-summary.md")

Copy-TemplateIfMissing `
    -TemplatePath (Join-Path $templateRoot "user-profile.md") `
    -DestinationPath (Join-Path $studyRoot "user-profile.md")

Copy-TemplateIfMissing `
    -TemplatePath (Join-Path $templateRoot "runtime-profile.md") `
    -DestinationPath (Join-Path $studyRoot "runtime-profile.md")

Write-Output "ready:   $studyRoot"
