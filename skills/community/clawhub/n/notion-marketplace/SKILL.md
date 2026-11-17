---
name: "notion-marketplace"
description: "Find, compare, and add Notion Marketplace templates with linked free shortlists, explicit workspace selection, browser-driven duplication, and Notion API verification."
---

# Notion Marketplace

Find templates through Notion's public Marketplace, add the selected template to the user's chosen workspace, and verify the resulting page through a Notion API connection. A saved link or browser-only success state is not an installation.

## Establish the Notion connection

Before a workspace mutation:

1. Discover the callable Notion connector or CLI available to the agent.
2. Run its read-only current-user or `self` operation and record the connected workspace name and ID when exposed.
3. Confirm that search and page-fetch operations are callable. Discovery and comparison may continue without them, but installation must stop because API verification cannot be completed.

Use the Notion API for baseline searches, page reads, and final verification. Use OpenClaw's browser tool only for Marketplace discovery and the `Add` flow that the API does not provide.

## Discover and shortlist

Free-only is the default. Treat a template as free only when its rendered card or template page visibly says `Free`; exclude missing, ambiguous, and conflicting prices. Include paid templates only after explicit user opt-in, and obtain action-time confirmation naming the template and price before checkout or spending money.

1. Open `https://www.notion.com/templates/category` with the browser tool and collect rendered anchors under `/templates/category/`. Resolve the subject only against these observed names and hrefs; keep no guessed slug list.
2. When the subject confidently matches an observed category, open its observed `/templates/category/<slug>` URL. Use an observed narrower subcategory only when the request clearly names it.
3. Otherwise open `https://www.notion.com/templates/search?query=<encodeURIComponent(subject)>`. If the rendered results contain one clearly matching category card, follow it and use the resulting canonical category URL; otherwise remain on search results.
4. On category pages, verify the visible sort remains `Popular`. Open the visible price filter, choose `Free`, and verify that the selected filter says `Free`. Never construct an undocumented free URL.
5. Read template cards in rendered DOM order. Pair each canonical `/templates/<slug>` link with the visible title, creator, and price in the same card. Deduplicate by canonical href and keep the first 3-5 cards labeled `Free`, preserving their order. On search fallback, apply the same card-local free-label rule if no Free filter is available.
6. Return a concise shortlist with every title linked to its canonical `https://www.notion.com/templates/<slug>` URL, creator when visible, and one sentence on fit. Wait for the user's selection unless the user delegated the choice.

## Choose the workspace and add

Before opening the mutating `Add` control, use the browser tool to open a fresh controlled tab at `https://app.notion.com/marketplace`.

1. Open Notion's workspace switcher and read every rendered workspace option. Exclude account actions such as `New workspace`, preserve guest labels, deduplicate the list, and ask the user which workspace should receive the template even when there is only one option.
2. Tell the user the default destination is that workspace's `Private` area unless they name another visible destination. State which workspace the Notion API connection can verify. If the chosen browser workspace and API workspace differ, stop and ask the user to align the browser session or API connection.
3. After the user chooses, re-read the switcher. Ask again only if the options materially changed or the choice disappeared. Select the choice and verify the sidebar workspace header changed.
4. Before `Add`, use the Notion connector to search for the exact Marketplace title and record matching page IDs and URLs as the baseline. Fetch plausible existing matches.
5. Open `https://app.notion.com/marketplace/templates/<verified-slug>` in the same controlled tab. Reconcile title, creator, and visible `Free` label with the shortlist. Stop on any paid price, checkout, or identity conflict.
6. Click `Add`, then choose `Add to Private` by default or the user's named visible destination. If a desktop-app prompt covers the destination menu, dismiss it and reopen `Add`. Record the new sidebar title because it may differ from the Marketplace title. Preserve existing permissions.
7. If the app session needs authentication, ask the user to sign in inside the OpenClaw-controlled browser and resume from the same page. Never request, read, or transmit credentials. If supported browser actions cannot operate a visible control, report that exact control and failure instead of switching to unrelated desktop automation.

The user's workspace choice authorizes the free duplication into that workspace and destination. Continue autonomously after that choice unless authentication or a new paid or permission boundary appears.

## Verify the installed page

After the browser reports duplication:

1. Search the Notion API for both the Marketplace title and the new sidebar title. Compare results with the baseline; a new result or newly surfaced recent Private page is the candidate.
2. Fetch the candidate through the API and confirm its page ID or URL, title, and recognizable template content or child structure.
3. Poll only for a short bounded interval when duplication is asynchronous. If no new fetchable page appears, report browser success as unverified and do not claim installation.

Report the chosen Marketplace template name and link, selected workspace and destination, installed Notion page URL or ID, and the specific API search and fetch evidence.
