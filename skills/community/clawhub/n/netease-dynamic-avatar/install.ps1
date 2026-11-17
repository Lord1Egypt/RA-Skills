# Install netease-dynamic-avatar into the local harness skills directory.
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File install.ps1
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Root "D:\my\skills"
#
# Default target: $env:DSH_HOME\skills  (DSH_HOME defaults to %USERPROFILE%\.dsh)
#
# NOTE: this file is intentionally ASCII-only so Windows PowerShell 5.1
# parses it correctly regardless of the console code page.
param(
    [string]$Root = ""
)

$ErrorActionPreference = "Stop"

$repo = "https://github.com/yuan-dev39/netease-dynamic-avatar.git"

if ([string]::IsNullOrWhiteSpace($Root)) {
    $base = if ($env:DSH_HOME) { $env:DSH_HOME } else { Join-Path $env:USERPROFILE ".dsh" }
    $Root = Join-Path $base "skills"
}

$dest = Join-Path $Root "netease-dynamic-avatar"

Write-Host "==> target: $dest"
New-Item -ItemType Directory -Force -Path $Root | Out-Null

if (Test-Path (Join-Path $dest ".git")) {
    Write-Host "==> existing git repo, pulling"
    git -C $dest pull --ff-only
}
elseif (Test-Path $dest) {
    $bak = "$dest.bak." + [int][double]::Parse((Get-Date -UFormat %s))
    Write-Host "==> existing non-git folder, backing up to $bak"
    Move-Item -LiteralPath $dest -Destination $bak
    git clone --depth 1 $repo $dest
}
else {
    git clone --depth 1 $repo $dest
}

if (-not (Test-Path (Join-Path $dest "SKILL.md"))) {
    Write-Host "ERROR: $dest\SKILL.md not found - install failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "OK installed: $dest" -ForegroundColor Green
Write-Host "   Restart your session (or reload the harness Web GUI) to pick up the skill."
Write-Host ""
Write-Host "Optional - the converter script needs Pillow:"
Write-Host "   python -m pip install --no-user --target `"$dest\pylibs`" pillow"
