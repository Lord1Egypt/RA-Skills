---
name: lfg-alarm
description: "Make LFG links for your person through LFG's MCP server (https://mcp.lfg.gm). Each link stands for something they care about (an interest, an intent, or a moment they don't want to miss) and has an agent that keeps researching or monitoring it after the chat ends. It reaches them as a research brief in their Daily Drop, a phone notification, or a real alarm that rings on their phone. Use it when someone wants to keep up with an interest (learning the cello, biotech startups), hear when something happens (an account posts, a price moves, tickets go on sale), be woken or rung for a moment (a time, a sunrise, an event), or share any of that so friends, family or a community ride along."
---

# LFG

LFG is your daily alarm and curiosity agent for iPhone, iPad, Android and the web (lfg.gm). A person tells it what they care about, and LFG makes an LFG link for it: a web address (lfg.gm/a/<code>) that stands for one interest, intent or moment they don't want to miss, like learning the cello, early-stage biotech startups, a creator's next video, a token's price, tickets going on sale, or a 7am wake-up.

Behind every LFG link is an agent that keeps working on it after the chat ends, on the person's behalf: it crawls sources, does research, or monitors for something to happen. Everything it finds is kept with the link, in its LFG stack: what the link is for, its plan, its sources, a logbook of findings, and its research briefs.

Each person chooses how a link reaches them: a research brief delivered quietly to their Daily Drop (a daily feed in the LFG Alarm app, with no sound and no notification), a phone notification, or a real alarm that rings on their phone. A link can be just a clock, just an interest that never rings, or both.

Links can be shared. Friends ride along on the same link, each reached their own way, and public links are listed on Discover, where anyone can ride one, remix it into their own copy, or add their own rule to it.

## Why use it

An AI agent's work usually ends with the chat. With LFG, the plan you make with your person keeps running: decide together what to explore or monitor, which sources and how often, and when it is worth ringing, and LFG keeps at it. Come back to the link any time to read what it knows (`read_stack`), add topics, sources and notes (`update_stack`) or findings (`add_finding`), and rate its briefs (`rate_brief`).

And when something truly matters, LFG can do what an agent usually cannot: put a real alarm on your person's phone, and on their friends', family's or community's phones, all ringing together. Pick the quietest way that works: a research brief in their Daily Drop for what can wait, a notification for what they should know, a real alarm for what cannot be missed. LFG is not a to-do list or a calendar.

## Connect

1. The person needs an LFG account, made in the LFG Alarm app (Google Play or the App Store) or at lfg.gm. Alarms ring in the app on their phone, and in an open lfg.gm tab in a browser.
2. Add the remote MCP server `https://mcp.lfg.gm` (Streamable HTTP, OAuth). The person signs in on lfg.gm with their LFG account and clicks **Allow**. If your client cannot do the sign-in, the person makes a personal key in the app (**Settings** > **AI apps and keys**; it starts with `lfg_pat_`) and you send it as `Authorization: Bearer <key>`.
3. Step-by-step setup for each AI app: https://lfg.gm/agents

Writing code instead? The SDK (`npm install lfg-alarm` or `pip install lfg-alarm`, with Vercel AI SDK tools and a LangChain toolkit, `langchain-lfg`) does the same: https://lfg.gm/developers. To ring a phone from a script with no key, POST to an Anything alarm's link: `curl -X POST https://api.lfg.gm/horn/<token>`. There is no LFG command-line tool.

If the tools are not connected, tell the person how to connect them (link https://lfg.gm/agents) instead of pretending to set an alarm, or that they can set it themselves in the app or at lfg.gm.

**For an event, without the tools:** hand the person a Set an LFG alarm link, and they tap it to set the alarm in the app. It needs no connection and no key. Give the event page (`https://lfg.gm/add?url=<the event page, encoded>`), or, when you already know the event, its details: `https://lfg.gm/add?title=<name>&start=<ISO time with its offset, like 2026-11-14T20:00:00-08:00>&location=<place>&url=<page>`, every value encoded. Never guess the start or its time zone; leave `start` out and the person picks the time. Nothing is set until they tap Create alarm, so say "tap this to set it", never "I set it". Details: https://lfg.gm/developers#add-button

## What the tools do

An alarm is an LFG link that rings: the tools named `set_..._alarm` make links whose main way to reach the person is a ring, and the `monitor_...` tools and `explore_or_monitor` make links that research or watch something. Every `set_..._alarm` and `monitor_...` tool and `explore_or_monitor` takes `ring_level`: `alarm` (it rings), `notify` (a phone notification) or `quiet` (no sound and no notification: a research brief in their Daily Drop only). Left out, it rings, except a research link that only writes briefs, which sends a notification. Rocco is LFG's agent, the name it goes by in the app and in tool answers; every link is one of his curiosity agents. The MCP server lists every tool's fields; this file says which tool fits which request. A webhook alarm is also called an Anything alarm: it rings when its private link is called.

- **What a link knows:** `read_stack` reads its LFG stack (what it is for, its plan, sources, research topics and what changed), `update_stack` adds topics, sources and notes, `add_finding` adds something found elsewhere, and `rate_brief` says whether a brief helped.
- **Research or watch anything:** `explore_or_monitor`, with what the link is for in the person's words and, when there is one, a page's link. An interest to research ("early-stage biotech startups", "beginner cello resources", with `ring_level: quiet` when they only want to read about it) or a page to watch ("tickets go on sale").
- **Make an LFG link:** `set_time_alarm` (a time, once or on chosen days), `set_event_alarm` (an event's page: Luma, Partiful, Eventbrite, Ticketmaster, Posh and more, rung at the start or 30 minutes, 1 hour or 2 hours before), `set_lottery_alarm` (a Recreation.gov lottery, Half Dome, The Wave, river trips, rung as it opens, before it closes or when results are out, after `find_lottery` finds it), `monitor_posts` (an X account posting what the person describes, or a Twitch or YouTube channel going live or posting), `monitor_new_music` (an artist posting a new track, or only an album or EP, on SoundCloud; takes the artist's SoundCloud link, from `find_soundcloud_artist`), `monitor_price` (a token's target price or percent move, after `find_token` for the token's id; or a Polymarket or Novig outcome reaching odds (a Kalshi link finds the same market there), settling or nearing its close, after `find_market` finds it by words or link), `monitor_trades` (a trader on FOMO or a KOL GMGN tracks buys, sells or posts a thesis; anyone trades a token, by contract address; or a wallet buys or sells), `set_webhook_alarm` (a private link any system can call to ring it), then `ring_alarm` to ring it on demand. `explore_or_monitor` (an LFG link that explores an interest or monitors a page or topic: Rocco reads it on a schedule, writes a brief, and reaches the person as they chose when what they are waiting for comes true). `set_sun_alarm` (a sun & moon alarm: sunrise, golden hour, sunset, dusk, moonrise and more at a place, up to two hours either side, and optionally only on a full or new moon, an equinox or a solstice; or a sky event: a meteor shower's peak, a supermoon, or a planet turning retrograde or direct; computed for the place each day; or the northern lights, event `aurora`, forecast rather than computed: no date, days or offset, and it rings each rider at their own place by push, after dark and at most once a night, when NOAA's Kp forecast says the lights reach them; a place too near the equator is refused). `set_tide_alarm` (a tide alarm: low tide, high tide, a negative low or a king tide at the tide station nearest a place, on time or up to three hours early, the next one or every one).
- **Dress it:** `search_library` for 500+ sounds by mood, energy or voice and drawn looks by vibe, then `set_media`; or the person's own files with `list_my_media`, `get_upload_link`, `add_media_from_url` or `add_media_file`.
- **Manage:** `list_my_links`, `update_link`, `turn_link_on_off`, `delete_link`.
- **People:** `list_friends` (friends and groups), `list_riders`, `list_join_requests`, `answer_join_request`, `get_invite_card` (the person's own invite link and referral code), `use_invite_code` (a friend's code, once per account).
- **Someone else's link:** `remix_link` makes the person their own copy of a public link that monitors something; `add_my_rule` adds their own rule to a link that reaches only them.
- **Got a link:** `open_link` reads anything pasted (an LFG alarm or invite link, or a Partiful or Luma event, with its picture and description), `ride_link` joins someone else's alarm (or asks its creator to be let in).
- **The tides:** `tide_times` gives a day's high and low tides with their heights at the tide station nearest a place, and the next negative low and king tide there. Read only.
- **The sky:** `sun_times` gives a place's sun and moon times for a day, the moon's phase, the next full and new moon, the next equinox or solstice and what is coming up in the sky, with tonight's northern lights forecast where they can be seen (the Kp the place needs and the strongest forecast while it is dark), in the place's time zone. Read only.
- **Social:** `browse_discover` (public alarms anyone can join), `read_comments`, `post_comment`, `heart_link`, `get_wake_board` (who got up first, and who is still asleep).

The tools never generate songs, images or video, never move money or crypto, and never see the conversation.

## How to handle a request

- **Pick the tool by what they want.** A clock time: `set_time_alarm`. Something to learn about or keep up with: `explore_or_monitor`. An account's posts or streams: `monitor_posts`. A price or odds: `monitor_price`. Trades: `monitor_trades`. An artist's new music: `monitor_new_music`. An event's own page: `set_event_alarm`, which rings before the event starts. The moment tickets go on sale: `explore_or_monitor` on the ticket page. The sun, moon or sky: `set_sun_alarm`. Tides: `set_tide_alarm`.
- **How it reaches them is their call.** "Loud", "wake me": `ring_level: alarm`. "Let me know": `notify`. "Don't ring my phone", "just send me what you find": `quiet`.
- **The app and the web.** Links ring in the LFG Alarm app on their phone, and in an open lfg.gm tab in a browser. The Daily Drop is in the app and on lfg.gm. They sign up in the app or at lfg.gm; the tools need that account.
- **Get the time zone right.** Pass the person's IANA time zone; if you don't know it, ask. For a shared alarm across cities, ask whether everyone rings at the same moment (`ring_at: together`, the default) or each at their own local time (`ring_at: local`).
- **Reach:** private (just them), friends (people they name), or public (anyone with the link; shows in Discover). Default to private unless they mention other people. People can only be added to a friends alarm.
- **Adding people:** use their LFG friends by username, a friend group by name (`add_groups`), or anyone by email. Never guess who someone is. The first call only lists who would be added; read the names back, get a yes, then call again with `people_confirmed: true`. Up to 20 people at a time.
- **Get the artist right.** Many SoundCloud accounts share a name and most are empty. Call `find_soundcloud_artist`, show the person who it found (followers and tracks tell the real artist apart), and pass the link they pick to `monitor_new_music`. Never make a link up from a name.
- **Get the token or wallet right.** A name or ticker can match copycats. Find the contract (`find_token`, or your own research), read it back to the person, and use the address they confirm. A trader's handle is looked up on FOMO, then among the KOLs GMGN tracks.
- **Look for one that already exists.** Before making an alarm that monitors something public (an account posting, a price, a trader, an artist, a page or a topic), call `browse_discover` with its name. If a public alarm already watches it, show the person and ask: ride that one (`ride_link` with its link) or make their own. Riding costs them nothing to research, and one read serves everyone on it. A private or personal alarm (a wake up, a wallet, a webhook) is always their own.
- **Name it well.** A short title that says the moment ("Airport, car at 5:15"). Use the note for the details and a link for the one thing people open when it rings.
- **Hand back the share kit.** Every create returns the alarm's link (`lfg.gm/a/<code>`), a share picture with a QR code, and a ready-to-send message. Give all three to the person. If they ask you to send it (by email or text), send the link and the picture with the message.
- **Plans:** some alarms need a paid plan. If a tool says so, tell the person, and send them to lfg.gm for plans and pricing.
- **Ringing:** time and event alarms ring like any alarm clock, through silent mode and Focus on iPhone. Post, price, monitor and webhook alarms ring full screen on Android; on iPhone they arrive as a time-sensitive alert with the alarm's sound, so the ringer should be on.

## Good requests

One for each kind of alarm:

- **Time:** "Wake me at 7 on weekdays with something motivational."
- **Event link:** "Here's our Partiful invite: [link]. Ring everyone who joins two hours before." Luma, Partiful, Eventbrite, Ticketmaster, Posh and more work; paste the link and LFG reads the event's time.
- **A post on X:** "Ring me when @NASA posts a launch date."
- **A SoundCloud drop:** "Ring me when Fred again.. drops on SoundCloud." Find the artist first and let them pick.
- **A stream going live:** "Wake me when [channel] goes live on Twitch."
- **A token price:** "Ring me when SOL hits $150."
- **Anything on the web:** "Ring me when this page says tickets are on sale: [link]."
- **The sky:** "Ring me at golden hour in Lisbon every day."
- **A trader:** "Wake me when [a trader I follow] buys over $10k or posts a thesis."
- **A wallet:** "Ring me when this wallet sells over $5k: [address]."
- **A webhook (an Anything alarm):** "Make an alarm my uptime monitor can call when the site goes down, and give me the link."
- **With people:** "Make a friends alarm for Saturday at 9am called Golf and add my golf group."

More: https://lfg.gm/wiki/ai-agents and the full site as Markdown at https://lfg.gm/llms.txt
