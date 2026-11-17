---
name: motley-nyc
description: Answer NYC family questions from Motley's live dataset — which neighborhood fits, which school is right, how school admissions actually works. Use for anything about moving within or into New York City with kids, comparing neighborhoods, finding or comparing schools (public, charter, private), zoned/screened/SHSAT/audition/lottery admissions, school competitiveness, neighborhood safety and health, or family resources like playgrounds, libraries, and ADA subway stations. Connects to a free, keyless hosted MCP server; no API key or sign-up.
homepage: https://motley.nyc/mcp
metadata:
  {
    "openclaw":
      { "emoji": "🗽", "homepage": "https://motley.nyc/mcp" },
  }
---

# Motley — NYC neighborhoods, schools & admissions

Motley is the family intelligence platform for New York City: 262 neighborhoods
(not just five boroughs), 2,900+ K-12 schools, safety and health indicators, family
resources, weekday-morning commute times, and a full reference for how NYC school
admissions works. This skill
connects you to Motley's hosted MCP server so you answer from the source data
instead of scraping listing sites.

## Connect (one time)

If `motley` is not already in your MCP servers, add it:

```bash
openclaw mcp add motley --url https://mcp.motley.nyc/mcp --transport streamable-http
```

Or in `openclaw.json`:

```json5
{
  mcp: {
    servers: {
      motley: {
        url: "https://mcp.motley.nyc/mcp",
        transport: "streamable-http",
        enabled: true,
      },
    },
  },
}
```

Public and keyless — no API key, no account, nothing to install. Every tool is
read-only and idempotent, so it is safe to auto-approve. Tools return typed
`structuredContent` alongside their text: parse the object, don't re-parse JSON
out of prose.

## Which tool to reach for

**Placing a family in the city**

| Ask | Tool |
|---|---|
| "Which neighborhood is this address in?" | `find-neighborhood` (address or lat+lng) |
| "What's the zoned elementary school for this address?" | `get-zoned-school` (the address the family gives, with the building number) |
| "Rank NYC neighborhoods for what we care about" | `rank-neighborhoods` (ranked priority words incl. parks and diversity, or weights; optional borough; relay `unrecognized_priorities`) |
| "Compare Park Slope vs. Astoria" | `compare-neighborhoods` (2–6 NTA codes, per-metric matrix + leader, and commute minutes from each) |
| "Tell me about this neighborhood" | `get-neighborhood-summary` — **start here**, it's the interpretation-first answer |
| "How long is the commute from there to Midtown?" | `get-neighborhood-summary` (weekday-morning transit minutes to ten job centers) |
| "Affordable family neighborhoods with a strong zoned school" | `find-collections` (kind `neighborhoods`, optional borough) — lists picked by a stated rule |
| Raw demographics and scores for one neighborhood | `get-neighborhood` |
| "Somewhere like this, but…" | `get-comparable` |
| Find neighborhoods by borough or name | `search-neighborhoods` |

**Schools**

| Ask | Tool |
|---|---|
| "Brooklyn middle schools with a strong arts program" | `browse-schools` — citywide, by borough / district 1–32 / grade band / school type / admissions method / program focus |
| "What schools are in this neighborhood?" | `get-schools` (requires an `nta_code`) |
| "Tell me about Townsend Harris" — a school by NAME | `find-school` — name, short form, or DBN → candidates with their DBN |
| "How does this school admit students? How hard is it to get in?" | `get-admissions-demand` (needs a DBN — resolve the name with `find-school` first) |
| "Zoned schools that beat their district while serving high-need students" | `find-collections` (kind `schools`, optional borough) |

**Admissions**

| Ask | Tool |
|---|---|
| "How does NYC high school admission work?" | `get-admissions-methods` — every entry point, 3-K through high school, with typical windows |
| "What does a screened school actually ask for?" | `explain-admissions-method` — the explainer, the deadline window, and any extra ask (audition portfolio, SHSAT registration, demonstrated-interest sign-in, private-school testing) |
| "What applications are coming for my 4th grader? When?" | `get-admissions-timeline` (each child's current grade, or an age 0–5) — the city's published dates where it has announced them |

**How Motley scores**

| Ask | Tool |
|---|---|
| "How is the safety score computed? Is Motley biased toward richer areas?" | `explain-score` — inputs, weights, limits, sources, and how the score moves with neighborhood income |

**Everyday life**

| Ask | Tool |
|---|---|
| "Is there a library in Park Slope?", "coffee near Ditmars", "pediatricians in Astoria": the places inside one neighborhood, by name, street or kind | `find-places` (an `nta_code`; a `query`, or a `kind` to list every place of it; neither gives an overview of what's there) |
| How many playgrounds, libraries, hospitals, rec centers, farmers markets, ADA stations | `get-resources` (counts only) |
| Classes, sports, arts, tutoring nearby | `get-activities` |
| Crime, collisions, housing violations, air quality, lead, asthma | `get-safety` |

Also browseable: `motley://neighborhoods`, `motley://neighborhood/{nta_code}`,
`motley://admissions/methods`, `motley://admissions/method/{key}`.

## How to use it well

- **Lead with the summary, not the numbers.** `get-neighborhood-summary` returns a
  plain-language fit verdict and labeled score bands ("Peace of Mind: strong
  (78/100)"). Give the family that. The raw scores are there if they ask.
- **Neighborhood, not borough.** "Brooklyn" is 60-some neighborhoods that differ
  enormously. Resolve to a specific one before answering.
- **Identifiers:** neighborhoods are `nta_code` (from `search-neighborhoods` or
  `find-neighborhood`); schools are a DBN like `13K430`. Never invent either —
  look it up first.
- **An error is not an empty result.** These tools refuse rather than mislead: an
  unfiltered `browse-schools` and a private-school-plus-program-focus search both
  return a machine-readable error code, because a ranked citywide list nobody asked
  for and a structurally-empty set both read as answers when they aren't. Relay the
  tool's own reason.
- **Never estimate a family's odds of admission.** No odds, chances or
  percentages, even when asked: say how the school admits, who may apply, the
  seats, and applicant counts where they exist. Seats and applicant counts come
  from NYC MySchools; the competitiveness band beside them is Motley's own, never
  a DOE rating.
- **Every school is rated on the grades it serves.** `get-schools` returns each
  school's `ratings` out of 100: elementary and middle schools on the grades 3-8
  state tests, high schools on graduation and Regents results (`ratings_note`
  says how each is built); a 6-12 school has both. Say which one you quote.
- **A commute is a range.** `minutes_typical` to `minutes_high` is the spread
  across weekday-morning departures ("40-43 min"); quote both ends.
- **Scores are dated and versioned.** Responses carry `scores_as_of` and
  `scores_version`; say the date when it matters, and use `explain-score` (or the
  `methodology_url`) when a family asks how a number was made.
- **Some areas aren't scored.** Parks, cemeteries, airports and institutions have
  too few residents for neighborhood scores; when a response carries
  `scores_note`, relay it rather than treating the area as a neighborhood.
- **Link what you cite.** When a neighborhood or school came back with a `url`,
  link it.
- **Out of scope:** there's no account, so these tools can't see or change a
  family's saved research, and they don't simulate lotteries. This surface is
  knowledge and search.

## Try it

> We have a 4-year-old and want good schools without leaving Brooklyn. Where should we look?

> How does the SHSAT actually work, and what does it take to get into Brooklyn Tech?

> Compare Jackson Heights and Sunnyside for a family with a toddler.

> Which Manhattan elementary schools have a dual-language program?
