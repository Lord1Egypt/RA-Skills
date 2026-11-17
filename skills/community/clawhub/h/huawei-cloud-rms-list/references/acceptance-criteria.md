# Acceptance Criteria — huawei-cloud-rms-list

Mapped to Issue #135.

- [x] Skill follows the Huawei Cloud Skill Specification (SKILL.md + scripts +
      references + templates).
- [x] Calls the RMS query interfaces by region / provider / resource type:
      `ListAllResources`, `ListResources`, `ListProviders`, `ListRegions`.
- [x] Pagination is complete: `marker`/`next_marker` for resources, `offset`/
      `total_count` for ListProviders; auto-paged up to a configurable max.
- [x] Output includes the key fields `resource_id` (`id`), `name`, `type`,
      `region_id` (plus provider / enterprise project / state / timestamps), with
      table / Markdown / JSON / CSV renderers.
- [x] Credential loading is consistent with the repository's other skills
      (AK/SK + SecurityToken + region via the hcloud profile or whitelisted SDK
      environment variables); no hardcoded secrets.
- [x] Runnable example commands and explicit error handling are documented
      (`--help` supported via argparse).
- [x] Strictly read-only: a write-intent guard rejects mutating intents before
      any command runs; the export file is written locally only.

## Out of scope

- Creating / deleting / modifying resources.
- RMS config aggregators, trackers, conformance packs, policy assignments.
- Writing the inventory back to any cloud service.
