# OpenClaw UX Ethnography Report - {{report_date}}

## Executive Summary

- {{summary_line_1}}
- {{summary_line_2}}
- {{summary_line_3}}

## Study Window

- Start: {{window_start}}
- End: {{window_end}}
- Timezone: {{timezone}}
- Consent granted: {{consent_granted}}
- Capture level: {{capture_level}}
- Scope: {{scope}}
- Retention days: {{retention_days}}

## Metrics

| Metric | Value | Notes |
| --- | --- | --- |
| Sessions analyzed | {{sessions_analyzed}} | |
| Total turns | {{total_turns}} | |
| Distinct tools used | {{distinct_tools_used}} | |
| Time to first useful result (median) | {{ttfur_median}} | Proxy |
| Error rate | {{error_rate}} | Proxy |
| Retry/loop signal count | {{retry_loop_signals}} | Proxy |

### Tools Used (Top)

- {{tool_name_1}}: {{tool_count_1}}
- {{tool_name_2}}: {{tool_count_2}}
- {{tool_name_3}}: {{tool_count_3}}

### Top Intents

1. {{intent_1}} ({{intent_1_count}})
2. {{intent_2}} ({{intent_2_count}})
3. {{intent_3}} ({{intent_3_count}})
4. {{intent_4}} ({{intent_4_count}})
5. {{intent_5}} ({{intent_5_count}})

## Top 5 Insights

1. **{{insight_1_title}}**  
   Evidence: {{insight_1_evidence_ids}}  
   Why it matters: {{insight_1_impact}}
2. **{{insight_2_title}}**  
   Evidence: {{insight_2_evidence_ids}}  
   Why it matters: {{insight_2_impact}}
3. **{{insight_3_title}}**  
   Evidence: {{insight_3_evidence_ids}}  
   Why it matters: {{insight_3_impact}}
4. **{{insight_4_title}}**  
   Evidence: {{insight_4_evidence_ids}}  
   Why it matters: {{insight_4_impact}}
5. **{{insight_5_title}}**  
   Evidence: {{insight_5_evidence_ids}}  
   Why it matters: {{insight_5_impact}}

## Top 5 Pain Points

| Pain Point | Severity | Frequency | Evidence |
| --- | --- | --- | --- |
| {{pain_1}} | {{pain_1_severity}} | {{pain_1_frequency}} | {{pain_1_evidence}} |
| {{pain_2}} | {{pain_2_severity}} | {{pain_2_frequency}} | {{pain_2_evidence}} |
| {{pain_3}} | {{pain_3_severity}} | {{pain_3_frequency}} | {{pain_3_evidence}} |
| {{pain_4}} | {{pain_4_severity}} | {{pain_4_frequency}} | {{pain_4_evidence}} |
| {{pain_5}} | {{pain_5_severity}} | {{pain_5_frequency}} | {{pain_5_evidence}} |

## Recommendations (3-7)

1. {{recommendation_1}}
2. {{recommendation_2}}
3. {{recommendation_3}}
4. {{recommendation_4}}
5. {{recommendation_5}}

## Anonymized Evidence Snippets

- {{snippet_1}}
- {{snippet_2}}
- {{snippet_3}}

## Open Questions

- {{open_question_1}}
- {{open_question_2}}
- {{open_question_3}}

## Next-Day Research Plan

1. {{next_step_1}}
2. {{next_step_2}}
3. {{next_step_3}}

## Provenance and Limits

- Raw events: `{baseDir}/data/{{report_date}}/raw_events.jsonl`
- Sessions index: `{baseDir}/data/{{report_date}}/sessions_index.json`
- Summary JSON: `{baseDir}/reports/{{report_date}}.summary.json`
- Capture constraints applied: {{capture_constraints}}
- Known data gaps: {{known_data_gaps}}
