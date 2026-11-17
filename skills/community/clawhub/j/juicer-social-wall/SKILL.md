---
name: juicer-social-wall
description: Run a live social media wall for an event, conference, wedding or campaign with Juicer. Collects posts with the event hashtag from Instagram, TikTok, X, Facebook, YouTube and more, moderates them so nothing embarrassing reaches the screen, and gives a link or embed for the big screen or website. Moderate from chat during the event. Use for "social wall", "hashtag wall", "event wall", "live tweet wall", "show the event hashtag on screen".
version: 1.0.3
metadata:
  openclaw:
    emoji: "📺"
    homepage: https://www.juicer.io
    primaryEnv: JUICER_API_KEY
    envVars:
      - name: JUICER_API_KEY
        required: false
        description: Optional. Only needed when the Juicer MCP server is not connected. Get one at https://www.juicer.io/developer
---

# Event social wall with Juicer

Goal: a wall that shows the event's hashtag posts live, with the organiser in control from their phone. Nothing goes on screen that they would not want there.

## Before the event

1. **Connect Juicer** (see the `juicer` skill). Check `get_account`: moderation needs a plan that includes it, and the wall counts as one feed.
2. **Ask**, in one message: event name and date, hashtags, the event's own accounts, the networks to include and whether every post needs approval before it shows (recommended for weddings, schools, big screens).
3. **Check the hashtag first** with `get_data_posts` (`#hashtag`, 1 to 3 credits per network). If it is already used by other people for other things, suggest a more unique tag before the event. Tell the user what you found.
4. **Create the wall**: `create_feed` named after the event.
5. **Add sources** with `create_source`: the hashtag on each network (use `list_platforms` for exact values) and the event's own accounts so official posts appear too. If a source needs the user's social account, send the link from `create_social_account_connect_url` and explain it.
   - **Instagram accounts: only the user's own.** An Instagram username source keeps updating only when that same account is connected through Instagram login. Before adding it, call `create_social_account_connect_url` with provider `instagram_login`, send the link (it expires in 30 minutes), confirm with `get_social_account_status`, then add the source. Someone else's account (a partner, a celebrity, a competitor) gets one first pull and then stops: tell the user that instead of adding it silently.
   - **Instagram hashtags** need an Instagram Business account connected through Facebook (provider `facebook`). Meta allows 30 different hashtags per week per business account.
   - **Plan limits on the free plan**: after the trial, X, TikTok hashtag and keyword, Reddit and LinkedIn sources stop syncing, Bluesky needs Pro or Enterprise and feeds refresh once a day. If `list_sources` shows a source as not syncable for one of these reasons, say so and show the upgrade link instead of handing over the feed as working.
   - **Credits**: each source costs credits for its first fetch (1 to 6 by network, same rates as data lookups). Check the balance first and tell the user what adding the sources will cost.
   - **Check every source after adding it**: `list_sources` shows each source's sync status. If one is not syncable, tell the user the reason in plain words and the fix. Never hand over an embed code as finished while its only source will not update.
6. **Set moderation** with `update_feed`:
   - `queue: true` when posts need approval (posts wait until approved).
   - `profanity: true`, `prevent_duplicates: true`.
   - `disallowed`: words and handles to block.
   - **AI moderation**: if `get_feed` shows `ai_moderation_available: true`, set `ai_moderation: true` and `ai_harmful_content_filter: true` in the same `update_feed` call, so hateful, violent, sexual and harassing posts are hidden even before anyone reviews the queue. Turn the user's own rules ("no ads", "no competitor promotions") into `ai_moderation_rules`. If the plan does not include it (`ai_moderation_not_available`) or the tool does not accept these fields, say AI moderation can be switched on in the Juicer dashboard and keep the approval queue on.
   - **Refresh rate**: a live wall needs new posts within minutes. Set `sync_interval: 5` (minutes) in the same `update_feed` call. If the plan does not allow it (`sync_interval_not_available`) or the tool does not accept the field, tell the user how often the wall refreshes now (once a day on the free plan) and that a faster refresh needs a higher Juicer plan, so they can upgrade before the event.
7. **Get the wall on screen**: `get_feed_embed`. For a big screen, use the iframe or JavaScript snippet in a full-screen page; for the event website, the snippet or the WordPress shortcode (needs the Juicer WordPress plugin). Display styles are chosen in the Juicer dashboard.
8. **Test together**: ask the user to post a test with the hashtag, then check it arrives with `list_feed_posts`.

## During the event

The user moderates by chatting with you:

- "What's waiting?" → `list_feed_posts` filtered to posts waiting for approval; show them numbered, short, with the poster's name.
- "Approve 1, 2 and 4" → `moderate_post` `approve` for each, or `bulk_moderate_posts` for many at once.
- "Hide the one from @..." → `moderate_post` `reject`.
- "Pin the speaker photo" → `moderate_post` `pin`.
- "Block the word X" → `update_feed` `disallowed`.

Offer to check for new waiting posts every few minutes with an OpenClaw Automation and send a short message only when something is waiting.

Before approving in bulk, read the posts yourself and point out anything that looks off-topic, rude or like spam, so the user decides with that in mind.

## After the event

Offer a recap: number of posts and posters, top posts by likes from `get_feed_analytics` and the wall itself as a link for the website. Ask before deleting the feed; many organisers keep the wall as a memory page.
