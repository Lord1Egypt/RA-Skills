# Per-Paper Output Layout

Prefer this layout for each paper inside the refreshed bundle:

```text
reports/
  per_paper/
    <paper-slug>/
      <paper-slug>_detailed_cn.md
      <paper-slug>_detailed_cn.pdf
generated/
  intermediate/
    <paper-slug>.json
generated/
  teaching/
    <paper-slug>/
      teaching_outline_cn.md
      slide_blueprint_cn.json
      qa_bank_cn.json
      role_play_discussion_pack_cn.md
generated/
  visuals/
    <paper-slug>/
      pages/
      visual_manifest.json
metadata/
  project_directory_index.json
```

For a session to be restartable from the next stage, the bundle should also carry:

- `metadata/delivery_bundle_manifest.json`
- `metadata/routing_status.json`
- `metadata/project_directory_index.json`
- `reports/project_directory_index.md`
- `reports/stage_delivery_handoff.md`
- `metadata/paper_batch_manifest.json`
- one per-paper `metadata/focus_specs/<paper-slug>.json` carrying the upstream `source_record` snapshot and upstream bundle context
- any review / rebuttal bundle needed by the paper

Teaching sidecars are optional derivatives. They must not replace `reports/per_paper/<paper-slug>/<paper-slug>_detailed_cn.md`, which remains the single authoritative report.
