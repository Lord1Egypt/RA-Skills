# User Configuration

## Pinboard API Authentication

This skill requires a Pinboard API token to read and modify bookmarks.

### Get Your Token

1. Log in to [Pinboard](https://pinboard.in/)
2. Go to **Settings** → **Password** tab
3. Find your **API Token** (format: `username:TOKEN`)

### Configure

Set the environment variable `PINBOARD_AUTH_TOKEN`:

```bash
# In your shell profile (~/.zshrc or ~/.bashrc)
export PINBOARD_AUTH_TOKEN="username:XXXXXXXXXXXXXX"
```

Or pass it directly when running:

```bash
PINBOARD_AUTH_TOKEN="username:XXXXXXXXXXXXXX" claude
```

> **Security note**: The token is passed as a URL query parameter. Treat your API token like a password and rotate it from Pinboard Settings if you believe it has been exposed.

### API Base URL

Default: `https://api.pinboard.in/v1`

All API calls append `?auth_token=$PINBOARD_AUTH_TOKEN&format=json` to requests.

### Rate Limits

Pinboard recommends at most one API call every 3 seconds. The skill handles this automatically by processing in batches with pauses between API calls.
