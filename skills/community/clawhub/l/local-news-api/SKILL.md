---
name: local-news-api
description: >-
  Use when someone asks what a local newsroom has published, is about to cover, or has
  reported before: what happened at a public meeting, when the next hearing or comment
  deadline falls, who said something on the record, what prior coverage exists to cite, what it
  published on a given day, or what to gather before writing a story.
  Reads published articles, meeting transcripts with speakers and timestamps, upcoming civic
  events, a people directory, beats and traceable prior-coverage citations from a Communities
  News newsroom's public API, for example Alaska News at alaskanews.com (the default).
  Read-only: it never writes back, and saves a local file only when asked. Reach for it
  even when the request never says "API" or names the newsroom, as in "has anyone reported on
  this", "when does the assembly next meet", "what did the mayor say about the port", "find
  me what was written before", "what ran yesterday", or "brief me before I write about the port".
license: MIT-0
compatibility: >-
  Python 3.9+, standard library only, no third-party packages. Needs network access to a
  Communities News newsroom (alaskanews.com unless NEWS_SITE says otherwise) and, for most
  modes, that newsroom's own cn_ API key in COMMUNITIES_NEWS_API_KEY.
allowed-tools: Bash
metadata:
  version: "1.6.2"
  author: Communities News LLC
  homepage: https://communities.news
  repository: news-community/news-skills
  openclaw: {"primaryEnv": "COMMUNITIES_NEWS_API_KEY", "requires": {"bins": ["python3"]},
    "homepage": "https://communities.news",
    "envVars": [
      {"name": "COMMUNITIES_NEWS_API_KEY", "required": false, "description": "Your cn_ key. digest, topics and tags run without it."},
      {"name": "NEWS_DESK_API_KEY", "required": false, "description": "Older name for the key, still read."},
      {"name": "ALASKA_DESK_API_KEY", "required": false, "description": "Oldest name for the key, still read."},
      {"name": "NEWS_SITE", "required": false, "description": "Newsroom origin; default https://alaskanews.com."},
      {"name": "NEWS_COMMUNITY", "required": false, "description": "Community slug; default alaska-news."},
      {"name": "PLATFORM_API_BASE", "required": false, "description": "API base; default NEWS_SITE + /api/v1."}]}
---

# Local News API

> **A read-only client for a local newsroom's public API** on the Communities News platform. It
> pulls published articles, the sources behind them (meeting transcripts, people quoted, video
> clips) and upcoming meetings and deadlines into **your own** work, under the newsroom's terms.

**The example throughout is Alaska News**, the first newsroom on the platform and the default:
site `https://alaskanews.com`, API `https://alaskanews.com/api/v1`, spec
`https://alaskanews.com/api/v1/openapi.json`. Every newsroom on the platform serves the same API
at its own domain.

**This skill only consumes.** It never submits, edits, or writes back to the platform.
Submitting content into the newsroom is a separate, editor-authenticated workflow that is not
part of this tool.

---

## What it is, and what it is not

| | |
|---|---|
| **Audience** | community journalists, bloggers, civic writers; one key each |
| **Direction** | READ ONLY. No `PATCH` / `PUT` / `DELETE`; its only `POST` is the read-only RAG query. A test enforces this. |
| **Local files** | none unless you ask: `brief --out FILE` saves the brief as Markdown at the path you give, **replacing** a file already there. Nothing else writes to disk. A test enforces this too. |
| **Auth** | **your own** `cn_` API key (`COMMUNITIES_NEWS_API_KEY`), ideally created **read-only**. `digest`, `topics` and `tags` need none. |
| **Output** | rendered markdown by default (paste into your draft), `--json` for raw. Every response carries the site's usage terms. |
| **Newsroom** | alaskanews.com (`/api/v1`) by default, a DEFAULT not a limit: `NEWS_SITE` + `NEWS_COMMUNITY` point it elsewhere. |
| **Runs on** | [`scripts/local_news_api.py`](scripts/local_news_api.py), Python 3, standard library only, no dependencies. |

**It is not** a content generator. It produces *source material* that you turn into your own
article, script, or post.

---

## Terms (read this before you publish anything from it)

**The terms are read from the newsroom on every run, not compiled in.** The client fetches
`robots.txt`'s `Content-Signal` (the machine-readable location defined by contentsignals.org),
falling back to `llms.txt`. alaskanews.com currently declares:

- **`ai-train=no`** you may not train models on the content.
- **`search=yes`** it may surface in AI-powered search.
- **`ai-input=yes`** you may quote it **with attribution and a backlink**.

Fetched, not compiled in, so a newsroom's change of stance shows up at once and a different
newsroom's reporting never carries Alaska's terms. **If the terms cannot be read, the output says so
and invents nothing.**

Every mode prints that reminder under its output. It is not decoration: the person running this
is republishing someone else's reporting, and the attribution + backlink is the consideration
for using it. If you generate content from an article, name the newsroom (Alaska News, for alaskanews.com) and
link the source.

---

## Auth: your own key, and only what it reaches

Create a key in your account on the newsroom's site; for Alaska News,
[alaskanews.com/profile/settings](https://alaskanews.com/profile/settings). **Tick "Read-only"**, and
know its one cost first: **`rag` will not work**, because its read-only query is an HTTP `POST`.

The guarantee a read-only key gives is concrete: the server rejects every `POST`/`PUT`/`PATCH`/`DELETE`
before a handler runs, so the key cannot change anything, whatever code or agent holds it. This client
never writes either, but that is a promise in code you would have to read. A read-only key is still a
credential: if it leaks, whoever has it can read what it reaches and spend its rate limit, so revoke a
leaked one at the same settings page.

Then either export the key (works from anywhere):

```bash
export COMMUNITIES_NEWS_API_KEY=cn_...
```

or drop it in a gitignored `.env.local` next to the script (or in your project root, which may
hold the key but never `NEWS_SITE` or `PLATFORM_API_BASE`):

```bash
echo 'COMMUNITIES_NEWS_API_KEY=cn_...' >> scripts/.env.local
```

Access is tiered on the platform side, and your key may not reach everything.

| Mode | Reach | Note |
|---|---|---|
| `digest` | **public** | recent stories; `--date` for one day's, a summary each. Verified 2026-09-30 |
| `search` | **any valid key** | six corpora; `external_documents` and `social_post` are editor/admin only |
| `angles` | **any valid key** | discovery scaffold; runs on the `/search` surface |
| `brief` | **any valid key** | research brief: one `/search`, arranged for a writer, then four blanks |
| `article` | **public by URL/slug**, keyed by id | the id form returns the richer record |
| `transcript` | **any valid key** | full meeting transcript with speakers + timestamps |
| `events` | **any valid key** | `GET /calendar`, date-ranged. Re-verified 2026-09-09 |
| `communities` | **any valid key** | the slugs `--community` accepts |
| `browse` | **any valid key** | the published article list; `--tag` for one beat |
| `people` / `person` | **any valid key** | speaker directory, and one actor's coverage |
| `topics` / `tags` | **public** | beats ranked by coverage, and the subject vocabulary. Verified 2026-09-29 |
| `rag` | **role-gated** | an external consumer key saw 403 on 2026-07-23; slow (~1-2 min) where allowed |
| `clip` | **id only** | resolves a known id to its public MP4 URL. You cannot BROWSE clips: see below |

**Some endpoints are not role gates, and no upgrade reaches them.** A set of routes authenticate by
**cookie session only**: they read the browser's Supabase session rather than the API-key path, so
they refuse *every* `cn_` key, including an admin's. `GET /clips` (browse) and
`GET /transcripts/search` are the two you are most likely to want; `GET /transcript/<id>/speakers`
is a third, which is why you can read every word of a meeting and not learn who said it.

**You need not take that list from this file.** `GET /api/v1/me` returns a `reachability` block
derived from the platform's own router, and `check` renders it: `session_auth_only` (nothing to
request) apart from `requires_role` (a membership you could be granted). Those endpoints return
**403** with `error: session_auth_only` and a remedy, not a bare 401 that reads like a bad key.

Use `search --corpus transcripts` instead of `transcripts/search`, and get clip ids from `search` or
an article.

**How much weight these rows carry.** They come from two passes with two different keys, and only
one of them tells you about external reach. Read
[`references/verification.md`](references/verification.md) before changing any claim here about what
a key reaches. Run `check` for the only answer that is about *your* key.

**Run `check` first.** It asks the server what your key reaches, and probes a handful of endpoints
directly on top of that. It reports whether your key is **read-only**, your role per community, the
endpoints no key reaches and the ones a membership would unlock. It takes about five seconds:

```bash
python3 scripts/local_news_api.py check
```

---

## Modes

```bash
python3 scripts/local_news_api.py check                               # what does MY key reach? (run first)
python3 scripts/local_news_api.py digest                              # recent stories (no key)
python3 scripts/local_news_api.py digest --date today                 # one day's stories, a summary each (no key)
python3 scripts/local_news_api.py browse --sort new                   # what has been PUBLISHED (no query)
python3 scripts/local_news_api.py search "port of alaska settlement"  # --corpus, --since, --until
python3 scripts/local_news_api.py angles "port of alaska" --intent track  # discovery: fix 2 Ws, expand the rest
python3 scripts/local_news_api.py brief "port of alaska"             # research brief before writing (--out FILE)
python3 scripts/local_news_api.py article <id | slug | url>           # full article
python3 scripts/local_news_api.py transcript <source-id>              # meeting transcript
python3 scripts/local_news_api.py events                              # what is coming UP (next 30 days)
python3 scripts/local_news_api.py rag "public comment deadlines"      # answer + citations (not with a read-only key)
python3 scripts/local_news_api.py clip <clip-id>                      # resolve a known clip id to its MP4 URL
python3 scripts/local_news_api.py communities                         # slugs valid for --community
python3 scripts/local_news_api.py people "dunleavy"                   # the Who axis: named speakers
python3 scripts/local_news_api.py person <person-id>                  # one actor + the coverage they appear in
python3 scripts/local_news_api.py topics                              # the beats, ranked by coverage
python3 scripts/local_news_api.py tags "port" --category organization # the subject vocabulary
```

**`topics` is the beats; `tags` is the whole vocabulary.** `topics` lists the topic-category tags
(Government, Infrastructure, Health...) ranked by articles published, each naming its parent; counts
do not roll up into the parent. `tags` searches every tag: `organization`, `topic` or `location`. A
slug from either is what `browse --tag` takes. Both are public.

**`browse` vs `search`.** `search` answers "what do you have about X". `browse` answers "what has
been published", which is the question you ask before you know what X is. `--sort` takes
`new`/`hot`/`top`/`popular`/`timeline`/`alphabetical`, and `--tag <slug>` lists a single beat.

**A day's stories: `digest --date`.** `today`, `yesterday` or `YYYY-MM-DD`: every story published
that day, newest first, with time, place, one-line summary and link. It asks the public feed for
exactly that day, so no key. The day is the newsroom's own, in the time zone the feed reports
(Alaska News: America/Anchorage); `--tz <Area/City>` overrides it.

**A research brief: `brief "<topic>"`.** The step before writing. One `/search` across everything
your key reaches, in a writer's order (prior coverage, the meeting record, people on the record,
events, beats), then four blanks to fill first: why it matters, whose voice is missing, what you will
cite, and a premise check. Assembled, not generated: no model call, and the judgment is yours.
`--out brief.md` also saves it, with the terms, at that path on your machine, replacing a file
already there. It is the only file this skill writes.

## Pointing it at another newsroom

Every newsroom on the platform serves the same API at its own domain, so another newsroom is
configuration, not a fork:

```bash
export NEWS_SITE=https://<host>          # the newsroom; its API is <host>/api/v1
export NEWS_COMMUNITY=<slug>             # default for --community
export COMMUNITIES_NEWS_API_KEY=cn_...   # (NEWS_DESK_API_KEY, ALASKA_DESK_API_KEY still work)
```

**alaskanews.com remains the default**, and today it is the only newsroom live on this platform, so
that default is also the whole of production. Nothing about a market is compiled in: the terms, the
`See also` links, the reachability report, every request path and every "create a key here" message
follow whatever `NEWS_SITE` and `--community` say. `check` prints which newsroom and community it is reporting on, because a
reachability report that does not name its subject is the kind of thing you read wrongly once.

**Paging.** Every list mode takes `--limit` and `--offset`, and prints `showing 1-20 of 340` with the
next `--offset` when there is more. A page that quietly drops the rest is how you conclude there are
three of something when there are ninety.

Add `--json` for raw responses, `--community <slug>` to target a community other than `alaska-news`
(run `communities` to see which slugs exist).

**The When axis: `--since` / `--until`.** `search` and `angles` both take `--since YYYY-MM-DD` and
`--until YYYY-MM-DD`, which map to the API's `date_from` / `date_to` on the articles corpus. This is
the only one of the five Ws the server can filter on, and it is the axis the `angles` intents talk
about holding or expanding, so `--intent precedent --until 2020-01-01` is how you actually ask the
question that intent describes. Result lines carry the date for the same reason: you cannot check
the two-axis relevance rule below against results whose dates are hidden.

**`events` is forward-looking.** It reads `GET /calendar`, whose window starts now and runs 30 days
(`--days` to change it, `--type meeting|public_notice|community_event|class` to narrow), so it never
lists a past meeting as upcoming. To search events by relevance across all time, including past ones,
use `search "<q>" --corpus events`. `/calendar` has no full-text parameter, so a query argument to
`events` filters the window client-side on title and location.

---

## Every output points onward

Every mode ends with prioritized **Next steps** (each with its *why*), the related modes and a see-also,
and errors carry a recovery rather than a bare status. `--json` is the machine surface and stays valid
JSON. How that works, including the API's own `next_steps`: [`references/output.md`](references/output.md).

---

## Working the story: the five Ws (the `angles` mode)

Treat Who, What, When, Where, Why as five independent axes. The investigative method has two modes,
and they land on opposite sides of this tool's read-only line:

- **Matching** (ranking which stories are genuinely related) is axis-weighted similarity. That is
  the **server's** job; it happens inside `/search` and `/rag/query`. This client does not re-do it.
- **Discovery** (fix two Ws, expand the rest) is a workflow of chained searches, and that is exactly
  what a sourcing tool can scaffold. It is what `angles` runs.

`angles --intent` names which two Ws you fix:

| Intent (the two Ws it fixes) | `--intent` | Runs now: one `/search` over | Suggested next |
|---|---|---|---|
| similar stories (What + Why) | `similar` | articles | `rag` to hold What+Why and vary When |
| historical precedent (What + Why) | `precedent` | articles, transcripts | `--until` an earlier year |
| track a company or agency (Who + What) | `track` | articles, transcripts | the actor across more years |
| local coverage (Where + What) | `local` | articles, events, transcripts | `--community <slug>` is the Where |
| same narrative angle (Why + What) | `angle` | articles | `rag` on who is using the framing |

Each run is **one** `/search`; everything in the last column is a Next step you choose to run, so you
drive the depth, not the key's rate limit.

**The one rule to carry:** two matching dimensions (the topic **and** the actor, say) tell you a piece
is *relevant*; they do not make a claim *corroborated*. Several articles can repeat one underlying
source. Verify a claim against an independent source, ideally the primary record, before you treat it
as confirmed, and cite a specific piece, never "previously reported".

---

## Method: internal before external

Before you reach for a general web search, ask whether the newsroom (Alaska News, by default) has already covered this. Run
`search` first. If the answer is in the corpus, you save an external lookup and you can cite specific
prior reporting; if it isn't, you now know it's a genuine gap. The reorder is the value.

When you cite "previously reported," cite a **specific** article (its id or URL), never a generic
phrase with no matching published story behind it.

---

## Honest limits (as of 2026-09-09)

- **What was verified, with which key:** [`references/verification.md`](references/verification.md).
  `check` is the only answer about *your* key.
- **`rag` is role-gated and slow.** An external key saw 403. Where it is allowed, it synthesizes an
  answer over retrieved passages and measured **84 seconds** on 2026-09-09, so the client gives it a
  180s budget, and a timeout is reported as one. Quote its **citations**
  (each carries a verbatim excerpt and a url), never its synthesized paragraph: the paragraph is a
  summary of someone else's reporting and is not itself attributable.
- **You cannot browse clips or use `/transcripts/search` with any key.** Both are cookie-session
  endpoints, not role gates. See the auth section above.
- **`angles` and `brief`** each make one `/search` call, so any key that reaches `search` reaches
  them. `angles`' suggested `rag` follow-ups inherit rag's role limit.
- **Rate limits.** 300 reads/min per user (and 180 writes/min, which nothing here uses). A 429 is a
  back-off, not a permission problem.
- **This is not a submission tool.** If you want your work published *on* the newsroom, that is a
  newsroom workflow, not this.

### Not covered here, deliberately

**`person` reports "appears in", not "quoted in", and the distinction is load-bearing.**
`/persons/<id>/articles` returns a UNION: articles where an attribution matched the person's name,
and articles structurally linked to them. Only the first kind carries a verbatim excerpt. Rows with a
quote are marked `quoted (Nx)`; when a whole page has none, the client says so, because "Dunleavy
appears in this piece" and "Dunleavy said this in this piece" are different claims and only one of
them is quotable. Open the article and confirm before you attribute words to anyone.

Everything else on the read surface that a consumer key reaches is now wrapped. What remains
unwrapped is write-side or editor-only, and out of scope by design.
