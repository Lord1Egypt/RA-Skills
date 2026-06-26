## Description: <br>
Fetches US 10-year Treasury yield data from CNBC and Treasury.gov, writes it to CSV, and records a minimal run log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kid0114](https://clawhub.ai/user/kid0114) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect daily US 10-year Treasury yield data from public sources into a CSV file with a simple execution log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts CNBC and Treasury.gov and depends on those public pages remaining reachable and parseable. <br>
Mitigation: Run it only in environments where those outbound requests are acceptable, and review the CSV/log output for partial or failed fetches. <br>
Risk: Rerunning the skill on the same day replaces that day's CSV row instead of preserving every run. <br>
Mitigation: Keep separate backups or copy the CSV before reruns when per-run history is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kid0114/myskill1) <br>
- [CNBC US10Y quote](https://www.cnbc.com/quotes/US10Y) <br>
- [Treasury.gov daily treasury yield curve](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value=2026) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [CSV data file and plain-text log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No user parameters; rerunning on the same day replaces that day's CSV row.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
