## Description: <br>
Multi-lender mortgage rate comparison that scrapes lender and benchmark rates, ranks them lowest to highest, and tracks day-over-day changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seang1121](https://clawhub.ai/user/seang1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home buyers, mortgage watchers, and automation agents use this skill to compare mortgage rates across lenders and national benchmarks for a configured ZIP code. It is intended for monitoring and reporting, not for making lending or financial decisions without review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scraper sends the configured or command-line ZIP code to multiple lender and benchmark sites. <br>
Mitigation: Use only ZIP codes acceptable to share with those sites and review site terms before scheduled or repeated use. <br>
Risk: The artifact includes an undocumented local browser-control fallback that connects to 127.0.0.1:18800 via CDP. <br>
Mitigation: Do not run or expose that fallback unless it is removed or changed to require explicit opt-in with an isolated browser profile. <br>
Risk: Mortgage-rate scraping can return stale, missing, or incorrectly extracted values when public pages change or block automation. <br>
Mitigation: Review the generated report before relying on it and confirm important rates against lender disclosures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seang1121/mortgage-rate-lookup) <br>
- [Project homepage](https://github.com/seang1121/Multi-Lender-Mortgage-Rate-Lookup) <br>
- [Freddie Mac PMMS history CSV](https://www.freddiemac.com/pmms/docs/PMMS_history.csv) <br>
- [Mortgage News Daily mortgage rates](https://www.mortgagenewsdaily.com/mortgage-rates) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text report to stdout, with optional local JSON history.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+, patchright, Chromium installation, and a ZIP code; supports --zip and --headed options.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
