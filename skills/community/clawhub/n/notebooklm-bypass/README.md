# OpenClaw NotebookLM Stealth Auth Skill

This is a custom drop-in skill for the [OpenClaw Framework](https://github.com/openclaw/openclaw) that permanently solves the "Authentication expired" login loop encountered when using the NotebookLM CLI.

## Background: The Multi-Day Auth Loop Nightmare
For days, OpenClaw users have faced a critical bug: Google frequently rotates session cookies for security. When these cookies expire, the `notebooklm` CLI tool crashes with an `Authentication expired` error. 

Normally, this breaks headless AI agents completely. The agent fails its task, drops what it's doing, and the human user is forced to intervene, open their terminal, manually run `notebooklm login`, wait for the browser, and press Enter. If you tried to bypass it using the `NOTEBOOKLM_AUTH_JSON` environment variable, the Playwright CLI tool would often drop the cookies due to a `SameSite: Lax` cross-origin security bug.

This skill fixes all of that by **giving your OpenClaw agent the ability to self-heal its own authentication.**

---

## Features
- **One-Click Consent Recovery**: When OpenClaw gets an auth error, it asks your permission before running the included script to fetch fresh cookies, ensuring no silent credential harvesting occurs.
- **Native Playwright Integration**: The script opens a visible browser window for 5 seconds to naturally bypass Google's "unsecure browser" bot detection.
- **Windows Auto-Injection**: Automatically injects the refreshed cookies natively into the `NOTEBOOKLM_AUTH_JSON` persistent environment variable, bypassing the Playwright cross-origin security drop bug.

---

## The A-Z Setup Guide


### Step 2: The One-Time Interactive Login
You must establish a persistent Chrome profile that is logged into your Google Account.
1. Open your terminal and run:
   ```bash
   notebooklm login
   ```
2. A browser window will open. Log into your Google account.
3. Once you see the NotebookLM dashboard, go back to your terminal and **Press Enter**.
4. This saves a persistent profile to `~/.notebooklm/browser_profile`.

*(You never have to do Step 1 or 2 again. From now on, the script handles it.)*

### Step 3: Install the OpenClaw Skill
1. Clone or download this repository.
2. Move the folder into your OpenClaw workspace's `skills` folder and name it `notebooklm-bypass` so the path looks like this:
   `openclaw/workspace/skills/notebooklm-bypass/SKILL.md`
3. Ensure you have the Python Playwright package installed (used by the automation script):
   ```bash
   pip install playwright
   playwright install chromium
   ```

### Step 4: How it Works Automatically

If you look inside the `SKILL.md` file provided in this folder, you will see a specific instruction rule given to the AI:

> **4. Auth Recovery**: If `notebooklm` fails with "Authentication expired", you MUST ask the user for explicit permission before recovering. Propose running `python {WORKSPACE_DIR}\skills\notebooklm-bypass\scripts\auto_playwright.py`. If and only if they approve, run the script. This script steals fresh cookies and automatically injects them into your Windows Environment Variables. Once complete, retry your command.

Because the OpenClaw agent reads `SKILL.md` before using tools, it now knows exactly how to identify a cookie expiration crash, propose the Python script solution to you, wait for your go-ahead, and confidently retry the task without manually touching the browser!

---

---

## How to Share & Contribute
If you want to share this fix with other OpenClaw users:
1. **GitHub**: Link directly to this repository. Users can clone it straight into their `skills` folder.
2. **ClawHub**: If this is published on ClawHub, users can install it directly via the ClawHub UI.
3. **Discord**: You can zip the folder and drop it into the OpenClaw Discord server's `#skills` channel. Tell them to install it as `notebooklm-bypass` to gain self-healing capabilities.
