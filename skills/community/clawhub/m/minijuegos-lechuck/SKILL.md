---
name: minijuegos-lechuck
description: "Integrate Minijuegos.com (Miniplay) LeChuck JS SDK into HTML5 games. Use when a user wants to: (1) add Minijuegos/Miniplay platform integration to a game, (2) authenticate players via the LeChuck SDK, (3) implement achievements, stats, or leaderboards for Minijuegos.com, (4) troubleshoot LeChuck SDK issues (missing user ID, params lost on redirect, data not sent on game over), (5) register Minijuegos users in a custom backend. Covers full auth flow, nginx config, backend endpoint, achievements, stats, leaderboard, and the critical death/game-over data flush fix. Required env vars: MINIPLAY_API_ID (public numeric ID from Minijuegos dev panel), MINIPLAY_API_KEY (server-side secret for write operations — never expose in client code), JWT_SECRET (for signing session tokens)."
metadata:
  requirements:
    env:
      - name: MINIPLAY_API_ID
        description: "Public numeric ID from Minijuegos dev panel. Used in the token validation URL — visible in server logs, not a secret."
        required: true
      - name: MINIPLAY_API_KEY
        description: "Server-side secret from Minijuegos dev panel. Required for write operations (stats, achievements). Never expose in client code, URLs, or source control."
        required: true
      - name: JWT_SECRET
        description: "Secret for signing JWT session tokens for authenticated players. Must be strong and kept out of source control."
        required: true
---

# Minijuegos.com — LeChuck SDK Integration

## Setup

Add the SDK to your HTML `<head>`. This is a **third-party vendor script** from Minijuegos — only load it from the official domain:

```html
<!-- Official Minijuegos/Miniplay SDK — verify this URL with your Minijuegos contact -->
<script src="https://ssl.minijuegosgratis.com/lechuck/js/latest.js"></script>
```

## Auth Flow

Minijuegos embeds the game in an iframe with this URL:
```
https://yourgame.com/?mp_api_user_id=X&mp_api_user_token=Y&...
```

The SDK reads these params automatically. Listen for the ready event:

```javascript
LeChuckAPI.events.onApiReady(function() {
  const uid = lechuck.user.getId();
  const tok = lechuck.user.getToken();
  if (uid) {
    // User is logged in — authenticate with your backend
    _mpAuthWithServer(uid, tok);
  }
});
```

> ⚠️ `lechuck.getUser()` does NOT exist. Always use `lechuck.user.getId()` and `lechuck.user.getToken()`.

> ⚠️ In dev/unpublished games Minijuegos does NOT inject `mp_api_user_id` — uid will be null until the game is published.

## Nginx — Critical: Preserve Query Params on Redirect

If you redirect `/` → `/game/`, you MUST preserve query params or the SDK starts without a user:

```nginx
# ❌ WRONG — loses ?mp_api_user_id=X&...
location = / { return 301 /game/; }

# ✅ CORRECT
location = / { return 301 /game/$is_args$args; }
```

Also use `credentialless` COEP (not `require-corp`) — `require-corp` blocks external SDKs:
```nginx
location /game/ {
  add_header Cross-Origin-Embedder-Policy "credentialless";
  add_header Cross-Origin-Opener-Policy "same-origin";
}
```

## Backend: Register Minijuegos Users

Validate the token server-side before creating a user. See `references/backend.md` for the full endpoint, DB schema, and where `MINIPLAY_API_KEY` is used.

Key points:
- Validate token: `GET https://api.minijuegos.com/lechuck/client-js/user/{uid}/authenticate/?api_id=XXXX&user_token={tok}&mobile=0&locale=es_ES`
- If `status.success = true` → valid; HTTP 403 with `status.success = false` → invalid
- If `email` is NOT NULL in your DB, use a synthetic email: `miniplay_{uid}@miniplay.local`
- Add `miniplay_id VARCHAR(64) UNIQUE` column to your users table
- Backend returns JWT via **HttpOnly cookie** (not in response body); frontend must use `credentials: 'include'`

## Achievements

```javascript
// Unlock an achievement by UID — client-side via LeChuck SDK
function _mpUnlockAchievement(uid) {
  if (typeof lechuck !== 'undefined' && lechuck.unlockAchievement) {
    lechuck.unlockAchievement(uid);
  }
}
```

Achievement images: PNG 64×64, hosted on your server. Register UIDs in the Minijuegos dev panel.

## Stats

Stats are type REPLACE (send accumulated totals, not deltas):

```javascript
lechuck.set_stat('kills', totalKills);    // total kills ever
lechuck.set_stat('plays', totalPlays);   // total games played
lechuck.set_stat('wins', totalWins);
// etc.
```

## Leaderboard

```javascript
lechuck.set_score(score);  // call once per game session
```

## ⚠️ Critical: Flush Data Before Game Over / Restart

The LeChuck SDK sends data via async HTTP requests. If the game resets immediately after calling the SDK, the browser cancels in-flight requests and data is lost.

**Use `navigator.sendBeacon` when possible** (fires even on page unload), or fall back to a `setTimeout` guard:

```javascript
function gameOver(finalStats) {
  // 1. Send all data to SDK
  lechuck.set_score(finalStats.score);
  lechuck.set_stat('kills', finalStats.totalKills);
  finalStats.newAchievements.forEach(uid => _mpUnlockAchievement(uid));

  // 2. Guard: wait for requests before resetting
  // sendBeacon is fire-and-forget safe on unload; setTimeout is a best-effort fallback.
  // 500ms covers most network conditions but is not a guarantee — avoid immediate reloads.
  setTimeout(function() {
    showGameOverScreen();
  }, 500);
}
```

> Note: `setTimeout` is a pragmatic fix — it handles the majority of cases but can fail on very slow connections. If data reliability is critical, implement a server-side session endpoint instead of relying on client-side SDK calls at game over.

## Portal Detection

To show the correct login prompt (Miniplay vs Minijuegos):

```javascript
// Use var (not const/let) — needs to be accessible outside try{}
var _portal = 'unknown';
try {
  const a = window.location.ancestorOrigins;
  if (a && a.length) {
    if (a[0].includes('miniplay.com')) _portal = 'miniplay';
    else if (a[0].includes('minijuegos.com')) _portal = 'minijuegos';
  }
  if (_portal === 'unknown' && document.referrer) {
    if (document.referrer.includes('miniplay.com')) _portal = 'miniplay';
    else if (document.referrer.includes('minijuegos.com')) _portal = 'minijuegos';
  }
} catch(e) {}
```

## Tokens: Dev vs Prod

Dev API_ID/API_KEY ≠ Prod. Update credentials in your `.env` when publishing.

## References

- Full backend endpoint + DB migration + `MINIPLAY_API_KEY` usage: `references/backend.md`
- All 17 achievement UIDs and stat definitions: `references/achievements.md`
