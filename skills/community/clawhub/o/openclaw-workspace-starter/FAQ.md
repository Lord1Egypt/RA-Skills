# FAQ — Common Questions & Fixes

## My agent doesn't respond
- **Check your API key.** Go to Config → Environment and make sure your AI provider key is set.
- **Is the gateway running?** Look for the green "Health OK" badge in the top-right of the dashboard. If it's red or missing, restart OpenClaw.
- **Is the model set?** Go to Agents → click your agent → check that a Primary Model is selected.

## My agent forgot everything
Sessions reset periodically — that's normal. Your agent's memory lives in files:
- **MEMORY.md** = long-term memory (survives resets)
- **memory/YYYY-MM-DD.md** = daily notes (survives resets)
- If those files are intact, your agent hasn't really forgotten — it'll catch up when it reads them next session.

If you want a fresh start on purpose: type `/new` or `/reset` in chat.

## My agent is too expensive
- **Switch models.** Type `/model list` in chat and pick a cheaper one (e.g., Sonnet instead of Opus, or a local model).
- **Check usage.** Go to the Usage page and look at Cost view to see what's burning money.
- **Compress history.** Type `/compact` to shrink your conversation and save tokens.
- **Reduce heartbeat frequency.** Less frequent check-ins = fewer tokens.

## My agent's personality is wrong
Edit **SOUL.md** — changes take effect next session (or type `/reset` to start fresh immediately). Iterate until it feels right. This usually takes a few tries.

## My agent is too chatty / too quiet
- Too chatty → Add to SOUL.md Standing Orders: "Keep responses under 2 paragraphs unless I ask for more"
- Too quiet → Remove brevity rules from SOUL.md, or add: "Explain your thinking"

## How do I restart my agent?
- **Fresh conversation:** Type `/new` in chat (keeps settings, clears chat history)
- **Full restart:** Click Apply in Config, or restart the OpenClaw service

## My agent doesn't know about something I told it yesterday
Your agent's memory is in files. If it forgot:
1. Check `memory/` folder — is yesterday's file there?
2. Check `MEMORY.md` — was it captured in long-term memory?
3. If not: tell your agent "write this down" next time. It'll save to a file.

## How do I send files to my agent?
In webchat: drag and drop a file onto the chat, or paste an image. Your agent can see images and read text files.

## How do I get files FROM my agent?
Ask your agent to save it to a specific path, then download via your file transfer method (WinSCP, SCP, SFTP, etc.).

Note: The webchat doesn't have a built-in file download button — this is a known limitation.

## Something broke and I don't know what happened
1. Check the **Logs** page (left sidebar → Logs)
2. Look at the **Debug** page for gateway health
3. Ask on the [OpenClaw Discord](https://discord.com/invite/clawd) — the community is helpful

## I want to undo everything and start over
Your workspace files are just text files. Delete them and copy the template again. Your agent starts fresh next session.

Nothing you do in the workspace can break OpenClaw itself — the worst case is always "delete files and start over."
