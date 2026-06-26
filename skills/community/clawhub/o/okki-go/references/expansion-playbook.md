# Prospecting Expansion Playbook

Expansion owns new customer-route branches after a visible batch is exhausted or the user explicitly asks for alternate routes. It is not hidden recovery and never authorizes paid actions.

## Pagination First

Before Expansion, inspect compact batch metadata:

1. If `has_next_page=true`, or `next_offset` exists and is less than `available`, stay in `L0_PAGINATION`.
2. If batch state is missing or stale, recover the batch or rerun a free lookup before deciding.
3. If the user says results are wrong, supplier-like, or not buyers, use `search-strategy.md` unless they only asked for the next page.

## Trigger Conditions

Expansion is appropriate when:

- the current route is exhausted and the user wants more prospects
- the user asks for other customer types, applications, cooperation modes, or routes
- L2 searched one graph path and the user confirms trying a second route
- the current route remains low-yield after the small recovery budget

Do not use Expansion for "next page" when pagination exists, or for latest/source-backed market research.

## Branch Proposal

Offer 2-3 distinct customer-side routes, such as:

- channel/resale
- installation/integration
- service/maintenance/retrofit
- project/specification
- direct operator/use

Each branch should include:

- branch label
- why the route could buy, resell, install, integrate, maintain, retrofit, specify, or use the offer
- one recall-first payload idea
- local priority rule
- avoid/not-recommended signals

The user confirms one branch. Search only that branch. If the user asks to try all, ask which branch to start with unless they explicitly accept sequential searches.

## Payload Guard

Every branch payload applies the Company Search Keyword Contract from `SKILL.md`:

- minimal keyword shape plus geography when supplied
- Chinese target-side index terms by default
- secondary buyer-route signals kept local when they may over-narrow recall
- no default `AND` or packed three-field payloads

## Result Presentation

After a confirmed branch search:

- show the company discovery result using `output-contracts.md`
- label the branch used
- add priority/observe/not-recommended guidance only when the user asked for analysis or the route is guided

Before unlock, contact search, or email send, use `paid-actions.md`.
