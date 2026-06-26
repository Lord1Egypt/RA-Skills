# Configuration

## Optional breach-check setup

This skill can optionally use the Have I Been Pwned API for email breach checks.

### Required variable
- `HIBP_API_KEY`

Example:
```bash
export HIBP_API_KEY="your_hibp_api_key"
```

### Optional local secret file
You can also store the key in a local private file such as:
- `~/.openclaw/secrets/hibp_api_key`

Example:
```bash
mkdir -p ~/.openclaw/secrets
printf '%s\n' 'your_hibp_api_key' > ~/.openclaw/secrets/hibp_api_key
chmod 600 ~/.openclaw/secrets/hibp_api_key
```

## Resolution order
When implementing breach checks, prefer:
1. `HIBP_API_KEY`
2. `~/.openclaw/secrets/hibp_api_key`
3. explicit user-provided key only if necessary

## HIBP endpoint
Typical endpoint pattern:
- `https://haveibeenpwned.com/api/v3/breachedaccount/{email}`

Use the provider documentation for required headers and rate-limit handling.
