# Output Contract for OpenClaw Self-Improve

This document specifies the exact structure and required sections for each output file in an improvement run.

## run-info.md

**Purpose**: Metadata about the run configuration and environment.

**Required Sections**:
- `# Run Info` (heading)
- `- Timestamp (UTC): <value>` (bullet)
- `- Mode: <value>` (bullet)
- `- Repo: <value>` (bullet)
- `- Objective: <value>` (bullet)
- `- Scope: <value>` (bullet)
- `- Validation Gate: <value>` (bullet)
- `- Git Commit: <value>` (bullet)
- `- Git Branch: <value>` (bullet)
- `- Is Git Repository: <value>` (bullet)
- `- Logging Enabled: <value>` (bullet)

**Valid Status Values**: N/A (informational only)

## baseline.md

**Purpose**: Starting state, metrics, and risk assessment before improvements.

**Required Sections**:
- `# Baseline` (heading)
- `## Objective` (heading)
- `## Scope` (heading)
- `## Repo State` (heading)
  - `- Commit: <value>` (bullet)
  - `- Branch: <value>` (bullet)
  - `- Is Git Repository: <value>` (bullet)
- `## Reproduction` (heading)
- `## Metrics` (heading)
- `## Risks` (heading)
- `## Status` (heading)
  - `- <status_value>` (bullet)

**Valid Status Values**: `pass`, `fail`, `blocked`, `inconclusive`

## hypotheses.md

**Purpose**: Ranked improvement hypotheses.

**Required Sections**:
- `# Hypotheses` (heading)
- `## Hypothesis 1` (heading)
- `## Hypothesis 2` (heading)
- `## Hypothesis 3` (heading)
- `## Ranking` (heading)

**Valid Status Values**: N/A (informational only)

## proposal.md

**Purpose**: Approval package with planned changes and rollback plan.

**Required Sections**:
- `# Proposal` (heading)
- `## Selected Hypothesis` (heading)
- `## Planned Changes` (heading)
- `## Files To Edit` (heading)
- `## Validation Gate` (heading)
- `## Rollback Plan` (heading)
- `## Approval Status` (heading)
  - `- <approval_status>` (bullet)

**Valid Approval Status Values**: `pending`, `approved`, `approved and implemented`, `rejected`, `blocked`

## validation.md

**Purpose**: Validation results and before/after comparison.

**Required Sections**:
- `# Validation` (heading)
- `## Commands Run` (heading)
- `## Results` (heading)
- `## Baseline vs New` (heading)
- `## Pass/Fail` (heading)
- `## Status` (heading)
  - `- <status_value>` (bullet)

**Valid Status Values**: `pass`, `fail`, `blocked`, `inconclusive`

## outcome.md

**Purpose**: Summary of changes, evidence, and next iteration.

**Required Sections**:
- `# Outcome` (heading)
- `## Summary` (heading)
- `## Evidence` (heading)
- `## Residual Risk` (heading)
- `## Next Iteration` (heading)
- `## Status` (heading)
  - `- <status_value>` (bullet)

**Valid Status Values**: `pass`, `fail`, `blocked`, `inconclusive`

## run.log (optional)

**Purpose**: Detailed execution log for debugging and audit trail.

**Format**:
```
================================================================================
OpenClaw Self-Improve Run Log
Started: <timestamp>
Run Directory: <path>
Mode: <mode>
Objective: <objective>
================================================================================

[TIMESTAMP] [LEVEL] Message
[TIMESTAMP] [LEVEL] Message
...

================================================================================
Run Initialization Completed: <timestamp>
================================================================================
```

**Valid Log Levels**: `INFO`, `WARN`, `ERROR`

## JSON Output Files

### run-info.json

**Purpose**: Machine-readable run metadata.

**Required Keys**:
- `timestamp_utc` (string)
- `mode` (string)
- `repo` (string)
- `objective` (string)
- `scope` (string)
- `validation_gate` (string)
- `git_commit` (string)
- `git_branch` (string)
- `generated_at_utc` (string)
- `artifacts` (object)
  - `markdown` (object)
    - `run_info` (string)
    - `baseline` (string)
    - `hypotheses` (string)
    - `proposal` (string)
    - `validation` (string)
    - `outcome` (string)
  - `json` (object)
    - `run_info` (string)
    - `summary` (string)

### summary.json

**Purpose**: High-level summary for CI/CD integration.

**Required Keys**:
- `run_dir` (string)
- `timestamp_utc` (string)
- `mode` (string)
- `objective` (string)
- `scope` (string)
- `approval_status` (string)
- `baseline_status` (string)
- `validation_status` (string)
- `outcome_status` (string)
- `selected_hypothesis` (string)
- `next_iteration` (string)
- `generated_at_utc` (string)

**Valid Status Values**: `pass`, `fail`, `blocked`, `inconclusive`
**Valid Approval Status Values**: `pending`, `approved`, `approved and implemented`, `rejected`, `blocked`

## Validation Rules

1. All required sections must be present in their respective files
2. Status values must be one of the valid values listed above
3. Timestamps must be in ISO 8601 format (YYYY-MM-DD HH:MM:SS UTC)
4. File paths must be absolute or relative to the run directory
5. JSON files must be valid JSON with proper formatting (2-space indentation)
6. All markdown files must use GitHub-flavored markdown syntax
