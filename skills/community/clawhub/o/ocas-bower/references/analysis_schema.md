# Analysis Schema

Canonical data formats for Bower's structural model, proposals, and log records.

---

## Folder index (folder_index.json)

Written during Phase 1 (tree discovery) of `bower.scan.deep`. Contains the full folder tree with metadata and permissions — no file records. Small even for large Drives because folder count is a fraction of file count.

```json
{
  "scan_id": "string -- unique identifier (scan_{hash})",
  "discovered_at": "string -- ISO 8601",
  "folder_count": "number",
  "root_folders": ["string -- Drive folder IDs at depth 1"],
  "taxonomy": {
    "labels": ["string -- inferred category labels from folder names"],
    "depth_distribution": {"1": 0, "2": 0, "3": 0, "4+": 0}
  },
  "folders": {
    "FOLDER_ID": {
      "name": "string",
      "path": "string",
      "depth": "number",
      "parent_id": "string|null -- null for root-level folders",
      "child_folder_count": "number -- direct child folders",
      "effective_permissions": [
        {
          "emailAddress": "string|null",
          "domain": "string|null",
          "type": "string -- user|group|domain|anyone",
          "role": "string -- reader|commenter|writer|owner"
        }
      ]
    }
  }
}
```

---

## Folder scan (scans/{folder_id}.json)

One file per top-level folder tree, written during Phase 2 (folder scanning) of `bower.scan.deep`. Contains all file records for that folder and its descendants. Each file is small enough to write atomically and hold in memory independently.

```json
{
  "folder_id": "string -- top-level folder ID this scan covers",
  "folder_path": "string -- full path of the folder",
  "scan_id": "string -- parent scan ID from scan_progress.json",
  "scanned_at": "string -- ISO 8601",
  "file_count": "number",
  "content_read_count": "number",
  "content_skip_count": "number",
  "files": [
    {
      "id": "string -- Drive file ID",
      "name": "string",
      "mimeType": "string",
      "parent_id": "string -- immediate parent folder ID",
      "parent_path": "string -- full path string for readability",
      "depth": "number -- 1 = root level",
      "modifiedTime": "string -- ISO 8601",
      "starred": "boolean",
      "size": "number|null -- bytes",
      "is_folder": "boolean",
      "content_summary": "string|null -- 150-word max extract of apparent document type, topic, and named entities. null if unreadable, skipped, or a folder",
      "content_read": "boolean -- true if content was successfully read during this scan",
      "existing_description": "string|null -- current Drive description field value at time of scan",
      "proposed_description": "string|null -- Bower-generated description (50-120 words). null if file is unreadable or a folder",
      "permissions": [
        {
          "emailAddress": "string|null -- null for domain or anyone grants",
          "domain": "string|null",
          "type": "string -- user|group|domain|anyone",
          "role": "string -- reader|commenter|writer|owner",
          "inherited": "boolean -- true if inherited from an ancestor folder"
        }
      ]
    }
  ]
}
```

Files at the Drive root (no parent folder) are collected in a special scan file: `scans/_root.json`.

---

## Drive digest (drive_digest.json)

Lightweight summary of the Drive's organizational state, updated incrementally after each folder scan. Small enough to hold in memory. Contains no individual file records — only per-folder statistics and Drive-wide aggregates. See `organization_rules.md` for the full specification of what the digest captures and how analysis uses it.

```json
{
  "scan_id": "string",
  "last_updated": "string -- ISO 8601",
  "scan_coverage": "number -- 0.0 to 1.0, fraction of top-level folders scanned",
  "total_files": "number",
  "total_folders": "number",
  "median_depth": "number",
  "median_files_per_folder": "number",
  "dominant_naming": "string|null",
  "dominant_date_convention": "string|null",
  "domains_detected": [
    {
      "domain": "string",
      "root_path": "string",
      "mode": "string -- prescriptive|descriptive",
      "confidence": "string -- high|med|low"
    }
  ],
  "sacred_folders": ["string -- folder IDs"],
  "root_level_file_count": "number",
  "stale_staging_count": "number",
  "description_coverage": "number -- 0.0 to 1.0",
  "cross_folder_patterns": [
    {
      "pattern": "string -- human-readable description",
      "folders": ["string -- folder IDs"],
      "count": "number|null"
    }
  ],
  "folder_stats": {
    "FOLDER_ID": {
      "path": "string",
      "depth": "number",
      "file_count": "number",
      "subfolder_count": "number",
      "last_modified": "string -- ISO 8601",
      "mime_type_distribution": {"string": "number"},
      "naming_pattern": "string|null",
      "date_convention": "string|null",
      "detected_domain": "string|null",
      "domain_confidence": "string|null",
      "has_year_subfolders": "boolean",
      "sacred": "boolean",
      "outlier_count": "number",
      "root_files_count": "number"
    }
  }
}
```

The digest is updated after each folder scan — never rebuilt from scratch. Each folder's contribution (file counts, naming patterns, domain signals) is merged into the running totals and per-folder stats. Drive-wide aggregates (medians, dominant patterns, cross-folder patterns) are recalculated from the per-folder stats after each merge.

---

## Proposal record (proposals.jsonl)

One record per proposal, appended by `bower.analyze`.

```json
{
  "proposal_id": "string -- unique identifier (p_{hash})",
  "generated_at": "string -- ISO 8601",
  "scan_id": "string -- source scan that generated this proposal",
  "proposal_type": "string -- move|rename|create_folder|describe_overwrite",
  "source_id": "string -- Drive file/folder ID",
  "source_path": "string -- full path at time of scan",
  "source_name": "string -- current filename at time of scan (for rename proposals)",
  "destination_id": "string|null -- target parent folder ID (null for create_folder, rename, describe_overwrite)",
  "destination_path": "string -- full destination path (same as source_path for rename and describe_overwrite)",
  "new_name": "string|null -- proposed filename for rename proposals only",
  "previous_value": "string|null -- existing description at proposal generation time (for describe_overwrite proposals)",
  "proposed_description": "string|null -- proposed Drive description (for describe_overwrite proposals)",
  "outlier_class": "string -- location|content_mismatch|depth|name_inconsistency|stale_staging|duplicate_candidate|poor_name|missing_description|weak_description|domain_prescriptive|domain_descriptive",
  "domain": "string|null -- domain name if this proposal was generated by domain logic",
  "confidence_tier": "string -- high|med|low",
  "content_signal": "boolean -- true if content summary contributed to this proposal",
  "auto_approved": "boolean -- true if approved automatically via pattern promotion",
  "pattern_key": "string|null -- pattern key used for auto-approval or feedback suppression",
  "reasoning": "string -- one to three sentences explaining the proposal",
  "status": "string -- pending|approved|executed|failed|skipped|expired",
  "skip_reason": "string|null -- source_moved|description_changed|cap_exceeded or null",
  "approved_at": "string|null -- ISO 8601",
  "executed_at": "string|null -- ISO 8601",
  "expires_at": "string -- ISO 8601 -- proposal auto-expires if not approved by this date",
  "error": "string|null -- error message if status is failed"
}
```

---

## Move log record (move_log.jsonl)

One record per successfully executed operation, appended by `bower.apply`.

```json
{
  "log_id": "string -- unique identifier (mvl_{hash})",
  "proposal_id": "string|null -- null for auto-writes",
  "executed_at": "string -- ISO 8601",
  "file_id": "string -- Drive file ID",
  "file_name": "string",
  "source_path": "string",
  "destination_path": "string",
  "operation": "string -- move|rename|create_folder|describe_auto|describe_overwrite",
  "previous_value": "string|null -- previous filename (rename), previous description (describe_*), or null (move/create)"
}
```

---

## Undo log record (undo_log.jsonl)

One record per successfully executed undo, appended by `bower.undo`.

```json
{
  "undo_id": "string -- unique identifier (undo_{hash})",
  "original_log_id": "string -- mvl_ record this undo reverses",
  "executed_at": "string -- ISO 8601",
  "file_id": "string -- Drive file ID",
  "file_name": "string",
  "restored_from_path": "string -- where the file was when undo ran",
  "restored_to_path": "string -- original source_path from the move log",
  "operation": "string -- move|rename|describe_auto|describe_overwrite -- mirrors the original operation being reversed",
  "error": "string|null"
}
```

---

## Scan event record (scan_events.jsonl)

One record per scan run.

```json
{
  "event_id": "string -- evt_{hash}",
  "scan_id": "string",
  "scan_type": "string -- deep|light",
  "started_at": "string -- ISO 8601",
  "completed_at": "string -- ISO 8601",
  "file_count": "number",
  "folder_count": "number",
  "content_read_count": "number -- files whose content was successfully read",
  "content_skip_count": "number -- files skipped for content reading",
  "description_proposed_count": "number -- files for which a proposed_description was generated",
  "checkpoint_id": "string|null -- last saved checkpoint ID if scan was resumed, null if clean start",
  "drift_rate": "number|null -- fraction of sampled files found at a different location than the structural model. null for deep scans",
  "abort_reason": "string|null -- drift_threshold_exceeded|interrupted or null",
  "error": "string|null"
}
```

---

## Analysis event record (analysis_events.jsonl)

One record per `bower.analyze` run.

```json
{
  "event_id": "string -- evt_{hash}",
  "scan_id": "string -- scan this analysis is based on",
  "analyzed_at": "string -- ISO 8601",
  "outliers_found": "number",
  "proposals_generated": "number",
  "proposals_by_tier": {"high": 0, "med": 0, "low": 0},
  "proposals_by_type": {"move": 0, "rename": 0, "create_folder": 0, "describe_overwrite": 0},
  "domain_proposals_count": "number -- proposals generated by domain-specific logic",
  "auto_approved_count": "number -- proposals auto-approved via pattern promotion",
  "domains_active": ["string -- domain names that contributed proposals this run"],
  "domain_candidates": ["string -- unknown domain patterns flagged for user acknowledgment"],
  "describe_auto_queued": "number -- files queued for auto-write (empty description, no approval needed)",
  "skipped_duplicates": "number -- proposals skipped due to deduplication",
  "suppressed_by_feedback_count": "number -- proposals suppressed due to feedback patterns",
  "recalibration_adjustments": "object -- outlier classes adjusted this run and direction: {class: 'downgraded'|'suppressed'|'eligible_for_promotion'}",
  "expired_count": "number -- pending proposals marked expired this run",
  "content_influenced_count": "number -- proposals where content signal contributed",
  "permission_blocked_count": "number -- moves suppressed due to permission change risk",
  "permissions_available": "boolean -- false if Drive permission data was unavailable; all moves suppressed when false"
}
```

---

## Preference profile (preference_profile.json)

Written by `bower.scan.deep`. Reconciled (not overwritten) on each subsequent deep scan -- locked fields are preserved. User-editable.

```json
{
  "generated_at": "string -- ISO 8601",
  "scan_id": "string -- scan that last updated this profile",
  "naming": {
    "date_format": "string|null -- YYYY-MM-DD|YYYY-Q#|MM-YYYY|none",
    "date_position": "string|null -- prefix|suffix|none",
    "capitalization": "string|null -- title|lower|upper|mixed",
    "separator": "string|null -- space|hyphen|underscore|mixed",
    "locked": "boolean"
  },
  "depth_preference": {
    "median_depth": "number",
    "prefer_fine_grained": "boolean -- true if avg files/folder < 10",
    "locked": "boolean"
  },
  "sacred_folders": [
    {
      "folder_id": "string",
      "folder_path": "string",
      "reason": "string -- unchanged_90_days|user_locked",
      "locked": "boolean"
    }
  ],
  "domains_detected": [
    {
      "domain": "string -- taxes|projects|home|finance|legal|medical|archive|education",
      "root_folder_id": "string",
      "root_folder_path": "string",
      "mode": "string -- prescriptive|descriptive",
      "locked": "boolean"
    }
  ],
  "auto_approved_patterns": [
    {
      "pattern_key": "string",
      "promoted_at": "string -- ISO 8601",
      "confidence": "string -- med|high",
      "execution_count": "number",
      "undo_count": "number",
      "supporting_proposal_ids": ["string"],
      "locked": "boolean"
    }
  ],
  "class_precision": {
    "location": "number",
    "content_mismatch": "number",
    "depth": "number",
    "name_inconsistency": "number",
    "stale_staging": "number",
    "duplicate_candidate": "number",
    "poor_name": "number",
    "domain_prescriptive": "number",
    "domain_descriptive": "number"
  },
  "suppressed_classes": ["string -- outlier classes currently suppressed due to low precision"]
}
```

---

Extends ConfigBase from spec-ocas-shared-schemas.md.

```json
{
  "skill_id": "ocas-bower",
  "skill_version": "1.0.0",
  "config_version": "2",
  "created_at": "string -- ISO 8601",
  "updated_at": "string -- ISO 8601",
  "drive_root": "root",
  "scan_schedule_light": "0 2 * * *",
  "scan_schedule_deep": "0 1 * * 0",
  "timezone": "America/Los_Angeles",
  "auto_approve_tiers": [],
  "forbidden_parent_ids": [],
  "proposal_expiry_days": 14,
  "apply_cap": 25,
  "describe_auto_cap": 50,
  "drift_abort_threshold": 0.15,
  "content_read_max_mb": 5,
  "quiet_mode": false,
  "founding_run_complete": false,
  "arrival_detection_enabled": true,
  "health_score_history_weeks": 8,
  "retention": {
    "days": 365,
    "max_records": 10000
  }
}
```

`auto_approve_tiers` defaults to empty (no auto-approval). Set to `["high"]` only after the user explicitly authorizes it.

`forbidden_parent_ids` is an explicit list of Drive folder IDs Bower must never move files into or out of. User-configurable.

---

## Feedback log record (feedback_log.jsonl)

One record per user undo or explicit rejection, appended by `bower.undo` and `bower.proposals.reject`.

```json
{
  "feedback_id": "string -- unique identifier (fb_{hash})",
  "timestamp": "string -- ISO 8601",
  "feedback_type": "string -- undo|reject",
  "proposal_id": "string -- the proposal being reversed or rejected",
  "proposal_type": "string -- move|rename|describe_overwrite",
  "outlier_class": "string -- the outlier class that generated the proposal",
  "source_path": "string",
  "destination_path": "string",
  "folder_context": "string -- parent folder path of the file at time of feedback",
  "pattern_key": "string -- composite key used for suppression: '{outlier_class}:{source_folder_label}:{destination_folder_label}'"
}
```

Bower reads `feedback_log.jsonl` at the start of every `bower.analyze` run to build a suppression map. See organization_rules.md for suppression logic.

---

## Scan progress (scan_progress.json)

Tracks the state of an in-progress or completed deep scan. Updated after each folder completes. Enables resume across sessions — kill the process at any point and nothing is lost.

```json
{
  "scan_id": "string -- unique identifier (scan_{hash})",
  "started_at": "string -- ISO 8601",
  "phase": "string -- tree_discovery|folder_scanning|complete",
  "total_folders": "number -- count of top-level folders to scan",
  "scanned_folders": ["string -- folder IDs that have been fully scanned"],
  "pending_folders": ["string -- folder IDs not yet scanned"],
  "current_folder": "string|null -- folder ID currently being scanned, null if between folders",
  "current_folder_page_token": "string|null -- Drive API page token for resuming within a large folder",
  "total_files_scanned": "number -- running total across all folders",
  "last_checkpoint_at": "string -- ISO 8601"
}
```

On `bower.scan.deep` start:
1. Check for existing `scan_progress.json`.
2. If found with `phase != complete` and `started_at` less than 7 days ago: resume from `current_folder` or next `pending_folders` entry.
3. If found but older than 7 days: delete all `scans/*.json` and start fresh.
4. If not found: start fresh with Phase 1 (tree discovery).

On successful completion of all folders: set `phase: complete`. Do not delete `scan_progress.json` — it records when the last full scan finished.


## Drive health snapshot (health_history.jsonl)

One record appended per Sunday deep scan.

```json
{
  "snapshot_id": "string -- unique identifier (hs_{hash})",
  "recorded_at": "string -- ISO 8601",
  "scan_id": "string",
  "health_score": "number -- 0 to 100",
  "score_components": {
    "outlier_density": "number -- fraction of files that are outliers (lower is better)",
    "description_coverage": "number -- fraction of readable files with a non-empty description",
    "domain_structure_completeness": "number -- average completeness across detected domains",
    "naming_consistency": "number -- fraction of files following dominant naming convention",
    "stale_staging_fraction": "number -- fraction of files in staging folders 30+ days"
  },
  "files_organized_since_last": "number -- moves + renames executed since previous snapshot",
  "active_patterns": "number -- auto-approved pattern count",
  "domains_active": ["string"],
  "suppressed_classes": ["string"]
}
```

Health score formula: `100 - (outlier_density * 40) - ((1 - description_coverage) * 20) - ((1 - domain_structure_completeness) * 20) - ((1 - naming_consistency) * 10) - (stale_staging_fraction * 10)`. Clamp to 0-100.
