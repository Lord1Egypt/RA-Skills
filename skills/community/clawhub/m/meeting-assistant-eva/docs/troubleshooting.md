# Troubleshooting Guide

## Known Issues & Solutions

---

### Zoom SDK Missing

**Symptom:**
```
[Zoom] Zoom SDK native addon is not available.
Expected native addon: services/vexa-bot/build/Release/zoom_sdk_wrapper.node
Zoom Meeting SDK binaries are proprietary and must be downloaded separately from Zoom.
```

**Cause:** `vexaai/vexa-lite` Docker image does not include Zoom's proprietary native SDK binaries. These must be licensed from Zoom and downloaded separately.

**Solution:** Use **Google Meet** instead. Google Meet works via browser automation and requires no proprietary SDK.

**Status:** Open — Zoom support requires either building a custom Vexa image with Zoom SDK binaries, or waiting for Vexa to bundle them.

---

### Zoom OAuth Credentials Required (secondary Zoom issue)

**Symptom:**
```
[Zoom] ZOOM_CLIENT_ID and ZOOM_CLIENT_SECRET environment variables are required
```

**Cause:** Even with credentials configured, Zoom join fails due to the SDK issue above.

**Solution:** `ZOOM_CLIENT_ID` and `ZOOM_CLIENT_SECRET` are already set in `docker-compose.yml`. But they're irrelevant until the SDK binary issue is resolved.

---

### Whisper Transcription: `model=default` Error

**Symptom:**
```
ValueError: Invalid model size 'default', expected one of: tiny.en, tiny, base.en, base, ...
```

**Cause:** Vexa's internal `whisper_live.remote_transcriber` hardcodes `model=default` in OpenAI API requests. The `fedirz/faster-whisper-server` rejects this as an invalid model name.

**Solution:** The `whisper-proxy` container intercepts requests and rewrites the multipart form body:
```
name="model"\r\n\r\ndefault  →  name="model"\r\n\r\nSystran/faster-whisper-base
```

Ensure the proxy container is running:
```powershell
docker ps | Select-String "whisper-proxy"
# Should show: vexa-whisper-proxy   Up X seconds
```

If missing, ensure `whisper_proxy.py` exists at `C:\Users\zeron\AppData\Local\Temp\whisper_proxy.py` and restart compose.

---

### `host.docker.internal` Unreachable from Containers

**Symptom:** Running a proxy on Windows localhost and Docker containers can't reach it via `host.docker.internal`.

**Cause:** In this Docker Desktop + WSL2 configuration, `host.docker.internal` does not resolve from within Docker containers. The error is `Network is unreachable` or `Connection refused`.

**Solution:** Run the proxy service INSIDE Docker (as a `whisper-proxy` compose service) rather than on the Windows host. The proxy can reach other containers via Docker DNS names (e.g., `http://whisper:8000`).

---

### Audio Transcription: No Segments

**Symptom:** `segments: []` in transcript response even after extended recording.

**Causes and solutions:**

| Cause | Check | Fix |
|---|---|---|
| No microphone audio | Bot log shows `audioTracks=0` | Ensure a participant has their mic on |
| Screen share audio only | Bot sees video but no audio tracks | Screen share system audio cannot be captured by Vexa |
| Whisper proxy not rewriting | Check proxy logs for `Systran in body: False` | Restart `vexa-whisper-proxy` |
| Whisper server returning 500 | Check `docker logs vexa-whisper` | Ensure `WHISPER__MODEL=Systran/faster-whisper-base` |
| Model not downloaded | Whisper logs show download attempt | Wait for model download on first start (~1-2 min) |

To check bot audio status:
```powershell
docker exec vexa-meeting-bot cat /var/log/vexa-bots/vexa-bot-7-c724c8b7.log | Select-String "audio"
# Look for: audioTracks=1 (working) vs audioTracks=0 (no audio)
```

---

### Vexa Container Restart Loop

**Symptom:** `vexa-meeting-bot` shows "Up 2 seconds" repeatedly (keeps restarting).

**Causes:**

1. **Migration failure** (cosmetic): `FAILED: Path doesn't exist: alembic` — this is a warning, not fatal. The container continues after this.

2. **Transcription service unreachable**: If `TRANSCRIBER_URL` points to a host that Vexa can't reach at startup, it exits. Ensure the proxy container is up before Vexa starts.

**Check logs:**
```powershell
docker logs vexa-meeting-bot --tail 30
```

---

### Docker Image Pull Fails: `docker-credential-desktop not in PATH`

**Symptom:**
```
error getting credentials - err: exec: "docker-credential-desktop": executable file not found in %PATH%
```

**Cause:** Docker credential helper is not in PATH when running Docker CLI from WSL or certain PowerShell contexts.

**Solution:** Add Docker bin directory to PATH before running pull:
```powershell
$env:PATH += ';C:\Program Files\Docker\Docker\resources\bin'
docker pull <image>
```

---

### Chat Messages Appear as Garbled/Mojibake

**Symptom:** Chinese characters in chat appear as `æµè¯` or `??` instead of `测试`.

**Cause:** PowerShell `Invoke-WebRequest` does not send UTF-8 JSON by default.

**Solution:** Always use Python for sending chat messages with Chinese content:
```python
import json, urllib.request

body = json.dumps({"text": "中文消息"}, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(
    url, data=body,
    headers={"Content-Type": "application/json; charset=utf-8", "X-API-Key": KEY},
    method="POST"
)
urllib.request.urlopen(req)
```

The `MeetingBot.send_chat()` method uses `requests` library which handles encoding correctly.

---

### Bot Can't Join: `409 Conflict`

**Symptom:**
```
HTTPError: HTTP Error 409: Conflict
```

**Cause:** A bot is already joined (or in the process of joining) for this meeting ID.

**Solution:** Leave the existing bot first:
```python
requests.delete(f"{VEXA}/bots/google_meet/{meeting_id}", headers={"X-API-Key": KEY})
time.sleep(3)
# Then rejoin
```

---

### `vexa_api_key` Returns 403 Forbidden

**Symptom:** API calls return `{"detail": "Invalid API token"}` or 403.

**Causes:**

1. Using the admin token (`openclaw-meeting-bot`) for user API calls — the admin token only works for `/admin/` endpoints with `X-Admin-API-Key` header.
2. User token expired or database was reset.

**Solution:** Recreate the user token:
```powershell
$admin = @{ 'X-Admin-API-Key' = 'openclaw-meeting-bot'; 'Content-Type' = 'application/json' }
# Check if user exists
Invoke-WebRequest 'http://localhost:8056/admin/users' -Headers $admin -UseBasicParsing
# Create new token
Invoke-WebRequest 'http://localhost:8056/admin/users/1/tokens' -Method POST -Headers $admin -UseBasicParsing
# Update config.json with new token
```

---

### WSL Path Issues with Docker

**Symptom:** Docker compose can't find files at `\\wsl.localhost\Ubuntu\...` paths.

**Cause:** Docker Desktop runs on Windows and cannot access WSL filesystem paths directly in volume mounts.

**Solution:** Copy files from WSL to a Windows-accessible path first:
```powershell
Copy-Item "\\wsl.localhost\Ubuntu\home\zeron\.openclaw\...\whisper_proxy.py" `
    "C:\Users\zeron\AppData\Local\Temp\whisper_proxy.py"
```
Then reference `C:/Users/zeron/AppData/Local/Temp/whisper_proxy.py` in compose volumes.

---

## Diagnostic Commands

```powershell
# Check all container statuses
docker ps --format "table {{.Names}}\t{{.Status}}"

# Check Vexa startup log
docker logs vexa-meeting-bot --tail 50

# Check whisper proxy log (with debug)
docker logs vexa-whisper-proxy --tail 20

# Check whisper model loading
docker logs vexa-whisper --tail 20

# Check if Vexa API is responding
Invoke-WebRequest 'http://localhost:8056/meetings' `
    -Headers @{'X-API-Key'='dGosC39FSoaw0UpIVdhroaz42heFR0ou4bC5yiIc'} -UseBasicParsing

# Check whisper proxy works
Invoke-WebRequest 'http://localhost:8000/v1/models' -UseBasicParsing

# Check bot is active in a specific meeting
(Invoke-WebRequest 'http://localhost:8056/bots/google_meet/pmn-eatb-cyf' `
    -Headers @{'X-API-Key'='...'} -UseBasicParsing).Content
```

## Pending Development Items

| Item | Priority | Notes |
|---|---|---|
| Screen capture / visual analysis | High | Use `pc_control` screenshot tool instead of Vexa (which doesn't capture incoming video) |
| Audio transcription end-to-end test | High | Requires working microphone; pipeline is verified, just needs mic audio input |
| Zoom support | Medium | Requires custom Vexa image with Zoom SDK binaries |
| `launch.py` integration | Medium | Update to use correct compose file path and token |
| Persist compose file | Low | Currently at Windows temp; should be in skill directory accessible to Docker |
| Virtual microphone support | Low | Use VB-Audio VoiceMeeter to route system audio to virtual mic for testing |
