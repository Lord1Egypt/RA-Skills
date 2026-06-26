# Sources Zip Layout

Use a single zip bundle with folders like:

- `papers/main/`
- `reviews/openreview/`
- `supplementary/`
- `generated/visuals/`
- `generated/intermediate/`
- `generated/teaching/`
- `generated/routing/`
- `reports/per_paper/`
- `reports/stage_delivery_handoff.md`
- `metadata/delivery_bundle_manifest.json`
- `metadata/routing_status.json`
- `metadata/project_directory_annotations.json`
- `metadata/project_directory_index.json`
- `metadata/paper_batch_manifest.json`
- `reports/project_directory_index.md`

If ChatGPT needs page images or visual manifests, put them under `generated/visuals/`.

Prefer one detailed report per paper under `reports/per_paper/<paper-slug>/`.

For a fresh session to continue from this bundle alone, also keep:

- one per-paper `metadata/source_record.json` snapshot or the equivalent `metadata/focus_specs/<paper-slug>.json`
- `reports/stage_delivery_handoff.md`
- `metadata/delivery_bundle_manifest.json`
- `metadata/routing_status.json`
- `metadata/project_directory_index.json`
- `reports/project_directory_index.md`

The next stage should read those files before scanning the tree ad hoc.

Teaching materials under `generated/teaching/` are derivative sidecars for explanation, Q&A, role-play discussion, and slide blueprints. They must point back to the authoritative detailed report.
