---
name: openpot-awareness
description: Teaches this agent how to serve content to the OpenPot iOS client — cards, apps, page captures, calendar, voice, chat persistence, and onboarding
emoji: 🫕
version: 6.0.0
homepage: https://openpot.app
---

# OpenPot Awareness Skill

You are connected to **OpenPot** — a native iOS app that serves as a
command center for AI agents. OpenPot has configurable tabs: **Chat**
(always on), **Pulse** (notification cards), **Calendar**, **Apps**,
**Terminal**, and **Agents** (always on). Users choose which tabs to
display in Settings — not every user will have all tabs visible.

## Three Output Surfaces

| Surface | When to use | How |
|---------|-------------|-----|
| Chat | Default. Conversations, answers, follow-ups. | Normal chat response |
| Pulse cards | Proactive output: reports, alerts, briefs. | `POST /api/cards` |
| Web apps | Persistent tools the user returns to. | Build HTML, serve via `/api/apps` |

**Default to chat.** Use cards for output the user did not ask for in
the current conversation. Use apps only when the user requests a
persistent tool.

## Decision Framework — Chat vs. Card vs. App

| Situation | Surface | Why |
|-----------|---------|-----|
| User asked a question | Chat | They're in a conversation. Answer there. |
| Cron job produced output | Card | User didn't ask. Push it to Pulse. |
| Alert threshold crossed | Card | Proactive. User needs to know. |
| User asked for a persistent tool | App | They want something that lives in their toolkit. |
| User asked about a previous card | Chat | They're referencing it in conversation. |
| Scheduled digest or rollup | Card | Proactive summary, not a conversation. |

**When in doubt, use chat.** Cards and apps are for specific use cases.

## Triggers

Activate this skill when:

- User says **"OpenPot sync"** — run the sync process (see Sync section)
- User sends a **page capture** (message contains
  `---PAGE CAPTURE CONTEXT---`) — see Page Captures section
- User asks about **setting up OpenPot** — see Onboarding section
- User asks about **calendar**, **voice**, **chat persistence**, or
  **building an app** — see the relevant section below
- User asks **"what OpenPot features do I support?"** — check status
- User asks to **"set up chat persistence"** or **"save my chats"** —
  see Chat Persistence section

---

# Pulse Cards

Pulse cards are proactive notifications you push to the user's OpenPot
app. They appear in the Pulse tab as a card stream.

## When to Create a Card

- Scheduled output (cron jobs): morning briefs, DCA signals, health checks
- Threshold alerts: a metric crossed a boundary the user cares about
- Proactive observations: something changed that the user should know
- Digests: summaries of activity over a time period

Do NOT create a card for content the user asked for in the current
conversation. That belongs in chat.

## Card API

**Endpoint:** `POST /api/cards`

**Required fields:**

| Field | Type | Description |
|-------|------|-------------|
| title | String | Card headline. Under 60 characters. |
| body | String | 1-2 line summary visible on the compact card. |
| category | String | Determines Pulse channel routing. Use canonical list below. |
| agent_id | String | Your agent ID. |

**Optional fields:**

| Field | Type | Description |
|-------|------|-------------|
| priority | String | `"normal"` (default) or `"high"`. Reserve high for genuinely urgent items. |
| origin | String | Why this card was created: `"cron"`, `"alert"`, `"agent_initiated"`, `"announce"`. |
| expanded_body | String | Full markdown report. When present, the card is tappable and opens a detail view. |
| actions | [String] | Action buttons in the detail view. Vocabulary: `"discuss"`, `"dismiss"`, `"acknowledge"`, `"snooze"`. |

## Body Text Rule

The `body` field is ALWAYS a complete thought. Never a sentence fragment
that leaves the user wondering what the rest says. If the body is cut
off mid-sentence, the card feels broken.

- Short notifications (1-2 lines): write the complete message
- Medium content (4-10 lines): write the full text — OpenPot unfolds it inline
- Reports with tables/sections: keep body as 1-2 line summary, put detail in expanded_body

## Minimal Card Example

```json
{
  "title": "System Health Check",
  "body": "All services operational. CPU 23%, memory 41%.",
  "category": "system",
  "agent_id": "your-agent-id",
  "priority": "normal",
  "origin": "cron"
}
```

## Report Card Example (with expanded detail)

```json
{
  "title": "Weekly DCA Signals",
  "body": "5 double-down signals, 4 baseline holds.",
  "category": "finance",
  "agent_id": "your-agent-id",
  "priority": "normal",
  "origin": "cron",
  "expanded_body": "## Weekly DCA Signal Report\n\n**Generated:** Monday 4:30 PM ET\n\n| Ticker | Price | Signal | Conviction |\n|--------|-------|--------|------------|\n| CRCL | $2.14 | Double-down | High |\n| AFRM | $41.30 | Double-down | Medium |\n\n4 baseline holds. Market weakness = accumulation window.",
  "actions": ["discuss", "dismiss"]
}
```

## Canonical Category List

Use these exact strings. Inconsistent casing or synonyms create
duplicate channels.

| Category | Use for |
|----------|---------|
| briefing | Morning briefs, evening summaries, weekly rollups |
| system | Health checks, service status, uptime reports |
| finance | DCA signals, portfolio updates, market observations |
| calendar | Schedule digests, conflict alerts, deadline warnings |
| projects | Task updates, milestone tracking, blockers |
| education | Learning content, research summaries |
| health | Health tracking, medication reminders |
| entertainment | Media recommendations, leisure suggestions |

You may create new categories when the user's needs expand. When you
do, include a note in your first card: "I've created a new Pulse
channel for [topic]. You can rename or reorganize it."

## Expanded Cards (Tap-to-Open Detail)

When a card represents a report, include an `expanded_body` field
with the full markdown content.

- Keep `body` as a 1-2 line summary (the compact card preview).
- Put the full analysis in `expanded_body` using markdown.
- Include `"actions": ["discuss", "dismiss"]` for report cards.
- Cards without `expanded_body` are glanceable only.
- Keep total expanded_body under 4,000 characters.

**Cards that SHOULD have expanded_body:** DCA signal reports, morning
briefs, system health diagnostics, any multi-item analysis or report.

**Cards that should NOT:** Simple reminders, single-fact notifications,
calendar alerts.

## Action Buttons

| Action | Button Label | Behavior |
|--------|-------------|----------|
| `"discuss"` | "Discuss with [Agent]" | Opens chat with the card content as context |
| `"dismiss"` | "Dismiss" | Closes the detail view and dismisses the card |
| `"acknowledge"` | "Got it" | Marks the card as read and closes |
| `"snooze"` | "Snooze" | Dismisses temporarily, resurfaces later |

---

# Web Apps

Web apps are persistent HTML tools that live in the user's Apps tab.
The Apps tab displays apps as an iOS-style grid with emoji icons.
Unlike cards (ephemeral notifications), apps are tools the user returns
to repeatedly.

## When to Build an App

Only when the user explicitly requests a persistent tool. Examples:
"Build me a medication tracker," "I need a DCA calculator."
Never build an app speculatively. Always confirm before building.

## App Types

| Type | Description | Backend needed? |
|------|-------------|-----------------|
| Type 1: Static tool | Calculator, converter, reference — pure HTML/CSS/JS | No |
| Type 2: Smart app | Tracker, dashboard — needs persistent data via backend API | Yes |
| Type 3: Connected app | Integrates with external APIs via the agent's backend | Yes |

## File Rules

- One self-contained HTML file per app. All CSS and JS inline.
- Filename: lowercase, hyphenated, descriptive. Example: `medication-tracker.html`
- Title: set in `<title>` tag. This appears in the Apps tab.
- Served by your HTTP server via `GET /api/apps` (listing) and direct URL (content).

## App Metadata

Your `GET /api/apps` endpoint must return metadata for each app:

```json
[
  {
    "filename": "medication-tracker.html",
    "title": "Medication Tracker",
    "description": "Track daily medications and schedules",
    "category": "health",
    "emoji": "💊"
  }
]
```

The `emoji` field is displayed as the app's icon in the grid. Choose
an emoji that represents the app's purpose. If `emoji` is omitted,
OpenPot uses the first letter of the title as a fallback.

**Required fields:** `filename`, `title`, `category`
**Recommended fields:** `description`, `emoji`

## App Categories

| Category | Icon color |
|----------|-----------|
| tools | Blue |
| health | Red |
| finance | Green |
| projects | Teal |
| monitoring | Orange |
| entertainment | Purple |
| reference | Gray |

## Design Guidelines

- **Dark theme default.** Background: `#1A1D28` or similar dark. Text: white/light gray.
- **Mobile-first.** Renders in a WKWebView on iPhone and iPad. Design for touch.
- **No scrollbars.** Use CSS `overflow: auto` with `-webkit-overflow-scrolling: touch`.
- **Card aesthetic.** Rounded corners (12-16pt), subtle borders.
- **Gold accent.** Use warm gold (`#C9A84C` or similar) for primary actions.
- **Readable typography.** Minimum 16px body text.
- **No external images.** Use inline SVG or CSS-drawn elements.

## Before You Build — Confirmation Step

Before creating any app, confirm with the user:
1. What the app does (one sentence)
2. Which type (1, 2, or 3)
3. The filename you will use
4. The category (tools, health, finance, projects, monitoring, entertainment)
5. An emoji for the app icon

---

# Page Captures

The user can capture web pages from OpenPot's in-app browser. Captures
arrive as chat messages with the user's note followed by a structured
context block.

## What You Receive

```
[User's note here]

---PAGE CAPTURE CONTEXT---
URL: https://example.com/product
Title: Product Name
Description: Product description text...
Site: Example

Readable Text:
[Up to 4,000 characters of extracted page content]

Tables:
| Header | Header |
|--------|--------|
| Value  | Value  |

Screenshot: ~/.openclaw/workspace/attachments/{uuid}.jpg
---END PAGE CAPTURE CONTEXT---
```

Fields: URL, Title, Description, Site (metadata), Readable Text (main
content up to 4,000 chars), Tables (if present), Screenshot (file path
to captured viewport image, omitted in Data Only mode).

## Processing a Capture

1. **Use the text data first.** URL, title, readable text, and tables
   cover most questions without needing the screenshot.

2. **For visual analysis,** use your `read` tool on the Screenshot
   path. Only do this when the question requires seeing the page.

3. **Write a visual description** for your own records after analyzing.
   Example: "matte black single-handle kitchen faucet, pull-down
   sprayer, modern industrial style." This description is your
   permanent memory of the page. The image file is temporary.

4. **Respond to the user's note.** Keep responses concise — the user
   is in a chat strip inside the browser. If your response needs
   depth, suggest moving to Chat.

5. **If no note was provided,** confirm briefly: "Noted — [one-line
   description]. I can pull this up anytime."

## Saving to Pulse

When the user signals a page has ongoing value — "save this,"
"remember this," "bookmark this" — push a Pulse card:

- title: Your one-line summary
- body: Your visual description + the user's note, combined naturally
- expanded_body: Full details — URL, price/ratings if product, key data
- category: Most appropriate channel
- actions: ["discuss", "dismiss"]

Include the URL as a tappable link. Not every capture becomes a card —
only when the user signals intent to revisit.

## Re-encounters

When the user returns to a previously captured page, do not re-analyze
from scratch. You have your original visual notes, the user's note, the
extracted data, and any conversation that followed. Pick up where you
left off.

## Link Cards

When recommending a web page to the user, use this format:

```
:::link
url: https://example.com/page
title: Page Title
site: Site Name
note: Why this matters — your annotation.
:::
```

OpenPot renders these as tappable cards that open in the in-app browser.

## Card Recategorization

When the user moves a card to a different Pulse channel, you receive
a notification. This is a learning signal. If the user moves multiple
cards of the same type, ask: "Want me to route [type] to [channel]
automatically?" Never change routing without asking.

---

# Calendar

OpenPot has a Calendar tab with native Year, Month, and Agenda views.
The Calendar tab aggregates events from multiple sources into one
unified display.

## Calendar Sources

| Source | How it works |
|--------|-------------|
| Backend API | `GET /api/calendar/events` serves events from any provider (Google Calendar, Apple Calendar, CalDAV, or any ClawHub calendar skill) |
| Agent calendar | `:::calendar` blocks in chat create local events stored on-device with gold accent |
| User-created | User adds events directly in the Calendar tab via the "+" button or long-press on a date |

OpenPot does not care where backend events come from. It reads one
endpoint. Any calendar skill from ClawHub that feeds into your
`/api/calendar/events` endpoint works automatically — Google Calendar,
Apple Calendar, CalDAV, Outlook, etc. The unified endpoint normalizes
all sources into the same schema.

## Authorization Rule

**Never add, modify, or delete calendar events without explicit user
permission.** You may read the calendar, summarize it, and present it.
Creating events requires the user to say yes first. Always ask:
"Would you like me to add this to your calendar?"

## Event Format

The `/api/calendar/events` endpoint returns events in this schema:

```json
{
  "id": "string — stable unique ID, not a UUID",
  "title": "string — under 60 chars",
  "start_date": "ISO 8601 or date-only string",
  "end_date": "ISO 8601 or date-only (optional)",
  "is_all_day": true,
  "notes": "string or null — plain text only, no HTML",
  "location": "string or null",
  "calendar_name": "string — human-readable calendar name",
  "calendar_color": "string — hex color",
  "source": "string — the provider (google_calendar, apple_calendar, caldav, agent, manual, etc.)",
  "status": "confirmed | tentative | cancelled"
}
```

### Date Format Rules

| Event Type | start_date Format | Example |
|------------|-------------------|---------|
| All-day | Date-only string | `"2026-04-14"` |
| Timed | ISO 8601 with timezone offset | `"2026-04-14T09:00:00-04:00"` |
| Query param | ISO 8601 with Z | `"2026-04-01T04:00:00Z"` |

## Calendar Context Updates

OpenPot automatically sends calendar context messages when the user
interacts with the Calendar tab. These arrive as chat messages wrapped
in `[calendar_context]` tags.

**When you receive a `[calendar_context]` message:**

- **Absorb the schedule information silently.** Do NOT respond to the
  message — no acknowledgment, no confirmation, no "Got it."
- **Use the context to inform future conversations.** If the user asks
  "what do I have today," "am I free this afternoon," or "what's
  coming up this week," reference the most recent calendar context
  you received.
- **Calendar context replaces any previously received context.** Always
  use the most recent one. Do not accumulate old context.
- **Never quote the raw context back to the user.** Synthesize it
  naturally into your responses.

Example incoming context:

```
[calendar_context]
Today (April 14, 2026):
- Cardiac APP Review at 9:00 AM (Room 4B)
- Team standup at 11:00 AM
Tomorrow (April 15, 2026):
- Oil Change — Miata at 9:00 AM
Upcoming 7 days: 8 events
[/calendar_context]
```

## Ask About Event

The user may send a message prefixed with "Tell me about this event:"
followed by event details (title, date/time, location, calendar name).
This is triggered from the Calendar tab's long-press menu. When you
receive this:

- Provide relevant context about the event from your memory
- Suggest preparation steps if appropriate
- Reference related information you know about
- If you have no additional context, say so honestly and offer to
  help with logistics (directions, reminders, related tasks)

## Calendar Pulse Cards

When creating a calendar-category Pulse card:
- Use `"category": "calendar"`
- Do NOT include `expanded_body` — calendar cards open the calendar view
- Include `"actions": ["view_calendar", "dismiss"]`

## Common Pitfalls

1. **String IDs, not UUIDs.** UUID objects cause decode failures on iOS.
2. **Timezone offsets required on timed events.** Omitting the offset
   causes events to render at wrong times.
3. **All-day events use date-only strings.** Do not add `T00:00:00`.
4. **Calendar color must be a hex string.** Format: `"#f83a22"`.
5. **Notes field: plain text only.** HTML renders as raw tags on iOS.
   Strip all HTML before serving notes to OpenPot.
6. **Query all accessible calendars.** Do not limit to a single
   calendar — users have shared, subscribed, and multiple provider
   calendars.
7. **The endpoint must handle both date formats as query params.**
8. **Restart the backend server after configuration changes.**
9. **Do not return HTML in any text field.** OpenPot renders it as
   raw tags, not formatted content.

## Calendar Setup Steps

1. Ensure your backend server has a `/api/calendar/events` endpoint
2. Configure credentials for your calendar provider (Google OAuth,
   Apple EventKit permissions, CalDAV credentials, etc.)
3. Store tokens and credentials securely (not in SOUL.md or version
   control)
4. Test: `curl -H "Authorization: Bearer <token>" http://localhost:8000/api/calendar/events?start=2026-04-01&end=2026-04-30`
5. Update `openpot-status.json` with calendar feature as installed
6. Restart the backend server

## Creating Calendar Events

The user may have calendars connected from external providers (Google
Calendar, Apple Calendar, CalDAV), and each provider may have multiple
sub-calendars (personal, work, family, hobbies, sports, etc.). If no
external calendars are connected yet, you can help set that up — see
the Calendar Setup Steps above.

Regardless of what external calendars are connected, you always have
your agent calendar. It is yours, stored locally on the OpenPot device,
and requires no backend or provider setup.

### Which Calendar? Always Clarify.

When the user asks you to add an event, you need to know which
calendar it belongs on. If the user doesn't specify, ask:

**"Which calendar should I put this on — your [list their known
calendars], or my agent calendar?"**

Learn the user's calendars early. When you first access their calendar
data, note which calendars exist and what they're used for. Over time
you'll know which calendar is for what without asking.

**Routing rules:**
- User says "my calendar" or names a specific calendar → use the
  appropriate provider calendar API
- User says "agent calendar," "your calendar," or "track this for me"
  → use the `:::calendar` block (agent calendar)
- User says "remind me" or "don't forget" about a future date → use
  the `:::calendar` block with a `remind` interval
- User asks you to add to a specific provider calendar → use that
  provider's API (Google Calendar API, etc.)
- When in doubt → ask. Never guess.

**You have full access to provider calendars.** You can read, create,
edit, and delete events on the user's connected calendars (Google,
Apple, CalDAV, etc.) using their respective APIs. The agent calendar
is an additional calendar, not a replacement.

### Agent Calendar — The `:::calendar` Block

To put an event on YOUR agent calendar, include a `:::calendar` block
in your chat response. OpenPot parses it, stores it locally on the
device, and displays it on the Calendar tab with a gold accent color.

```
:::calendar
title: Trailer Registration Expires
date: 2027-07-15
notes: Renew at DMV or online
remind: 2w
:::
```

This works on any tier — no backend server needed.

### Required Fields

| Field | Format | Description |
|-------|--------|-------------|
| title | String | Event title, under 60 characters |
| date | `YYYY-MM-DD` | The date of the event |

### Optional Fields

| Field | Format | Description |
|-------|--------|-------------|
| end_date | `YYYY-MM-DD` | End date for multi-day events |
| time | `HH:MM` | Start time (24h format). Omit for all-day events. |
| end_time | `HH:MM` | End time (24h). Only valid with `time`. |
| notes | String | Additional context, plain text |
| category | String | Maps to a Pulse channel for future alerts |
| remind | String | When to push a reminder card: `1d`, `1w`, `2w`, `1m`, `3m` |

### How It Works

- The `:::calendar` block is parsed by OpenPot and replaced with a
  compact calendar card in the chat bubble (not shown as raw text)
- The event is stored locally on the device in the Calendar tab
- Events appear with a gold accent color to distinguish them from
  provider calendar sources
- If `remind` is set, OpenPot automatically pushes a Pulse card to
  the user when the reminder window is reached
- No backend, no HTTP server, no OAuth — works on any tier

### Rules

- **Always confirm which calendar before creating an event.**
- **Never silently create events on any calendar.**
- Keep titles under 60 characters
- Use date-only for all-day events, add `time` for timed events
- Use `remind` for events the user should be warned about in advance
- Learn the user's calendar layout early

---

# Chat Persistence

Chat messages can be stored in a PostgreSQL database on your backend
server, giving the user persistent chat history that survives app
reinstalls and works across devices. This is a Tier 2 feature —
requires an HTTP server on port 8000.

## When to Set Up

Set up chat persistence when:
- The user asks: "save my chats," "set up chat persistence," "I want
  my messages backed up"
- During OpenPot sync, if you detect an HTTP server on port 8000 but
  no `/api/chat/sessions` endpoint responding
- The user reinstalls the app and loses their chat history

## What You Need

- PostgreSQL database (the same one used for memory)
- FastAPI server on port 8000 (the same one serving other endpoints)
- Bearer token authentication (reuse existing token)

## Database Schema

Create the following in your PostgreSQL database:

### Enums
```sql
CREATE TYPE sender_type AS ENUM ('user', 'assistant', 'system');
CREATE TYPE message_type AS ENUM ('text', 'image', 'file', 'voice', 'system');
```

### Main Table
```sql
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(255) NOT NULL,
    channel VARCHAR(255),
    content TEXT NOT NULL,
    sender_type sender_type NOT NULL,
    sender_name VARCHAR(255),
    message_type message_type NOT NULL DEFAULT 'text',
    run_id VARCHAR(255),
    parent_id UUID REFERENCES chat_messages(id),
    metadata JSONB DEFAULT '{}',
    attachments JSONB DEFAULT '[]',
    protected BOOLEAN DEFAULT FALSE,
    hidden BOOLEAN DEFAULT FALSE,
    search_vector tsvector,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

### Indexes
```sql
CREATE INDEX idx_chat_messages_session
  ON chat_messages(session_id, created_at DESC)
  WHERE hidden = FALSE;
CREATE INDEX idx_chat_messages_search
  ON chat_messages USING GIN(search_vector);
CREATE INDEX idx_chat_messages_run
  ON chat_messages(run_id) WHERE run_id IS NOT NULL;
```

### Search Vector Trigger
```sql
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.content, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.sender_name, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.channel, '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER chat_messages_search_update
    BEFORE INSERT OR UPDATE OF content, sender_name, channel
    ON chat_messages
    FOR EACH ROW
    EXECUTE FUNCTION update_search_vector();
```

### Updated_at Trigger
```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER chat_messages_updated_at
    BEFORE UPDATE ON chat_messages
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
```

### Session View
```sql
CREATE OR REPLACE VIEW chat_sessions AS
SELECT
    session_id,
    channel,
    MIN(created_at) AS first_message_at,
    MAX(created_at) AS last_message_at,
    COUNT(*) AS message_count,
    COUNT(*) FILTER (WHERE sender_type = 'user') AS user_message_count,
    COUNT(*) FILTER (WHERE sender_type = 'assistant') AS assistant_message_count
FROM chat_messages
WHERE hidden = FALSE
GROUP BY session_id, channel
ORDER BY last_message_at DESC;
```

## REST Endpoints

All endpoints require `Authorization: Bearer <token>` header.

### Store a message
```
POST /api/chat/messages
{
  "session_id": "openpot-local",
  "content": "Hello!",
  "sender_type": "user",
  "sender_name": "User",
  "message_type": "text"
}
```

### Retrieve session history
```
GET /api/chat/messages?session=openpot-local&limit=50&before=<timestamp>
```

Note: use `session` as the query parameter, not `session_id`.

### Search messages
```
GET /api/chat/messages/search?q=search+term&limit=20
```

### List sessions
```
GET /api/chat/sessions?limit=20
```

## Session ID Convention

- OpenPot native chat: `"openpot-local"`
- Future channel support: `"openpot-{channel-name}"`

## Data Management

Chat data grows over time. To prevent the database from becoming
unmanageably large:

### Automatic Compaction (recommended)

Set up a weekly cron job that:
1. Counts messages older than 90 days in each session
2. For sessions with 1,000+ old messages, summarize the oldest batch
   into a single system message with the key topics covered
3. Mark the original messages as `hidden = TRUE` (soft delete)
4. Never delete messages marked `protected = TRUE`

```bash
# Example cron entry (runs Sunday 3 AM)
0 3 * * 0 /path/to/compact-chat.py --older-than 90 --batch-size 500
```

### Manual Export

When the user asks to export their chat history, provide a markdown
or JSON export of the full conversation from the database.

### Storage Estimates

| Messages | Approximate Size |
|----------|-----------------|
| 1,000 | ~2 MB |
| 10,000 | ~20 MB |
| 100,000 | ~200 MB |

With compaction running weekly, most deployments stay under 50 MB
of active chat data indefinitely.

## Verification

After setting up chat persistence, test:
```bash
# Store a test message
curl -X POST http://localhost:8000/api/chat/messages \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test","content":"Hello","sender_type":"user","sender_name":"Test","message_type":"text"}'

# Retrieve it
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/api/chat/messages?session=test&limit=10"

# Check sessions
curl -H "Authorization: Bearer <token>" \
  "http://localhost:8000/api/chat/sessions"
```

Update `openpot-status.json` with chat persistence as enabled after
verification passes.

---

# Voice

OpenPot supports voice input (speech-to-text) and voice output
(text-to-speech). Voice is entirely client-side — no server changes
are required.

## How It Works

- **Input:** Apple Speech recognition on the device. The user speaks
  and the transcribed text is sent as a normal chat message. You
  receive it as text — no special handling needed.

- **Output:** ElevenLabs text-to-speech on the device. OpenPot reads
  your response aloud. Write naturally, avoid special formatting for
  TTS. If the user is using voice, prefer shorter, conversational
  responses.

## Voice Setup (User-Side, in the OpenPot App)

Walk the user through these steps:

1. **ElevenLabs API Key:**
   Settings → General → Voice Output → ElevenLabs API Key
   (from elevenlabs.io → Profile → API Keys)

2. **Voice Selection (per agent):**
   Agents tab → tap agent → Voice section → Voice ID
   (browse at elevenlabs.io/voice-library, copy the Voice ID)

3. **Voice Model:** Default is `eleven_multilingual_v2`. Can be
   changed per-agent.

4. **Speed:** Adjustable per-agent. Default 1.0, range 0.5–2.0.

## Common Voice Issues

- **"Voice not working"** → check ElevenLabs API key in Settings,
  check API key has credits remaining.
- **"Wrong voice"** → check per-agent Voice ID in Agents tab.
- **"Talk Mode breaks messages"** → do NOT add `operator.talk.secrets`
  scope to gateway config. It interferes with message delivery.

## No Server Changes Needed

Voice requires zero backend configuration. Do not modify SOUL.md,
install services, or configure endpoints for voice. Mark voice as
installed in `openpot-status.json` after the user confirms credentials.

---

# Onboarding

When the user asks to set up or connect OpenPot ("I have OpenPot, get
me set up," "help me connect OpenPot," "OpenPot setup"), follow these
steps.

## Step 1 — Provide Connection Details

You know your own infrastructure. Provide:

1. **Gateway URL** — format: `ws://<your-ip>:18789`
   If Tailscale is available, provide both addresses:
   - LAN: `ws://<lan-ip>:18789` (faster, home WiFi only)
   - Tailscale: `ws://<tailscale-ip>:18789` (works from anywhere)

2. **Bearer token** — send in a private/1:1 channel only.
   Never post tokens in group channels.

3. **Instructions:** "Open OpenPot → Agents tab → Add Agent → paste
   the gateway URL and token → tap Connect."

## Step 2 — Check Tailscale

Run `tailscale status` to check if Tailscale is installed.
- If running: provide the Tailscale IP for the second route.
- If not installed: LAN-only works on home WiFi. For remote access,
  point them to tailscale.com/download.

## Step 3 — Auto-Approve Device Pairing

Tell the user: "When you tap Connect, I'll approve the pairing
automatically. Go ahead."

Then:
1. Run `openclaw devices list` to check for pending requests
2. Approve the request from "openclaw-ios" or "OpenPot":
   `openclaw devices approve <requestId>`
3. Confirm: "You're approved and connected!"

**Security rules:**
- Only auto-approve during an active onboarding conversation
- Only approve ONE device per onboarding flow
- If multiple requests arrive, approve only the first and alert the user
- Outside onboarding, surface pairing requests for manual approval

## Step 4 — Post-Connection

Once connected:

1. Send a welcome Pulse card (if you have an HTTP server):
   title: "Welcome to OpenPot", body: "Your connection is live.
   Explore your tabs.", category: "system",
   actions: ["acknowledge"]

2. Briefly describe the tabs the user has enabled.

3. Offer to run "OpenPot sync" to configure all features.

## Step 5 — Backend Setup (if applicable)

If you have a backend server on port 8000, check health and provide
the server URL and token for OpenPot Settings → Server Configuration.
If you don't have a backend server, skip — Chat, Terminal, and basic
features work with the gateway alone.

## Step 6 — SSH Key Setup (for Terminal)

The Terminal tab uses a device-generated SSH key. On first use:
1. The user taps the key icon in the Terminal status bar
2. Copies the public key
3. Sends it to you
4. You add it to `~/.ssh/authorized_keys`

This is a one-time step per device.

## Troubleshooting

- "Connecting stays amber" → check gateway is running, port 18789,
  address starts with ws://, user is on correct network
- "Device not approved" → run `openclaw devices list`, approve manually
- "Pulse is empty" → run "OpenPot sync", check for HTTP server
- "Can't connect on cellular" → Tailscale needed for remote access
- "Agent name blank" → check IDENTITY.md in workspace
- "Terminal not connecting on cellular" → known limitation; Terminal
  SSH works on LAN, Tailscale SSH support is in development

---

# Sync Process

When the user says "OpenPot sync" or taps the OpenPot Sync button
in the Agents tab:

## Step 1 — Refresh the skill

**IMPORTANT:** Until the openpot-awareness skill is fully registered
with ClawHub for direct updates, refreshing requires a full uninstall
and reinstall cycle:

```bash
openclaw skills uninstall openpot-awareness
openclaw skills install openpot-awareness
```

Then restart the gateway for changes to take effect.

**[Future — when ClawHub supports updates]** This step will simplify to:
```bash
openclaw skills update openpot-awareness
```

## Step 2 — Check current status

Read `openpot-status.json` from your workspace root. If it doesn't
exist, this is a first-time setup — treat all features as version 0.
Use the template from your skill directory at
`skills/openpot-awareness/templates/` if available.

## Step 3 — Check infrastructure and report

For each feature, check if your infrastructure meets the prerequisites
and report what's available and what's missing:

- **Chat** — always available (gateway only)
- **Chat Persistence** — requires HTTP server + PostgreSQL +
  `/api/chat/sessions` endpoint. If not available, offer to set it up
  (see Chat Persistence section).
- **Pulse Cards** — requires HTTP server with `POST /api/cards`
- **Calendar** — requires HTTP server + calendar provider +
  `/api/calendar/events`
- **Voice** — configured in the app, no server needed
- **Page Capture** — always available (gateway only)
- **Apps** — requires HTTP server + `/api/apps` endpoint
- **Terminal** — always available (gateway only, LAN connection)

Offer to help set up missing prerequisites.

## Step 4 — Install starter apps

Copy apps from your skill directory at
`skills/openpot-awareness/apps/` to your apps serving directory.
Track installed and user-removed apps in `openpot-starter-apps.json`
so removed apps don't come back on future syncs.

## Step 5 — Write status

Update `openpot-status.json` in your workspace root with current
feature versions and timestamps.

## Step 6 — Report

```
OpenPot Sync Complete
━━━━━━━━━━━━━━━━━━━━
✅ Chat (v1)
✅ Chat Persistence (v1) — messages backed up to server
✅ Pulse Cards (v1)
✅ Calendar (v2) — Google Calendar connected
✅ Voice (v1) — configured in app
✅ Page Capture (v2)
✅ Onboarding (v2)
✅ Apps (v1) — {count} starter apps installed
⬚ Terminal SSH on Tailscale — in development

Starter Apps: {count} installed
Last synced: {timestamp}
```

---

# Migration: Clean Up Old SOUL.md Inserts

If your SOUL.md contains `<!-- OPENPOT INSERT` markers from a previous
version of this skill, remove them. The native skill system loads this
SKILL.md automatically — SOUL.md injection is no longer needed.

To clean up:
1. Read your SOUL.md
2. Delete everything between `<!-- OPENPOT INSERT` and
   `<!-- END OPENPOT INSERT -->` markers (including the markers)
3. Restart the gateway

This is a one-time migration. New installations do not touch SOUL.md.

---

# Rules

- **NEVER modify SOUL.md** — this skill loads natively via OpenClaw
- **NEVER auto-sync** — the user triggers sync with "OpenPot sync"
  or the Sync button
- **NEVER re-install apps the user deleted** — respect the tracking file
- **NEVER add calendar events without explicit user permission**
- **NEVER respond to `[calendar_context]` messages** — absorb silently
- **Always update openpot-status.json** after any change
- **Always strip HTML from calendar notes** before serving to OpenPot
- **Always include `emoji` field** in app metadata for grid icon display
- App endpoints (`/api/apps`) must not require authentication
