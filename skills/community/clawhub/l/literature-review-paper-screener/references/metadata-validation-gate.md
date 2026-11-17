# Metadata Validation Gate — V1 (local, authoritative identity check)

> Scope: an independent quality gate between local **evidence collection** and the **handoff**
> stage. It validates only **bibliographic identity** — it never touches search logic, screening
> logic (CRAAP, Topic Relevance, Reading Role, Priority), the Cloud DAG, or workbook batching.
> Runs entirely on the Local Agent (internet-enabled); the Cloud never validates metadata.
>
> Core principle: **a correct summary does not prove that the citation metadata is correct.**
> Evidence content and bibliographic identity are validated separately.

## STEP — Metadata Authority Validation

Before any literature record is written into the per-paper handoff record
(`handoff_p<record_id>.json`), validate its bibliographic metadata against authoritative
sources. This validation applies independently to every literature record.

### 1. Required Metadata Fields

Validate, when available:

- Title
- Author(s)
- Publication Year
- Journal / Source
- Volume
- Issue
- Pages / Article Number
- DOI
- PMID

### 2. Source Priority

Use authoritative bibliographic databases only. Validation priority:

1. **PubMed** — for PMID and biomedical literature metadata
2. **Crossref** — for DOI and publication metadata

Do not treat search snippets, AI-generated citations, publisher snippets, or previously
collected metadata as authoritative verification.

### 3. Validation Rules

For each record:

#### DOI Validation

If a DOI is provided:

- Verify that the DOI resolves or is found in Crossref.
- Confirm that the Crossref record refers to the same publication.
- Compare at minimum: **Title, Publication Year, Journal, Author(s)**.

If the DOI refers to a different publication or cannot be verified:
`DOI_STATUS = INVALID` — the DOI must not be included as verified metadata.

#### PMID Validation

If a PMID is provided:

- Verify the PMID against PubMed.
- Confirm that the PubMed record refers to the same publication.
- Compare at minimum: **Title, Publication Year, Journal, Author(s)**.

If the PMID refers to a different publication:
`PMID_STATUS = MISMATCH` — the PMID must not be included in the final record.

### 4. Cross-Field Consistency Check

A literature record must not combine metadata from different publications.

The following identifiers must refer to the same publication:

- Title
- DOI
- PMID
- Journal
- Publication Year

If any identifier belongs to a different publication, the record's `metadata_status` is
`MISMATCH` — do not attempt to guess which field is correct. Return the record to the evidence
collection stage for re-verification.

### 5. Validation Outcome

Each record receives one of three statuses:

#### VERIFIED

All available identifiers match the same publication → record may enter the handoff file.

#### PARTIALLY VERIFIED

The publication is confirmed, but one identifier is unavailable or cannot be verified.
Example: Title and PMID confirmed, DOI unavailable → record may enter the handoff file, but
the unavailable field must be explicitly marked: `DOI = NOT VERIFIED`. Do not invent or
infer a replacement.

#### MISMATCH / INVALID

Any DOI, PMID, or core bibliographic field refers to another publication → record must NOT
enter the handoff file. Return the record for re-collection.

### 6. No-Inference Rule

Never construct, infer, or guess bibliographic metadata. Do not:

- Guess a DOI from a title
- Copy a DOI from a similar paper
- Assume a PMID belongs to a paper because the topic is similar
- Combine a verified PMID with an unverified journal citation
- Repair metadata using semantic similarity alone

Bibliographic identity requires authoritative source confirmation.

### 7. Outcome rule — which records may proceed

Only records whose `metadata_status` is `VERIFIED` **or** `PARTIALLY VERIFIED` may proceed to
the next stage. Records marked `MISMATCH` or `INVALID` must be blocked before:

- the handoff file
- Cloud upload
- Screening
- Final user delivery

---

## Implementation notes (Local Agent)

1. **Where it runs:** after evidence collection (Skill step 5), before writing each
   `handoff_p<record_id>.json` (step 6). One gate pass per unique candidate.
2. **Record in the handoff record:** add
   `"metadata_status": "VERIFIED" | "PARTIALLY VERIFIED" | "UNCONFIRMED"` and, for partially
   verified or unconfirmed records, mark the unverified identifiers explicitly (e.g.
   `"doi": "NOT VERIFIED"`). **Status semantics (do not conflate):**
   - `VERIFIED` — identity confirmed against an authoritative source (DOI/PMID resolved).
   - `PARTIALLY VERIFIED` — some identifiers confirmed, others not; the record is real but
     incomplete. Allowed into handoff **only** with the unverified identifiers marked.
   - `UNCONFIRMED` — **no authoritative confirmation of the publication's existence/identity**
     could be obtained at all (e.g. unindexed preprint, hallucination risk). These records are
     **excluded from automated handoff and cloud screening** and surfaced to the owner for a
     decision. Never label an unconfirmed record `PARTIALLY VERIFIED` to let it through.
3. **Outcome ledger:** keep a short per-run gate ledger (record_id → status → evidence checked)
   so the final delivery can state how many records passed the gate.
4. **MISMATCH/INVALID handling:** return to evidence collection for re-verification of that
   record; do not silently drop it (available-data principle). If re-verification cannot
   resolve identity, surface it to the owner with the conflicting values — never guess. The
   owner decides keep/drop; a dropped record is excluded from handoff with the reason recorded.
5. **Records with no DOI/PMID:** the publication may still be confirmed via authoritative
   title(+author+year) lookup in Crossref/PubMed. If no authoritative confirmation can be
   obtained at all (e.g. very new preprints, niche publications not indexed by either database):
   **do not mark VERIFIED and do not mark PARTIALLY VERIFIED** — mark `UNCONFIRMED`, keep the
   record (never silently drop valid literature), **exclude it from automated handoff and cloud
   screening**, and surface it to the owner in the gate ledger and delivery summary for an
   explicit keep/drop decision. Owner decision overrides per record, and a kept UNCONFIRMED record
   is only sent to the cloud if the owner explicitly approves it after being shown the risk.
6. **Gate ledger:** record per run: record_id → status → identifiers checked → outcome notes.
   The delivery summary states how many records passed, how many were blocked, and how many
   await owner decision.