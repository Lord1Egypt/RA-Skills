# <source_name> — <one-line description>

## What this source has

<2–3 paragraphs: corpus size, time range, coverage, distinguishing features. Be specific about *what data is in there*, not just "lots of data". Mention units, schemas, identifiers (e.g., DOI, CIK, FIPS).>

## Auth

| | |
|---|---|
| Required | yes / optional / none |
| Env var | `XXX_KEY` |
| Account URL | https://… |
| Plan tier | free |

If account is required, Reach is authorized to register at the URL above using `<agent-email>`. See `references/account_provisioning.md`.

## Limits

| | |
|---|---|
| Daily | N or — |
| Monthly | N or — |
| Rate | "X req/sec" or descriptive |

## Endpoints

```bash
python3 scripts/reach.py query <name> <action> '<params_json>'
```

| Action | Purpose | Params |
|---|---|---|
| `<action>` | <one-line description> | `{"key": "<type>"}` |

## Worked examples

```bash
# <one-line description>
python3 scripts/reach.py query <name> <action> '{"k": "v"}'
```

## Response shape

What you get back, with the keys most useful to the calling agent.

## Pitfalls

- <gotchas, off-by-one, format quirks>

## Source links

- API docs: …
- Terms: …
