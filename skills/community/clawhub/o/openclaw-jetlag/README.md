# openclaw-jetlag

Scans your Google Calendar for upcoming flights, calculates the timezone shift, and writes a personalized circadian adjustment plan back to your calendar. No manual input — it reads your existing flight events and does everything automatically.

**What gets written:** Detects your flights automatically, generates a circadian adjustment plan, writes 14+ events to your Google Calendar with reminders — bedtime shifts, light exposure windows, melatonin timing, and arrival-day strategy.

---

## Setup

### Path 1 — OpenClaw users (you're probably here)

You already have Google OAuth credentials from your OpenClaw setup. Ask your Claw bot:

> "What is your Google Client ID and Secret from your config?"

Then:

```bash
git clone https://github.com/chadholdorf/openclaw-jetlag.git
cd openclaw-jetlag
npm install
cp .env.example .env
```

Open `.env` and paste in the values your Claw bot gave you:

```
GOOGLE_CLIENT_ID=<your client ID>
GOOGLE_CLIENT_SECRET=<your client secret>
```

```bash
node index.js
```

On the first run a browser window opens — sign in, click **Allow**, paste the code back into the terminal. Done. Your calendar will have the plan within seconds.

---

### Path 2 — Fresh setup (no OpenClaw)

**Requirements:** Node.js 18+. Check with `node --version`. Download at https://nodejs.org if needed.

#### Step 1 — Clone and install

```bash
git clone https://github.com/chadholdorf/openclaw-jetlag.git
cd openclaw-jetlag
npm install
cp .env.example .env
```

#### Step 2 — Create a Google Cloud project

1. Go to [console.cloud.google.com](https://console.cloud.google.com) and sign in.
2. Click the project dropdown (top-left) → **New Project** → give it any name (e.g. `jetlag`) → **Create**.
3. Make sure the new project is selected in the top-left dropdown before continuing.

#### Step 3 — Enable the Google Calendar API

1. Left sidebar → **APIs & Services → Library**.
2. Search `Google Calendar API` → click the result → **Enable**.

#### Step 4 — Configure the OAuth consent screen

1. Left sidebar → **APIs & Services → OAuth consent screen**.
2. Choose **External** → **Create**.
3. Fill in the required fields: App name (anything), User support email, Developer contact email.
4. Click **Save and Continue** through the Scopes page (no changes needed).
5. On **Test users** → **+ Add Users** → enter your Google account email → **Add** → **Save and Continue**.
6. Click **Back to Dashboard**.

#### Step 5 — Create OAuth credentials

1. Left sidebar → **APIs & Services → Credentials**.
2. **+ Create Credentials → OAuth 2.0 Client ID**.
3. Application type: **Desktop app** → give it any name → **Create**.
4. Copy the **Client ID** and **Client Secret** from the dialog that appears.
5. Open `.env` and paste them in:

```
GOOGLE_CLIENT_ID=<paste Client ID here>
GOOGLE_CLIENT_SECRET=<paste Client Secret here>
```

#### Step 6 — Run it

```bash
node index.js
```

A browser window opens (or a URL is printed if the browser can't open automatically). Sign in, click **Allow**, paste the code back into the terminal. Authorization is saved to `.oauth-token.json` — subsequent runs skip this step entirely.

---

## Using as an OpenClaw Skill

Symlink or copy `~/openclaw-jetlag` into your OpenClaw skills directory so Claw picks it up.

**One-time prerequisite:** run `node index.js` manually once to complete the OAuth browser flow. Claw can't do that interactively — but once `.oauth-token.json` exists, it takes over from there.

Then just message your bot: **"check my flights"** or **"run jetlag planner"**. Claw will run the planner and report back which flights were detected and how many calendar events were created.

---

## How it works

- Scans the next 90 days of your primary Google Calendar
- Detects flights from United, Delta, American, Southwest, and 20+ other airlines
- Skips short hops with under a 2-hour timezone difference
- Generates a 1–5 day adjustment plan scaled to the size of the shift
- Writes all events back to your calendar automatically with reminders

### How plans are scaled

| Timezone shift | Runway before departure | Melatonin |
|---|---|---|
| 2–3 hours | 1 day | No |
| 4–6 hours | 2 days | Yes |
| 7–9 hours | 3 days | Yes |
| 10+ hours (e.g. SFO → India) | 5 days | Yes |

---

## Troubleshooting

**Flight not detected**
Google Calendar auto-imports flights from Gmail confirmation emails. The event title needs to include the airline name and route — e.g. `United Airlines flight SFO to ORD` or `Delta: JFK → LAX`. If your event title looks different, rename it to include the airline and the 3-letter airport codes.

**Auth error / token expired**
Delete the saved token and re-run:
```bash
rm .oauth-token.json && node index.js
```

**Want to add an airport**
Edit the `AIRPORT_TZ` map near the top of `index.js` — add a `'XXX': 'Region/City'` entry using the airport's IATA code and a valid [tz database name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

---

## License

MIT
