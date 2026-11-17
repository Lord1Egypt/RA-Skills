---
name: news-triage
version: 0.2.1
license: MIT-0
description: Research and compare news from the Chinng AI-Agent Portal. Use when finding relevant articles, investigating a topic, or preparing a sourced news summary.
---

# News triage

Use the `portal` MCP server declared by this plugin.

Standalone install (no plugin): register the read-only MCP endpoint first — `openclaw mcp add portal --transport http https://portal.chinng-lab-srv.dev/mcp`. Other MCP clients: <https://portal.chinng-lab-srv.dev/mcp>.

1. Discover candidates with the portal's listing or search tools. Inspect metadata and summaries before requesting bodies.
2. Select only the records needed for the task, then retrieve those records individually.
3. Respect each record's `license_note` and omission metadata. Never reconstruct content withheld by the portal.
4. Cite the portal record and retain its original source link when presenting findings.

## What a news record actually contains

Most external news is `link-only`. Those records carry no summary at all — only the title, the metadata fields, and the links — and their `summary_omitted_reason` says why. Triage them on title, `tags`, `keywords_en`, `entities_en`, and `numeric_facts`, which remain available, and present them as dated pointers.

A `full` news record's body is a wrapper: the title, the summary repeated as `TL;DR`, the tags as `Key Points`, then an empty `Details` section. There is no article text behind it. Retrieving the body of a news record therefore rarely adds anything the listing did not already return, so retrieve one only when the summary is genuinely needed and was not present in the listing.

Treat `entities` as a triage hint whose precision varies by source, and ignore `related_auto` entirely.

Keep discovery token-light: list or search first, retrieve bodies only when they materially improve the answer.
