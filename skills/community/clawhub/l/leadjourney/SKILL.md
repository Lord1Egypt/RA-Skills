---
name: leadjourney
description: Connect OpenClaw to LeadJourney marketing attribution. Answer which ads, campaigns and channels bring leads and revenue, read a lead's full journey, run LeadJourney reports, read live ad platform data, request ad account changes that a person must confirm inside LeadJourney, and set up LeadJourney tracking on a website.
version: 1.0.1
homepage: https://leadjourney.io
metadata:
  openclaw:
    homepage: https://leadjourney.io
---

# LeadJourney

LeadJourney is marketing attribution: it follows a click from the ad or post that produced it to the lead it became and the revenue that lead eventually earned. This skill connects OpenClaw to LeadJourney's hosted MCP server and explains how to use it well.

## When to use

- The user asks which channels, campaigns, ads or creatives bring leads, conversions or revenue
- The user asks about a specific lead, or pastes a LeadJourney lead link
- The user wants a LeadJourney report or dashboard, or numbers from an ad platform connected to LeadJourney
- The user wants to add LeadJourney tracking to a website, or asks why leads are not arriving

## Connect (once)

LeadJourney is a remote MCP server at `https://api.leadjourney.io/mcp`. Sign-in is OAuth with the user's own LeadJourney account; there is no API key to ask for.

1. Check whether it is already configured: `openclaw mcp status`. If a server named `leadjourney` is listed and signed in, skip to "Use".
2. Add the server:

   ```bash
   openclaw mcp add leadjourney --url https://api.leadjourney.io/mcp --transport streamable-http --auth oauth
   ```

3. Sign in:

   ```bash
   openclaw mcp login leadjourney
   ```

   This prints a LeadJourney sign-in link. Give it to the user and ask them to open it, sign in, and approve the connection themselves. The user signs in only in their own browser; their LeadJourney password is not needed here.
4. Confirm with `openclaw mcp status`.

If sign-in fails with a redirect error, the gateway is probably behind its own public domain. Ask the user to run `openclaw mcp login leadjourney` from the OpenClaw CLI on their own machine instead.

## Use

### Workspace first

No tool takes a workspace id. Every tool acts on the user's current LeadJourney workspace, so start by checking which one is active. When the user names a different client or brand, list the workspaces and switch before answering. Which tools are available depends on the user's permissions in that workspace; a missing tool means a missing permission, not an error.

### Reports

- Fixed reports cover traffic channels, campaigns and ad creatives, with leads, conversions, spend and revenue.
- For anything else, describe the report builder first and only then run a report. Metric and dimension ids cannot be guessed, and an invented id returns empty rows instead of an error.
- Date ranges are in the workspace's timezone.

### Leads

Search leads by email, phone or name, then read the lead's journey for its full timeline of clicks, sessions, conversions and CRM stages. Use the journey whenever asked to summarise or advise on one lead.

### Live ad platform data

Answer performance questions from LeadJourney's own reports by default; naming a platform is not a request for live data. Use the live ad data tools only when the user asks for live, platform-side numbers, or needs something the reports do not have, such as search terms, placements, budgets, bidding or targeting. Describe the platform's live data first to learn its metric and breakdown names.

A platform counts the conversions it can see; LeadJourney knows which became real leads and revenue. When both appear, show them side by side and trust LeadJourney's numbers.

### Changing ad accounts

Ad changes (pausing, budgets, bids, keywords) are only ever requested. Nothing changes until a person confirms the request inside LeadJourney using the link the request returns. Say so plainly, and never claim a change was applied.

### Tracking setup on a website

The LeadJourney tracking script records visits, clicks and form submissions on the site and sends them to LeadJourney. Explain that to the user before installing it.

1. Read the workspace's onboarding status. An unverified tracking domain is the usual reason nothing arrives, and no code change fixes it: tell the user to finish the DNS record in LeadJourney first.
2. Detect the website's stack and form builder from its URL.
3. Ask the user to copy their tracking script from LeadJourney under Settings, Tracking. Never invent the snippet; it is specific to the workspace.
4. Check how the site handles cookie consent (a consent banner or consent management platform, or Google Consent Mode). If one is in place, load the script the way that setup requires, for example behind the right consent category, and ask the user which category applies when it is unclear.
5. If the website's code is available, add the script once, site-wide, in the page head (for Next.js the root layout, for Nuxt the app head config, otherwise the shared layout or index.html). With Google Tag Manager, add it as a Custom HTML tag on all pages instead.
6. Do not strip `gclid`, `fbclid` or `utm_*` parameters in redirects, because attribution depends on them.
7. After the user deploys, verify the script on the live URL. A negative result on a client-rendered site can be a false negative; say so rather than declaring it missing.

## Privacy

Requests go to LeadJourney's MCP server and are answered from the user's LeadJourney workspace, with the permissions of the user who signed in. How LeadJourney handles that data is set out in its privacy policy: https://leadjourney.io/privacy-policy/. The user can revoke access in LeadJourney under Atlas settings, MCP, Connected applications.
