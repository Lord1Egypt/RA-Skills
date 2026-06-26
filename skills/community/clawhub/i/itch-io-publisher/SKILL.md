---
name: itch-io-publisher
description: Read itch.io creator stats and publish or update itch.io game builds from Windows using the itch.io server-side API and Butler. Use when the user asks to check itch.io account or game stats, list their games, validate an itch.io API key, install Butler for itch publishing, or upload or push a local build folder or zip to an itch.io project channel such as username/game:html5.
---

# itch-io-publisher

Keep this skill self-contained. Do not rely on bundled helper scripts being present. Run explicit PowerShell commands directly so the user can inspect exactly what will happen.

## Workflow

1. Validate the API key if needed.
2. Read account and game stats if the user wants visibility first.
3. Install Butler if it is missing.
4. Dry-run a push before a live upload when the target or source path is new.
5. Only do a live push after the user has identified the project target and local build source.

## Key limits

- The public server-side API is suitable for reading account and game data and for purchase or download-key verification.
- Normal page editing is not exposed here; expect metadata edits to require the itch.io web dashboard.
- Build publishing is done with Butler, not the read-oriented JSON API.

## Validate key and read stats

Run this PowerShell directly:

```powershell
$key = '<API_KEY>'
$base = "https://itch.io/api/1/$key"
$me = Invoke-RestMethod -Uri "$base/me" -Method Get -TimeoutSec 30
$games = Invoke-RestMethod -Uri "$base/my-games" -Method Get -TimeoutSec 30

$totalViews = 0
$totalDownloads = 0
$totalPurchases = 0
foreach ($game in $games.games) {
  $totalViews += [int]$game.views_count
  $totalDownloads += [int]$game.downloads_count
  $totalPurchases += [int]$game.purchases_count
}

[pscustomobject]@{
  account = $me.user
  totals = [pscustomobject]@{
    views = $totalViews
    downloads = $totalDownloads
    purchases = $totalPurchases
    games = @($games.games).Count
  }
  games = $games.games
} | ConvertTo-Json -Depth 8
```

Use this to validate the key, fetch profile info, list games, and summarize views, downloads, and purchases.

## Install Butler

If Butler is not installed yet, run this PowerShell directly:

```powershell
$dest = Join-Path $env:LOCALAPPDATA 'OpenClaw\tools\butler'
New-Item -ItemType Directory -Force -Path $dest | Out-Null
$zipPath = Join-Path ([System.IO.Path]::GetTempPath()) 'butler-windows-amd64.zip'
Invoke-WebRequest -Uri 'https://broth.itch.zone/butler/windows-amd64/LATEST/archive/default' -OutFile $zipPath -TimeoutSec 120
Expand-Archive -Path $zipPath -DestinationPath $dest -Force
& (Join-Path $dest 'butler.exe') version
```

This downloads the latest Windows Butler build from `broth.itch.zone` into `%LOCALAPPDATA%\OpenClaw\tools\butler`.

## Push a build

Dry-run first when possible:

```powershell
$key = '<API_KEY>'
$source = 'D:\path\to\build'
$target = 'username/game:html5'
$butlerDir = Join-Path $env:LOCALAPPDATA 'OpenClaw\tools\butler'
$butler = Join-Path $butlerDir 'butler.exe'
if (!(Test-Path $butler)) {
  throw "butler.exe not found. Install Butler first."
}
if (!(Test-Path $source)) {
  throw "Source path not found: $source"
}
$tmpDir = Join-Path ([System.IO.Path]::GetTempPath()) 'openclaw-itch'
New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null
$tokenFile = Join-Path $tmpDir 'butler_creds.txt'
Set-Content -Path $tokenFile -Value $key -NoNewline
try {
  & $butler -i $tokenFile push $source $target --dry-run
}
finally {
  Remove-Item $tokenFile -Force -ErrorAction SilentlyContinue
}
```

Live push:

```powershell
$key = '<API_KEY>'
$source = 'D:\path\to\build'
$target = 'username/game:html5'
$butlerDir = Join-Path $env:LOCALAPPDATA 'OpenClaw\tools\butler'
$butler = Join-Path $butlerDir 'butler.exe'
if (!(Test-Path $butler)) {
  throw "butler.exe not found. Install Butler first."
}
if (!(Test-Path $source)) {
  throw "Source path not found: $source"
}
$tmpDir = Join-Path ([System.IO.Path]::GetTempPath()) 'openclaw-itch'
New-Item -ItemType Directory -Force -Path $tmpDir | Out-Null
$tokenFile = Join-Path $tmpDir 'butler_creds.txt'
Set-Content -Path $tokenFile -Value $key -NoNewline
try {
  & $butler -i $tokenFile push $source $target --if-changed
}
finally {
  Remove-Item $tokenFile -Force -ErrorAction SilentlyContinue
}
```

## Target format

Use Butler targets in the form:

- `username/game:channel`
- `game_id:channel`

Common HTML game channel names include `html5` or `web`, but use the channel the user has configured on itch.io.

## Safe defaults

- Do not paste API keys back into chat unless the user explicitly asks.
- Do not live-push to itch.io without a specific source path and target confirmed by the user.
- Prefer dry-run first for a new project or channel.
- If a push fails, inspect Butler's exact error rather than guessing.
