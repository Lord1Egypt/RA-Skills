# Security Notes

This skill is designed to bridge OpenClaw with Manus task APIs.

## Credentials

- The package intentionally does **not** include `MANUS_API_KEY`.
- Each user must configure credentials locally in `~/.config/manus-openclaw-bridge/manus.env`.

## Download safety

The collector script validates file download URLs before fetching them.

Allowed rules:
- scheme must be `https`
- host must match a Manus-controlled allowlist

If a returned URL does not satisfy those rules, the script will not download it.

## Packaging guidance

Before publishing:
- ensure no `.env` or secret files are bundled
- keep API keys out of docs, scripts, and examples
- prefer least-privilege runtime environments when running task collectors
