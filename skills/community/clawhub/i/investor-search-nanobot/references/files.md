# File formats — columns, reasons and examples

Open this when you are about to write a batch with `store.py add`, or when you need to know
what a column or a pending reason means. The rules that decide *what* goes in a row are in
`SKILL.md`; this file is the shape of the rows.

### `investors.csv` — UTF-8 with BOM

| column | meaning |
|---|---|
| `id` | stable row id — joins to `sources.csv` |
| `name` | best-looking form |
| `type` | the six values above |
| `investor_evidence` | `invests` · `operating_group` · `syndicate` · `unclear` |
| `matches_request` | `yes` · `no` · **blank when undeterminable** |
| `website` | registrable domain as written |
| `headquarters` | city, country |
| `headquarters_partial` | `yes` when only the country is established |
| `person` | **the most senior individual you actually saw** |
| `role` | their title as the page states it |
| `people_known` | how many named people you saw — one row is one firm, not one person |
| `linkedin` | profile or company URL |
| `sectors` | as the firm describes them |
| `fold_conflict` | the other name this row's key collided with |
| `formerly` | the firm's previous name, where a page states one |
| `type_blanked_reason` | `contradicts_request` — the only value; empty otherwise |
| `part_of` | the parent, where a page stated one |
| `sovereign_parent` | the sovereign fund above it, where there is one |
| `key_quote` | one sentence that **evidences this firm is what the row says it is** |
| `key_quote_url` | the page that sentence is on |
| `checked` | ISO date |
| `provenance` | one of the five labels |

**Illustrative — invented firms, to show the shape, not a run's output:**

```
id,name,type,investor_evidence,matches_request,website,headquarters,headquarters_partial,...
f-001,Nadira Capital Partners,family_office,invests,yes,nadiracapital.example,"Lisbon, Portugal",,
f-002,Orsett Group,unknown,operating_group,,orsett.example,Portugal,yes,
```

The request named a type, so `f-001` — a match — carries `yes`. `f-002` shipped as `unknown`,
so whether it matches the named type **could not be determined**, which is the one case the
column's blank is for; a stated type that simply differs would carry `no`. Its
`investor_evidence` is still `operating_group` — you can see that a firm runs its own
businesses and still be unable to type it. `f-001` was sourced to a city, `f-002` only to a
country, hence `headquarters_partial`. Neither row would exist without a `sources.csv` row per
filled field.

**`key_quote` must evidence the row, not merely come from the page.** A sentence defining
what a family office *is in general* evidences nothing, and a reader scanning the file reads
a native-language quote as proof. **No evidencing sentence → leave it empty and say so.** A row with no `key_quote`, or with `provenance` *source NOT fetched*, is never a match: `store.py` leaves `matches_request` blank and `finish` lists it under `no_quote_or_not_fetched`. Fetch the firm's own page before you judge it.
*"Original language" means the language of the page you read*, not of the country.

### `sources.csv` — one row per citation

```
id,field,rung,url
f-018,website,1,https://example.com/about
f-018,headquarters,2,https://registry.example/entry?id=7&x=1
```

**A field may carry citations at more than one rung** — that is good, not a problem. It does
mean *"rows resting on a rung-4 source alone"* is a `NOT EXISTS` question (no citation at
rung 1–3 for that field), never `WHERE rung = 4`.

**A separate file, not a packed cell.** Every in-cell format tried broke (`why.md`), and one
row per citation carries the rung as a real column.

### `investors-pending.csv` — offered, not resolved

```
name,reason,note,first_seen,source_url
```

| reason | meaning | resolvable? |
|---|---|---|
| `budget` | never got to it | **yes** |
| `sourceUnchecked` | page exists, could not be fetched | **yes** |
| `noHeadquarters` | HQ not established yet — **two headquarters is not this**, see Job 2 | **yes** |
| `unresolvedJob0` | Job 0 could not be decided even as `unclear` — you never found enough of the firm to judge | **yes** |
| `outOfCountry` | real, wrong market — **including a local fund whose manager is abroad**; say which in `note` | no — **terminal** |
| `outOfScopeSovereign` | sovereign or state parent | no — **terminal** |
| `namedFamilyNotFirm` | a capital pool named only as "the X family" | no — terminal unless a vehicle name turns up |
| `individualNotFirm` | a named angel with no vehicle — a real investor, but one row is one firm | no — terminal |
| `hqNotPublished` | `noHeadquarters` re-checked on the firm's own site **and** a business registry, and no headquarters is published anywhere; `note` must name what was searched | no — terminal |

**Closing a pending row.** Every resolvable row has a way out that is not `--early`:

- **It is a firm you already hold under another name** (same website) — send it in `investors` with that website. `add` reports it as `already_held` and clears the pending row.
- **You found the headquarters** — send the firm in `investors`; the row clears.
- **It is not an investor** — send it in `rejected`.
- **You re-checked and no headquarters is published** — send it again in `pending` with reason `hqNotPublished` and a `note` naming the pages and registry you searched. `add` moves the row; it stays in the file and the report.

**Gate 1 counts only the resolvable reasons.** Terminal rows stay in the file and in the report, but never hold a run open — `store.py status` shows them apart as `pending` versus `pending_open`. **`finish --early` takes only `user` or `blocker: …`** — never use it to get past a gate.

**`individualNotFirm` is not a rejection.** Individual angels are legitimate targets; they
simply do not fit a row that means "one firm". Keep them here with their source so the reader
can take them.

**Only the resolvable reasons hold Gate 1 shut.**

### `investors-rejected.csv` — **local working file, never published**

```
name,reason,evidence,checked,source_url
```

`adviserNotInvestor` · `notAnInvestor` · `sourceDead` · `unsourceable`.

**Two of these four are permanent and two are not.** `adviserNotInvestor` and
`notAnInvestor` describe the firm, so never search them again. **`sourceDead` and
`unsourceable` describe one page on one day** — re-offer them on a later run, because a
different route may source them properly. They are in this file so you can see the call was
made, not to suppress the name forever.

**Keep the names, keep the file local.** Shipping a result set to a client means
`investors.csv` plus a **count** of rejections, never the list.

---

## The headers `store.py init` writes

For reference only — the script writes these itself, and you never write them by hand.

```
investors.csv           (UTF-8 with BOM)
id,name,type,investor_evidence,matches_request,website,headquarters,headquarters_partial,person,role,people_known,linkedin,sectors,fold_conflict,formerly,type_blanked_reason,part_of,sovereign_parent,key_quote,key_quote_url,checked,provenance
sources.csv             id,field,rung,url
investors-pending.csv   name,reason,note,first_seen,source_url
investors-rejected.csv  name,reason,evidence,checked,source_url
rounds.csv              round,query,surface,offered,survived,dry_streak,fetch_failed,at
ledger.txt              #LEDGER v2 market=<market> date=<ISO>
                        #SCOPE <the scope line from index.md>
                        key|name|domain|status
                        #END rows=0
```
