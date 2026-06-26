# Cookie Configuration

Load this document only when the user mentions cookies, VIP-only tracks, grey tracks, or login-required tracks.

`go-music-api` supports:
- startup loading from `cookies.json`
- runtime updates with `POST /api/v1/system/cookies`

Prefer the runtime API in this skill.

## Linux/macOS

```bash
PORT="$(cat "$HOME/.openclaw/music/port" 2>/dev/null || echo 8080)"
curl -fsS -X POST "http://localhost:${PORT}/api/v1/system/cookies" \
  -H "Content-Type: application/json" \
  -d '{
    "netease": "MUSIC_U=xxx; __csrf=yyy;",
    "qq": "qm_keyst=xxx; uin=yyy;",
    "soda": "sessionid=xxx;"
  }'
curl -fsS "http://localhost:${PORT}/api/v1/system/cookies"
```

## Windows

```powershell
$portFile = Join-Path $env:USERPROFILE ".openclaw\music\port"
$port = if (Test-Path $portFile) { (Get-Content $portFile).Trim() } else { "8080" }
$body = @{
  netease = "MUSIC_U=xxx; __csrf=yyy;"
  qq      = "qm_keyst=xxx; uin=yyy;"
  soda    = "sessionid=xxx;"
} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "http://localhost:$port/api/v1/system/cookies" -ContentType "application/json" -Body $body
Invoke-RestMethod -Method Get -Uri "http://localhost:$port/api/v1/system/cookies"
```

## Notes

- Do not print full cookie values back to the user unless explicitly requested.
- After setting cookies, retry the same track before switching source.
- If runtime update fails, fall back to upstream `cookies.json` support.
