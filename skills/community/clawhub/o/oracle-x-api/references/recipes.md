# Multi-step reads

Single questions are single calls — the table in SKILL.md covers those. These
are the sequences worth knowing, because each one has an ordering that matters:
a later call is cheaper, better targeted, or only interpretable because of what
an earlier one returned.

Run independent calls concurrently. Every step below that does not depend on
the previous step's output can be issued in the same batch.

---

## 1. A full workup on one asset

The question behind "what's going on with ETH" is really four questions. Answer
them in one pass rather than four round trips of conversation.

```
GET /api/price/{symbol}             → the number itself
GET /api/technical/{symbol}         → zones, RSI, trend per timeframe
GET /api/liquidations/map/{symbol}  → where leverage is stacked
GET /api/rag/insights/{symbol}      → what the memory holds about it
```

All four are independent — issue them together.

Read them in that order when you write the answer. The technicals say where
price is; the liquidation levels say what happens if it gets there; the RAG
insights say whether this configuration has resolved one way before. A workup
that gives levels without the third part is a chart reading, not intelligence.

If the ticker is an equity, add ownership:

```
GET /api/ownership/assets/{symbol}          → institutional positions
GET /api/asset-detail/{symbol}?type=stock   → P/E, sector, analyst targets
```

`type=stock` is not optional for an equity: the parameter defaults to the
crypto branch, which resolves through CoinGecko and answers 404 for a ticker.

`examples/01_asset_workup.py` runs exactly this.

---

## 2. From a headline to a thesis

```
GET  /api/news?limit=20&asset_type=crypto
GET  /api/news/{news_id}/analysis            → cached LLM read; may 404
POST /api/news/{news_id}/analysis/jobs       → only if the cache missed
GET  /api/news/analysis/jobs/{job_id}        → poll
POST /api/rag/news-similarity                → only if `precedents` was absent
```

Check the cache before starting a job. Analysis is generated once and stored,
so the common case costs one call, and starting a job for something already
analysed spends the operator's provider budget for a result they already have.
One trap: the cached read answers `200` with a JSON `null` body when nothing
has been generated — not `404`. Test the body, not the status.

The stored analysis also carries a `precedents` list, because the pipeline runs
the similarity lookup itself. When it is there, use it; `POST
/api/rag/news-similarity` is for the case where it is not.

`examples/02_news_thesis.py` runs this sequence.

The last step is the one that turns news into a thesis. A regulatory headline
that resembles four previous headlines, each followed by a two-day drawdown, is
a different object from one with no precedent in the store — and only the
similarity call can tell you which you have.

---

## 3. Is the backdrop supporting this move?

```
GET /api/macro/regime      → the label, the score, the note
GET /api/macro/board       → indices, metals, ratios behind the label
GET /api/chains/board      → on-chain activity
GET /api/chains/anomalies  → anything off its own baseline
GET /api/fear-greed        → both gauges
```

Independent; issue together.

The regime label is computed in Python and is always present. The note beside
it is written by the model layer and may be absent, in progress, or unavailable
because the operator runs with the model layer off — say the label without the
note rather than waiting for it.

Chain anomalies are scored against each chain's own history. "Fees elevated on
Solana" means elevated *for Solana*, which is why the anomaly endpoint is worth
calling separately from the board.

---

## 4. Precedent for the current setup

The reason to prefer Oracle-X over a search engine: the store holds what this
instance actually observed.

```
GET  /api/rag/query?q=<description of the setup>&symbol=<sym>
GET  /api/rag/event-at-date?...        → what surrounded a specific date
POST /api/rag/scenario                 → grounded "what if"
GET  /api/rag/stats                    → how much history there is
```

Call `/api/rag/stats` when a query comes back thin. A store with a few hundred
documents cannot support a claim about historical patterns, and saying "the
memory is too sparse to answer that" is the correct answer in that case.

`GET /api/rag/compare/{a}/{b}` answers relative questions in one call —
prefer it to two separate insight calls when the question is comparative.

---

## 5. Handing the whole question to the Oracle

When the question is genuinely open — "is this a good entry", "what should I
be watching this week" — the terminal's own chat has the same data plus the
memory plus the planner.

```
GET  /api/chat/status                  → is a provider serving?
POST /api/chat/jobs                    → start (auth)
GET  /api/chat/jobs/{job_id}           → poll until done
```

Use the job form over `POST /api/chat` for anything substantial: the synchronous
endpoint holds the connection until an answer exists, which for a multi-tool
turn can be minutes. The job form reports its steps while it runs, so progress
is visible.

`examples/03_chat_job.py` implements the poll loop.

Do not route simple factual questions here. A price lookup costs one cached
HTTP call through `/api/price` and one LLM invocation through chat; the answer
is the same and only one of them bills the operator.
