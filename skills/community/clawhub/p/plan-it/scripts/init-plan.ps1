# init-plan.ps1 — scaffold plan.html from a chosen template (Windows PowerShell).
#
# Usage:
#   .\init-plan.ps1                           # interactive prompt for template
#   .\init-plan.ps1 <template-name>           # named template
#   .\init-plan.ps1 <template-name> -Slug NAME  # parallel-plan mode under .planning\NAME\

param(
    [string]$Template = "",
    [string]$Slug = ""
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

function Try-Join {
    param([string]$Base, [string]$Tail)
    if (-not $Base) { return $null }
    return (Join-Path $Base $Tail)
}

$Candidates = @(
    (Join-Path $ScriptDir "..\templates"),
    (Try-Join $env:CLAUDE_PLUGIN_ROOT "templates"),
    (Try-Join $env:USERPROFILE ".claude\skills\plan-it\templates"),
    (Try-Join $env:USERPROFILE ".claude\plugins\marketplaces\plan-it\templates")
)

$ResolvedTemplates = $null
foreach ($c in $Candidates) {
    if ($c -and (Test-Path $c -PathType Container)) {
        $ResolvedTemplates = $c
        break
    }
}

if (-not $ResolvedTemplates) {
    Write-Error "[plan-it] templates/ dir not found. Reinstall the skill."
    exit 1
}

if (-not $Template) {
    Write-Host "Available templates:"
    Get-ChildItem -Path $ResolvedTemplates -Filter "*.html" | ForEach-Object {
        Write-Host ("  " + $_.BaseName)
    }
    Write-Host ""
    $Template = Read-Host "Choose template"
}

$Src = Join-Path $ResolvedTemplates "$Template.html"
if (-not (Test-Path $Src)) {
    Write-Error "[plan-it] template not found: $Template"
    Get-ChildItem -Path $ResolvedTemplates -Filter "*.html" | ForEach-Object {
        Write-Host ("  " + $_.BaseName)
    }
    exit 3
}

if ($Slug) {
    $DestDir = Join-Path ".planning" $Slug
    New-Item -ItemType Directory -Force -Path $DestDir | Out-Null
    $Dest = Join-Path $DestDir "plan.html"
    New-Item -ItemType Directory -Force -Path ".planning" | Out-Null
    Set-Content -Path ".planning\.active_plan" -Value $Slug -NoNewline
} else {
    $Dest = "plan.html"
}

if (Test-Path $Dest) {
    $Ts = Get-Date -Format "yyyyMMdd-HHmmss"
    Copy-Item -Path $Dest -Destination "$Dest.backup.$Ts"
    Write-Host "[plan-it] existing $Dest backed up to $Dest.backup.$Ts"
}

Copy-Item -Path $Src -Destination $Dest -Force
Write-Host "[plan-it] created $Dest from template $Template"
Write-Host "[plan-it] open it: pwsh scripts\render-plan.ps1"
