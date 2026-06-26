# Requirements

## Runtime dependencies

- OpenClaw
- Bash
- curl
- Python 3.9+
- Node.js 18+ (required for slides JSON -> PPTX conversion)

## Required configuration

Create this file on each machine:

`~/.config/manus-openclaw-bridge/manus.env`

Example:

```bash
MANUS_API_KEY='your-manus-api-key'
MANUS_AGENT_PROFILE='manus-1.6'
MANUS_TASK_MODE='agent'
MANUS_API_BASE='https://api.manus.ai'
```

## Security model

- No secrets are included in the package.
- `MANUS_API_KEY` must be supplied locally by each installer.
- `MANUS_API_BASE` must be explicitly set locally and must use HTTPS.
- Downloaded result files are only fetched from HTTPS URLs on an allowlisted set of Manus-controlled hosts.
- Redirect targets are validated again after the HTTP request is opened.
- If Manus returns a file URL outside the allowlist, the downloader will refuse to fetch it and will record a `download_error` instead.
