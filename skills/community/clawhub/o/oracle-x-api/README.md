# Oracle-X API — AgentSkill

Read live market intelligence from a running [Oracle-X](https://github.com/Yigtwxx/OracleX)
terminal: spot prices and candles for crypto (BTC, ETH, SOL) and equities,
computed support/resistance zones, news with its LLM analysis, macro regime,
per-chain metrics, liquidations, funding rates, open interest, whale flow,
institutional ownership, Polymarket prediction-market odds, and a vector memory
of past market events.

This is the read side of a server you run, not a data source of its own. It
needs a reachable instance — by default `http://localhost:8000`.

**Borsa İstanbul is a separate skill.** The same instance also serves BIST
equities, TEFAS funds, KAP disclosures and VİOP, but that is 32 endpoints —
a third of the allowlist — and an install that never asks about Turkey pays
for them on every query. They live in
[`oracle-x-bist`](https://github.com/Yigtwxx/OracleX/tree/main/agent-skill/oracle-x-bist),
which is worth a look even without a server: how a lira return is turned into
a real one, and why a VİOP margin-call price cannot be computed from anything
public, hold whether or not an instance is running.

## Install the MCP server first; add this if you write code against the API

The repository ships the same instance as
[`mcp-server/`](https://github.com/Yigtwxx/OracleX/tree/main/mcp-server) — 36
MCP tools, six of them Turkish. **That is the one to install if you want the terminal's numbers to
reach a model at all**, because a tool list already sits in the model's context
and the only decision left is which tool to call. A skill has to be looked up
first, and the section below is the measurement showing that it is not.

This skill is the better of the two for one job: writing code against the API.
There an agent reaches for documentation on its own, and
[`references/endpoints.md`](references/endpoints.md) is generated from the
running app rather than remembered. Installing both is the normal case.

## Before you install: it will not trigger on its own

This was measured, not assumed. Twenty realistic queries — "what is BTC doing",
"where are ETH's levels", "why did SOL move today" — were run against three
rewrites of this skill's description. The agent chose to consult the skill on
almost none of them. Whenever it did, it used it correctly; it simply did not
go looking. Rewording moved nothing, and the original description scored best
of the three.

The cause is structural rather than editorial. A skill has to be *looked up*,
and a model asked what BTC is doing already believes it can answer. No wording
gets in front of that, because the decision to go looking comes first.

That leaves two ways to install it honestly:

* **Ask for it by name.** "Use the Oracle-X skill and tell me where BTC's
  levels are" works exactly as designed — the endpoint map, the auth rules and
  the refusal to invent a number are all there once the skill is open.
* **Writing code against the API.** Here an agent reaches for documentation on
  its own, and `references/endpoints.md` is generated from the running app
  rather than remembered.

This is why the MCP server is named first above rather than as an alternative:
the skill is for writing code against Oracle-X, the tools are for asking it
questions, and only one of the two gets consulted unprompted.

## Configure

```bash
export ORACLE_X_URL=http://localhost:8000   # default; set for a remote instance
export ORACLE_X_TOKEN=...                   # only for chat and watchlist
```

Most of the surface is open on a default instance. The token is a Supabase
access token and is needed only for endpoints scoped to a person — see
[`references/auth.md`](references/auth.md).

## What is inside

```
SKILL.md                # the decision table: which question → which endpoint
references/
├── endpoints.md        # generated — every allowlisted endpoint, in full
├── auth.md             # tokens: obtaining, using, verifying
└── recipes.md          # the multi-step reads worth knowing
examples/               # runnable httpx clients
```

`SKILL.md` loads whenever the skill triggers, so it holds only what an agent
needs to choose correctly. The `references/` files are read on demand — the
endpoint reference alone is 800 lines and has no business in context until a
call actually needs it.

## The rule worth knowing before the first call

Oracle-X declines rather than guesses: 404 when a symbol cannot be resolved,
503 when an upstream is dead and an empty list would be a lie. A refusal is an
answer, and passing it on unchanged is the point — in a trading terminal a
plausible wrong number is worse than an error. `SKILL.md` spends a section on
this, and the examples under `examples/` show the difference between "no data"
and "the lookup never happened".

## Source

Generated and maintained in
[Yigtwxx/OracleX](https://github.com/Yigtwxx/OracleX/tree/main/agent-skill).
The endpoint reference is regenerated from the backend's OpenAPI schema and CI
fails if the committed copy has drifted, so it cannot silently describe routes
the API no longer serves.
