---
name: "producthunt-wingman"
slug: "ph-wingman"
version: "1.6.1"
description: "Premium PH outreach agent — automates community discovery, enrichment, and LinkedIn engagement locally."
tags: ["producthunt", "outreach", "linkedin", "marketing", "automation"]
author: "techievena"
homepage: "https://producthunt.eonik.ai"
requirements:
  binaries:
    - python3
    - curl
metadata:
  openclaw:
    requires:
      env:
        - OPENAI_API_KEY
        - LAUNCH_DATE
        - PH_LAUNCH_URL
      optionalEnv:
        - ANTHROPIC_API_KEY
        - GOOGLE_API_KEY
    primaryEnv: OPENAI_API_KEY
---

# ProductHunt Wingman: Local-First Outreach

Premium ProductHunt outreach agent. This skill operates by managing a local background server that orchestrates community discovery, profile enrichment, and LinkedIn engagement.

### 🛡️ Security & Privacy Audit
> [!IMPORTANT]
> This skill executes code located in the `server/` directory of the installed package.
> Before your first run, please review the local files (`server/main.py`, `server/linkedin_agent.py`) to verify network calls and data handling. 
> The agent uses your **local browser session** for LinkedIn; it never asks for or stores your password.

### 📦 Prerequisites
- **Python 3.9+** and **Chrome/Chromium** installed.
- **Environment Variables**:
  - `OPENAI_API_KEY`: Required for message personalization.
  - `LAUNCH_DATE`: Your ProductHunt launch date (`YYYY-MM-DD`).
  - `PH_LAUNCH_URL`: Your product's PH launch URL.

### 🛠️ Runtime Instructions
1. **Local Server Check**:
   - The agent first checks if the Mission Control dashboard is reachable at `http://localhost:3847`.
   - If not, it enters the `server/` directory, ensures the virtual environment is ready (`./setup.sh`), and starts the service (`python3 main.py`).
2. **Dashboard Management**:
   - Once the server is live, the agent can trigger pipelines, check status, or pause/resume outreach by making local API calls to the dashboard.
3. **LinkedIn Authentication**:
   - On the first run, a local browser window will open. **You must manually log in to LinkedIn** in this window. The session is saved locally in `server/.browser_profile/`.

### 🗣️ Voice/Chat Commands
- *"Start my PH outreach"* → Triggers the 5-phase discovery and enrichment pipeline.
- *"Enrich new prospects"* → Systematically visits profiles to extract rich "Genome" data.
- *"Check my launch status"* → Returns a high-density summary of the outreach funnel.
- *"Pause wingman"* → Pauses the background scheduler.

### 📅 Automatic Triggers
- **Daily Discovery**: Runs at 9 AM local time via cron.
- **Outreach Loop**: Enforces connection budgets to protect your account.

### 🚀 Dashboard Features
Accessible locally at `http://localhost:3847`:
- **Prospect Genome:** Deep dive into each member's profile data.
- **Message Editor:** Review and manually edit AI-generated outreach DMs.
- **Outreach Kanban:** Real-time visibility into the campaign funnel.
