# Entity Formation and Governance

Choosing a structure is a tax and exit decision with legal packaging. Keeping the structure working is a paperwork discipline: the liability shield is not a property of the entity, it is a property of how the entity is operated.

**Before advising**, read `## Legal Context` in `~/Clawic/data/lawyer/memory.md` for the existing entities, `entity_type` in `config.yaml`, and `filings/<year>.md` per the `## Boxes` index for what has already been filed. Before any equity question — an issuance, a grant, a leaver, a dilution number — open `artifacts/cap-table.md` first: answering from a remembered ownership percentage is how a grant gets approved twice. Anything involving issuing shares, options or tokens to investors is a Red Flags row: securities law attaches to the offer, not the sale.

**Contents:** [Choosing A Structure](#choosing-a-structure) · [Where To Incorporate](#where-to-incorporate) · [Formation Checklist](#formation-checklist) · [Founders And Vesting](#founders-and-vesting) · [Equity For Employees](#equity-for-employees) · [Keeping The Shield](#keeping-the-shield) · [Governance Mechanics](#governance-mechanics) · [Cap Table Hygiene](#cap-table-hygiene) · [Multi-Entity Structures](#multi-entity-structures) · [Annual Obligations](#annual-obligations) · [Winding Down](#winding-down)

## Choosing A Structure

Four questions decide it, in order: who owns it, how profits are taxed, who will invest, and what the exit looks like. Legal form follows.

| Structure | Liability | Taxation (US) | Fits |
|---|---|---|---|
| Sole proprietor / sole trader | None — personal assets exposed | Personal | A test, a side project, nothing with real counterparty risk |
| Partnership (general) | Joint and several, unlimited | Pass-through | Almost never by choice; often created accidentally by two people doing business together without documents |
| LLC | Limited | Pass-through by default; can elect corporate or S-corp treatment | Operating businesses, property holding, consultancies, anything without institutional investors |
| S-corporation | Limited | Pass-through with payroll-tax planning; strict eligibility (US persons only, one class of stock, ≤100 shareholders) | Profitable small companies whose owners work in them |
| C-corporation | Limited | Entity-level tax, then dividends | Anything raising venture capital or issuing options at scale |
| UK Ltd / German GmbH / Spanish SL and equivalents | Limited | Corporate | The standard operating vehicle in their jurisdictions |

Institutional investors in the US buy preferred stock in a Delaware C-corp, and most funds cannot hold pass-through interests at all. If venture funding is the plan, the LLC will be converted, and converting later costs legal fees and sometimes tax.

## Where To Incorporate

- Incorporate where the business actually operates unless there is a reason not to. Forming in one state and operating in another means **foreign qualification** in the operating state anyway: two sets of fees, two annual filings, two registered agents.
- Delaware's advantages are real for venture-backed companies: a specialised court of chancery without juries, deep case law, and investor familiarity. For a five-person consultancy in Ohio it is pure overhead.
- Offshore structures for tax reasons are a specialist matter with substance requirements, controlled-foreign-company rules and reporting obligations. Do not improvise them.
- Cross-border founders: where the company is managed and controlled can determine tax residence regardless of where it was registered.

## Formation Checklist

1. Name availability in the register, plus trademark clearance and domain — a registered company name gives no trademark rights (`ip.md`).
2. Articles / certificate of incorporation filed; authorised share capital set with room for a future option pool.
3. Registered agent and registered office appointed and maintained.
4. Tax registrations: EIN or local equivalent, VAT/sales tax where thresholds are met, payroll registration before the first hire.
5. Governing document executed — operating agreement (LLC) or bylaws plus organisational consent (corporation). This is the document nobody writes and everybody needs.
6. Founder share issuance documented, paid for, and recorded in the register of members / stock ledger.
7. **IP assignment from every founder and early contributor into the company**, covering work done before incorporation. The most common diligence gap there is (`diligence.md`).
8. Bank account, and the discipline of never mixing it with personal money.
9. Beneficial-ownership reporting where required — several jurisdictions maintain registers with filing deadlines and penalties, and the US requirement has changed more than once through litigation and rulemaking. Verify the current position before assuming it does or does not apply.
10. Insurance appropriate to the activity; directors and officers cover if there is an outside board.

## Founders And Vesting

The founder agreement is worth more than the certificate of incorporation. It answers: who owns what, what happens when someone leaves, who decides what, and how a deadlock breaks.

- **Vesting**: standard is 4 years with a 1-year cliff, applied to founders as well as employees. Founders resist it and then need it — the co-founder who leaves in month seven with 33% of the company is the reason every investor demands it.
- Acceleration: single-trigger (on acquisition) is founder-friendly and buyer-hostile; double-trigger (acquisition **and** termination without cause within a window) is the market compromise.
- Leaver provisions: good leaver keeps vested equity, bad leaver (fraud, breach, resignation inside a period) forfeits at cost. Define the categories precisely; "bad leaver" defined by the board's discretion is a dispute in waiting.
- Roles, decision rights and time commitment in writing. A part-time founder with full equity is the second most common founder dispute.
- Deadlock resolution for 50/50 splits: a casting vote, a shoot-out clause, or a third director. Two equal founders with no mechanism is a company that can be frozen by one disagreement.

## Equity For Employees

- **83(b) election (US)**: on restricted stock subject to vesting, filing within **30 days of grant** elects to be taxed on the value at grant rather than at each vesting date. No extensions, no exceptions, and the value at grant is usually near zero. Missing it can convert a nominal grant into a large tax bill on paper gains. This is the single most consequential 30-day window in startup practice.
- Option grants: board approval (or delegated committee), a written plan, a grant notice, and a fair-market-value exercise price. Pricing options below fair market value creates immediate tax problems for the recipient — US companies use a 409A valuation to establish it defensibly.
- ISOs versus NSOs (US): ISOs have favourable tax treatment with strict conditions ($100,000 annual vesting limit, employees only, 90-day post-termination exercise window to keep the treatment). NSOs are flexible and taxed at exercise.
- Non-US equivalents have their own approved schemes with real tax advantages and strict conditions — the UK EMI scheme is the canonical example, with eligibility limits and a notification deadline after grant.
- Contractors and advisers cannot receive ISOs; use NSOs, warrants or a separate adviser agreement with its own vesting.
- Every grant is recorded in the cap table (`~/Clawic/data/lawyer/artifacts/cap-table.md`) on the day it is approved, not when the paperwork is chased.

## Keeping The Shield

Limited liability is defeated by treating the company as a wallet. Courts in most systems will disregard the entity ("pierce the veil") on evidence of:

| Evidence | Fix |
|---|---|
| Commingled funds — personal expenses on the company account | Separate accounts, documented expense policy, reimbursements not direct payments |
| Undercapitalisation at formation relative to the risks taken | Fund the entity properly, and carry insurance |
| No corporate formalities — no minutes, no consents, no records | The governance discipline below |
| Contracts signed personally or in a trade name | Correct entity and signature block every time (SKILL.md Rule 7) |
| The company used to perpetrate a fraud or evade an obligation | No fix; this is the core case |

Personal guarantees defeat the shield voluntarily and are the most common route to founder liability. Landlords, banks and some suppliers ask as a matter of course; the ask is negotiable, and the cap and duration are more negotiable than the guarantee itself (`agreements.md`).

## Governance Mechanics

- **Board versus shareholders**: directors manage; shareholders own and vote on fundamental matters. Reserved matters (issuing shares, borrowing above a limit, selling the business, changing the constitution) are listed either in law or in the shareholders agreement, and acting without the required approval makes the act challengeable.
- **Written consents** are how small boards act: circulate, sign, file. Unanimous written consent replaces a meeting in most systems for most decisions.
- **Minutes** need to record the decision and the fact that it was considered, not the debate. Minutes that editorialise become evidence.
- **Conflicts of interest**: disclose, record the disclosure, and have the conflicted person abstain. Related-party transactions approved without disclosure are voidable and are found in every diligence process.
- Directors owe duties (care, loyalty, and in some systems duties to creditors when insolvency approaches) personally. A director who continues trading while insolvent risks personal liability — wrongful trading in the UK, comparable regimes elsewhere. That is a Red Flags escalation.
- Shareholders agreement topics that the constitution does not cover: transfer restrictions, pre-emption, tag-along and drag-along, information rights, dividend policy, deadlock, and exit.

## Cap Table Hygiene

One source of truth — `~/Clawic/data/lawyer/artifacts/cap-table.md`, or, if the table itself lives in a cap-table platform or a spreadsheet, that same file holding its `file:` or `<kind>:<locator>` pointer plus the summary — updated on the day of each transaction, reconciled to the signed documents and to the statutory register. Every diligence process finds discrepancies between the spreadsheet, the ledger and the executed grants, and every discrepancy costs time at exactly the moment there is none.

Track in `artifacts/cap-table.md`, one row per holding: security type and class, number, price paid, issue date, vesting start and schedule, cliff, expiry, and the document evidencing it. Options are tracked as granted, vested, exercised, cancelled and available in the pool — not as one number. Holders are named there and nowhere else in the lawyer box: the person record belongs to the shared `contacts.md`.

## Multi-Entity Structures

Reasons that justify a second entity: real operations in another country, ring-fencing a genuinely different risk (a property, a regulated activity), a holding company for an exit or for group relief, and an investor structure that requires it. Reasons that do not: aesthetics and premature tax planning.

Each entity multiplies filings, accounts, and intercompany paperwork. Intercompany arrangements need written agreements and defensible transfer pricing; groups that move money without documentation create tax exposure in both jurisdictions (`accountant`).

## Annual Obligations

Jurisdiction-specific; verify current amounts. The pattern to build into `## Due`:

| Obligation | Example |
|---|---|
| Annual report / confirmation statement | Delaware corporate annual report and franchise tax due 1 March; Delaware LLC annual tax due 1 June; UK confirmation statement annually |
| Financial statements filing | Required in most non-US systems within a set period after year end |
| Registered agent renewal | Annual; lapse leads to loss of good standing |
| Beneficial ownership updates | Where a register applies, changes typically reportable within a short window |
| Tax filings | Corporate, payroll, sales tax and VAT on their own cycles (`accountant`) |
| Board and shareholder annual meeting or written consent | Required by many bylaws even if the law is flexible |

Loss of good standing escalates quietly: penalties, then inability to file suit or register a security interest in the state, then administrative dissolution — after which contracts signed in the company's name have no company behind them.

## Winding Down

Dissolution is a process, not an abandonment. Stopping filings leaves the entity administratively dissolved with liabilities intact and directors exposed. The sequence: board and shareholder approval, notify and pay or provide for creditors in the statutory order, deal with employees properly (`employment.md`), terminate contracts and leases (`obligations.md`), final tax returns and clearances, cancel registrations and licences, distribute what remains, file the dissolution, and keep the records for the statutory retention period.

Insolvency changes the order and the duties — directors' obligations shift toward creditors and personal liability becomes possible. That is a Red Flags escalation, not a self-service process.

**After any entity action**, write in the same turn (`memory-template.md`): entity names, numbers, jurisdictions, registered agent and officers into `## Legal Context` in `memory.md`; every formation, filing, share issuance, grant and dissolution as a row in `~/Clawic/data/lawyer/filings/<year>.md`; every recurring filing deadline into `## Due`; every share issuance, grant, transfer, exercise and cancellation into `~/Clawic/data/lawyer/artifacts/cap-table.md` on the day it is approved; and durable documents — the operating agreement, the founder agreement, the option plan, a governance calendar, a board-consent template — into `~/Clawic/data/lawyer/artifacts/` with their `## Boxes` lines. Registration numbers and officer names are public identifiers and belong in the file; registry portal logins and tax-authority credentials do not (SKILL.md, secrets).
