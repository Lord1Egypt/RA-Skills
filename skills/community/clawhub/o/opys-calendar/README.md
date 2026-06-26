<div align="center">
  <h1>🤖 Opy's Calendar</h1>
  <p><strong>A calendar built specifically for AI agents, and optimized for humans. Designed to work seamlessly with OpenClaw and ClawHub.</strong></p>
</div>

![Main Calendar View](./public/screenshots/main-view.png)

## Overview

Opy's Calendar bridges the gap between AI scheduling and human usability. Traditional web calendars trap data in complex databases or opaque APIs. Opy's Calendar fundamentally shifts this paradigm by storing **everything in Markdown (`.md`) files**. 

This allows your local and remote AI agents (using LLMs) to *natively* read, write, and reason about your schedule, without needing complex integration wiring—while still providing you with a beautiful, fast, and fully-featured React frontend.

![Stats View](./public/screenshots/stats-view.png)

## Highlights

*   🧠 **Agent-Optimized:** Events and settings are saved on disk as plain Markdown and JSON. Your agents can read your schedule like a normal document and modify it instantly.
*   📸 **Agent Snapshots:** Configurable snapshot window sizes so your agents can perfectly recall both historical interactions and upcoming obligations.
*   📊 **Intelligent Stats & Capacity Planning:** Built-in charts break down your time allocation vs. your free capacity based on configurable working hours and subjects. 
*   🔄 **Two-Way Google Calendar Sync:** Full bi-directional synchronization with Google Calendar so you don't have to give up your existing ecosystem. Colors translate perfectly.
*   ⚡️ **Incredibly Fast:** Local-first architecture using Vite and React means zero latency rendering.
*   🎨 **Beautiful UI:** A stunning, Apple-inspired interface with dynamic dark mode, horizontal sliding week views, and categorized event chips.

## How It Works

Your entire calendar lives in a single `calendar.md` file at the root of the project. Categories are defined in the YAML frontmatter, and events are stored serially:

```markdown
---
version: 1
title: Opy's Calendar
timezone: local
updatedAt: 2026-02-26T03:21:57.664Z
categories:
  - id: math
    label: Math
    color: "#3f51b5"
---

`evt_Abc123` | 2026-03-01T09:00 -> 2026-03-01T10:00 | Deep Work (math)
```

No databases to migrate. No API rate limits for your local LLMs. Just plain text.

## Getting Started

1. **Install dependencies:**
    ```bash
    npm install
    ```
2. **Set up Google Sync (Optional):**
    Create a `.env` file with your Google OAuth credentials:
    ```
    GOOGLE_CLIENT_ID=your_client_id
    GOOGLE_CLIENT_SECRET=your_client_secret
    ```
3. **Run the App:**
    ```bash
    npm run dev
    ```
    This concurrently starts the Express File API and the Vite frontend. Open `http://localhost:5173`.

## CLI Interface

As an agent-first tool, we also provide a powerful CLI to interact with the schedule without touching the React app:

```bash
# Get a summary of the next week
npm run cli summary

# Add an event via shell
npm run cli add --title "Meeting with Bob" --start "2026-03-10T14:00:00" --end "2026-03-10T15:00:00" --category "work"
```
