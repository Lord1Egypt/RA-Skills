# OpenAlex Skill — README

This folder is the **agent skill** for OpenAlex: a structured knowledge pack that teaches an agent how to use OpenAlex well. It does not run anything — the callable tools live in the **OpenAlex MCP server** (`../mcp/`).

---

## What the skill is

A set of Markdown documents the agent reads to:

- Decide **when** OpenAlex is the right source (and when it is not).
- **Resolve** names to entity IDs.
- Build **filtered works queries** and aggregations.
- **Read** results (including reconstructing abstracts from the inverted index).
- **Cite** results correctly (title, authors, year, DOI, OpenAlex ID/URL).
- Handle errors, rate limits, and deep paging.

OpenAlex is **free** and needs **no API key**. Setting `OPENALEX_MAILTO` joins the faster polite pool (recommended).

---

## MCP vs. Skill

| | **MCP server** (`../mcp/`) | **Skill** (this folder) |
|---|---|---|
| Form | Running process, 6 tools over stdio | Markdown knowledge |
| Gives | Live API calls | Workflows, syntax, citation rules, recipes |
| Needs runtime? | Yes (Node ≥ 18) | No |
| Use for | Retrieving data | Reasoning & planning queries |

Use them **together**: the skill makes the agent call the MCP tools correctly.

---

## Folder map

```
skill/
├── SKILL.md                         # FEATURED — the full skill (numbered sections)
├── README.md                        # this file
├── reference/
│   ├── entities-and-filters.md      # entity types, ID prefixes, filters, sort, cursor
│   ├── endpoints.md                 # 6 tools + generic pattern + API catalog pointer
│   ├── response-fields.md           # meta/results/group_by, work & author fields, abstracts, citing
│   ├── common-errors.md             # HTML 404 / 429 / empty: cause + reaction
│   └── best-practices.md            # discovery, filters, polite pool, citation, caching, integrity, cursor
├── recipes/
│   ├── literature-search.md
│   ├── author-profile.md
│   └── citation-trends.md           # group_by year
├── prompts/
│   ├── query-building.md
│   └── citation-generation.md
└── tests/
    ├── skill-evaluation.md
    └── failure-cases.md
```

---

## Pairing with `openalex-mcp`

1. Install the MCP server (no key) — see `../mcp/docs/01-installation.md`.
2. Set `OPENALEX_MAILTO` for the polite pool — see `../mcp/docs/02-configuration.md`.
3. Load this skill so the agent applies the discovery → query → cite workflow.
4. The agent now calls `openalex_search`, `openalex_works`, `openalex_get`, `openalex_authors`, `openalex_group_by`, and `openalex_request` correctly.

> Verification needed: confirm tool names and behavior against the installed MCP server and <https://docs.openalex.org>.
