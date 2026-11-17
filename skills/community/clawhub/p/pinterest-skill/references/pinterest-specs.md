# Pinterest: limits, rules and how pins are found

Checked November 2026. Each line names its source; "Pinterest" means Pinterest's own pages or API
spec, "practitioner" means people who run Pinterest accounts for a living, "measured" means a study
of real pins. When Pinterest's pages disagree, the stricter number is used.

## Text

| Field | Limit | Source |
|---|---|---|
| Title | 100 characters; about the first 40 show in feeds | Pinterest API spec v5.28 (github.com/pinterest/api-description); product specs (help.pinterest.com/en/business/article/pinterest-product-specs) |
| Description | 800 characters; some screens and many guides still use 500 | API spec; product specs |
| Alt text | 500 characters | API spec |
| Link | 2,048 characters | API spec; WoopSocial schema |

Hashtags have not been clickable since about 2020; Pinterest calls them optional and points to
keywords instead (practitioners agree they no longer help).

## Media

| Type | Rules | Source |
|---|---|---|
| Image | PNG or JPEG, up to 20 MB, 2:3 recommended (1000x1500); taller than about 1:2.1 is cut in the feed | Pinterest product specs |
| Video | MP4, MOV or M4V, H.264 or H.265, 4 s to 15 min, up to 2 GB; 1:1, 2:3, 4:5 or 9:16; 720p or more; 6 to 15 s recommended | Pinterest product specs; create.pinterest.com/fundamentals |
| Carousel | 2 to 5 images (API) | API spec; not sent by this skill |

Idea Pins were merged into regular pins in 2023 (create.pinterest.com/blog/new-pin-format-update).

## How pins are found

- Pinterest ranks by relevance and engagement. Keywords count in the pin title, description,
  board title and description, and the page's URL; the image, text and keywords should match the
  landing page. (Pinterest: help.pinterest.com/en/business/article/pin-performance-and-distribution)
- Boards: specific, keyword-named ("vegan breakfast recipes"), 20 to 100 pins each. (Pinterest:
  create.pinterest.com/fundamentals)
- Text on the image is optional but helps; keep it readable on a phone, the key message at the top.
  (Pinterest: fundamentals; business.pinterest.com/creative-best-practices)
- Logo small, the subject in a real setting, "genuine rather than overly produced". (Pinterest:
  creative best practices; fundamentals)
- Plan 45 to 60 days ahead (Pinterest); practitioners plan 2 to 3 months ahead for big seasons.

## Fresh pins and repeats

- Pinterest asks for original content regularly; repeatedly saving the same pins or re-uploading
  content can get an account blocked from creating pins as spam. (Pinterest: pin performance article)
- Practitioners make several different designs per page and space them out; new images for a page
  keep getting distributed where re-uploads of the same image don't.

## Pace and spam

- Community guidelines (May 2026): no repetitive or deceptive content made to earn money; link
  shorteners can be blocked when abused; deceptive redirects are banned; no automation Pinterest
  hasn't approved (the official API and approved partners are fine). (policy.pinterest.com)
- There's no official daily cap. Practitioners in 2026 recommend a few fresh pins a day at most,
  consistency over volume. This skill defaults to 1 a day per account and stops above 5 (change
  `rules.max_per_day` if the account is established and the user wants more).
- Triggers practitioners name for spam flags: bursts, one URL to many boards in a short time,
  duplicate images, regulated niches (health claims, weight loss, gambling).

## Timing and results

- There's no set engagement window; older pins can take off later. (Pinterest: pin performance article)
- New pins often get few impressions in their first days and keep being distributed for months, so
  practitioners judge pins over two to three months, never in the first week.
- Metrics: impressions, saves, pin clicks (close-up opens), outbound clicks (to the site).
  Practitioners judge by outbound clicks first, then saves. Outbound clicks for a site need a
  business account with the website claimed. (Pinterest: help.pinterest.com/en/business/article/pinterest-analytics)

## AI images

- Since April 2025 Pinterest labels images "AI modified", from file metadata and its own
  classifiers. Since October 2025 people can see less AI content in beauty, art, fashion and home
  decor. (Pinterest announcements, reported by TechCrunch 2025-04-30 and 2025-10-16)
- The API now has an `ai_disclosures` field; WoopSocial doesn't send it, so say it in the
  description.

## Developer access (why WoopSocial)

A new Pinterest developer app starts on Trial access: its pins are visible only to the person who
made them. Public pins need Standard access, with an app review and a demo video of the sign-in
flow. (developers.pinterest.com/docs/key-concepts/access-tiers) Posting through WoopSocial uses its
approved app, so none of that applies.
