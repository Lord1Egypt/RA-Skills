# Resy

**Status:** ⚠️ Working (auth-dependent)
**Last tested:** 2026-04-03
**Method:** REST API with token auth (recommended); browser automation fallback (unauthenticated venues only)

---

## Overview

Resy's API requires authentication for most restaurants. Unauthenticated browser automation works for
some venues (e.g. 7 Adams) but returns empty results for popular or auth-gated restaurants (e.g. Copra).

The reliable approach: exchange credentials for an auth token, use it against the REST API.
Token is cached for 12 hours to avoid repeated auth requests.

**Credentials are portable across machines via environment variables** — no machine-local session file needed.

---

## Setup

Set three environment variables (add to `~/.zshrc`, `~/.bashrc`, or `.env`):

```bash
export RESY_API_KEY="your-api-key"       # From your Resy account or shared widget key
export RESY_EMAIL="you@example.com"      # Resy account email
export RESY_PASSWORD="yourpassword"      # Resy account password
```

Without these, `scripts/resy.py` falls back to unauthenticated browser automation with a warning.

---

## Token flow

1. Check for cached token in `{agent_root}/commons/data/ocas-spot/resy-token.json`
2. If cached and not expired (12h TTL), use it
3. Otherwise: `POST api.resy.com/3/auth/password` → token string
4. Cache token with `expires_at = now + 43200`

**Auth request:**
```
POST https://api.resy.com/3/auth/password
Authorization: ResyAPI api_key="{api_key}"
Content-Type: application/x-www-form-urlencoded

email=...&password=...
```

**Response:**
```json
{ "token": "...", ... }
```

---

## API reference

### Venue ID lookup

```
GET https://api.resy.com/3/venue?url_slug={slug}&location={city_slug}
Authorization: ResyAPI api_key="{api_key}"
X-Resy-Auth-Token: {token}
```

Returns JSON with `.venue.id.resy` — the numeric venue ID required for availability queries.

### Availability check

```
GET https://api.resy.com/4/find?day={YYYY-MM-DD}&party_size={N}&venue_id={id}
Authorization: ResyAPI api_key="{api_key}"
X-Resy-Auth-Token: {token}
```

Returns `.results.venues[].slots[].date.start` — ISO datetime strings. Time is at characters [11:16].

---

## Implementation

**File:** `scripts/resy.py`

```python
# Authenticated path (requires env vars)
token = get_token()          # Fetches or returns cached token
venue_id = _resolve_venue_id(slug, city, token, api_key)
result = _check_api(venue_id, date, party_size, token, api_key)

# Unauthenticated fallback (some venues only)
result = _check_browser(slug, date, party_size, city)
```

---

## Tested

| Restaurant | Date | Method | Result |
|---|---|---|---|
| 7 Adams | 2026-03-31 | Browser (unauth) | ✅ Available |
| Copra | 2026-04-03 | Browser (unauth) | ❌ Empty (auth required) |
| Copra | — | API (auth) | ✅ Expected working |

---

## Key findings

1. **Browser automation unreliable for popular venues** — auth-gated restaurants return no slots
2. **API auth works** — `POST /3/auth/password` returns a long-lived token (~12h)
3. **Token is portable** — stored in `{agent_root}/commons/data/ocas-spot/resy-token.json`, valid across machines when credentials are set
4. **Venue ID required for API** — slug alone is not enough; use `/3/venue?url_slug=...` to resolve
5. **URL parameters still needed for browser fallback** — `?date=YYYY-MM-DD&seats=N`

---

## Rejected methods

| Method | Result |
|--------|--------|
| Unauthenticated API | HTTP 419 |
| Browser automation (no auth) | Works only for some venues |
| Machine-local session file | Not portable across systems |

---

## Related

- See `square.md` for similar SPA browser patterns
- See `sevenrooms.md` for widget-based booking flow
- See `opentable.md` for session persistence approach (single-machine only)