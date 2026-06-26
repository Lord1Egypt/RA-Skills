# Analysis Framework — UxrObserver Report Distillation

This document defines the methodology for synthesizing raw observation data into insights for the research report. The Distiller Agent (or inline distillation in single-agent mode) follows this framework.

## Phase 1: Data Assembly

1. **Determine reporting window** from `last-sent-report.json`
2. **Load all observations** from session directories within the window
3. **Load all surveys** from the same window
4. **Load aggregate files** for longitudinal context
5. **Load system events** for data quality assessment

## Phase 2: Quantitative Analysis

### Compute Key Metrics

- Total interactions observed
- Total sessions (group by session_id)
- Use case frequency distribution (from observations + aggregates)
- Satisfaction ratings: mean, median, range, trend (from surveys)
- Frustration rate: % of surveys reporting frustration
- Delight rate: % of surveys reporting delight or magic moments
- Failure rate: % of observations with failure outcomes
- Survey completion rate: surveys collected / tasks completed
- Total estimated cost: sum of estimated_cost_usd across observations
- Average session duration
- Average tool calls per task
- Observation gap time

### Trend Computation

Compare current period metrics to prior period (if data exists):
- Use case distribution shift (which categories grew/shrank?)
- Satisfaction trend direction (improving, declining, stable?)
- Failure rate trend
- Cost trend
- Session length trend
- Complexity trend (are tasks getting more or less complex?)

Use simple directional indicators: `↑ increasing`, `↓ decreasing`, `↔ stable`

## Phase 3: Qualitative Analysis

### Verbatim Organization

1. **Extract all verbatims** from observations and surveys within the window
2. **Deduplicate** (same quote appearing in observation + survey for same task)
3. **Categorize thematically:**
   - **Wins & Delight** — positive reactions, praise, surprise, magic moments
   - **Pain Points & Frustrations** — negative reactions, complaints, friction expressions
   - **Expectations & Mental Models** — statements revealing what the user expected
   - **Suggestions & Wishes** — explicit feature requests or improvement ideas
   - **Unprompted Commentary** — spontaneous observations not prompted by surveys

4. **Rank by signal strength:** Verbatims expressing strong emotion or revealing deep insight get priority placement in the report

### Task-Level Pairing

For each task in the reporting window:
1. Pair the observation record with its post-task survey response (if collected)
2. Write or verify the task context narrative
3. Identify the key verbatims for this specific task
4. Note friction signals and value delivered

### Pattern Recognition

Look for recurring patterns across tasks:

- **Clustering:** Do certain failure types cluster around specific use cases?
- **Sequences:** Do certain interaction sequences reliably produce frustration or delight?
- **Time patterns:** Are there times of day associated with different experience quality?
- **Complexity correlation:** Does task complexity predict satisfaction?
- **Tool correlation:** Do specific tools correlate with success or failure?
- **Model correlation:** If models vary, does model choice affect experience?
- **Skill correlation:** Do certain skills correlate with better/worse outcomes?

### Insight Generation Rules

Every insight in the report MUST:
1. **Reference specific data** — task numbers, verbatim quotes, metrics
2. **State the pattern** — what is happening?
3. **State the evidence** — how many times? which tasks? what did the user say?
4. **Suggest the implication** — what does this mean for the product/experience?

**DO NOT:**
- Generate insights not supported by the data
- Speculate about causes without evidence
- Present opinions as findings
- Ignore contradictory evidence

## Phase 4: Chart Generation

Generate all applicable charts using `scripts/generate-charts.py` or inline matplotlib.

Required charts (if sufficient data):
1. Use case distribution (bar)
2. Satisfaction trend (line)
3. Failure type distribution (donut)
4. Session activity timeline (heatmap)
5. Cost over time (area)
6. Sentiment distribution (stacked bar)
7. Task complexity distribution (bar)
8. Tool usage frequency (bar)

Charts should be clean, professional, and immediately readable. Use the color palette defined in the generate-charts script.

## Phase 5: Recommendation Generation

Recommendations must be:
1. **Evidence-based** — tied to specific findings from this reporting period
2. **Actionable** — something that could be changed or improved
3. **Prioritized** — most impactful first
4. **Scoped** — realistic given what the data shows

Format:
```
**[Recommendation]** — [What to do]
Evidence: [Specific data points, task references, verbatims]
Expected impact: [What improvement this would drive]
```

Limit to 3-5 recommendations per report. Quality over quantity.

## Phase 6: Data Quality Assessment

Document any issues that affect the reliability of the data:
- Observation gaps (from Sentinel agent / gap detection)
- Low survey completion rates
- Integrity check failures
- Estimation confidence notes
- Periods with sparse data

This goes in the "Data Quality Notes" section at the end of the report.

## Phase 7: Redaction & Assembly

1. Run the PII redaction pass (per `references/redaction-rules.md`)
2. Log all redactions
3. Assemble the full report following the template in `references/report-template.md`
4. Insert charts at marked locations
5. Final quality check: Does every insight have evidence? Are all charts included? Is the executive summary accurate?
