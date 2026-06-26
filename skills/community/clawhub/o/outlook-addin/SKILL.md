---
name: outlook-addin
description: Outlook sidebar add-in that brings the full power of your OpenClaw agent into Microsoft Outlook. Chat with your agent about any email, use all your tools and skills, draft replies — directly from the inbox. Works with Outlook Desktop (Classic) and Outlook Web (OWA). Use when a user wants to integrate OpenClaw with Outlook, chat with their agent from email, or set up an AI sidebar in Outlook.
---

# OpenClaw Outlook Add-in

An Office.js sidebar add-in that connects Outlook to your local OpenClaw Gateway via WebSocket. Select any email, and your full agent — with all tools, skills, and automations — is available right in the sidebar.

**Repository:** https://github.com/nachtsheim/openclaw-outlook-addin (MIT)

## Quick Start

```bash
git clone https://github.com/nachtsheim/openclaw-outlook-addin.git
cd openclaw-outlook-addin
npm install
npx office-addin-dev-certs install   # first time only
npm run dev                           # starts https://localhost:3000
```

Then add `https://localhost:3000` to Gateway allowed origins and sideload `manifest.xml` into Outlook.

Full setup instructions, architecture details, auto-start config, and troubleshooting: see [README](https://github.com/nachtsheim/openclaw-outlook-addin#readme).
