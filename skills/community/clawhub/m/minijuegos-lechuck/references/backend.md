# Backend — Minijuegos Auth Endpoint

## DB Migration

```sql
ALTER TABLE users ADD COLUMN miniplay_id VARCHAR(64) UNIQUE;
CREATE INDEX idx_users_miniplay_id ON users(miniplay_id);
```

## Token Validation Endpoint

```
GET https://api.minijuegos.com/lechuck/client-js/user/{user_id}/authenticate/
  ?api_id={API_ID}
  &user_token={token}
  &mobile=0
  &locale=es_ES
```

**Response:**
- `{ "status": { "success": true }, "user": { "name": "PlayerName", ... } }` → valid
- HTTP 403 + `{ "status": { "success": false } }` → invalid token

## Express/Node.js Endpoint

```javascript
// POST /api/auth/miniplay
router.post('/miniplay', async (req, res) => {
  const { miniplay_id, token } = req.body;

  if (!miniplay_id || !token) {
    return res.status(400).json({ error: 'Missing miniplay_id or token' });
  }

  // 1. Validate token with Minijuegos API
  // MINIPLAY_API_ID is the public identifier — visible in this URL
  const validateUrl = `https://api.minijuegos.com/lechuck/client-js/user/${miniplay_id}/authenticate/`
    + `?api_id=${process.env.MINIPLAY_API_ID}&user_token=${token}&mobile=0&locale=es_ES`;

  let mpData;
  try {
    const response = await fetch(validateUrl);
    mpData = await response.json();
  } catch (err) {
    return res.status(502).json({ error: 'Could not reach Minijuegos API' });
  }

  if (!mpData?.status?.success) {
    return res.status(403).json({ error: 'Invalid Minijuegos token' });
  }

  // 2. Create or update user
  // email NOT NULL workaround: use synthetic email
  const syntheticEmail = `miniplay_${miniplay_id}@miniplay.local`;
  const username = mpData.user?.name || `Player_${miniplay_id}`;

  const user = await db.query(`
    INSERT INTO users (miniplay_id, email, username)
    VALUES ($1, $2, $3)
    ON CONFLICT (miniplay_id) DO UPDATE
      SET username = EXCLUDED.username, updated_at = NOW()
    RETURNING *
  `, [miniplay_id, syntheticEmail, username]);

  // 3. Return JWT via HttpOnly cookie (more secure than localStorage)
  const jwtPayload = { userId: user.rows[0].id, miniplay_id };
  const token_jwt = jwt.sign(jwtPayload, process.env.JWT_SECRET, { expiresIn: '7d' });

  // Prefer HttpOnly cookie over localStorage to reduce XSS exposure
  res.cookie('session', token_jwt, { httpOnly: true, secure: true, sameSite: 'Lax', maxAge: 7 * 24 * 3600 * 1000 });
  res.json({ user: user.rows[0] });
});
```

## Server-Side Write Operations (MINIPLAY_API_KEY)

`MINIPLAY_API_KEY` is the server-side secret used to sign server-to-server write requests (stats and achievements). It must **never** appear in client bundles, browser code, or URLs.

```javascript
// POST /api/miniplay/stats  — called by your game server after a session ends
router.post('/miniplay/stats', requireAuth, async (req, res) => {
  const { miniplay_id, stats } = req.body;

  // MINIPLAY_API_KEY authorizes server-to-server write calls
  const signature = createHmac('sha256', process.env.MINIPLAY_API_KEY)
    .update(`${miniplay_id}:${stats.kills}:${stats.plays}`)
    .digest('hex');

  // Example: push stats to Minijuegos server-side endpoint
  await fetch(`https://api.minijuegos.com/lechuck/server/user/${miniplay_id}/stats/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Api-Id': process.env.MINIPLAY_API_ID,
      'X-Api-Key': process.env.MINIPLAY_API_KEY,   // ← server-side only
      'X-Signature': signature,
    },
    body: JSON.stringify(stats),
  });

  res.json({ ok: true });
});
```

> If Minijuegos does not offer a server-to-server stats endpoint in your plan, stats and achievements can be sent directly from the client via the LeChuck JS SDK (`lechuck.set_stat()` / `lechuck.unlockAchievement()`). In that case `MINIPLAY_API_KEY` is only needed if your backend validates write requests independently. Confirm with Minijuegos support which model applies to your API tier.

## Frontend: Call the Endpoint

The backend sets the JWT in an **HttpOnly cookie** — the frontend never sees or stores the token.
Use `credentials: 'include'` so the browser sends/receives the cookie cross-origin.

```javascript
async function _mpAuthWithServer(uid, tok) {
  try {
    const response = await fetch('/api/auth/miniplay', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',   // required for cross-origin HttpOnly cookie
      body: JSON.stringify({ miniplay_id: uid, token: tok })
    });
    const data = await response.json();
    // Backend returns { user } — JWT is in the HttpOnly cookie, NOT in data.token
    // Do NOT store the token in localStorage — it's handled server-side
    if (data.user) {
      _showWelcomeHero(data.user.username);
    }
  } catch (err) {
    console.error('Miniplay auth failed:', err);
  }
}
```

## Environment Variables

```env
# MINIPLAY_API_ID — public identifier, used in token validation URL
# (visible in server logs — not a secret, but keep it in env anyway)
MINIPLAY_API_ID=9113

# MINIPLAY_API_KEY — server-side secret, used for write operations (stats/achievements)
# NEVER include in client code, front-end bundles, or validation URLs
MINIPLAY_API_KEY=your_api_key_here

# JWT_SECRET — signs player session tokens; must be strong and kept out of source control
JWT_SECRET=your_jwt_secret_here

# Use dev values during development, update to prod values before publishing
```

> **Important:** `MINIPLAY_API_ID` is used in the token validation `GET` URL — it appears in request logs.
> `MINIPLAY_API_KEY` is the write-access secret and must only exist on the server.
> These are two different credentials with different sensitivity levels.
