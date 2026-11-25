---
name: ppl
description: "Create and manage AI series and videos on PPL (ppl.xyz) for a creator through the PPL connector: read their characters, series and world, write a prompt for a video model, quote the gem price, render an episode as a draft, follow the job, manage series, world assets, collabs and drafts, and read stats and earnings. Use when the user mentions PPL, their PPL characters or series, making or editing an episode, a collab, gems, or their PPL drafts."
version: 1.0.0
homepage: https://www.ppl.xyz/mcp
metadata:
  openclaw:
    emoji: "🎬"
    homepage: https://www.ppl.xyz/mcp
---

# PPL

PPL (ppl.xyz) is where a creator makes AI series and videos with their own
characters. Through the PPL connector you act on the creator's own account,
with the same rules, prices and limits as the app. This skill is how to do
that well. The full tool list is in [references/tools.md](references/tools.md).

Generated from the PPL server. Do not edit by hand.

## Connect PPL to OpenClaw (once)

If no `ppl__` tools are available, PPL is not connected yet. Ask the
creator before changing their OpenClaw config, then run:

```sh
openclaw mcp set ppl '{"url":"https://api.ppl.xyz/mcp?ref=clawhub","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login ppl
```

`login` prints a link. The creator opens it, signs in to PPL (in the PPL app
or with Google on ppl.xyz), picks what OpenClaw may do and a daily gem limit,
and approves. OpenClaw then saves the sign-in and renews it on its own. Check
it with `openclaw mcp probe ppl`. The creator can change permissions or
disconnect at any time in PPL › Settings › Connected Apps.

In OpenClaw the tools are named `ppl__<tool>` (for example
`ppl__show_home`); the tool names below are without that prefix.

## Start every session

1. If the creator is new to this connection or unsure what to make, call
   `show_home`: their characters, series, gems, videos left today and
   ideas for the next episode, as a card where cards are supported.
   Otherwise call `get_account`: the plan, gems, caps and what this
   connection may do.
2. Call `list_characters` and `list_series` to find what the creator is
   talking about. Use ids from these tools; never invent one.
3. Before writing a prompt or picking settings, call `get_creation_guide`.
   Lengths, prices and prompt limits depend on the creator's plan and
   change over time. Do not rely on what you remember.

If a tool you expect is missing from your tool list, the creator has that
switch off for this app. Say so and point them to PPL › Settings › Connected
Apps. Do not look for a way around it.

## Making an episode

1. Read the show with `get_series` (synopsis, cast, the season plan and its
   next planned episode). For ideas, `get_episode_ideas`.
2. Read the character's world with `get_world` when the scene needs a saved
   location, prop, look or crew member.
3. Write the prompt. It is rendered as written (an idea's summary sent
   unchanged is the one thing PPL writes out for you, to the length).
4. Price it with `get_quote` and tell the creator the gems before you spend.
5. Call `create_episode` with `maxGems` set to what they agreed to and a
   fresh `idempotencyKey`. Then follow the job with `get_job`.

How creating works:

- create_episode renders your prompt exactly as written. PPL adds only a short identity and voice line for the characters; it does not rewrite the prompt. One exception: a get_episode_ideas summary (or title) passed as the whole prompt, unchanged, is a one-line idea, and PPL writes it out to fill the length you picked, as it does when a creator taps that idea in the app. Change a word and it renders as written.
- Every render lands as a draft. Nothing is posted until publish_draft is called (if this connection is allowed to publish) or the creator publishes in the app.
- Pass seriesId to make the next episode of a series (and planSlot to fill a planned episode from get_series). Leave seriesId out for a standalone video.
- Add the creator’s saved locations (locationIds), props (propIds) and up to 6 cast characters. There is no fixed number of locations or props: each model takes a fixed number of reference images (referenceBudget in get_creation_guide: imageSlots, and how many a character, a location and a prop each use). Characters are placed first, then locations, then props, in the order you pass them. On Seedance models tagged locations and props are sent as reference images; on other models they are described in the prompt only.
- When you tag more than the model can use as images, get_quote and create_episode say so in referencesNotUsed with the counts left out: tell the creator before rendering, or tag fewer. Nothing is refused for it, and everything tagged is still named in the prompt.
- For a collab with another creator’s character pass collabCharacterId. That character must allow collabs with this one.
- An outside image (a link, or a file the creator has) is never used directly in a video. Bring it in with import_image or start_upload, turn it into a location, prop, vehicle or crew member with create_asset (PPL re-draws it in the character’s art style), then tag that asset here by its id from get_world.
- A video is 15, 30 or 60 seconds: Free includes 15, Pro 15 and 30, Studio all three (lengthsByPlan in get_creation_guide). A length above the creator’s plan is refused with plan_locked. Other lengths a model renders (5, 10, 20, 25) are still accepted when sent, within the plan’s longest.
- Write the prompt for the length it will be rendered at: get_creation_guide pacing gives, for each length, how many beats fit, the most spoken words, and the shape (15 seconds: one idea, one turn and a button; 30: setup, turn, payoff; 60 is rendered as two 30-second parts cut together, so write two movements, each complete, with its own spoken line). create_episode renders the prompt as written and does not re-fit it: when the creator changes the length, rewrite the prompt for the new length (cut or add beats and lines) before you quote and create. A prompt with more speech than the length holds comes back rushed or cut off.
- Every plan renders video at 480p, on the model PPL picks: leave model and quality out of get_quote and create_episode. A model key or a higher quality that is sent is still accepted; 720p and 1080p are rendered and priced at 480p. Extending, editing or re-rendering an older 720p or 1080p draft is also rendered and priced at 480p, and an extended video is saved at 480p as a whole.
- Every image (a look, a location, a prop, a poster take) is drawn on PPL’s default image model at 1K, one image per request, on every plan. No tool takes an image model, size or count.
- A model’s lengthsSeconds are single renders; its longLengthsSeconds are longer videos PPL renders and extends in one go, when the plan allows them. A finished draft can also be made longer afterwards with extend_draft, up to the limit get_draft_prices states, which can be more than the plan’s picker lengths.
- Give a new crew member a name in create_asset. Without one PPL coins it, and sometimes cannot.
- PPL saves the named supporting characters and pets a video introduces as cast (crew with source "episode" in get_world), unless the character has Auto Save Assets off. To bring one back, name them in the prompt or pass their id in cast: they render from their saved look. A cast member only becomes a character with its own profile when the creator asks for that (claim_cast_member, which uses a character slot). A cast member made by hand (create_asset with kind crew) is free, up to 10 a day per creator; past that create_asset returns rate_limited until the next day.
- A prompt may call a person, a pet, an object or a place by a proper name ("Nina", "the Eternal Stone", "the North Tower"). One that is already in the character’s world (get_world) is sent to the video model as a reference without being tagged. A saved cast member the prompt names is used even when you also pass other cast. For props and locations, the ones you pass in propIds or locationIds are the only ones of that kind. A new one is drawn first, as part of the render job, sent to the video model and saved to the world for free, at most 2 cast, 3 props and 1 location per video; this adds one to three minutes to the job and never changes its price. Roles and generic things ("his sister", "a sword", "a room") are not drawn, and real people and existing franchise characters are refused. This is off when the character has Auto Save Assets off, and never happens on a collab. After a video, an object or place the prompt did NOT give a name is saved to the world only when a later video shows it again; give it a name in the prompt to keep it from the first video. The character’s own worn or carried gear is never saved as a prop.
- Write every spoken line in quotes with its speaker (Nina says: "We are closed."), or ask for narration or a voice-over. A prompt with no spoken line and no ask for speech is rendered with nobody speaking: PPL tells the model so and sends no voice reference (on WAN and Kling it writes a line or two instead).
- A prompt that is about a song being performed or played (a music video, "drops a track", "the chorus plays", someone sings or raps) is made as a music video or a musical: PPL writes the song and the character sings it. Music that is only in the scene ("a song plays softly on the radio") stays an ordinary video, which gets an instrumental score under it unless the prompt has its own "Music:" line.
- Renders take one to several minutes. Poll get_job about every 30 seconds. Never start the same render again while one is running.

## Spending gems

- Gems are the creator's money. State the price and get a clear yes before
  any call that spends them. Never raise `maxGems` on your own to get past a
  refusal.
- `maxGems` is the most the call may cost. A call that would cost more is
  refused with the real price and nothing is charged; show the creator that
  price and ask.
- `idempotencyKey` is a new unique string for each new request. If a call
  times out or you are unsure it went through, send the SAME key again: you
  get the first result and nothing is charged twice. A new key is a new
  purchase.
- Each connection has a daily gem limit the creator chose (2,500, 5,000, 10,000 or no
  limit; it starts at 10,000). When it is reached, calls that spend are
  refused until midnight Pacific. Only the creator can change it, in the app.
- A failed render is not charged. `retry_job` starts it again as a new,
  charged render; ask first. A storyboard's render was paid for with its
  storyboard: its retry gives those gems back once, then is charged the
  same way.
- You cannot buy gems, change the plan, cash out or move money. Send the
  creator to the PPL app for those.

## Drafts, publishing and releasing

- Renders land as drafts. Show the creator the draft (`get_job`,
  `list_drafts`) and let them decide.
- To change a draft: `get_draft_prices`, then `rerun_draft` (another take),
  `edit_draft` (a described change) or `extend_draft` (more seconds). Each
  costs gems. `discard_draft` removes one for good; its gems are not
  returned.
- `publish_draft` posts a draft where other people can see it, and
  `release_episode` releases a held episode to followers. Do either only
  when the creator has asked for that specific draft or episode to go out.
  A finished render is not a request to publish.

## The character's world

- `get_world` lists looks, locations, props and crew with their ids. Tag
  them in `create_episode` by id.
- When the creator asks to see their world, call `show_world`: the same
  result, drawn as a gallery where the assistant supports cards. Use
  `get_world` for every other read.
- `create_asset` adds a location, prop, vehicle or crew member from a
  description; `edit_asset` re-draws one in place and `restore_asset` undoes
  the last change. `get_asset_ideas` suggests what to add.
- A new look is two steps: `create_style` draws a draft, and `save_style`
  makes it the character's current look and re-draws their sheets. Saving
  costs gems and changes how the character appears everywhere; confirm first.
- Images from outside: `import_image` for a public link, or
  `request_upload` to show the creator a file picker (`start_upload` for a
  client that can send a file itself). An outside image is only ever a
  reference that PPL re-draws in the character's art style.
- `remove_asset` deletes a location or prop for good. Do it only when the
  creator asked for that item to go.

## Series

- `create_series` develops a new show from a premise (the first for a
  character is free, later ones cost gems) and `save_series` keeps it,
  which makes it active so episodes can be made. `update_series_settings` changes what episodes cost viewers
  and how they are released; switching release to "at once" releases
  everything that was waiting, so confirm first.
- `delete_series` and `delete_episode` cannot be undone for viewers. Name
  the series or episode back to the creator and get a yes.

## New characters

- `start_character` begins a new main character from a written
  description. PPL draws it in each art style, designs voices and proposes
  names, traits and backstories; that part is free. The backstory can also
  be the creator's own words (`update_character_draft` `backstory`, up
  to 1,000 characters); PPL's backstories are then only suggestions. An account has one
  character draft at a time, shared with the app: if one exists, ask before
  replacing it.
- Where the assistant shows PPL's character card, the creator picks the
  look, voice, name, personality and backstory in the card and creates the
  character there, after a confirm step. The card keeps itself up to date:
  do not list the options again and do not call `get_character_draft` to
  check on it.
- Without the card, read the options with `get_character_draft` (it says
  what is still being made) and show the creator the look images and voice
  samples as links. Record what they pick with `update_character_draft`.
- `finish_character` creates the character and cannot be undone from
  here. It counts toward the plan's limit on main characters. Without the
  card, show the chosen look, voice and name and get a clear yes first. The
  creator's current character stays selected in the app unless they ask to
  switch.
- A character is never made from a photo here; that is done in the PPL app.

## Collabs

- Another creator's character can only be used if they allow it. Check with
  `get_collab_access`; find partners with `find_collab_partners`.
- `request_collab_approval` and `request_series_collab` send a request to
  another person, and `respond_collab` answers one. These reach real people
  and accepting a booking shares the series' earnings. Send or answer only
  what the creator asked for, one at a time, never in bulk.

## Stats, earnings and questions

- `get_stats` shows views, likes, shares, followers and unlocks.
  `get_earnings` shows what the creator earned. Gems viewers spent
  (`get_stats`) are not the same as money earned (`get_earnings`).
- For how PPL works (plans, gems, selling episodes, releases), use
  `lookup_product_help` instead of guessing.

## When a call is refused

Refusals come back with a `code` and a message for the creator. Relay the
message; do not retry the same call hoping for a different answer.

| Code | What to do |
|---|---|
| `not_allowed` | The switch for this is off. The creator can turn it on in PPL › Settings › Connected Apps. |
| `quote_exceeds_max` | Tell the creator the real price and ask before raising `maxGems`. |
| `insufficient_gems` | The creator needs more gems; that happens in the PPL app. |
| `plan_locked` | The creator's plan does not include this. Say which plan does. |
| `daily_video_cap`, `weekly_video_cap` | The plan's render limit is reached. Say when it resets. |
| `rate_limited` | Wait a minute. A daily limit resets at midnight Pacific. |
| `prompt_refused` | PPL's safety check refused the prompt. Do not rephrase to get around it. |
| `collab_not_allowed` | The other character does not allow this collab. Offer to send a request. |
| `upload_refused` | The image was not accepted; the message says why. |
| `not_found`, `conflict`, `invalid_request`, `invalid_settings` | Re-read the ids and the creation guide, then correct the call. |
