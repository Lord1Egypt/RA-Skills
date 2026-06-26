# Setup & Installation Guide

## Prerequisites

| Requirement | Version | Location |
|---|---|---|
| Docker Desktop | Latest | `C:\Program Files\Docker\Docker\` |
| Conda environment | `meeting-assistant` | `D:\program\codesupport\anaconda\envs\meeting-assistant\` |
| Python (conda env) | 3.11+ | `D:\program\codesupport\anaconda\envs\meeting-assistant\python.exe` |
| anthropic SDK | 0.84.0+ | Installed in conda env |
| WSL2 Ubuntu | Any | For running Claude Code |

## Step 1: Prepare Docker Compose File

The docker-compose.yml in the skill directory is the source of truth, but Docker
must run it from a **Windows path** (not a WSL path). Copy it to Windows temp:

```powershell
Copy-Item "\\wsl.localhost\Ubuntu\home\zeron\.openclaw\workspace\skills\meeting-assistant\docker-compose.yml" `
    "C:\Users\zeron\AppData\Local\Temp\vexa-compose.yml"
```

**Important**: The compose file must also include the whisper proxy service.
See the [full compose file](#docker-compose-reference) below.

## Step 2: Start Infrastructure

```powershell
$env:PATH += ';C:\Program Files\Docker\Docker\resources\bin'
docker compose -f C:\Users\zeron\AppData\Local\Temp\vexa-compose.yml up -d
```

Wait ~30 seconds for all services to become healthy:

```powershell
docker ps --format "table {{.Names}}\t{{.Status}}"
# Expected:
# vexa-meeting-bot     Up X seconds (healthy)
# vexa-whisper-proxy   Up X seconds
# vexa-whisper         Up X seconds
# vexa-postgres        Up X seconds (healthy)
```

## Step 3: Create Vexa User Token

This is a one-time setup. The token is already created and stored in `config.json`.

If you need to recreate it:

```powershell
# 1. Create user (admin endpoint)
$headers = @{ 'X-Admin-API-Key' = 'openclaw-meeting-bot'; 'Content-Type' = 'application/json' }
Invoke-WebRequest -Uri 'http://localhost:8056/admin/users' -Method POST `
    -Headers $headers -Body '{"email":"agent@openclaw.ai"}' -UseBasicParsing

# 2. Create token for user ID 1
Invoke-WebRequest -Uri 'http://localhost:8056/admin/users/1/tokens' -Method POST `
    -Headers $headers -UseBasicParsing
# Save the returned token to config.json → bot.vexa_api_key
```

Current token: `dGosC39FSoaw0UpIVdhroaz42heFR0ou4bC5yiIc`

## Step 4: Verify Setup

```powershell
$h = @{ 'X-API-Key' = 'dGosC39FSoaw0UpIVdhroaz42heFR0ou4bC5yiIc' }
(Invoke-WebRequest 'http://localhost:8056/bots/status' -Headers $h -UseBasicParsing).Content
# Expected: {"running_bots":[]}
```

## Docker Compose Reference

The complete docker-compose.yml with all required services:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: vexa-postgres
    environment:
      - POSTGRES_USER=vexa
      - POSTGRES_PASSWORD=vexa_pass
      - POSTGRES_DB=vexa
    volumes:
      - vexa_pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U vexa"]
      interval: 5s
      timeout: 3s
      retries: 5
    restart: unless-stopped

  whisper:
    image: fedirz/faster-whisper-server:latest-cpu
    container_name: vexa-whisper
    environment:
      - WHISPER__MODEL=Systran/faster-whisper-base
      - WHISPER__LANGUAGE=zh
    restart: unless-stopped

  whisper-proxy:
    image: python:3.11-slim
    container_name: vexa-whisper-proxy
    ports:
      - "8000:8000"
    volumes:
      - C:/Users/zeron/AppData/Local/Temp/whisper_proxy.py:/proxy.py:ro
    command: python3 /proxy.py
    depends_on:
      - whisper
    restart: unless-stopped

  vexa:
    image: vexaai/vexa-lite:latest
    container_name: vexa-meeting-bot
    ports:
      - "8056:8056"
    environment:
      - DATABASE_URL=postgresql://vexa:vexa_pass@postgres:5432/vexa
      - ADMIN_API_TOKEN=openclaw-meeting-bot
      - TRANSCRIPTION_ENABLED=true
      - TRANSCRIBER_URL=http://whisper-proxy:8000/v1/audio/transcriptions
      - REMOTE_TRANSCRIBER_URL=http://whisper-proxy:8000/v1/audio/transcriptions
      - TRANSCRIBER_API_KEY=openclaw-key
      - REMOTE_TRANSCRIBER_API_KEY=openclaw-key
      - ZOOM_CLIENT_ID=YZXafYz5STiVV3qbh2Sh0w
      - ZOOM_CLIENT_SECRET=IlvPhToAqWorTeW3qLLNUTnF9I1ItxUs
    depends_on:
      postgres:
        condition: service_healthy
      whisper-proxy:
        condition: service_started
    restart: unless-stopped

volumes:
  vexa_pgdata:
```

**Note**: The `whisper_proxy.py` file must be at `C:\Users\zeron\AppData\Local\Temp\whisper_proxy.py`
on the Windows host. Copy it from `scripts/whisper_proxy.py` if missing.

## Environment Variables Summary

| Variable | Value | Purpose |
|---|---|---|
| `ADMIN_API_TOKEN` | `openclaw-meeting-bot` | Vexa admin API authentication |
| `ZOOM_CLIENT_ID` | `YZXafYz5STiVV3qbh2Sh0w` | Zoom Marketplace app credential |
| `ZOOM_CLIENT_SECRET` | `IlvPhToAqWorTeW3qLLNUTnF9I1ItxUs` | Zoom Marketplace app credential |
| `TRANSCRIBER_URL` | `http://whisper-proxy:8000/v1/audio/transcriptions` | Route audio through proxy |
| `WHISPER__MODEL` | `Systran/faster-whisper-base` | Faster-whisper model to preload |
| `ANTHROPIC_API_KEY` | (from Claude Code environment) | Only needed for standalone mode |

## Conda Environment

The `meeting-assistant` conda environment must have:

```
anthropic>=0.84.0
requests
```

Install if missing:
```powershell
D:\program\codesupport\anaconda\envs\meeting-assistant\python.exe -m pip install anthropic requests
```

## Stopping Everything

```powershell
$env:PATH += ';C:\Program Files\Docker\Docker\resources\bin'
docker compose -f C:\Users\zeron\AppData\Local\Temp\vexa-compose.yml down
```

To also remove stored recordings/database:
```powershell
docker compose -f C:\Users\zeron\AppData\Local\Temp\vexa-compose.yml down -v
```
