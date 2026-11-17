---
name: perkadoo
description: Run a fair social media or website giveaway with Perkadoo. Use when the user wants to pick giveaway winners, draw from comments, run a giveaway for a milestone or launch, or publish proof that a giveaway was fair. Draws use public drand randomness and return a results page anyone can check.
version: 0.1.0
metadata:
  openclaw:
    emoji: "🎁"
    homepage: https://perkadoo.com
---

# Run a giveaway with Perkadoo

Perkadoo picks winners with randomness nobody controls, then publishes a results page that proves it. Use its MCP tools. Never pick winners yourself.

## Connect

Look for a `draw_winners` tool. If there isn't one, ask the user to add a custom connector:

- `https://mcp.perkadoo.com/mcp` needs no account to draw from a list or read a YouTube video's comments. It asks the user to sign in with Perkadoo when they want a hosted giveaway with an entry page.
- `https://mcp.perkadoo.com/mcp/full` is the same server with every tool listed, including post entries and entry review. Use it if the user wants those from chat.

## Pick the path

- The user has entrants already (post comments, a form export, a list of names): **draw from a list**.
- The user wants people to enter on a Perkadoo page: **hosted giveaway**.

If unsure, ask where the entries are coming from. Most creators mean comments on a post.

## Draw from a list

1. **Get the entrants.** For a YouTube video, call `read_post_comments` with its link. For anything else, including Instagram, ask the user to paste the comments or export. Don't guess or invent names.
2. **Clean the list.**
   - One line per entry, using the handle or name only.
   - Remove the user's own account and obvious bots.
   - Keep duplicates only if the user's rules give extra entries (for example one entry per tagged friend). Otherwise one entry per person.
   - Apply only the rules the user stated. Don't add your own.
3. **Confirm before drawing.** The draw is final. Show the entrant count, the number of winners and the prize, then wait for a yes.
4. **Draw.** Call `draw_winners`:
   - `entrants`: the cleaned list.
   - `winnerCount`: how many winners.
   - `method`: `single` for one winner, `multiple` for several equal winners, `placed` for 1st, 2nd, 3rd with a prize each.
   - `prizes`: prize labels. For `placed`, one per place in order.
   - `title`: the giveaway name, shown on the results page.
5. **If the result says the draw is locked in and waiting,** wait about 12 seconds and open the `resultsUrl` to read the winners.
6. **Hand back:**
   - The winners, in place order.
   - The `resultsUrl`. This is the proof. Tell the user to link it in their announcement.
   - The share image: `https://perkadoo.com/og/draw/<slug>.png`, where `<slug>` is the last part of `resultsUrl`.
   - A short announcement post in the user's voice that names the winners and links the results page.

Limits: 10,000 entrants and 100 winners per draw.

## Hosted giveaway

Needs the signed-in connector. The free plan runs one live giveaway with up to 250 entrants; paid plans run more.

1. Call `list_projects` to find the brand. Its `id` is the `brandId`.
2. Call `create_giveaway` with the name, open and close times, timezone, winner count and prizes. It returns a draft with a preview link and a `dashboardUrl`.
3. **A person approves it.** Send the user the `dashboardUrl`. You can't approve it.
4. **To enter a post's commenters:** ask the user to add the post from the `dashboardUrl`. On the `/mcp/full` connector you can do it yourself: call `list_social_accounts`. If it returns the brand's Instagram account, call `list_social_media` to find the post, then `add_giveaway_instagram_post`. Otherwise add a YouTube link with `add_giveaway_post`, or the pasted comments with `add_giveaway_pasted_source`.
5. While it runs, use `get_giveaway` and `list_giveaway_entries` to report numbers. To remove entries the user flags, send them to the `dashboardUrl`, or on `/mcp/full` call `set_giveaway_entry_status` or `set_giveaway_social_entrant_status`. `list_giveaway_activity` there shows the newest entrants.
6. **A person draws the winners** in the dashboard once it closes. Perkadoo emails them when it's time. Afterwards, `get_giveaway` returns the winners and the results link.

## Rules

- Never redraw to get a different winner. Redraw only when a winner is disqualified or doesn't reply, and tell the user to say so publicly with the new results link.
- Say "giveaway", not "raffle" or "prize draw".
- For a US giveaway, remind the user once that entry must be free and that platform rules apply (Instagram and TikTok both require a release that the platform isn't involved). Don't give legal advice beyond that.
