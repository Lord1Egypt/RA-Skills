# Report Template — UxrObserver Research Report

This is the complete template for the daily/periodic research report. When generating, follow this structure exactly. The report should be created as a **Google Doc** using available Google Docs/Drive tools. If those tools are unavailable, generate as Markdown and prompt the user to share manually.

## Chart & Visualization Requirements

Every report MUST include data visualizations. Charts make patterns visible that tables alone cannot communicate. Generate charts using the `scripts/generate-charts.py` script, or create them inline using matplotlib/plotly if Python is available.

### Required Charts (include if sufficient data exists)

1. **Use Case Distribution** — Horizontal bar chart
   - X-axis: count of interactions
   - Y-axis: use case categories sorted by frequency
   - Color: gradient from most to least frequent
   - Include percentage labels on bars

2. **Satisfaction Trend** — Line chart with data points
   - X-axis: date/time
   - Y-axis: satisfaction rating (1-5 scale)
   - Show individual ratings as dots, rolling average as line
   - Add horizontal reference line at 3.0 (neutral)
   - If multi-day report, show daily average trend

3. **Failure Type Distribution** — Donut/pie chart
   - Segments: failure types from the taxonomy
   - Label each segment with type name and count
   - Use warm/red palette for severity emphasis
   - Include "no failures" as a segment if applicable

4. **Session Activity Timeline** — Scatter/bubble plot or heatmap
   - X-axis: time of day
   - Y-axis: date
   - Bubble size or color intensity: number of interactions
   - Shows when the user is most active

5. **Estimated Cost Over Time** — Area chart
   - X-axis: date
   - Y-axis: estimated cost in USD
   - Stacked by: input tokens, output tokens, tool overhead
   - Show cumulative total as a secondary line

6. **Sentiment Distribution** — Stacked bar chart
   - X-axis: date (or session if single-day)
   - Y-axis: count of interactions
   - Stacked segments: delighted, positive, neutral, frustrated, confused, angry, resigned
   - Color palette: green (delighted) → yellow (neutral) → red (angry)

7. **Task Complexity Distribution** — Bar chart
   - Shows proportion of trivial/simple/moderate/complex/multi-session tasks
   - Useful for understanding the sophistication of usage

8. **Tool Usage Frequency** — Horizontal bar chart
   - Which tools are used most often
   - Helps identify which capabilities are most leveraged

### Optional Charts (include when relevant)

- **Failure Rate Over Time** — line chart showing if things are improving
- **Survey Completion Rate** — gauge or progress bar
- **Value Delivered Distribution** — treemap of value categories
- **Sub-Agent Architecture Diagram** — text-based or SVG flow diagram
- **Prompt Style Evolution** — stacked area showing how user's prompting style changes

### Chart Generation

Charts should be generated as PNG images and either:
- **Embedded in Google Doc** via Google Docs API image insertion
- **Saved to `~/.uxr-observer/reports/charts/`** and referenced in the Markdown report

Use `scripts/generate-charts.py` with the following interface:
```bash
python scripts/generate-charts.py \
  --data-dir ~/.uxr-observer \
  --output-dir ~/.uxr-observer/reports/charts \
  --start-date 2026-03-01 \
  --end-date 2026-03-03
```

If Python/matplotlib is not available, generate charts as ASCII art or text-based tables as fallback. If generating a Google Doc, use the Google Sheets API to create embedded charts (create a hidden spreadsheet with the data, create charts, copy chart images into the Doc).

---

## Report Structure

```markdown
# UxrObserver Research Report

**Reporting period:** [start date/time] → [end date/time]
**Days covered:** N
**Total interactions observed:** N
**Report generated:** [timestamp]
**Participant ID:** [anonymous hash]

---

## Executive Summary

3-5 sentences. What happened? What are the headline findings?
What is the single most important insight from this reporting period?

---

## Usage Overview

### Key Metrics
- **Total tasks observed:** N
- **Total sessions:** N
- **Total estimated API cost:** $X.XX (±$X.XX)
- **Average session duration:** Xm
- **Average tasks per session:** X.X
- **Post-task surveys completed:** N / N possible (X%)
- **Average satisfaction rating:** X.X / 5
- **Tasks with reported frustration:** N (X%)
- **Tasks with reported delight:** N (X%)
- **Observation gaps detected:** N (total gap time: Xh)

### Use Case Frequency Distribution

[INSERT: Use Case Distribution bar chart]

| Rank | Use Case Category | Count | % of Total | Trend vs. Prior |
|------|-------------------|-------|------------|-----------------|
| 1    | coding            | 34    | 42%        | ↑ +8%           |
| 2    | writing           | 18    | 22%        | ↔ stable        |
| ...  | ...               | ...   | ...        | ...             |

### Satisfaction Trend

[INSERT: Satisfaction Trend line chart]

### Model & Infrastructure
- **Primary model:** [name] (X% of interactions)
- **Secondary models:** [if any]
- **Environment:** [detected environment]
- **Sub-agent architecture:** [description]
- **Most-used skills:** [list with frequency]

### Estimated Cost Breakdown

[INSERT: Cost Over Time area chart]

| Category           | Est. Tokens | Est. Cost |
|--------------------|-------------|-----------|
| Input tokens       | X           | $X.XX     |
| Output tokens      | X           | $X.XX     |
| Tool call overhead | X           | $X.XX     |
| **Total**          | **X**       | **$X.XX** |

---

## Activity Patterns

[INSERT: Session Activity Timeline heatmap/scatter]

[INSERT: Sentiment Distribution stacked bar chart]

[INSERT: Task Complexity Distribution bar chart]

[INSERT: Tool Usage Frequency bar chart]

---

## Detailed Task Log

For every interaction observed during the reporting period:

### [Task N]: [Brief description]
**Timestamp:** [datetime]
**Category:** [use case] | **Complexity:** [level] | **Outcome:** [result]
**Model:** [model] | **Tools used:** [list] | **Est. cost:** $X.XX
**Satisfaction rating:** X/5

**What happened:**
[task_context_narrative — 3-5 sentences, written for someone who wasn't there]

**User verbatims:**

**[Researcher interpretation header]**
> "[User's exact words]"

**[Researcher interpretation header]**
> "[User's exact words]"

**Friction signals:** [list or "none"]
**Value delivered:** [list or "none"]

**Survey response (if collected):**
- Rating: X/5
- Rationale: > "[verbatim]"
- Frustration: Yes/No → "[verbatim detail]"
- Best part: > "[verbatim]"

---
*(Repeat for every observed interaction)*

---

## Fail State Analysis

### Failure Summary

[INSERT: Failure Type Distribution donut chart]

| Failure Type     | Count | Severity Distribution      | Most Common Recovery |
|------------------|-------|---------------------------|---------------------|
| misunderstanding | 5     | 3 moderate, 2 minor       | user correction     |
| tool_error       | 3     | 1 severe, 2 minor         | retry               |
| ...              | ...   | ...                       | ...                 |

[INSERT: Failure Rate Over Time line chart — if multi-day]

### Critical Failures (if any)
[Detailed narrative with full context and verbatims]

### Failure Trends
[Are failures increasing or decreasing? Clustering around specific use cases?]

---

## Verbatim Gallery

All notable user quotes, organized thematically with researcher headers:

### Wins & Delight
**[Researcher interpretation]**
> "[Exact quote]"
— Context: [what was happening]

### Pain Points & Frustrations
**[Researcher interpretation]**
> "[Exact quote]"
— Context: [what was happening]

### Expectations & Mental Models
**[Researcher interpretation]**
> "[Exact quote]"
— Context: [what was happening]

### Suggestions & Wishes
**[Researcher interpretation]**
> "[Exact quote]"
— Context: [what was happening]

### Unprompted Commentary
**[Researcher interpretation]**
> "[Exact quote]"
— Context: [what was happening]

---

## Sub-Agent Architecture Analysis

[If applicable: describe the architecture, what's working, what's not.
Include text-based architecture diagram if multi-agent setup detected.]

---

## Patterns & Insights

### What's Working Well
[Insights grounded in specific data. Reference task numbers and verbatims.]

### Recurring Pain Points
[Pain points with frequency counts, supporting verbatims, task references]

### Emerging Themes
[Cross-cutting patterns suggesting deeper UX issues or opportunities]

### User Skill Development
[How is the user's relationship with OpenClaw evolving? Efficiency? Sophistication?]

### Value Proposition Evidence
[Where does OpenClaw deliver the most value? Highest satisfaction use cases?]

---

## Recommendations

Based on data from this reporting period:

1. **[Recommendation]** — [Evidence: task refs, verbatims, metrics]
2. **[Recommendation]** — [Evidence]
3. **[Recommendation]** — [Evidence]

---

## Data Quality Notes

- **Observation gaps:** [details or "none detected"]
- **Self-monitor status:** [integrity check results]
- **Redactions applied:** [count] items across [categories]
- **Survey completion rate:** X%
- **Estimation confidence:** Token/cost estimates carry ±20% margin

---

*This report was generated locally by UxrObserver v1.0.0*
*Reporting period: [start] → [end]*
*⚠️ PII and sensitive data have been automatically redacted. See redaction log for audit.*
*📧 To share: tell OpenClaw who to email this to.*
```

## Google Doc Specific Instructions

When creating the report as a Google Doc:

1. **Title format:** "UxrObserver Report — [Start Date] to [End Date]"
2. **Use heading styles:** Heading 1 for main sections, Heading 2 for subsections, Heading 3 for task entries
3. **Tables:** Use native Google Doc tables, not markdown tables
4. **Charts:** Generate chart images and insert them inline at the marked `[INSERT: ...]` locations. If using Google Sheets for charts:
   - Create a hidden spreadsheet with the chart data
   - Create the chart in Sheets
   - Export chart as image
   - Insert image into the Doc at the appropriate location
5. **Verbatim quotes:** Format with indented blockquote styling (indented paragraph, italic or gray text)
6. **Color coding:** Use subtle background colors for key metrics — green for positive, red for pain points, yellow for neutral
7. **Table of contents:** Auto-generate at the top of the document
8. **Page breaks:** Insert before major sections (Executive Summary, Detailed Task Log, Verbatim Gallery)
