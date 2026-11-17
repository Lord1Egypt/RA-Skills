---
name: cold-email-autopilot
description: Run a small, researched cold email campaign every day: find people with a real signal (a post, a job listing, a launch), verify their work email, write one short personal email each, send from the user's own mailbox, and handle replies. Use when the user has cold email copy or a playbook but nobody to run it daily. Runs on Nodo over MCP; new workspaces get 5,000 free credits.
---

# Cold email on autopilot

A great cold email template does nothing until someone finds the right people, checks their addresses and sends it every day. This skill runs that loop, small and careful, from the user's own mailbox.

## What it does

1. Each day, finds a handful of people with a fresh, public reason to hear from the user: they posted about the problem, launched something, or are hiring for it.
2. Finds and verifies their work email. No guessed addresses, no bought lists.
3. Writes one short email per person that opens on their signal and asks one easy question (for example "Could I send you a few short ideas on X?").
4. Sends from the user's mailbox with a daily cap and spacing, logs every send, never emails the same company twice.
5. Reads replies: answers simple ones from facts the user approved, alerts the user to everything else, honours every "no" at once.

## Set it up

1. If Nodo is not connected yet, fetch and follow https://mcp.nodo.com/start.md yourself (Nodo MCP server `https://mcp.nodo.com/api/user/mcp`, OAuth, no API key). The user only approves the sign-in.
2. Agree with the user: who to target, which signal counts, the offer, and the facts the reply handler may use.
3. Store the mailbox app password as a Nodo secret. Never paste it into chat or a file.
4. Build the workflow (find, verify, draft, send, replies), run it in draft mode, let the user approve the drafts, then schedule it with a low daily cap.

New Nodo workspaces start with 5,000 free credits, about 50 euros of usage.

## Rules

- Small and relevant beats big. Keep the daily cap low, especially on a new domain.
- Every email includes a simple way to opt out, and opt-outs are permanent.
- Follow the anti-spam law where the recipient lives. Never invent a reason for writing.

More: https://nodo.com
