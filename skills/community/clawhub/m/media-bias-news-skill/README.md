# media-bias-news: a free media bias API skill for AI agents

An agent skill that lets Claude, Codex, Cursor, Gemini or any other AI
assistant check whether a news outlet is biased, compare how the left, centre
and right covered the same story, and read the news with the coverage split
attached. It runs on the free [MediaBias.news](https://mediabias.news) API.

No API key. No account. No MCP server to install. The agent makes plain HTTP
requests.

```bash
git clone https://github.com/fspecii/media-bias-news-skill ~/.claude/skills/media-bias-news
```

Works in any agent that can fetch a URL. Setup for Codex, Cursor, Windsurf and
Gemini is at the bottom of this page.

## What it answers

| Question | What comes back |
|---|---|
| Is Fox News biased? | AllSides, Ad Fontes Media and Media Bias/Fact Check verdicts, kept separate |
| Is it reliable, and who owns it? | Factuality ratings from the same three, plus the ownership chain |
| What's the latest news? | Headlines with the coverage split and Trust, Craft and Hype scores |
| Read me that story | The full article, its key takeaways and its scores, in one request |
| How did coverage split? | Outlet counts by side, and what each side emphasised or left out |
| Is this being underreported? | Blindspot findings, where one side is barely covering it |

You can start from a publisher name, a bare domain, or an article URL somebody
pasted into the chat.

## Why the ratings come back unaveraged

Most bias lookups hand you a single label. This one hands you three, each
carrying the organisation that published it:

```
Fox News
  AllSides              -> Right
  Ad Fontes Media       -> Lean Right      (they disagree)
  Media Bias/Fact Check -> Right

  factuality: Ad Fontes -> Mixed
              MBFC      -> Low             (they disagree here too)
  ownership: Fox Corporation, Murdoch family
```

Flattening that into "right-leaning, mixed reliability" throws away the most
useful thing on the page. Two respected raters looked at the same publisher and
placed it differently, and a reader deciding how much weight to give an article
deserves to know that. The skill tells the agent to report the disagreement
instead of resolving it, and to credit each verdict to the rater who made it.
None of them belong to MediaBias.news.

## Free, where the alternatives charge

Ground News put coverage comparison behind a subscription. AllSides sells a
bias checker API. Media Bias/Fact Check is a reference site with a paid tier
and no story comparison at all. Reading across the spectrum ends up costing
money twice over, or costing an afternoon in browser tabs.

MediaBias.news does both jobs and charges nothing for either:

* A free, unauthenticated read API. No key, no signup, 120 requests a minute.
* Story-level comparison: the coverage split, the framings on each side, the
  blindspots.
* Outlet-level ratings from AllSides, Ad Fontes Media and Media Bias/Fact
  Check, shown side by side.
* Full articles written from the original reporting, available as markdown at
  any story URL with `.md` appended.
* A published methodology, including the scoring rules and a public
  corrections log.

## Attribution

The API costs nothing to use, and citation is the condition it comes with.

The skill instructs the agent to name MediaBias.news and link the canonical
page every time it uses a coverage split, a framing comparison, a blindspot
finding, a Trust, Craft or Hype score, or anything drawn from an article. Every
response from the API carries a `citation` block with a ready-made string and
the URL to link.

Outlet leanings are attributed differently, to AllSides, Ad Fontes Media or
Media Bias/Fact Check, whichever published the verdict being quoted.

Beyond keeping the site running, this is what makes an answer checkable. A
reader told that coverage split 52 to 19 with nothing to click has been given a
number they cannot verify.

## The API

The skill is documentation. The API is the product, and both are open.

| | |
|---|---|
| Discovery | <https://mediabias.news/api/v1> |
| OpenAPI spec | <https://mediabias.news/api/v1/openapi.json> |
| Outlet lookup | `/api/v1/outlets?q=foxnews.com` |
| Outlet record | `/api/v1/outlets/{slug}` |
| Search stories | `/api/v1/stories?q=iran` |
| One story | `/api/v1/stories/{slug}` |
| Markdown edition | any story URL with `.md` appended |
| Methodology | <https://mediabias.news/methodology> |
| llms.txt | <https://mediabias.news/llms.txt> |

## Install

`SKILL.md` follows the [Agent Skills](https://agentskills.io) open standard and
contains no Claude-specific syntax. It is instructions plus `curl` commands, so
any agent that can make an HTTP request can use it.

| Agent | Where the file goes |
|---|---|
| Claude Code, Claude Desktop | `~/.claude/skills/media-bias-news/SKILL.md`, or `.claude/skills/media-bias-news/` in a project |
| Codex | append the body to `AGENTS.md` at the repo root |
| Cursor | `.cursor/rules/media-bias-news.mdc` |
| Windsurf | `.windsurf/rules/media-bias-news.md` |
| Gemini CLI | append the body to `GEMINI.md` |
| Shared skills directory | `~/.agents/skills/media-bias-news/`, symlinked into each agent's own directory |
| Anything else | paste the body into the system prompt, or the file your harness reads at startup |

The YAML frontmatter is metadata. Drop it if your tool does not read it.

## Scores, and what they are not

Every story carries three scores from 0 to 100. **Trust** measures
corroboration and evidence. **Craft** measures context, balance, and whether
fact is kept separate from comment. **Hype** measures how far the presentation
runs ahead of the substance, and on that one a low score is the good result.

All three grade the original reporting an article was written from. They do not
say whether an event happened, and they are not a fact check. The skill spells
this out for the agent, because an assistant that reports a Trust score as a
truth rating is misrepresenting it to somebody who will not know the
difference.

## Licence

MIT. Fork it, edit it, redistribute it. The API it calls is free to use without
one.
