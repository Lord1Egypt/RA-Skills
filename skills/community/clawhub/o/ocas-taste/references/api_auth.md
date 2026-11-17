# API authentication patterns

This document holds service-specific OAuth and API-auth code that taste needs
for Gmail, Google Calendar, and Spotify access. These patterns materially
affect correctness, which is why they live here as Python rather than prose.
Long-term this content belongs in the shared `ocas-auth` skill; taste holds it
until that skill lands.

## Gmail API credential loading (multi-profile)

`himalaya` is not installed in the target environment and cannot be installed
(no cargo/Rust toolchain, PEP 668 blocks pip). Email scanning must use the
Gmail API directly via `google.oauth2.credentials.Credentials`.

Key detail: the token file uses key `token`, not `access_token`, for the
OAuth access token. Pass `token=token_data.get('token')` when building
`Credentials`. The `gmail.readonly` scope is sufficient for scanning.

Tokens can live under either the user profile or the agent profile. Never
use the agent profile for email scanning — it has no consumption emails.
Always try the user token first and fall back to the agent token only for
calendar if the primary is missing.

### Token file locations

This system uses a single centralized Google auth helper at `<hermes-home>/scripts/google_auth.py`. All standalone Python scripts import from it:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('<hermes-home>/scripts')))
from google_auth import get_service, get_gmail_service, get_drive_service, get_calendar_service, get_people_service
```

The helper handles token refresh automatically. Credentials are stored at `Google OAuth credentials`.

### Two Google accounts

- **<operator>'s account** (`<user-google-email>`): Used for user data (email, calendar, contacts, Drive). OAuth client in <operator>'s own Google Cloud project.
- **the agent's account** (`<agent-email>`): Used for agent operations (sending email as the agent, agent's own calendar). OAuth client in the agent's own Google Cloud project.

Each account has its own OAuth client in its own Google Cloud project. Never mix them.

### Recovery when tokens are revoked

If refresh fails with `invalid_grant`, the token is definitively dead. Re-authorize with:

```bash
python3 <hermes-home>/skills/infrastructure/google-workspace-auth/scripts/google_oauth_init.py
```

### Known pitfall: Calendar API scope not in token

If `build('calendar', 'v1', credentials=creds)` raises `googleapiclient.errors.UnknownApiNameOrVersion`, the OAuth token lacks calendar scope. Both accounts now have full calendar scopes — if this error occurs, the token file may be stale. Delete it and re-authorize.

## Spotify OAuth (Spotipy)

Spotify app credentials are loaded from environment, not hardcoded in
scripts. Set `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` in
`~/.hermes/.env`:

```
SPOTIFY_CLIENT_ID=<client_id_from_developer_dashboard>
SPOTIFY_CLIENT_SECRET=<client_secret_from_developer_dashboard>
```

`hermes mcp call` does not exist — the Hermes MCP CLI only supports `add`,
`remove`, `list`, `serve`, `test`, and `configure`. For programmatic Spotify
access from cron scripts, use Spotipy directly with a cached OAuth token:

```python
import os, spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]

sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=str(CACHE_FILE),
)
token_info = sp_oauth.get_cached_token()
sp = spotipy.Spotify(auth=token_info['access_token'])

results = sp.current_user_recently_played(limit=50)
top_tracks = sp.current_user_top_tracks(limit=20, time_range='short_term')
```

### Known pitfall: Spotify token has no refresh_token

The `.cache` file at `{agent_root}/commons/data/ocas-taste/.cache` may contain
an expired `access_token` with no `refresh_token`. All four auth approaches
(Spotipy cached token, MCP JSON-RPC, Client Credentials, browser automation)
fail headlessly because Spotify's user-data endpoints require the OAuth
Authorization Code flow with interactive browser login.

Resolution: the user runs `npx @darrenjaws/spotify-mcp setup` in a
browser-accessible environment, which writes tokens to
`~/.spotify-mcp/tokens.json`. Gate the cron job on a valid-token check to
avoid repeated failed runs.

### Spotify history puller script

The active script is `scripts/spotify_history_puller.py` (not MCP). It uses
the Spotify Web API directly with OAuth refresh token. Env vars are loaded
from `~/.hermes/.env`. The script now reports which specific credentials are
missing vs present in its error message, making it clear when only
`SPOTIFY_REFRESH_TOKEN` is absent.

Script location: `{skill_root}/scripts/spotify_history_puller.py`
Data output: JSON to stdout (array of track objects)
Errors: stderr with missing-credential details, exit code 1