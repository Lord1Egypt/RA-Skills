# `marketup-uc` references

These files hold **copy-paste curl / jq details** so [`../SKILL.md`](../SKILL.md) can stay decision-oriented (when to call what, business rules) without repeating long command blocks. That keeps the main skill smaller for the prompt and easier to maintain when endpoints change.

| File | Covers |
| --- | --- |
| [find-leads.md](./find-leads.md) | Detail, quick search, `.../leads/list`, jq snippets |
| [leads-mutations.md](./leads-mutations.md) | Create, modify field, follow-up, assign, tags, receive, return |
| [leads-history.md](./leads-history.md) | Remark / change / behavior history GETs |
| [convert-and-forms.md](./convert-and-forms.md) | Form field query, lead → account convert |
| [pool-and-users.md](./pool-and-users.md) | Lead pool list filters, pool config, current user, team user search |
| [accounts-query.md](./accounts-query.md) | Account detail/list/advanced-filter query patterns |
| [accounts-mutations-and-pool.md](./accounts-mutations-and-pool.md) | Account create, modify, and account pool config |
| [setup-marketup-api-key.md](./setup-marketup-api-key.md) | Missing-key preflight setup flow via script |

All examples assume you inject `Authorization` + `Referer` per [`../SKILL.md`](../SKILL.md) **调用规范** (e.g. `CURL_HEADERS` pattern in `find-leads.md`).
