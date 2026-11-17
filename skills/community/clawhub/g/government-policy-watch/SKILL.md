---
name: government-policy-watch
version: 0.2.1
license: MIT-0
description: Track official government documents in the Chinng AI-Agent Portal — US Federal Register, EU EUR-Lex, and Japanese agency feeds. Use for regulatory monitoring, comment deadlines, effective dates, and primary-source policy reading.
---

# Government policy watch

Use the `portal` MCP server declared by this plugin.

Standalone install (no plugin): register the read-only MCP endpoint first — `openclaw mcp add portal --transport http https://portal.chinng-lab-srv.dev/mcp`. Other MCP clients: <https://portal.chinng-lab-srv.dev/mcp>.

Government records are the portal's primary-source family. Most carry `license_note: full` with `redistribution: true`. Note that this permits reuse of what the portal stores; it does not mean the portal stores the document text. Government bodies are a wrapper around the summary, and their `Details` section is empty. The official URL is the only route to the document itself.

1. Narrow candidates with the structured fields of the government listing: `country`, `source`, `document_type`, `agency_names`, and the published-date bounds. Use portal search restricted to the government category only when the structured filters cannot express the request.
2. Retrieve the full record for each selected document and read `summary_source` first — it decides whether the summary can be reported at all. Take the issuing agency, type, and identifiers from `provenance` (`issuer`, `doc_type`, `doc_id`, `action`) and from `agency_names` / `document_number` / `document_type`, never from the summary text.
3. For recurring runs, combine newly published documents with the portal's change feed and the previously saved cursor so revised documents are not missed. Distinguish a new document from a revision of one already reported.
4. Report each document with its issuing agency, document type and number, new-or-revised status, who is affected, any comment deadline or effective date, and both the official source link and the portal link.

## `summary_source` decides what may be reported

- `official` — the summary is the agency's own abstract. Report it as the document's abstract.
- `llm` / `rss` / anything else — the summary is generated or feed-derived. Do not report it as the document's content.

A generated summary is not a substitute for the record's structured fields. Take the issuing agency, jurisdiction, type, and identifiers from `provenance` and the structured fields, and cross-check any agency named in summary text against `provenance.issuer` and `agency_names` before reporting it. When the two disagree, report the structured fields. Do not assume `summary_en` is an English translation.

When a document's substance is needed and `summary_source` is not `official`, say that the portal holds no usable text for it and point to the official URL, rather than restating the generated summary.

Preserve dates in the form the source uses. Japanese-era dates, comment deadlines, and effective dates must come from the official document rather than from a translated or generated restatement.

## Scope and attribution

Ignore `related_auto`, and treat `entities` on government records as an unverified signal; neither is a sound basis for selecting documents.

Persist a new change cursor only after the batch has been processed successfully. Follow each record's license and omission metadata, and always retain the official document URL alongside the portal URL.
