# Google Health API — OAuth setup (one time, ~10 min)

Goal: let `google-health-cli` read **your own** Google Health data (the elliptical sessions your watch logs)
using read-only OAuth. You create a personal Google Cloud project, enable the Google Health API, and authorize
it for your own account in **Testing** mode. No fees, no app review for personal use.

> Use the **same Google account that owns your watch data** (the account your watch syncs to)
> everywhere below.

## 1. Create a project
1. Go to <https://console.cloud.google.com/>.
2. Project dropdown (top bar) → **New Project** → name it `ghealth-personal` → **Create**.
3. Make sure that project is selected.

## 2. Enable the Google Health API
1. <https://console.cloud.google.com/apis/library> → search **"Google Health API"**.
2. Open it → **Enable**.
   - If it won't enable / says you need access or verification to *enable* it →
     **stop and tell Claude** (this is the one scenario we flagged as a risk).

## 3. Configure the consent screen (Google Auth Platform)
1. **APIs & Services → OAuth consent screen** (newer console: **Google Auth Platform → Branding/Audience**).
2. User type: **External** → **Create**.
3. App name: `ghealth-personal`. User support email + developer email: your email.
4. Save through the steps. On the **Audience** / publishing screen, leave
   **Publishing status = Testing**.
5. **Test users → Add users →** your own Google account → Save.
   (Testing mode + you as a test user is what lets you authorize the restricted
   health scopes without a production review.)

## 4. Create an OAuth client
1. **APIs & Services → Credentials → Create Credentials → OAuth client ID**.
2. Application type: **Desktop app**  ← important (gives a client secret +
   loopback redirect, which the loopback login flow needs).
3. Name it `google-health-cli` → **Create**.
4. Copy the **Client ID** and **Client secret** (or download the JSON).

## 5. Point google-health-cli at the client + log in
Put the client id/secret in `config.json`:

```json
{
  "client_id": "PASTE_CLIENT_ID",
  "client_secret": "PASTE_CLIENT_SECRET"
}
```

(Or set `GOOGLE_HEALTH_CLIENT_ID` / `GOOGLE_HEALTH_CLIENT_SECRET` in the environment instead.) Then:

```sh
google-health-cli auth login     # read-only scopes only — there is no write mode
```

`auth login` opens a browser:
1. Sign in as that same Google account.
2. You'll see **"Google hasn't verified this app."** This is expected — it's your
   own project. Click **Advanced → Go to ghealth-personal (unsafe)**.
3. Grant the **read-only** Google Health permissions. The tool requests all six read
   scopes (profile, settings, activity & fitness, health metrics & measurements,
   sleep, nutrition) so it can read every data type — none of them grant write access.

The token is cached locally (owner-only, `0600`) and auto-refreshed on use.

## 6. Confirm
```sh
google-health-cli doctor      # expect  "tokenValid": true
```
Then tell Claude — everything after this runs locally on this machine.

---

### If consent is blocked even as a test user
If step 5 says the app must be verified before you (a test user) can consent,
that's the residual risk we flagged. Options, in order: (a) re-check you're
listed under **Test users** and logging in as that exact account; (b) confirm
the scopes shown are the `googlehealth.*` read scopes; (c) tell Claude — we'd
weigh whether the limited verification is worth it or fall back to manual cardio
logging. We won't force it.
