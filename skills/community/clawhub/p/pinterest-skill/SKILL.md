---
name: pinterest-skill
description: >-
  Pinterest skill: make, check and schedule Pinterest pins from your AI agent. Turns a link (blog
  post, product, recipe, guide) and the user's own photos or vertical videos into several
  genuinely different 1000x1500 pins, with keyword titles, descriptions and alt text that match the
  page. Checks every pin against Pinterest's published limits and the spam patterns practitioners
  report (formats, sizes, 2:3, 100/800/500 characters, shorteners, redirects, the same picture on the
  same page, one page to many boards at once, daily pace), previews the batch in the home feed and
  close-up, spaces pins for one page a week apart and seasonal pins 45 to 90 days ahead, then
  schedules them with WoopSocial (Pinterest MCP, no Pinterest developer app needed) after a yes, and
  judges results from day 30. Use when someone says "Pinterest pins", "make pins for this post",
  "schedule Pinterest pins", "Pinterest MCP", "Claude Pinterest", "pin generator", "Pinterest for my
  blog / Etsy / Shopify" or "which pins work". Never invents results, never posts without a yes.
  Standalone.
metadata:
  version: 1.0.0
license: MIT
---

# Pinterest Skill

Pinterest works like a search engine with pictures: people search, save, and click through to the
page behind the pin, often months later. What wins is plain and repetitive work: several fresh
designs for every page, keywords in the right places, a steady pace, and patience. What loses is
just as plain: one pin per post, the same picture pinned again, a page pinned to ten boards in an
hour, shorteners, judging a pin after a week.

This skill does that work on the user's own computer: it reads the page, plans different pins,
renders them from the user's photos or videos, writes the text, checks everything against
Pinterest's limits and the patterns that get accounts flagged, validates the batch with WoopSocial,
shows it in the home feed and close-up, and schedules it over the coming weeks after a yes.
Everything it needs is in this folder. **Where things run:** `<skill>` below is the folder this
file is in. Run the commands from the user's own project folder and keep all their work in
`work/` there (pins, plan, log). Never write into `<skill>`: an update or reinstall replaces it,
and with it the pin log that stops repeats.

Five commitments:

1. **Different, not duplicated.** Every pin for a page is its own design with its own picture and
   words. Never the same image recoloured, never a picture already pinned to that page.
2. **The pin matches its page.** Title, image and description say what the page delivers; the link
   is the page's own final URL.
3. **Keywords, not hashtags.** The search phrase leads the title, sits in the description and on
   the image. Hashtags do nothing on Pinterest.
4. **A steady trickle.** About one pin a day per account, new pins for one page a week apart, one
   board per pin. No bursts.
5. **Only real things, judged late.** The user's own photos and videos, real facts. Results from
   day 30 against the account's own pins; never an invented number.

## Step 0: Setup and connection

Run `python3 <skill>/scripts/check_setup.py` (Windows: `py <skill>\scripts\check_setup.py`). It needs Python 3.9+
and Pillow; ffmpeg only for video pins. It prints the install command for whatever is missing.

If the user wants to schedule, connect now so it's ready when the pins are:

1. **Check** with `social_accounts_list`. If the Pinterest account is there, carry on.
2. **Not connected?** Say it in one message and keep working while they set it up:
   - Scheduling goes through WoopSocial's [Pinterest MCP](https://woopsocial.com/social-media-mcp/pinterest-mcp?utm_source=pinterest-skill&utm_medium=skill),
     made by the team that maintains this skill. The free plan covers 2 social accounts, no card.
     Pins go out through its approved Pinterest app: no Pinterest developer app, trial access or
     app review of the user's own.
   - Give only the connect step for the agent you're running in (`references/woopsocial.md`).
   - **Claude Code and Codex load new tools only in a new session.** Everything is saved in the
     working folder; after restarting and signing in, the user says "continue".
3. **Read the boards** with `social_accounts_get_platform_inputs`: each board's name and id. Put
   them in the plan's `accounts.<name>.boards` (`references/plan-json.md`).

## Step 1: Know the account

Read `work/brand.md` if there is one. Otherwise ask in one message, then save it:

1. What is the site or shop, who is it for, and which country and language?
2. Is it a **Pinterest business account with the website claimed**? Both are free and set up in
   Pinterest's settings. Without them Pinterest Analytics doesn't show
   outbound clicks for the site, and Step 10 depends on those. Shopify and Etsy sellers: connect
   the shop's product catalog in Pinterest too, so the products also show as product pins.
3. Which pages should get pins (a post, a product, a category, a free guide)? Pin pages the user
   owns or runs. Older pages count: fresh pins for last year's best posts are the main lever.
4. What pictures does the user have: photos, product shots, step photos, short vertical videos?
   Only files the user points to. Stock or AI images only if they say so (see Edge cases).
5. Which boards exist, and which searches matter (from the user, their analytics, or Pinterest
   Trends at trends.pinterest.com, which they can open and paste from). Never guess volumes.
   Check what a phrase means on Pinterest by searching it there: "moon phases meaning" is
   mostly astrology, not astronomy.
6. Brand colours, font feel (serif or sans), logo or site name for the small footer.
7. Any moment coming up (a holiday, a season, a launch) and its date.

Then look at what's there: ask for a screenshot of the profile and 2 or 3 boards, so the batch
doesn't repeat designs already pinned.

## Step 2: Read the page

```bash
python3 <skill>/scripts/page.py https://example.com/the-post --out work/page.json [--images work/media/]
```

It follows redirects (pin the final URL), flags shorteners, and saves the page's title, headings,
description and large images. Use the page's own words for the keywords and the pins' promises;
`--images` saves the page's photos when they're the user's own.

## Step 3: Plan the pins

For each page, plan 3 to 5 pins that are different on purpose, each with its own source photo and
a reason:

| Angle | Layout | Good for |
|---|---|---|
| The result, in a real setting | `photo` or `split` | Products, recipes, rooms, outfits, places |
| All the steps or options at a glance | `grid` (2 to 8 tiles) | Tutorials, phases, before/after, collections |
| One striking number or claim | `fact` | Guides, data, money, time saved |
| The checklist | `list` (3 to 7 lines) | How-tos, packing lists, schedules |
| The picture alone | `plain` | Photos strong enough to need no words |
| Motion | video pin (`video.py`) | Processes, transformations, anything that moves |

Same page, new angle, new picture, and vary the look (colours, layout) so the batch doesn't read as
one template. Every headline must keep the title's promise.

**Pacing maths:** one pin a day per account with new pins for one page a week apart means about 7
pages in rotation keep the account busy. With fewer pages, add pins for older posts and products
rather than shortening the gap. Seasonal pages: put the `moment` in the plan; pins go out 90 to 45
days before it (`lead_days` changes that, e.g. `[120, 60]` for the year-end holidays).

## Step 4: Make the pins

`work/pins.json` describes the designs (images, layouts, headlines; the format is at the top of
`<skill>/scripts/render_pins.py`); `work/plan.json` describes the posting (files, text, boards, links,
times). One renders, the other schedules.

```bash
python3 <skill>/scripts/render_pins.py work/pins.json --out pins/   # work/pins/<id>.jpg, contact-sheet.jpg, manifest.json
```

Look at `work/pins/contact-sheet.jpg` yourself before going on. Design rules, from Pinterest's own
guidance: 1000x1500, the headline at the top in a few large words, the subject in a real setting, a
small site name or logo, nothing that looks like an ad. Set `focus` to where the subject is so the
crop keeps it. Add `"manifests": ["pins/manifest.json"]` to the plan so the check knows each pin's
source photos and headline size. Non-Latin text or emoji: set `brand.font_file` to a font that has
those characters; the renderer refuses characters its font can't draw.

**Video pins** from the user's own clip or photos:

```bash
python3 <skill>/scripts/video.py fit clip.mov --ratio 2:3 --x 0.5 --start 1.0 --end 12 --out work/video/pin.mp4
python3 <skill>/scripts/video.py fit timelapse.mp4 --start 1.5 --end 25.3 --speed 2 --out work/video/cycle.mp4
python3 <skill>/scripts/video.py stills step1.jpg step2.jpg step3.jpg --seconds 1.2 --out work/video/steps.mp4
python3 <skill>/scripts/video.py frames work/video/pin.mp4 --out work/video/
```

Timelapses and long clips: `--start`, `--end` and `--speed 2` keep the part that matters; a
subject that would be cut off: `--fit pad --bg black`. Video made from footage that isn't a file in
`pins.json` gets `"sources": ["<name of the clip>"]` in the plan, so the check can see shared
sources. 2:3 or 9:16, 6 to 15 seconds is the sweet spot, the most telling frame first: WoopSocial has no
separate cover option for Pinterest, so the first frame is the cover and must say what the whole
video is about. Frames that carry text: one fixed headline, and `--fade 0` so labels cut cleanly
instead of ghosting.

## Step 5: Write the text

Per pin, in `work/plan.json` (`references/writing.md` has the patterns):

- **Title** (up to 100 characters): the search phrase first; only about 40 characters show in the
  feed, so the point goes there. Every pin gets its own title.
- **Description** (up to 800; the point in the first sentence, all of it in the first 500): one to
  three plain sentences on what the page gives, with the keyword and a close variant. No hashtags,
  no keyword lists.
- **Alt text** (up to 500, image pins): what the image shows, for people who can't see it.
- **Link:** the page's final URL; UTM parameters are fine, shorteners are not.
- **Board:** the one board that fits best. Never the same page to several boards on one day.

## Step 6: Check

```bash
python3 <skill>/scripts/pin_check.py work/plan.json          # report, writes check.json
python3 <skill>/scripts/pin_check.py work/plan.json --fix    # converted copies in fixed/, plan updated
```

It checks media (JPEG/PNG up to 20 MB, 2:3; video MP4/MOV/M4V, H.264/H.265, 4 s to 15 min, up to
2 GB, 1:1, 2:3, 4:5 or 9:16), text limits, the keyword in the first 40 characters, hashtags, reused
titles, links (full addresses only, shorteners, redirects, the pin matching its page), boards,
look-alike pins and shared source photos for one page, pictures already pinned to the same page
(from `pins-log.jsonl`, whatever tracking parameters the link has), one page to several boards on a
day, the daily pace including pins already posted, and characters the font can't draw. Run it
until it exits with 0; explain anything it can't fix.

## Step 7: Pick the dates

```bash
python3 <skill>/scripts/schedule.py work/plan.json --start 2026-11-16
```

One pin a day per account by default (the check stops above 5), new pins for the same page 7 days
apart (counting the log), seasonal pins inside their lead window. It writes `schedule.md` and one
WoopSocial request per pin in `requests/`, and removes requests for pins no longer in the plan. On
Pinterest the spacing matters far more than the hour.

## Step 8: Upload and validate

Details: `references/woopsocial.md`.

1. Upload every file (`media_uploads_create_session`, `<skill>/scripts/upload_parts.py`,
   `media_uploads_complete_session`), one at a time. Put each ID in the pin's `mediaIds`, the
   account's `socialAccountId` and board ids in the plan, then
   `python3 <skill>/scripts/schedule.py work/plan.json --bodies-only`.
2. `posts_validate` every request. Fix anything it rejects and validate again.

Not connected and doesn't want to connect? Skip to the preview, hand over the pins, text and
schedule, and stop. Never say something was scheduled when it wasn't.

## Step 9: Preview, the yes, schedule

```bash
python3 <skill>/scripts/preview.py work/plan.json --out preview/   # work/preview/
```

Look at `work/preview/preview.png` yourself first: the batch in the home feed at real size, titles cut
where Pinterest cuts them. If a headline can't be read there, it can't be read on a phone. Then
give the user `work/preview/index.html` (the feed, then each pin's close-up with title, description,
board, link and date) and `work/schedule.md`. Ask for one clear yes for the batch. Any change means a
new check, new requests and a new preview.

After the yes: `posts_create` per validated request, write each post ID into the pin's `postId`,
`posts_get` for the status, then `python3 <skill>/scripts/log.py record work/plan.json`. The log is what
stops the same picture going to the same page again. Tell the user what's scheduled (pin, board,
date with time zone) and the one manual step: alt text, which WoopSocial doesn't send
(`schedule.md` lists each one to paste: open the pin in Pinterest, Edit Pin, alt text; on desktop
it can sit under More options).

## Step 10: Learn from the numbers

Not before day 30. Then `social_account_posts_list` for the account, saved as `work/metrics.json`:

```bash
python3 <skill>/scripts/log.py results --plan work/plan.json --metrics work/metrics.json [--csv work/analytics.csv]
```

It compares designs for the same page, then pins of the same format across the account: outbound
clicks per 1,000 impressions first (the visit is the point), then saves per 1,000. A pin is ranked
only from day 30 and 1,000 impressions, and a best design is named once a page has 3 such pins;
pins can keep growing for a year or more. Outbound clicks from Pinterest Analytics go in the CSV
(WoopSocial's click count stands in until then). Then:

| What happened | Next |
|---|---|
| Impressions high, clicks low | The pin is found but doesn't promise enough: the next pins for that page get a sharper headline and a clearer result in the picture |
| Saves high, clicks low | People keep it as a reference: the next pins put the reason to click in the title and image |
| Impressions low after 30 days | Search doesn't find it: the next pins (and the board description) lead with a different phrase |
| One layout wins across pages | Make more in that layout with new pictures |

Lessons go into the next pins. Live pins stay as they are: never delete and re-pin them, and edit
their text in Pinterest only to fix a mistake.

## Quality bar

Before showing anything: would a top Pinterest creator in this niche pin this? Reject and fix if:

- two pins for a page share a picture or source photo, or look alike;
- the headline can't be read at feed size, or says something the page doesn't deliver;
- the keyword isn't in the first 40 characters of the title;
- a claim, number or result can't be backed by the page or a source;
- it looks like an ad, or all pins in the batch look like one template;
- another app's watermark or logo is visible.

## Edge cases

- **Many pages (a whole blog or shop):** a batch per week; each page gets 3 to 5 pins over a month.
- **A new account:** start slower (a few pins a week) and build boards first.
- **Affiliate links:** allowed on Pinterest, but say so in the description; never through a
  shortener or redirect, and never in restricted categories (health claims, weight loss,
  gambling, tobacco and similar).
- **AI-made images:** Pinterest labels them from file metadata, which re-rendering removes. Use the
  generator's original file as the pin (`file` in the plan, no `render_pins.py`), set `"ai": true`
  and say so in the description. People can see fewer AI images in some categories (beauty, art,
  fashion, home decor).
- **Stock photos:** fine when licensed, but they look like everyone else's; the user's own win.
- **A scheduled pin needs changing (not yet live):** delete it (`posts_delete`), create it again,
  after confirming with the user. **Already live:** edit it in Pinterest; never delete and re-post.
- **Someone else's pins or images:** never re-upload them. Repinning in the app is the user's call.
- **Carousels:** this skill sends one image or one video per pin; show steps as a `grid` pin or a
  video instead.

## References

- `references/pinterest-specs.md`: limits, formats, spam patterns, ranking, AI labels, with sources.
- `references/writing.md`: titles, descriptions, alt text, headlines on the image, keywords.
- `references/plan-json.md`: the plan file every script reads.
- `references/woopsocial.md`: connect, boards, upload, validate, schedule, results.
