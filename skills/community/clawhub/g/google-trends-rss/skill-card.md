## Description: <br>
Fetch and structure Google Trends daily trending-search data by country or region via the public RSS feed for snapshots, country comparisons, top daily searches, related news context, and export-ready trend tables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsjwong](https://clawhub.ai/user/wsjwong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Analysts, developers, and reporting workflows use this skill to fetch daily Google Trends RSS results for a selected country or region and format them for terminal review, automation, spreadsheets, or reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the daily command contacts Google Trends and depends on Google's feed availability, latency, and schema stability. <br>
Mitigation: Use appropriate timeouts, handle empty or changed feed fields, and review returned data before using it in reports or automation. <br>
Risk: The optional --out argument can create or overwrite the file path supplied by the user. <br>
Mitigation: Choose output paths deliberately and inspect generated JSON or CSV files before relying on them downstream. <br>
Risk: Server-resolved provenance is unavailable for this release. <br>
Mitigation: Review the included Python script and publisher profile before deploying the skill in sensitive environments. <br>


## Reference(s): <br>
- [Google Trends Connector Notes](references/google-trends-connector-notes.md) <br>
- [Google Trends RSS endpoint](https://trends.google.com/trending/rss) <br>
- [Legacy Google Trends daily RSS endpoint](https://trends.google.com/trends/trendingsearches/daily/rss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, csv files, shell commands] <br>
**Output Format:** [Terminal table, JSON, Markdown, or CSV file output from a Python command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports geo code, row limit, sort mode, output format, timeout, and optional output path.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
