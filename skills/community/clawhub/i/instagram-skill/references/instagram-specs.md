# Instagram in late 2026: what's true

Instagram changes these details often. Every line says where it comes from and when it was
checked. `scripts/ig_check.py` uses the same numbers (see `LIMITS` at its top); change both
together. Last checked: 2026-11-04.

## Through the API (Meta's content publishing docs)

| What | Limit |
|---|---|
| Images | JPEG only (no PNG, WebP or HEIC), sRGB, 320 to 1440 px wide, at most 8 MB |
| Image shape (feed) | 4:5 (0.8) to 1.91:1. Taller (3:4, 9:16) or wider is rejected |
| Carousel | 2 to 20 items; images and videos can be mixed; every item is shown at the first item's shape |
| Reels | MP4 or MOV, H.264 or HEVC, AAC audio, 23 to 60 fps, 3 s to 15 min, at most 300 MB; 9:16 at 1080x1920 is the target |
| Stories | One image or one video; video 3 to 60 s; no stickers, links or polls through the API |
| Reel extras | a cover image (JPEG), Trial Reels (`MANUAL` or `SS_PERFORMANCE` graduation) |
| Posts per account | 100 per 24 h in Meta's limits section (another part of the same page still says 50); anything near that reads as spam |
| Alt text | Meta's API has it for images; WoopSocial doesn't set it yet, so it's added in the app |

## In the app (Instagram's own announcements and help pages)

- **Hashtags:** at most 5 per post and per Reel since December 2025 (announced by Instagram's
  @creators account). More are cut or rejected.
- **Caption:** 2,200 characters, 20 @mentions. The feed shows about the first 125 characters
  (two lines) and then "... more".
- **Profile grid:** shows posts at 3:4 since January 2025. A 4:5 post (all the API can post)
  loses a thin strip on the left and right in the grid; landscape posts lose much more. Reel
  covers (9:16) show their middle 3:4. Keep cover text in the middle.
- **Reels in the main feed** are commonly shown cropped to about 4:5 (the middle of the 9:16
  frame); full screen in the Reels tab. Meta doesn't document this crop, it's what creators
  observe, so keep the hook and faces in the middle.
- **Reels interface:** the caption, account name and music line cover the bottom of the screen,
  the buttons sit on the right, the top bar at the top. Meta's safe-zone guidance (written for
  Reels ads, the best published numbers): keep the top 14%, the bottom 35% and 6% on each side
  clear of text. `reel.py zones` draws these areas.
- **Stories:** the progress bar and name cover roughly the top 250 px, the reply field the bottom
  250 px of a 1080x1920 frame. `render_slides.py` with `"ratio": "9:16"` keeps the design between.
- **3:4 uploads (1080x1440)** are accepted when posting in the app, not through the API.

## What Instagram has said about reach

- **Signals:** Adam Mosseri (head of Instagram) named watch time, likes per reach and sends per
  reach as the main signals (January 2025); sends count a bit more for reaching people who
  don't follow you yet.
- **Second chance for carousels:** someone who scrolls past without swiping may see the
  carousel again starting at slide 2. Slide 2 must work as a cover.
- **Original content:** Instagram recommends original content over reposts and reduces reach
  for accounts that mostly repost (Mosseri, 2024 and 2025). Since an update reported on
  2026-04-30 (PetaPixel) and in May 2026, this covers photos and carousels too, not only video:
  accounts that mostly repost others' photos and carousels get little or no recommendation,
  and a copy of someone else's image counts as a repost. The sources describe aggregator
  accounts; for a second account of your own, the same upload is likely seen as a repost of
  the first. Adding a border, caption or headline to someone else's media doesn't make it
  original (Planoly and Uppbeat summaries of the update). Videos with another app's watermark are not recommended either. For several
  accounts of your own, make a real version per account (other cover, other language, other
  order or angle), not just another caption.
- **Trial Reels:** shown to non-followers first; you or Instagram decide later whether
  followers see it. Available to professional accounts above a follower minimum (widely
  reported as 1,000 followers; Instagram doesn't publish it); WoopSocial's validation tells you
  when an account doesn't qualify. Good use: test two hooks of the same Reel as two Trial Reels.
- **AI label:** Meta's API has an AI-generated flag, but WoopSocial doesn't set it. If a post
  has realistic AI images, video or voices, add the "AI info" label in the app.
- **Search:** captions of public professional accounts can show up in Google results (since
  July 2025), and Instagram search reads captions too. The main phrase belongs in the first
  words of the caption.
- **Raw beats polished:** Mosseri's end-of-2025 posts said overly polished content is losing to
  content that feels real. Plain, readable slides and real footage fit that.

Nobody can promise reach. Say what Instagram has said, never a multiplier.

## Posting times

There is no universal best time. Instagram Insights shows when the user's own followers are
online (Professional dashboard > Total followers > Most active times). Use that; after enough
posts, `log.py results` shows which time slots worked for this account. Generic "best time"
tables are averages across other people's accounts: don't present them as advice.

## What the numbers mean

- WoopSocial reads per post: views, likes, comments, saves, shares and unique impressions
  (reach), collected over the first days. A missing number is "not reported", not zero.
- Follows from a post, profile visits, per-slide views and Reel watch time are in the app
  (Insights on the post). Ask the user to copy them into `insights.csv` when needed.
- Compare a post with the same account's own median, never with other accounts.
