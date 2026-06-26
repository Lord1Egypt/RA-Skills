# Backend Contract

The skill operates against a unified backend adapter contract. Each backend implementation or stub should expose the same conceptual methods.

## Adapter interface

- `check_prerequisites()`
  - Verify local tools, connectors, or configuration
- `authenticate()`
  - Guide or verify backend authentication
- `bootstrap_workspace(schema_manifest)`
  - Create the initial workspace structure
- `read_entities(query_spec)`
  - Read normalized entities from the backend
- `write_entities(change_set)`
  - Apply normalized writes to the backend
- `materialize_views(view_manifest)`
  - Create or refresh derived views
- `register_artifact(record)`
  - Record generated artifact metadata
- `describe_limitations()`
  - Return backend-specific support boundaries

## v1 adapter status

- `feishu_base_adapter`
  - fully implemented
- `notion_adapter_stub`
  - mapping + setup guidance only
- `obsidian_adapter_stub`
  - folder/template scaffolding guidance only

## Shared rules

- All writes should originate from the unified semantic model.
- All destructive operations should be previewed or clearly acknowledged.
- Existing backends must be inspected before migration.
- Artifact generation is downstream of structured data, not a substitute for it.
