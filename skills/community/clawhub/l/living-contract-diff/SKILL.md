---
name: living-contract-diff
description: Detect drift between what an API actually returns and what its OpenAPI spec promises. Builds a statistics-only baseline from recorded traffic (a HAR file), then diffs it against an OpenAPI 3.x spec (JSON or YAML) to report required fields the API never sends, type mismatches, undocumented fields and enum growth. Use when asked to check API contract drift, compare a spec against real responses, audit an OpenAPI spec against recorded traffic, or gate API changes in CI. Not for generating an OpenAPI spec from scratch, for live API monitoring, or for testing API behaviour — this tool compares recorded traffic against an existing spec.
license: MIT
compatibility: Requires Python 3.9+ and pip. Fully offline; traffic comes from files you supply — a HAR file or a folder of JSON samples — there is no live proxy.
---

# Living Contract Diff

## What this tool does

Living Contract Diff learns what an API actually returns from recorded
traffic, then diffs that observed contract against the declared
OpenAPI spec. `observe` reads a HAR file and writes a baseline of
statistics only — presence counts, type unions, nullability — never
payload values (one designed exception: fields with at most 20 distinct
values store those candidate values, because they are the contract).
`diff` compares a baseline with the spec and reports drift. Nothing
from a HAR or a spec is ever executed.

## Install

```bash
pip install git+https://github.com/RakTikoo/living-contract-diff
# or, isolated, with pipx:
pipx install git+https://github.com/RakTikoo/living-contract-diff
```

With uv:

```bash
uv tool install git+https://github.com/RakTikoo/living-contract-diff
```

This provides the `lcdiff` command (standard library only).

## Run

Build a baseline from recorded traffic, then diff it against the spec:

```bash
lcdiff observe --har traffic.har --out baseline.json
lcdiff diff --baseline baseline.json --spec openapi.json
```

Machine-readable report: add `--format json` to `diff`. The spec may
be YAML (`.yaml`/`.yml`) instead of JSON. `lcdiff diff-baseline --old
old.json --new new.json` compares two baselines with the same codes.
Reports go to stdout unless `--out FILE` is given (both diff modes).

No HAR? `lcdiff observe --samples-dir samples/ --manifest
manifest.json --out baseline.json` builds a baseline from a directory
of `.json` response samples plus an endpoint manifest JSON instead
(`--samples-dir` requires `--manifest`).

`diff` options: `--required-threshold 0.95` sets the presence rate
below which a required field is `REQUIRED_MISSING` (default 0.99;
0 < x ≤ 1). `--ignore-endpoint 'GET /health'` excludes endpoints
matching a glob (repeatable; matched against `METHOD /path` and the
path template).

Accepted drift: `lcdiff accept --report report.json --reason "…"
--out ledger.json` records every active finding of a JSON diff report
as accepted drift in a ledger, with the reason (`--reason` is
required and must not be empty; `--ledger existing.json` extends an
existing ledger, keeping the original reasons). Passing `--ledger
ledger.json` to `diff` or `diff-baseline` reports findings whose
(endpoint, code, field) identity is in the ledger as accepted — they
are printed in their own section, listed under `accepted` in the JSON
report, and never affect the exit code.

## Reading the results

Finding codes: `REQUIRED_MISSING` and `TYPE_MISMATCH` are breaking;
`UNDOCUMENTED_FIELD` and `ENUM_GROWTH` are warnings. Two documented
downgrades: a required field whose parent array was observed but
always empty is reported as a warning (unverifiable-because-empty),
and a type mismatch seen once in 20 or more observations is
downgraded to a warning with the count in the evidence. Every finding
names the endpoint, the field, and the evidence counts. Endpoints or
statuses in the spec with no observed traffic are listed as
`not_observed` — reported, never turned into findings.

Exit codes: `0` — no breaking drift (warnings may still be present).
`1` — breaking drift found. `2` — usage or tool error: an unreadable,
malformed or invalid input always exits 2 with an `error: …` message,
never a traceback and never a clean report.

Sample-size guard: an endpoint (per status) with fewer than 5 observed
JSON responses has all its findings downgraded to warnings, flagged
`low_sample` in the evidence — a tiny capture cannot break your build.
The JSON report carries `findings`, `not_observed`,
`endpoint_samples`, `accepted`, `summary` and `tool`.

## Limits

- Traffic comes only from files you supply — a HAR file, or a
  directory of `.json` response samples with an endpoint manifest.
  No live proxy or traffic interception, no request-body inference,
  no GraphQL/gRPC.
- Privacy is heuristic, not a guarantee: a short secret in a
  low-cardinality, innocuously named field *will* be stored as an enum
  candidate. Treat baselines as internal artefacts when traffic may
  contain sensitive values. (Fields named like passwords/tokens are
  denylisted, and anything over 20 distinct values stores no values.)
- Sparse fieldsets (`?fields=id,name`) cannot be detected from a HAR;
  mixed subsets blend into meaningless presence rates.
- YAML specs: a documented subset only — anchors, aliases, merge keys,
  custom tags and multi-document files are rejected with a named
  error. Local `$ref`s only; remote refs exit 2.
- Baselines are format version 2; a v1 baseline is rejected at load
  with a message telling you to regenerate it, never silently misread.
