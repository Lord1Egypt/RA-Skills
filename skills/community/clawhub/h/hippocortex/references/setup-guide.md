# Hippocortex Setup Guide

## Cloud (Recommended)

1. Go to https://dashboard.hippocortex.dev
2. Create an account and generate an API key
3. Set your environment variable:
   ```bash
   export HIPPOCORTEX_API_KEY="hx_live_..."
   ```
4. The default base URL is `https://api.hippocortex.dev` -- no need to set it unless using self-hosted

## Self-Hosted

Hippocortex can run on your own infrastructure. Use this when you need full data control or air-gapped operation.

### Docker Compose

```bash
git clone https://github.com/hippocortex/hippocortex-os.git
cd hippocortex-os
cp .env.example .env
# Edit .env with your configuration
docker compose up -d
```

### Environment Variables (Self-Hosted Server)

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | required |
| REDIS_URL | Redis connection string | optional |
| API_PORT | Port for the API server | 3100 |
| JWT_SECRET | Secret for token signing | required |

### Point Your Agent to Self-Hosted

Set the base URL to your self-hosted instance:

```bash
export HIPPOCORTEX_API_KEY="your-self-hosted-key"
export HIPPOCORTEX_BASE_URL="http://localhost:3100"
```

Or in `.hippocortex.json`:

```json
{
  "apiKey": "your-self-hosted-key",
  "baseUrl": "http://localhost:3100",
  "sessionId": "my-agent"
}
```

## Configuration File Reference

The `.hippocortex.json` file supports these fields:

| Field | Type | Required | Default |
|-------|------|----------|---------|
| apiKey | string | yes | -- |
| baseUrl | string | no | https://api.hippocortex.dev |
| sessionId | string | no | "openclaw" |

Place this file in your OpenClaw workspace root (`~/.openclaw/workspace/.hippocortex.json`).

## Verifying Setup

Test your configuration by running a synthesize call:

```bash
curl -s -X POST "${HIPPOCORTEX_BASE_URL:-https://api.hippocortex.dev}/v1/synthesize" \
  -H "Authorization: Bearer $HIPPOCORTEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "test", "query": "hello", "maxTokens": 100}'
```

A successful response returns a JSON object with a `memories` array (empty on first run).

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 401 Unauthorized | Check that HIPPOCORTEX_API_KEY is set and valid |
| Connection refused | Verify HIPPOCORTEX_BASE_URL points to a running instance |
| Empty memories | Expected on first use -- capture some conversations first |
| Timeout errors | Check network connectivity; self-hosted: verify the server is running |
