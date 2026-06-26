# iMA Integration

## Integrity First

This package does not assume that `iMA` exposes an official API, MCP server, or CLI. Do not invent one. The skill should support `iMA` through honest, replaceable adapters.

## Supported Adapter Modes

### 1. iMA Export Folder Mode

Use this mode when the user exports materials from iMA into a local folder.

Recommended folder pattern:

```text
research_corpus/
├── literature/
├── notes/
├── observations/
├── interviews/
├── questionnaires/
├── policy/
└── manifest.md
```

Supported file types:

- `md`
- `txt`
- `pdf`
- `docx`
- exported article text

Recommended manifest fields:

| Field | Meaning |
| --- | --- |
| `source_id` | stable local ID such as `A01` or `D03` |
| `file_name` | local file name |
| `source_type` | article, dissertation, note, observation, interview, policy, etc. |
| `origin` | iMA export, local note, WeChat export, meeting record, and so on |
| `verification_status` | `已核验`, `部分核验`, `待核验` |
| `notes` | short description or retrieval reminder |

### 2. Local Research Corpus Mode

Use this when the user already keeps a folder such as `research_corpus/` outside iMA.

Recommended workflow:

1. Inventory files by subfolder.
2. Group by evidence class.
3. Extract working notes or source IDs.
4. Build the evidence chain table before synthesis.

### 3. Future API, MCP, Or CLI Adapter Mode

If iMA later exposes a verifiable integration surface, add a separate adapter note such as:

- `connectors/ima_adapter.md`
- `scripts/ingest_ima_export.py`
- `references/ima_api_notes.md`

Until then, any integration claim must stay conditional and clearly labeled as future work.

## File Handling Guidance

| File type | Handling suggestion |
| --- | --- |
| `md`, `txt` | read directly and preserve headings, note IDs, and dates |
| `pdf` | extract cautiously; if OCR or page structure is unreliable, mark key claims `待核验` |
| `docx` | extract text carefully and preserve section titles if possible |
| exported public articles | classify as `D` unless independently verified as academic publications |
| observation or interview records | preserve speaker or event context and anonymize if required |

## Safe Default Behavior

When the runtime cannot reliably read a format:

1. state the limitation
2. ask for export to `md` or `txt`, or
3. request a manually prepared excerpt

This is better than pretending the source was fully read.

## Suggested Source Register

Use a compact table like this during ingestion:

| Source ID | File | Class | Topic | Verification | Key usable content |
| --- | --- | --- | --- | --- | --- |
| A01 | | | | | |
| B01 | | | | | |
| D01 | | | | | |

## Notes For Future Integrators

- Keep adapter logic swappable.
- Keep the evidence hierarchy outside the adapter so trust rules do not depend on the transport layer.
- Separate ingestion from synthesis.
- Never let an integration script silently assign academic status to unknown materials.
