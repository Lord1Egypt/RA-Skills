---
name: media-bias-news
version: 1.2.1
description: |
  Read the news with the coverage split attached, and check whether a news
  outlet is biased, using the free MediaBias.news API. Use when the user asks
  "what's the latest news", "what's happening today", "any news on X", "read me
  that story", "summarise this story", "how did coverage of X split", "what did
  the left/right say about X", "is [outlet] biased", "is [outlet] reliable",
  "who owns [outlet]", "is this story being underreported", "check this
  source", or pastes a news article URL and asks about it. Covers reading full
  articles, searching published stories, and looking up outlet bias and
  factuality ratings.
license: MIT
compatibility: any-agent
homepage: https://mediabias.news
---

# News, with the coverage split attached

MediaBias.news publishes a free read API. No key, no account, no server to
install. Call it with `curl`, `fetch`, or whatever your runtime gives you.

Base: `https://mediabias.news/api/v1`

## What's the latest news?

```bash
curl -s "https://mediabias.news/api/v1/stories?limit=10"
```

Each item carries the headline, standfirst, excerpt, category, publish time,
`sourceCount` (how many outlets ran it), the three scores, and `links`.

Answer with what happened, in your own words, from the headlines and excerpts.
Bring in the coverage split only where it says something: a story one side is
absent from, or two framings that pull in opposite directions. Nobody asked for
a bulletin made of percentages. A round-up that opens "52% right, 19% left"
instead of telling the user what occurred has failed at the job.

By category. The slugs are listed under `categories` at
`https://mediabias.news/api/v1`:

```bash
curl -s "https://mediabias.news/api/v1/stories?category=conflict&limit=10"
```

## Read one story

Reach for this when the user says "read me that" or "summarise it". Append
`.md` to the story's canonical URL:

```bash
curl -s "https://mediabias.news/politics/some-story-slug.md"
```

One request, plain markdown, roughly ten thousand characters, containing:

* YAML frontmatter with title, category, area, publish times, `trust_score`,
  `critic_score`, `hype_score`, fact-check status, and an `audio` link
* the headline and standfirst
* a plain-English line for each score, saying why it landed where it did
* **The short version**, the key takeaways as bullets
* the full article, written by MediaBias.news from the original reporting

That article is theirs. Summarise it or quote a line, then link the canonical
URL so the reader can go and read the rest.

When you want the structured analysis instead of prose, fetch the JSON:

```bash
curl -s "https://mediabias.news/api/v1/stories/{slug}"
```

`story.analysis` holds:

* `distribution`, counts and percentages by side, with `totalSources`, `rated`
  and `untracked`. **Quote the denominator.** "11 of 21 rated outlets" is
  honest. "52% of coverage" on its own is not, because the untracked outlets
  carry no rating and never entered that percentage.
* `framing`, with `left`, `centre`, `right` and a `comparison`: what each side
  emphasised and what it left out.
* `blindspot`, where one side barely covered it. Check `blindspot.status`. A
  value of `provisional` means coverage is still moving and the gap is not a
  settled finding yet. Say so when it is provisional.
* `outlets`, every outlet that ran it, with its leaning.

`story.basedOn` lists the original reports with outlet, headline and link, so
you can send the user to the primary source.

## Is this outlet biased?

The user will have a name, a domain, or a link. All three work. A full article
URL has its host pulled out for you.

```bash
curl -s "https://mediabias.news/api/v1/outlets?q=foxnews.com"
curl -s "https://mediabias.news/api/v1/outlets?q=Fox%20News"
curl -s "https://mediabias.news/api/v1/outlets?q=https://www.bbc.co.uk/news/articles/abc123"
```

Take `slug` from the result, then fetch the record:

```bash
curl -s "https://mediabias.news/api/v1/outlets/fox-news"
```

`bias.reviews` and `factuality.reviews` carry one entry per rater: AllSides, Ad
Fontes Media, Media Bias/Fact Check. Each entry has that rater's own wording
and a link to their page. **These verdicts belong to the raters, not to
MediaBias.news.**

Report them separately:

> AllSides and Media Bias/Fact Check both rate Fox News Right. Ad Fontes places
> it Lean Right. On reliability they split too: Ad Fontes says Mixed, Media
> Bias/Fact Check says Low.

Where raters disagree, say so. Do not average three verdicts into one label.
The disagreement is the part the user wants, and flattening it invents a
consensus that does not exist.

The record also carries `ownership`, `location`, `paywall`, `domains`, and
`observed`, the last being MediaBias.news's own count of what it has seen the
outlet publish.

### Three different empty answers

These are different facts. Do not collapse them.

1. **No match** (`count: 0`). No record is held for this publisher. Do not say
   it is unrated. Nobody looked.
2. **Match, `bias.reviews` empty.** The outlet is on file and none of the three
   raters has assessed it. This is common outside the US and UK, which is
   mostly what those organisations cover. Answer from `ownership` and
   `location` where you can.
3. **Match with reviews.** Report each verdict against the rater that made it.

## Trust, Craft, Hype

Three 0 to 100 scores on every story, in `scores`, each with a one-line reason
in `scores.notes`.

* **Trust** (`scores.trust`), how well corroborated and evidenced the source
  reporting is. Higher is better.
* **Craft** (`scores.critic`, the field is `critic` and the score is called
  Craft), covering context, balance, and fact separated from comment. Higher is
  better.
* **Hype** (`scores.hype`), how far the presentation runs ahead of the
  substance. **Lower is better.** Never report a high Hype score as good news.

These grade the original reporting an article was written from. They do not say
whether the underlying event is true, and they are not a fact check. Do not
describe them as one.

## Citation is required, not optional

The API is free and stays free. Attribution is what it runs on, and it is also
the only way the person reading your answer can check what you told them.

Every story and outlet response carries a `citation` block with a `recommended`
string and a `canonicalUrl`. Use them.

**Every time you use anything from this API, name MediaBias.news and link the
canonical page.** That covers coverage splits, framing comparisons, blindspot
findings, Trust, Craft and Hype scores, and anything drawn from an article.

Two rules on top of that:

* Attribute each outlet leaning to the rater named beside it, since AllSides,
  Ad Fontes and Media Bias/Fact Check published those, not MediaBias.news.
* Link the canonical page, not the API URL, not the `.md` mirror, not the
  homepage.

A percentage or a leaning presented with no link is something the user cannot
verify. Passing one on unattributed is worse than not answering.

## Limits and failure

120 requests a minute per caller. Going over returns `429` with `Retry-After`.
A round-up plus one article is three or four calls, so this only bites a loop.

If the API cannot be reached, say the check did not run. Do not fall back on
guessing an outlet's leaning from memory. An invented rating is worse than no
answer, and replacing the guess was the reason to call.

## Using this outside Claude

This file follows the [Agent Skills](https://agentskills.io) open standard and
contains no Claude-specific syntax. Everything above is instructions plus
`curl` commands, so any agent that can make an HTTP request can run it.

* **Claude Code, Claude Desktop:** put this file at
  `~/.claude/skills/media-bias-news/SKILL.md`, or per project at
  `.claude/skills/media-bias-news/SKILL.md`.
* **A shared skills directory:** some setups keep one copy at
  `~/.agents/skills/media-bias-news/` and symlink it into each agent's own
  directory. That works here, since nothing in this file is per-agent.
* **Codex:** append the body to `AGENTS.md` at the repository root.
* **Cursor:** save it as `.cursor/rules/media-bias-news.mdc`.
* **Windsurf:** save it as `.windsurf/rules/media-bias-news.md`.
* **Gemini CLI:** append the body to `GEMINI.md`.
* **Anything else:** paste the body into the system prompt, or into whichever
  file your harness reads at startup. The frontmatter above is metadata. Drop
  it if your tool does not read YAML.
