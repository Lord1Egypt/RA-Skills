$skillName = "hermesclawzero-auto-memory"
$targetDir = [System.IO.Path]::Combine($env:USERPROFILE, ".openclaw", "plugin-skills", $skillName)

Write-Host "Installing OpenClaw Auto Memory Skill..." -ForegroundColor Cyan

if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

Copy-Item -Path ".\*" -Destination $targetDir -Recurse -Force
Write-Host "Skill successfully installed to $targetDir" -ForegroundColor Green
Write-Host "OpenClaw will now use HermesClawZero for automatic memory persistence." -ForegroundColor Green
