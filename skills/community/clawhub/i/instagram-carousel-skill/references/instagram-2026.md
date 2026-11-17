# Instagram carousels in 2026: what's true

*Instagram changes these details often. Each line says where it comes from; re-check every
quarter.*

## Limits

- **Up to 20 slides** per carousel, in the app and through the API (Meta's content publishing
  docs).
- **API images:** JPEG only, aspect ratio between 4:5 and 1.91:1, up to 8 MB, sRGB. Every slide
  is cropped to the first slide's ratio. 3:4 images are accepted in the app (since May 2025) but
  rejected by the API.
- **The profile grid shows 3:4** (since January 2025), so 4:5 posts lose a thin strip on each
  side in the grid.
- **Hashtags:** at most 5 per post (Instagram's @creators account, December 2025).
- **Through the API you can't add music** to a carousel. Alt text and collaborators exist in
  Meta's API but WoopSocial doesn't set them yet; add them in the app after posting.
- Reported since March 2026: the app lets you reorder or remove slides after posting.

## What Instagram has said about reach

- **Signals:** Adam Mosseri (head of Instagram) named watch time, likes per reach and sends per
  reach as the main signals (January 2025). He said sends count a bit more for reaching people who
  don't follow you yet.
- **Second chance:** if someone scrolls past a carousel without swiping, Instagram may show it
  to them again later starting at slide 2 (Mosseri, as quoted in press coverage). Slide 2 must
  work as a cover.
- **Search:** captions of public professional accounts can show up in Google results (since
  July 2025). The main phrase belongs in the caption's first words.
- **Raw beats polished:** Mosseri's end-of-2025 posts said that overly polished content is
  losing to content that feels real. Plain, readable slides fit that better than glossy
  templates.

Nobody can promise reach. Say what Instagram has said, never a multiplier.

## Testing

- Trial posts (shown to non-followers first) exist for Reels only, not for carousels.
- To test covers, post a different cover on a later carousel with the same format, and compare
  against the account's own recent posts.

## What the numbers mean

- The API reports per post: views, reach, likes, comments, saves, shares, follows. It doesn't
  report per slide.
- The app shows more for carousels (for example which slide was viewed most). Ask the user to
  read it there when it matters.
- WoopSocial stores the lifetime numbers it collects (views, likes, comments, saves, shares,
  unique impressions) with a collection date. Collection runs on its own schedule; a missing
  number means "not reported", not zero.
