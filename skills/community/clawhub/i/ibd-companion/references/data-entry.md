# Data entry workflow

This guide describes how an agent should map confirmed source material to the
local database. It is a recordkeeping model, not medical advice.

## One source fact, one home

| Confirmed information | Store it in |
| --- | --- |
| Stable disease type, earliest symptom date, and diagnosis-record link | `disease_profile` |
| One actual infusion | `injections` |
| One actual blood draw, visit, procedure, or imaging appointment | `checkups` |
| One atomic value from that checkup | `checkup_results` |
| A metric's immutable definition | `metric_definitions` |
| Narrative report wording or a private attachment reference | `checkup_reports` |
| A clinician's explicitly confirmed conclusion | `checkup_assessments` |
| One large-review parent and its child checkups | `review_episodes` + `review_components` |
| Daily symptoms | `symptom_logs` |
| Food, sleep, stress, or other possible factors | `factor_terms` + `factor_logs` |

Do not duplicate one blood draw because it serves two contexts. Create one
`checkups(kind='lab')` row, then link it to an infusion and/or review as needed.

## Lab-report workflow

1. Confirm the source report and create or locate the one corresponding `lab`
   checkup.
2. Complete that checkup only when the actual draw/completion time is known.
3. For every value to retain, use an existing metric or explicitly register a
   new one first.
4. Add each result to the same checkup, preserving the report's actual unit,
   reference range, abnormal flag, and any relevant source note.
5. Keep narrative findings in a versioned `checkup_reports` row rather than
   turning them into model-generated conclusions.

## Custom metrics

Use `metric-add` only after the user explicitly adopts a metric from an actual
report or care plan:

```bash
python3 scripts/ibd_db.py metric-add \
  --code infliximab_level \
  --name "Infliximab level" \
  --value-type numeric \
  --default-unit "μg/mL"
```

- `code` must be stable lowercase `snake_case`; it is never renamed.
- Use `numeric` for a measured number and `qualitative` for a text result.
- `default_unit` is optional and is only a data-entry hint; do not convert or
  overwrite the actual unit reported by a laboratory.
- Do not invent reference ranges or abnormal flags. Store only those present
  on the report.
- If a metric is no longer wanted, use `metric-deactivate --code <code>`.
  Historical results remain intact and the metric cannot be used for new
  result entries.

## Review and assessment workflow

Create a `review_episodes` parent for a multi-test large review. Link each
actual lab, endoscopy, imaging, pathology, or visit checkup to it. Record a
clinician assessment only on its completed, assessment-bearing checkup and
only from explicit confirmed wording. Symptoms, metric values, and agent
interpretation must never create an assessment automatically.
