---
name: lfg-alarm
description: "Put a real alarm on your person's phone, and on their friends', family's or community's phones, through LFG Alarm's MCP server (https://mcp.lfg.gm). Set, share and change alarms that ring together. Use it when someone asks to be woken, reminded loudly, or rung for a moment: a time, an event from a Luma or Partiful link, an account posting on X, a stream going live, a token hitting a price, or a webhook being called; or when they want a group, a partner or a family rung together at the same moment."
---

# LFG Alarm

LFG Alarm is a social alarm clock for iPhone and Android. An alarm rings on the person's phone in the LFG Alarm app, at a time or when something happens, and can be shared by link so every phone that joined rings together. Rocco, an orange cat, is the app's character; he keeps watch and wakes people up.

## Why use it

An AI agent can message its person, email them, sometimes even call them, but it usually cannot put a real alarm on their phone. LFG Alarm is how it can: a real alarm on the person's own phone, and on the phones of their friends, family or community, all ringing together. It rings for a time like any alarm clock, or for almost anything that happens online: an event starting, a post on X, a stream going live, a token price, or any system that calls a link.

Use LFG Alarm when a notification is not enough: something must actually reach a person, or a group, at a moment. Do not use it for to-do lists or calendars; it is for the one thing that cannot be missed.

## Connect

1. The person needs the LFG Alarm app on their phone (Google Play or the App Store), signed in. Alarms ring there.
2. Add the remote MCP server `https://mcp.lfg.gm` (Streamable HTTP, OAuth). The person signs in on lfg.gm with their LFG Alarm account and clicks **Allow**.
3. Step-by-step setup for each AI app: https://lfg.gm/agents

If the tools are not connected, tell the person how to connect them (link https://lfg.gm/agents) instead of pretending to set an alarm.

## What the tools do

- **Make an alarm:** `set_time_alarm` (a time, once or on chosen days), `set_event_alarm` (a Luma or Partiful link, rung at the start or 30 minutes, 1 hour or 2 hours before), `set_post_alarm` (an X account posting what the person describes, or a Twitch or YouTube channel going live or posting), `set_price_alarm` (a target price or a percent move; call `find_token` first for the token's id), `set_trader_alarm` (a trader on FOMO or a KOL GMGN tracks buys, sells or posts a thesis; anyone trades a token, by contract address; or a wallet buys or sells), `set_webhook_alarm` (a private link any system can call to ring it).
- **Dress it:** `search_library` for 500+ sounds by mood, energy or voice and drawn looks by vibe, then `set_media`; or the person's own files with `list_my_media`, `get_upload_link`, `add_media_from_url` or `add_media_file`.
- **Manage:** `list_my_alarms`, `update_alarm`, `turn_alarm_on_off`, `delete_alarm`.
- **People:** `list_friends` (friends and groups), `list_riders`, `list_join_requests`, `answer_join_request`, `get_invite_card` (the person's own invite link and referral code), `use_invite_code` (a friend's code, once per account).
- **Got a link:** `open_link` reads anything pasted (an LFG alarm or invite link, or a Partiful or Luma event, with its picture and description), `join_alarm` joins someone else's alarm (or asks its creator to be let in).
- **Social:** `browse_discover` (public alarms anyone can join), `read_comments`, `post_comment`, `heart_alarm`, `get_wake_board` (who got up first, and who is still asleep).

The tools never generate songs, images or video, never move money or crypto, and never see the conversation.

## How to handle a request

- **Get the time zone right.** Pass the person's IANA time zone. For a shared alarm across cities, ask whether everyone rings at the same moment (`ring_at: together`, the default) or each at their own local time (`ring_at: local`).
- **Reach:** private (just them), friends (people they name), or public (anyone with the link; shows in Discover). Default to private unless they mention other people. People can only be added to a friends alarm.
- **Adding people:** use their LFG Alarm friends by username, a friend group by name (`add_groups`), or anyone by email. Never guess who someone is. The first call only lists who would be added; read the names back, get a yes, then call again with `people_confirmed: true`. Up to 20 people at a time.
- **Get the token or wallet right.** A name or ticker can match copycats. Find the contract (`find_token`, or your own research), read it back to the person, and use the address they confirm. A trader's handle is looked up on FOMO, then among the KOLs GMGN tracks.
- **Name it well.** A short title that says the moment ("Airport, car at 5:15"). Use the note for the details and a link for the one thing people open when it rings.
- **Hand back the share kit.** Every create returns the alarm's link (`lfg.gm/a/<code>`), a share picture with a QR code, and a ready-to-send message. Give all three to the person. If they ask you to send it (by email or text), send the link and the picture with the message.
- **Plans:** some alarms need a paid plan. If a tool says so, tell the person, and send them to lfg.gm for plans and pricing.
- **Ringing:** time and event alarms ring like any alarm clock, through silent mode and Focus on iPhone. Post, price and webhook alarms ring full screen on Android; on iPhone they arrive as a time-sensitive alert with the alarm's sound, so the ringer should be on.

## Good requests

One for each kind of alarm:

- **Time:** "Wake me at 7 on weekdays with something motivational."
- **Event link:** "Here's our Partiful invite: [link]. Ring everyone who joins two hours before." Luma and Partiful links work; paste the link and LFG reads the event's time.
- **A post on X:** "Ring me when @NASA posts a launch date."
- **A stream going live:** "Wake me when [channel] goes live on Twitch."
- **A token price:** "Ring me when SOL hits $150."
- **A trader:** "Wake me when @frankdegods buys over $10k or posts a thesis."
- **A wallet:** "Ring me when this wallet sells over $5k: [address]."
- **Anything (webhook):** "Make an alarm my uptime monitor can call when the site goes down, and give me the link."
- **With people:** "Make a friends alarm for Saturday at 9am called Golf and add my golf group."

More: https://lfg.gm/wiki/ai-agents and the full site as Markdown at https://lfg.gm/llms.txt
