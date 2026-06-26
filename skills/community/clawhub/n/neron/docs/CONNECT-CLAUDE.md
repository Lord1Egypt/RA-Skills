# Connect Neron to Claude

Use your knowledge graph directly inside Claude conversations.

---

## Steps

### 1. Get credentials from the bot

Open **@NeronBetaBot** in Telegram → send `/password`

You'll get:
- **User ID** (your Telegram ID)
- **Password**

Use the copy buttons to save both.

### 2. Add Neron as a connector in Claude

Go to **Customize** → **Connectors** → click **+** → **Add custom connector**

Fill in:
- **Name**: `Neron`
- **URL**: `https://mcp.neron.guru/mcp`

Click **Add**.

### 3. Connect

Neron appears under **Not connected** with a `CUSTOM` badge.

Click on it → click **Connect**.

An auth page opens: **"Connect to Claude"**. Enter:
- **Telegram ID** — from step 1
- **Webapp Password** — from step 1

Click **Connect to Claude**.

### 4. Done

Start a new conversation. Neron tools are now available (🔧 icon).

Try asking Claude:
```
What's in my Neron graph?
```

---

## What you can do now

Talk to Claude naturally — it reads your graph:

- **"How was my week?"** → mood trends, note count, energy patterns
- **"What tasks are stuck?"** → stale tasks ranked by priority
- **"What did I write about Dima?"** → finds all notes mentioning a person
- **"Find patterns in my mood"** → analytics on your emotional data
- **"Show me things related to X"** → semantic search across your entire graph
- **"Remember this: ..."** → creates a note in your graph

---

## Troubleshooting

**Connector not connecting** → Check URL is exactly `https://mcp.neron.guru/mcp` (no trailing slash).

**Auth page fails** → Re-run `/password` in the bot. Credentials may have been regenerated.

**No tools visible** → Start a **new** conversation after connecting. Tools don't appear in existing chats.
