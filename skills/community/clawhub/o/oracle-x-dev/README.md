# Oracle-X Development — AgentSkill

Conventions for extending the [Oracle-X](https://github.com/Yigtwxx/OracleX)
codebase: adding a FastAPI endpoint, wiring a new upstream into the health
badge, registering a blockchain adapter, writing a prompt, and testing any of
it the way that repository tests things.

## Install this only if you are working in that repository

It is not a general FastAPI or Next.js guide, and it will not help you use
Oracle-X — it encodes decisions specific to one codebase, several of which
would be wrong somewhere else. If you want to *read* a running instance, the
skill you want is `oracle-x-api`, or the repository's
[`mcp-server/`](https://github.com/Yigtwxx/OracleX/tree/main/mcp-server).

Working from a clone, you may not need it at all: the repository's `CLAUDE.md`
loads on its own and records what the system *is*. This skill records how to
extend it, and deliberately does not repeat that file.

## What it carries

```
SKILL.md                # the four quality gates, and the rules that bite
references/
├── endpoint.md         # router → service → cache → error, and registration
├── upstream.md         # http_client, and mapping a host onto the health badge
├── chains.md           # the duck-typed chain adapter contract
├── llm.md              # the provider chain, prompts as files, the note pattern
└── testing.md          # monkeypatch at the import site, and why lib/ holds the tests
```

The rules in `SKILL.md` are the ones review actually catches, ordered by how
expensive they are to find later — identity read from a request instead of
`AuthUser`, an unmeasured number rendered as `0`, a direct `httpx` call that
makes a dead provider report as healthy, a computed prompt name that passes
review and fails the suite. Each says why, because a rule whose reason is
missing gets "simplified" away by the next person.

Entirely hand-written. Conventions are not derivable from a schema, which is
why the sibling API skill has a generated reference and this one does not.

## Source

[Yigtwxx/OracleX](https://github.com/Yigtwxx/OracleX/tree/main/agent-skill).
