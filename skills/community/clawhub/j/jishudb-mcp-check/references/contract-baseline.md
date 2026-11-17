# Contract Baseline

- Skill version: `0.1.3`
- Target MCP contract: `jishudb-mcp-v2`
- Source artifact: `docs/contracts/jishudb-mcp-v2.json`
- Source contract digest:
  `709a2c7dd407c6303ef56b209dacd172e7e8c123bdc5492f578b610eb791544a`
- Expected `default` profile tools: `18` (or `19` with explicit preparation authority)
- Expected `jishudb` profile tools: `35` (or `36` with explicit preparation authority)

The digest identifies the repository contract used to design this Skill. The
running service may not expose a digest, so always compare visible tool names.
This revision adds runtime readiness and conditionally exposes bounded model
preparation. `kb_prepare_runtime` is optional and must be absent without explicit
onboarding preparation authority; ordinary read/write scope is insufficient. Record absent optional capabilities on
older deployments rather than assuming that a matching tool name supports them.

## Expected tools

```text
kb_list
kb_get_capabilities
kb_create
kb_get
kb_search
kb_upload
kb_prepare_upload
kb_list_documents
kb_get_document
kb_list_document_chunks
kb_read_document_text
kb_read_document_raw
kb_list_document_faq
kb_reindex_document
kb_import_url
kb_list_jobs
kb_get_job
kb_retry_job
kb_cancel_job
kb_read_handbook
kb_get_config
kb_delete_document
kb_delete_kb
kb_get_readiness
note_list
note_get
note_create
note_update
note_delete
note_link_to_kb
kb_update
kb_update_document
kb_get_job_trace
kb_list_sources
kb_sync_source
```

## Drift policy

- Contract name differs from `jishudb-mcp-v2`: stop with `FAIL`.
- A baseline tool is missing: stop with `FAIL`.
- `kb_prepare_runtime` is a conditional extension: require it only when capabilities
  advertise preparation authority. Do not fail an ordinary connection for its absence.
- New tools are present: test all known tools, list new tools as untested, and
  return no better than `PARTIAL`.
- A runtime-exposed digest differs: report the mismatch and return no better
  than `PARTIAL`, even when tool names are unchanged.
- Update this Skill version, test cases, expected counts, and digest whenever
  the accepted MCP contract changes.
