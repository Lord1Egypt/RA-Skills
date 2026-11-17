# Evidence package schema (local → cloud handoff)

**One file = one paper (V1.1 per-paper execution).** The Cloud template screens **one paper per
cloud task**, so every evidence file must contain exactly one paper's record. Each file keeps the
same shape the Cloud has already validated: a run-context block and a `papers` array holding
**exactly one** record. Never bundle multiple papers into one file — that reintroduces the
single-task timeout failure (StartToClose timeout on 20-paper single-row submissions).

- File naming: `handoff_p<record_id>.json` (e.g. `handoff_p001.json`).
- Every file carries the **same `run_context`** (identical copy) plus that paper's single record.
- The Cloud reads each row's `papers[0]`; record fields must carry explicit availability; never
  fabricate values.

## Serialization rules

- Compact JSON (no pretty-printing); keys in the fixed order shown in this document; stable byte
  encoding (`ensure_ascii=False`, UTF-8, no trailing whitespace) so the same record always
  serializes to identical bytes (reproducible rerun condition).
- A record with missing fields uses `""` / `false` / `[]` rather than omitting keys, per the
  available-data rules.
- **Record text defaults to English.** Fields the local agent writes (`available_content`,
  `available_evidence`, `missing_evidence`, `assessment_limitations`, `metadata_gate_notes`,
  notes) default to English, because the cloud template bound to this package is configured for
  English output. When the assignment or the user requires another language for those fields, use
  that language and record which one was used. Article content (abstract, full-text excerpts,
  structured info) always keeps its original language — never translate it.

## Run context block

```json
{
  "run_context": {
    "research_question": "...",
    "core_concepts": ["..."],
    "research_focus": "effect|impact|association|relationship|comparison|mechanism",
    "population": "...",
    "context": "..."
  }
}
```

These five keys are the run-context shape validated against the Cloud. Optional context such as
restrictions, assignment requirements, deadline, reading time, and citation count is passed to the
Cloud via the workbook fields (Assignment Requirements / Research Restrictions / etc.) — it does
not need to be repeated inside the evidence file (including it is harmless but not required).

## Paper record (papers[0] — exactly one per file)

```json
{
  "run_context": {
    "research_question": "...",
    "core_concepts": ["..."],
    "research_focus": "effect|impact|association|relationship|comparison|mechanism",
    "population": "...",
    "context": "..."
  },
  "papers": [
    {
      "record_id": "P001",
      "title": "...",
      "authors": "...",
      "publication_year": 2021,
      "source_journal_publisher": "...",
      "source_type": "peer-reviewed journal article",
      "doi": "...",
      "isbn": "",
      "url": "...",
      "database_record": "PMID: ...; PubMed",
      "abstract": "...",
      "available_content": {
        "full_text_available": true,
        "sections_available": ["introduction", "methods", "results", "discussion", "conclusion"],
        "methods_info": "...",
        "key_findings": "...",
        "results_info": "...",
        "conclusion": "..."
      },
      "links": ["https://doi.org/..."],
      "evidence_availability_level": "A",
      "available_evidence": "...",
      "missing_evidence": "...",
      "assessment_limitations": "...",
      "metadata_status": "VERIFIED",
      "metadata_gate_notes": "DOI resolved in Crossref; PMID matched in PubMed; all identifiers refer to the same publication."
    }
  ]
}
```

> The `run_context` block shown above is repeated identically in every per-paper file. The
> `papers` array holds exactly one record — this file's paper. (The standalone `run_context` block
> shown earlier is the shared copy every file embeds.)

> `metadata_status` is produced by the local **Metadata Validation Gate**
> (references/metadata-validation-gate.md) — `VERIFIED` or `PARTIALLY VERIFIED` only. For
> PARTIALLY VERIFIED records, mark each unverifiable identifier as `NOT VERIFIED` (e.g.
> `"doi": "NOT VERIFIED"`). Records that are `MISMATCH` / `INVALID` never reach this file. The
> Cloud ignores this field — it screens only the evidence content.

## Evidence Availability Level assignment

| Level | Package contains |
|---|---|
| A | Full text, or substantial full-paper content (Methods, Results, Discussion, Conclusion) |
| B | Abstract + substantial structured information |
| C | Title + metadata + Abstract |
| D | Title, authors, year, journal/publisher only |

Do not require full text for every paper. Paywalls, no open access, access restrictions, and PDF
retrieval failures are expected; they lower the level, never the paper's fate.
