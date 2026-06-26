## Description: <br>
Scrape a public Letterboxd user's watchlist into a CSV/JSONL list of titles and film URLs without logging in. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xnuminous](https://clawhub.ai/user/0xnuminous) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to export or mirror a public Letterboxd watchlist, or to build watch-next queues from public profile data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script writes to a user-chosen output path. <br>
Mitigation: Use a normal working-folder path such as watchlist.csv or watchlist.jsonl, and avoid important existing files. <br>
Risk: The skill scrapes public Letterboxd pages and may break if page markup changes. <br>
Mitigation: Review the output count and records after scraping, and update the scraper pattern if Letterboxd changes its HTML. <br>
Risk: Providing credentials is unnecessary for this public-watchlist workflow. <br>
Mitigation: Do not provide Letterboxd credentials; use only a public username. <br>


## Reference(s): <br>
- [Letterboxd](https://letterboxd.com) <br>
- [ClawHub skill page](https://clawhub.ai/0xnuminous/letterboxd-watchlist) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with shell commands; generated CSV or JSONL files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scraper writes title and film URL records to a user-chosen .csv or .jsonl output path.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
