---
name: leadshield-form-spam-blocker
version: 1.1.3
description: Filter contact form spam and unwanted sales pitches on HighLevel, WordPress, HubSpot, and custom websites. Set rules for each site and review blocked submissions. Built by Moosh Works (https://mooshworks.com).
---

# LeadShield Contact Form & B2B Solicitation Blocker

Author: Daniel Hallman ([Moosh Works](https://mooshworks.com))

Use **LeadShield** to check contact form submissions for spam or unwanted sales pitches, set screening rules for a site, review blocked submissions, or add form protection to a website.

## Quick start

1. Open the [LeadShield setup guide](https://ghlagencymcp.com/use-cases/ghl-contact-form-spam-blocker) from [Moosh Works](https://mooshworks.com) and choose your website or CRM.
2. Connect a client that supports Streamable HTTP MCP to `https://rankandrent-leads.hallmanlab.workers.dev/mcp`, or install the plugin from the [public repository](https://github.com/mooshee/leadshield-mcp).
3. Sign in to LeadShield and grant access to the intended sites. Use `leadshield_get_spam_policy` to confirm that the intended site's rules are available before changing them. If access is denied, ask the account owner to connect that site.

## What you can do

1. **Preview a screening decision** (`leadshield_screen_submission`). Check how a sample message matches the site's rules. This tool does not store or deliver a lead, update a workflow, or process payment. Describe the verdict and reason in plain language. Omit internal processing-stage labels unless the user asks for technical details. A spam verdict does not verify a person's identity or guarantee their intent.

2. **Review blocked submissions** (`leadshield_get_blocked_spam_report`). Choose a connected site and date range. Report the UTC dates, retained blocked-message count, and plain-language reasons. Counts cover retained records; they do not establish all screening attempts or an overall spam rate. An unsaved screening preview does not add a report record.

3. **Check site rules** (`leadshield_get_spam_policy`). Inspect the site's active rules and `formType` preset. Use the values returned by the tool when choosing a preset.

4. **Change site rules** (`leadshield_configure_spam_policy`). Preview the change with `dryRun: true`. After an authorized update, read the policy again to confirm the saved country, phone, link, and keyword rules. Rules are stored on the server.

5. **Generate setup instructions** (`leadshield_generate_guard_embed`). Request instructions for the intended website or workflow. Generating instructions does not install them. After an authorized installation, test accepted and blocked synthetic submissions and check the actual delivery destination. A form confirmation alone does not prove delivery.

## Service pricing

The connected website service offers free rule-based bot checks and pay-as-you-go message screening at $0.01 per submission. Read the current setup and pricing terms before enabling that service. ChatGPT screening previews do not process payments or establish a paid installation.
