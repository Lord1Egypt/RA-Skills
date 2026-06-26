## Description: <br>
Google Search Console data analysis and site management via google-search-console-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and SEO operators use this skill to run Google Search Console CLI workflows for search analytics, URL inspection, site property checks, and sitemap management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google credentials can expose Search Console properties if broad Application Default Credentials or over-scoped service accounts are used. <br>
Mitigation: Use a dedicated least-privilege service account limited to the intended properties and prefer explicit credential configuration. <br>
Risk: Write-capable commands can add or remove site properties and submit or delete sitemaps. <br>
Mitigation: Require explicit target-by-target confirmation before running site-add, site-remove, sitemap-submit, or sitemap-delete. <br>
Risk: Bulk query and inspection workflows can produce large exports containing site performance data. <br>
Mitigation: Confirm the intended property, date range, and output destination before exporting or piping bulk results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bin-huang/google-search-console-open-cli) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/bin-huang) <br>
- [google-search-console-cli documentation](https://github.com/Bin-Huang/google-search-console-cli) <br>
- [Google Search Analytics API](https://developers.google.com/webmaster-tools/v1/searchanalytics/query) <br>
- [Google URL Inspection API](https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect) <br>
- [Google Search Console Sites API](https://developers.google.com/webmaster-tools/v1/sites) <br>
- [Google Search Console Sitemaps API](https://developers.google.com/webmaster-tools/v1/sitemaps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands may emit pretty JSON, compact JSON, or NDJSON depending on command options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
