---
plan_id: preference-scan
name: Preference Scan
version: 1.0.0
description: Ingest recent activity → extract consumption signals → update preference model. Run weekly or after a period of high consumption activity.
parameters:
  lookback_days:
    type: number
    required: false
    default: 7
    description: Number of days of activity to ingest.
steps:
  - id: ingest-activity
    name: Ingest Recent Activity
    skill: ocas-taste
    command: taste.scan
    on_failure: abort
  - id: extract-signals
    name: Extract Consumption Signals
    skill: ocas-taste
    command: taste.ingest.signal
    on_failure: abort
  - id: update-model
    name: Update Preference Model
    skill: ocas-taste
    command: taste.model.status
    on_failure: skip
---

## Step 1: ingest-activity

**Skill:** ocas-taste
**Command:** taste.scan

**Inputs:**
- `lookback_days`: `{{params.lookback_days}}`

**Outputs:**
- `activity_count`: number of activity events ingested

**On failure:** abort

---

## Step 2: extract-signals

**Skill:** ocas-taste
**Command:** taste.ingest.signal

**Inputs:**
- `source`: recent_activity

**Outputs:**
- `signal_count`: number of ConsumptionSignals extracted

**On failure:** abort

---

## Step 3: update-model

**Skill:** ocas-taste
**Command:** taste.model.status

**Inputs:**
- `signal_count`: `{{steps.extract-signals.signal_count}}`

**Outputs:**
- `model_updated`: boolean

**On failure:** skip
**Notes:** Returns current model state after ingestion. Model update is automatic when signals are ingested.