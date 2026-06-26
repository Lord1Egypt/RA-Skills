## Output Rules

❝ **Never produce an inspection report unless it follows the format defined in `references/report-template.md`.** The report must use the Required Report Sections 1-6 structure, include all metrics listed under each section, and use the API Name column values for metric references. Deviating from this template is forbidden. ❞

1. For every section, identify the data source as `API` (via `/ts/query`) or `OS` (via shell scripts under `scripts/`).
2. If a metric is only partially supported, say so explicitly.
3. If multi-node evidence is incomplete, say which part is inferred versus directly observed.
4. Return inline Markdown report rather than claiming a saved file path unless a file tool actually created that artifact.
5. If the task runs in cluster mode, the report must cover all nodes rather than only a single node snapshot.
6. Scheduled inspection should recover thresholds and time-range hints from the task prompt; if missing, use defaults and document that assumption.
7. HTML and PDF are optional; default to Markdown. When generating PDF, HTML, or Markdown files, use UTF-8 character encoding, use relevant PDF or HTML generation skills to produce reports in the corresponding format if available.
8. If the user explicitly asks for charts, hand structured metrics to a visualization tool. Chart generation failure must not block the main report.
