---
name: growth-calendar
description: Plan, inspect and generate SEO articles on a Timothe Growth Calendar. Use when the user asks about their content calendar, article schedule, planned or published posts, topic clusters, or wants to plan or write SEO articles for their site.
homepage: https://timothe.ai/growth-calendar
metadata:
  openclaw:
    emoji: "📅"
---

# Timothe's Growth Calendar

Product page: [Growth Calendar](https://timothe.ai/growth-calendar)

Growth Calendar keeps a workspace's SEO content schedule: planned articles with publish dates,
reminder notes, and the articles already generated. Each planned article has a reservation that
fires on its date and writes the article without anyone being present.

The MCP tools act on the user's own workspace. Everything is scoped to the workspace their
connection is bound to, so there is no tenant to choose.

## Setup

The tools come from Timothe's hosted MCP server; nothing runs locally. If the tools named below are
not available yet, configure the server and sign in:

```bash
openclaw mcp add growth-calendar --url https://timothe.ai/mcp/growth-calendar --transport streamable-http --auth oauth
openclaw mcp login growth-calendar
```

The `--transport streamable-http` flag matters: the default SSE transport fails against this server
with a 405.

`login` opens a browser to sign in to Timothe; the client registers itself, so there is no API key
to paste. Credentials refresh on their own afterwards, and `openclaw mcp logout growth-calendar`
removes them. The connection acts on one Timothe workspace: whichever one the account is on when it
first signs in.

## Linking the user to their calendar

These tools return data, not a screen. When you report on something the user might want to look at
or edit by hand, give them the link:

- The calendar itself: `https://timothe.ai/tools/growth-calendar/app`
- One generated article: `https://timothe.ai/tools/growth-calendar/app?article=<trackId>/<date>`

The article parameter is the track id and the publish date joined by a slash, which is exactly the
pair you passed to `read_article`. For the "guides" track on 14 August 2026 that is
`?article=guides/2026-08-14`. Both values are URL-safe by schema, so nothing needs encoding.

## Read before you write

Start with `list_tracks`, then `get_calendar` for the month in question. A track is the
continuing publishing line a set of planned articles belongs to; its track id carries their
language and timezone, so you cannot write a correct `create_note` or `plan_cluster` call without
knowing which tracks exist. Guessing a track id creates a second, near-duplicate track.

`get_cluster_context` tells you what a track's current topic cluster is about and which dates
still expect an article. Read it before proposing new topics for an existing track, otherwise you
will suggest things the plan already covers.

`list_articles` takes no arguments and returns every planned article and every article already
written, across all tracks, with each one's title, the query it targets and its URL slug. This is
the overlap check to run before you plan anything new: it is how you notice that the workspace
already covers a query you were about to target a second time. It reports the 100 newest planned
articles and the 200 newest written ones, and says when a list stopped at that limit, which means
older articles exist that it did not show you.

## What costs credits

| Tool | Credits | Notes |
| --- | --- | --- |
| `serp_top` | 2 | Cheap enough to use freely |
| `site_keywords` | 5 | One domain per call |
| `keyword_ideas` | 20 | Priced per CALL, not per seed |
| `keyword_volumes` | 20 | Priced per CALL, not per keyword |
| `plan_cluster` | 200 | Takes several minutes |
| `generate_article` | 600 | Takes several minutes |

All six require a paid plan. Nothing else costs credits, including `list_articles`, the three
plan-item tools (`create_plan_items`, `update_plan_items`, `delete_plan_items`) and
`update_cluster_context`.

Check `get_credits` before proposing the expensive two. It reports the balance and whether the
workspace is on a paid plan, so you can say "this costs 600 and you have 1,200" instead of starting
a run that gets refused. It costs no credits.

Treat `plan_cluster` and `generate_article` as actions the user authorizes, not as steps you take to
explore. Say what it will cost and what it will produce, get a clear yes, then call it once. Never
call either one to find out what happens, and never retry after a failure without checking `get_run`
first: the run may have succeeded and the retry would be charged again.

The research tools are different in kind. They are cheap and fast, so once the user has agreed to
look into a topic, run them without asking permission for each one. Do tell them roughly what you
spent when you report back.

## Checking a market before committing to it

`serp_top`, `keyword_volumes`, `keyword_ideas` and `site_keywords` return real Google demand and
competition data for one market, in seconds. They exist so you can judge a topic yourself instead of
spending 200 credits on `plan_cluster` and finding out afterwards that nobody searches for it.

A market is a language plus a country, and the two matter independently: English sold to the UK is a
different demand curve and a different SERP from English sold to the US. Pass the `country` when you
know it, and take it from the track when you are working on an existing one.

A workable sequence before planning a cluster:

1. `keyword_ideas` on a few seed phrases, to see what the neighbourhood looks like and how big it is
2. `serp_top` on the two or three queries that matter most, to see who you would be up against
3. `keyword_volumes` on everything you are considering, in ONE call, to confirm the numbers

`site_keywords` is the one that finds angles you would not have thought of: point it at a competitor
domain and it shows which topics actually bring them traffic.

The cost discipline that matters: `keyword_ideas` and `keyword_volumes` are priced per call, so
sending 60 keywords in one call costs 20 credits and sending them one at a time costs 1,200. Collect
everything you want to check, then make one call. `keyword_volumes` takes up to 100 keywords and
`keyword_ideas` up to 20 seeds.

Report volumes you actually looked up. A keyword that comes back with no data has negligible volume,
which is a finding; do not fill the gap with an estimate.

## Long-running work

`plan_cluster` and `generate_article` return a run id immediately rather than a result. Poll
`get_run` with that id and the matching `job` value until the status is no longer `pending` or
`running`. A few minutes is normal. Leave a real gap between polls instead of checking in a tight
loop, and tell the user it is running rather than going silent.

## Planning a cluster

`plan_cluster` researches one pillar topic and lays a finite set of articles onto the calendar, one
planned item plus one reservation per publish date. It requires:

- `trackId`: a new short track id for a new cluster, or an existing track whose articles have all
  been generated
- `topic`: the pillar topic in a few words, at most 120 characters
- `language`: the market's language as a lowercase 2-letter subtag, which is also the language the
  articles are written in
- `timezone`: the IANA zone the publish dates and times are read in, such as `Asia/Tokyo`
- `cadence`: the publishing rhythm, as an object

`cadence` is what picks the calendar days the articles land on and the local time they publish at:

```json
{ "frequency": "weekly", "weekday": 2, "hour": 9, "minute": 0 }
```

`frequency` is `daily`, `weekdays` (Monday to Friday), `weekly` (needs `weekday`, 0 = Sunday
through 6 = Saturday) or `interval` (needs `intervalDays`, 2 to 365, weekends counted, so 2 means
every other day). `hour` is 0-23 and `minute` is 0-59, both read in the timezone above. Ask the user
for the rhythm rather than guessing; a weekday morning is the common choice.

Everything else is optional:

- `country`: the market's country as an uppercase 2-letter code, which scopes the research. Omit to
  use the language's largest search market
- `startDate`: the earliest date the first article may publish on. Omit it and the cluster starts on
  the next date the cadence allows
- `count`: at most 25, and a ceiling rather than a target. Fewer articles are planned when fewer
  angles have real demand, so a count of 12 can come back as 8. Omit it to let the research size the
  cluster
- `brief` and `referenceUrls`: what the writers should know, covered next

Ask about the business before choosing a topic, then check the topic against the research tools
above. A cluster planned from a guess produces a month of articles the user did not want, and each
one costs 600 credits to regenerate. Twenty credits of `keyword_volumes` is the cheapest insurance
available against that.

### `topic` is an anchor, not a brief

`topic` is the short pillar-topic anchor the cluster is built around, at most 120 characters:
"programmatic SEO for marketplaces", not a paragraph. Everything you know beyond that belongs in
`brief`, up to 8,000 characters of markdown carried into every article of the cluster: the audience,
the product, the angles to cover and the ones to avoid, terminology, the volumes you measured and
want cited, and what to leave alone because an existing article already covers it. `referenceUrls`
takes up to 8 URLs to read first, such as the user's own product pages or a competitor's article.

Guidance you only work out after the articles are on the calendar goes on the article instead: each
planned article carries a `note` of up to 2,000 characters, set by `create_plan_items` and changed by
`update_plan_items`.

### Tracks and dates

A track id nobody has used yet creates the track. A track that still has planned articles waiting
refuses a new cluster, so pick a fresh track id or reuse a track whose articles have all been
generated; the pending count and the active/completed state in `list_tracks` tell you which is which.

A track publishes at most one article per day. A day in the past is refused, and so is a day that
already has an article on that track. Those two rules hold for every tool that puts an article on a
day, not just this one.

## Adding articles you already researched

When you already know the set of articles you want, add them yourself instead of paying for the
research. `create_plan_items` costs no credits and takes the whole set in one call; `plan_cluster`
costs 200 credits and buys the research that decides what the set should be. Both end in the same
place: planned articles with a reservation on each date.

1. `list_articles`, so the new set does not compete with articles the workspace already has
2. `create_plan_items` once, with every article in the `items` array
3. optionally `update_cluster_context` on the track, so the set is written as one cluster
4. `generate_article` per article, when the user wants one written before its date instead of on it

`items` takes 1 to 50 articles. Each is addressed by `trackId` and `date` and carries the `title` (up
to 300 characters), the `targetQuery` it should win (omit to use the title) and the `note` the writer
should follow. `articleType`, `length`, `slug` and the publish `time` are optional.

The market and the clock are inherited: an article added to a track that already has planned articles
follows that track's language, country, timezone and publish time. A brand new track has nothing to
inherit, so its first item needs `language` and `timezone`, and later items in the same call inherit
from the earlier ones. One call can therefore create a whole new track from nothing.

Adding them spends no credits, and each article is charged 600 when it is written, either by
`generate_article` or by its reservation on its publish date. Say that when you propose a set: six
planned articles is 3,600 credits of writing ahead.

## Shared guidance for a track

`update_cluster_context` writes, or rewrites, the shared guidance behind one track's planned
articles: what the cluster is about, which article takes which angle, how they link to each other,
what each leaves to a sibling, and the brief they all follow. Every planned article on the track that
has not been written yet is put under it, so each one written from then on follows it. It costs no
credits and takes a minute or two.

It is optional. The workspace writing style reaches every article whether or not its track has shared
guidance, so this is not the price of a well-written article. Reach for it when you want the set to
behave as a cluster: internal links between the articles, and no two of them covering the same
ground.

Read `get_cluster_context` first and pass its `expectedDates` and its context version straight back as
`expectedDates` and `expectedContextVersion` (0 when the track has none yet). Those are what prove
the plan has not moved while the guidance was being written; on a conflict, read again and rebuild
instead of retrying the same call. `directions` says in your own words what the guidance should say or
how it should change, and `referenceUrls` (up to 8) points it at pages worth reading first.

## Editing the plan

`update_plan_items` changes planned articles that have not been generated yet: `title`,
`targetQuery`, `articleType`, `length`, the writer's `note`, the URL `slug`, and where it publishes
(`newDate`, `newTime`, `newTrackId`). Address each article by its track and the date it is currently
planned for.
An empty string in `note` or `slug` clears that field.

`delete_plan_items` removes planned articles and frees their days. Neither tool touches an article
that has already been generated.

Both take 1 to 50 items, and both are all or nothing: if the calendar refuses one item, nothing at
all is applied, and the reply names each offending item and why (no planned article on that day, that
day's article is already generated, that day is in the past, that day is already taken on that
track). Because the batch is judged on the calendar it would leave behind rather than item by item,
two articles can trade days inside one call.

Deleting cannot be undone. List the articles you are about to remove, get ONE explicit confirmation
from the user for the whole batch, then make ONE `delete_plan_items` call. Do not walk the user
through them one at a time.

`create_note` adds a dated reminder that gets emailed on its date. Use it for things the user needs
to do, not for articles to write.

## Reading and editing articles

`update_plan_items` above only works before an article exists. Once it has been generated, the
article itself is edited with `read_article` and `edit_article`.

`read_article` returns the editable source: line 1 is `revision: N`, then a blank line, then a
frontmatter with the editable fields (title, description, slug, note) followed by the markdown body.
That text is the exact thing `edit_article` matches against, so read before every edit rather than
working from an earlier copy.

`edit_article` applies exact string replacements in order. Copy each `oldString` verbatim from what
`read_article` returned and include enough surrounding context to make it unique, or pass
`replaceAll`. Frontmatter fields are edited like any other line, and deleting an optional
frontmatter line clears that field. Pass the revision you just read as `expectedRevision`.

Leave image lines and `gcimg:` placeholders alone. They are resolved when the article is displayed,
and rewriting them breaks the images.

The whole edit either applies and is saved, or nothing changes. On a revision conflict or a failed
match, read the article again and rebuild the edits against the new text; do not retry the same
strings. The result comes back with any remaining prose-lint warnings, which are advisory.

`get_calendar` returns a whole month and can be long. Summarize it for the user instead of pasting
it back.

## Workspace styles

Two workspace-wide documents steer every article the calendar generates: the writing style (voice,
structure, wording) and the image style (the art direction for the images generated inside
articles). Both follow the same read/update pattern as articles: the get returns `version: N` on
line 1, and the update takes that N as `expectedVersion`.

Read the relevant one (`get_writing_style` / `get_image_style`) before offering opinions on how
articles are written or how their images look. An image style at `version: 0` means the workspace
has not saved one; the built-in default returned after that line is what currently applies.

`update_writing_style` and `update_image_style` replace the whole document, so carry over
everything that should stay and change only what the user asked to change. On a version conflict,
read again and rebuild against the fresh text instead of retrying the same call. Style changes
apply to articles generated from then on, not to the ones that already exist.

Keep the image style a compact art-direction block: overall look, palette (hex values work well),
composition, mood. It is appended verbatim to every image-generation prompt, so vague prose
weakens every image and 1,200 characters is the hard cap.

The app also offers preset image styles (a look plus a color palette). When one is selected,
`get_image_style` shows a `preset:` line under the version, and `update_image_style` replaces that
selection with your custom text. That is the right call when the user wants a custom style; when
they just want a different look or color scheme, point them to the presets in the app instead.
