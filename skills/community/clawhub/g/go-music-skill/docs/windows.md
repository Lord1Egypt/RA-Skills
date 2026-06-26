# Windows Workflow

Load this document only when the user is on Windows or explicitly asks for Windows instructions.

## Requirements

- PowerShell 5.1 or later
- Windows amd64
- Access to GitHub Releases
- Python 3 for playback, cache handling, and metadata embedding

`go-music-api` upstream only provides the Windows amd64 release asset.

## Install and start the backend

Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1
```

What the script does:
- installs `go-music-api.exe` into `%USERPROFILE%\.openclaw\music`
- chooses a usable local port
- starts the backend in the background
- verifies health with a local API request

If installation fails:
- verify PowerShell version
- verify GitHub Releases reachability
- inspect `%USERPROFILE%\.openclaw\music\log.txt`
- confirm the downloaded file is `go-music-api_windows_amd64.zip`

## Download a song

Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/play.ps1 "稻香" "$env:USERPROFILE\.openclaw\media\daoxiang.mp3"
```

The Windows playback flow:
- finds Python in this order: `py -3`, `python`, `python3`
- tries `winget install --id Python.Python.3.12` if Python is missing
- searches with the local backend
- selects the best candidate
- downloads the stream to the requested path
- reuses cached files when possible
- runs `scripts/embed_metadata.py` when available

## Cookie support on Windows

If the user mentions cookies, VIP-only tracks, grey tracks, or login-required tracks, load `docs/cookies.md`.
