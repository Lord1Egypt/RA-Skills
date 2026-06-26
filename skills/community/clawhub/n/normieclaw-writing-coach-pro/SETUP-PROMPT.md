# Writing Coach Pro — Setup Guide

Welcome! This guide gets Writing Coach Pro running in about 5 minutes. No technical knowledge required.

---

## Step 1: Install the Skill

Copy the `writing-coach-pro` folder into your OpenClaw skills directory:

```
~/.openclaw/skills/writing-coach-pro/
```

If you purchased The Full Stack bundle, you already have this folder in your download. Just drag it in.

If you purchased Writing Coach Pro individually, unzip the download and move the folder to the path above.

## Step 2: Run Setup

Open your terminal and run:

```bash
bash ~/.openclaw/skills/writing-coach-pro/scripts/setup.sh
```

This creates the data directories and a default style profile. You'll see a confirmation message when it's done.

## Step 3: Talk to Your Agent

That's it. Your agent now knows how to coach your writing. Try these to get started:

- **Quick check**: Paste any text and say "review this"
- **Deep analysis**: Paste text and say "full review"
- **Get a rewrite**: Paste text and say "rewrite this"
- **Learn something**: Paste text and say "coach me on this"

## Step 4: Set Your Preferences (Optional but Recommended)

Tell your agent your preferences. You can do this conversationally:

- "I follow AP style"
- "I write in a conversational tone"
- "Set my target readability to 8th grade"
- "I always use the Oxford comma"
- "Show my profile"

Or say "set up my writing profile" and the agent will walk you through it interactively.

## Step 5: Keep Writing

Writing Coach Pro gets smarter every time you use it. It tracks which suggestions you accept and reject, and adjusts its feedback to match your style. After about 10 sessions, you'll notice the suggestions feel dialed in.

---

## What the Scripts Do

You don't need to run these manually — the agent handles it. But if you're curious:

| Script | What It Does |
|--------|-------------|
| `setup.sh` | Creates data folders and default config. Run once after install. |
| `export-report.sh` | Generates a writing analysis report as markdown or PDF. |
| `style-check.sh` | Scans a file for style inconsistencies from the command line. |

---

## Dashboard (Optional)

If you have the NormieClaw Dashboard installed, Writing Coach Pro automatically feeds it your writing stats. Check the `/writing-coach` route on your dashboard for trends and progress charts.

No dashboard? No problem. Say "show progress" to your agent anytime.

---

## Troubleshooting

**Agent doesn't recognize Writing Coach commands**
Make sure the folder is at `~/.openclaw/skills/writing-coach-pro/` (exact name matters). Restart your OpenClaw session.

**"No style profile found" messages**
Run the setup script again: `bash ~/.openclaw/skills/writing-coach-pro/scripts/setup.sh`

**Suggestions feel generic**
You probably haven't set your preferences yet. Say "set up my writing profile" or just keep using it — it learns automatically after a few sessions.

**Want to start fresh**
Delete the data folder and re-run setup:
```bash
rm -rf ~/.openclaw/skills/writing-coach-pro/data
bash ~/.openclaw/skills/writing-coach-pro/scripts/setup.sh
```

---

## Need Help?

- Visit [normieclaw.ai/support](https://normieclaw.ai/support)
- Email: support@normieclaw.ai
- Community: Join the NormieClaw Discord for tips and templates
