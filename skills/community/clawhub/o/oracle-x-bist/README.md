# Oracle-X BIST — AgentSkill

Borsa İstanbul for an agent: BIST equities and the XU100, TEFAS funds and their
holdings, KAP disclosures, VİOP futures margins, open interest and positioning,
foreign ownership, short-sale restrictions, and the Turkish macro series —
TÜFE inflation, the policy rate, USDTRY — that the rest is measured against.

## Half of it works with no server

This is the difference between this skill and its siblings. The endpoint half
calls a running [Oracle-X](https://github.com/Yigtwxx/OracleX) instance. The
other half is the market itself, and it applies the moment you install it:

* **A lira figure is not a return.** Every figure here is carried as `nominal`,
  `real` (deflated by consumer prices) and `usd` at once. Quote the lira number
  alone over a year of ~32% inflation and you have reported inflation as
  performance. A null `real` means the window could not be deflated — never
  that inflation was zero.
* **The VİOP scan range is not a margin call.** Takasbank publishes a one-day,
  99% price scan range; it does not publish a maintenance margin rate. The CCP
  procedure leaves the level to a General Letter and says maintenance is not
  applied at end of day. The "75% of initial" figure that circulates online
  comes from one undated guide. A call price for VİOP cannot be computed from
  anything public, and this skill says so rather than inventing one.
* **Takasbank's parameters are open; its website is not.**
  `www.takasbank.com.tr` sits behind bot protection and will not answer a
  script, which makes the numbers look unavailable. `wwwdata.takasbank.com.tr`
  is a separate host with an open listing, and the day's file is
  `pardosya/Prod/YYMMDD/TAKASEOD_…-001.zip`. The `/viop/SPAN/` path on the same
  host is a legacy archive frozen in March 2017 that still returns `200` —
  which is worse than a 404, because the numbers look current.
* **Reading that file costs two filters.** `setlMeth == "DELIV"` and a `pfCode`
  that does not end in `_C`, because the archive carries a portfolio per broker
  and a rights-issue portfolio beside each contract. Skip either and THYAO
  reads 13.4 as 14.0 — plausible, wrong, and silent.

`references/viop-margins.md` is the whole procedure, host to parser.

## Why this is separate from `oracle-x-api`

Because most installs are not in Turkey. BIST is 32 endpoints, a third of the
API surface, and carrying it costs context on every query that will never touch
it. Someone trading crypto and US equities installs
[`oracle-x-api`](https://github.com/Yigtwxx/OracleX/tree/main/agent-skill/oracle-x-api)
and nothing here. Someone who wants Borsa İstanbul adds this one. They share an
instance and a base URL, and neither needs the other.

If you want the terminal's numbers reaching a model without being asked for,
[`mcp-server/`](https://github.com/Yigtwxx/OracleX/tree/main/mcp-server) is the
one to install — a tool list already sits in the model's context, and a skill
has to be looked up first. That is measured, not assumed; the measurement is in
[`agent-skill/README.md`](https://github.com/Yigtwxx/OracleX/tree/main/agent-skill).
The rules above are the reason to install this skill anyway.

## Configure

```bash
export ORACLE_X_URL=http://localhost:8000   # default; set for a remote instance
```

No token: nothing in the BIST surface is scoped to a person.

## What is inside

```
SKILL.md                     # the rules, then the decision table
references/
├── endpoints.md             # generated — every BIST endpoint, in full
└── viop-margins.md          # reading Takasbank's SPAN file directly
```

`SKILL.md` loads whenever the skill triggers. The references are read on demand.

## Source

[Yigtwxx/OracleX](https://github.com/Yigtwxx/OracleX/tree/main/agent-skill).
`references/endpoints.md` is regenerated from the backend's OpenAPI schema and
CI fails if the committed copy has drifted, so it cannot silently describe
routes the API no longer serves.
