# Welcome! Let's Set Up Your Agent 👋

This takes about 10 minutes. You'll edit 3 files, glance at 2 others, and you're done.

**You don't need to understand how any of this works.** Just fill in the blanks.

---

## Step 0: Before You Start (Prerequisites)

Make sure these are done. If you're reading this in your workspace, you probably already did them:

- ✅ **OpenClaw is installed** — you ran the installer or `npm install -g openclaw`
- ✅ **Setup wizard completed** — you ran `openclaw onboard` and entered your API key
- ✅ **Dashboard is accessible** — open your browser and go to your OpenClaw URL (usually `http://localhost:18789` or your server's IP + port)

**If any of these aren't done yet:** Follow the [Getting Started guide](https://docs.openclaw.ai) first, then come back here.

**How to edit these files:** They're plain text files with a `.md` extension. Open them with any text editor — Notepad (Windows), TextEdit (Mac), VS Code, or even nano in a terminal. Just type, save, done.

---

## Step 1 of 5: Name Your Agent

Open **IDENTITY.md** (it's in this folder).

You'll see this:
```
- **Name:** [YOUR AGENT'S NAME]
- **Emoji:** [PICK ONE]
```

Replace the bracketed parts. Example:
```
- **Name:** Nova
- **Emoji:** ⚡
```

That's it. Save the file.

---

## Step 2 of 5: Tell Your Agent About You

Open **USER.md**.

Fill in the blanks. It asks for:
- Your name (or nickname — whatever you want to be called)
- Your timezone (like "America/New_York" or "Europe/London")
- What you do and how you like to be talked to

**Don't overthink this.** Write a few sentences. You can always come back and add more later.

---

## Step 3 of 5: Give Your Agent a Personality

Open **SOUL.md**.

This is the fun one. You're deciding WHO your agent is. The file has examples:
- Direct and efficient? Warm and supportive? Professional? Chaotic and creative?

Pick a style, write 2-3 sentences describing it, and fill in the Standing Orders (rules your agent always follows).

**Tip:** Start simple. "Be casual, keep it brief, don't sugarcoat things." You can tweak it over the first week as you figure out what works.

---

## Step 4 of 5: Quick Check

Glance at these files (you probably don't need to change anything):

**AGENTS.md** — Rules for how your agent behaves. The defaults are good. Skim it so you know what's in there.

**TOOLS.md** — Notes about your specific setup (like camera names or file transfer methods). Skip this for now. Come back when you need it.

**HEARTBEAT.md** — What your agent checks during periodic wake-ups. Read the setup recipe at the bottom if you want automatic check-ins.

**ACTIVE_PLAN.md** — Simple goal tracker. Fill it in when you have a goal you want your agent to nudge you about.

---

## Step 5 of 5: Delete This File

Seriously. You're done with setup. If you leave this file here, your agent reads it every single session and wastes tokens on instructions you've already followed.

Delete BOOTSTRAP.md (right-click → delete in a file manager, or `rm BOOTSTRAP.md` in a terminal). Done.

---

## Now What?

**Go to Chat** in your dashboard (left sidebar → Chat) and say hello. Your agent will read the files you just edited and know who it is, who you are, and how to act.

If something feels off:
- Agent too formal? → Edit SOUL.md, make it more casual
- Agent doesn't know something about you? → Add it to USER.md
- Agent too chatty? → Add "keep responses short" to SOUL.md Standing Orders

**Everything is editable.** Nothing is permanent. Experiment.

---

## If You're Lost

Read **UI_GUIDE.md** — it explains every page of the dashboard in plain English. Start with the 🟢 Simple Mode section (4 pages is all you need).

## Need Help?

- 📖 Docs: Click "Docs" in the left sidebar
- 💬 Community: [OpenClaw Discord](https://discord.com/invite/clawd)
- 🐦 Creator: [@TheShadowyRose](https://x.com/TheShadowyRose)
