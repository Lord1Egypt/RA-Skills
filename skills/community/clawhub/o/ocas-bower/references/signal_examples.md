# Bower Signal Emission Examples

Bower emits structured signals to See references/integration-notes.md for current backend architecture. for all entities and artifacts encountered during scans. Drive content is inherently user-owned — the user put it there, organized it, and chose to keep it — so all signals are emitted with `user_relevance: "user"`.

Signal files are written to the `signal` payload field in the journal entry. Bower writes signals during `bower.scan.deep` and `bower.scan.light` as entities are encountered. Duplicate signals for the same Drive artifact are deduplicated by `file_id`; Bower updates the existing signal rather than creating a new one when metadata changes (e.g., last modified date, sharing status).

## Signal types emitted

- **Thing/DigitalArtifact** — One signal per document, spreadsheet, presentation, PDF, image, or other file. Includes file type, MIME type, Drive path, last modified timestamp, sharing status, and content summary.
- **Entity/Person** — One signal per unique person encountered across shared-with metadata, document mentions, and collaborator lists. Deduplicated by email address.
- **Place** — One signal per location found in document content (travel itineraries, address lists, venue info, property documents).
- **Concept/Event** — One signal per event or project detected from document clusters (e.g., a folder of wedding documents, a project with multiple deliverables).
- **Concept/Idea** — One signal per theme or topic reflected by folder structure and document content patterns (e.g., sustained interest in cooking across recipe folders, research into home renovation).

## Signal schema examples

### Thing/DigitalArtifact signal

```json
{
  "id": "sig_{uuid7}",
  "source_skill": "ocas-bower",
  "source_type": "journal",
  "source_journal_type": null,
  "payload": {
    "proposed_type": "Thing",
    "thing_type": "DigitalArtifact",
    "name": "Q1 2026 Budget.xlsx",
    "metadata": "{\"file_id\": \"gdrive_abc123\", \"mime_type\": \"application/vnd.google-apps.spreadsheet\", \"path\": \"Finance/Budgets/\", \"last_modified\": \"2026-03-15T10:00:00Z\", \"shared_with\": [\"sarah@example.com\"]}"
  },
  "user_relevance": "user",
  "timestamp": "2026-03-17T10:00:04-07:00",
  "status": "active"
}
```

### Entity/Person signal

```json
{
  "id": "sig_{uuid7}",
  "source_skill": "ocas-bower",
  "source_type": "journal",
  "source_journal_type": null,
  "payload": {
    "proposed_type": "Entity",
    "thing_type": "Person",
    "name": "Sarah Chen",
    "metadata": "{\"email\": \"sarah@example.com\", \"relationship\": \"collaborator\", \"shared_files_count\": 12, \"domains\": [\"Finance\", \"Projects\"], \"last_seen\": \"2026-03-15T10:00:00Z\"}"
  },
  "user_relevance": "user",
  "timestamp": "2026-03-17T10:00:04-07:00",
  "status": "active"
}
```

### Place signal

```json
{
  "id": "sig_{uuid7}",
  "source_skill": "ocas-bower",
  "source_type": "journal",
  "source_journal_type": null,
  "payload": {
    "proposed_type": "Place",
    "thing_type": null,
    "name": "Portland Convention Center",
    "metadata": "{\"source_file\": \"gdrive_def456\", \"source_path\": \"Travel/Conferences/\", \"context\": \"venue for PyCon 2026\", \"address\": \"777 NE MLK Jr Blvd, Portland, OR 97232\"}"
  },
  "user_relevance": "user",
  "timestamp": "2026-03-17T10:00:04-07:00",
  "status": "active"
}
```

### Concept/Event signal

```json
{
  "id": "sig_{uuid7}",
  "source_skill": "ocas-bower",
  "source_type": "journal",
  "source_journal_type": null,
  "payload": {
    "proposed_type": "Concept",
    "thing_type": "Event",
    "name": "Kitchen Renovation 2026",
    "metadata": "{\"source_files\": [\"gdrive_ghi789\", \"gdrive_jkl012\"], \"source_path\": \"Home/Renovation/Kitchen/\", \"file_count\": 8, \"date_range\": \"2026-01 to 2026-03\"}"
  },
  "user_relevance": "user",
  "timestamp": "2026-03-17T10:00:04-07:00",
  "status": "active"
}
```

### Concept/Idea signal

```json
{
  "id": "sig_{uuid7}",
  "source_skill": "ocas-bower",
  "source_type": "journal",
  "source_journal_type": null,
  "payload": {
    "proposed_type": "Concept",
    "thing_type": "Idea",
    "name": "Machine Learning",
    "metadata": "{\"evidence_folders\": [\"Projects/ML-Research/\", \"Education/Coursera/\", \"Projects/DataPipeline/\"], \"evidence_file_count\": 34, \"domains\": [\"Projects\", \"Education\"], \"first_seen\": \"2025-06-12T00:00:00Z\"}"
  },
  "user_relevance": "user",
  "timestamp": "2026-03-17T10:00:04-07:00",
  "status": "active"
}
```
