## Description: <br>
Web scraping skill for LinkedIn job postings using public API endpoints; extracts job data without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicolassantos23](https://clawhub.ai/user/nicolassantos23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to search public LinkedIn job postings by keyword, location, and filters, then collect listing details through a CLI or Python module. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: LinkedIn scraping may violate LinkedIn terms or trigger IP blocking when used at high volume. <br>
Mitigation: Review LinkedIn terms before use, keep usage low-volume, and follow the documented throttling guidance. <br>
Risk: The skill makes web requests and can save scraped job data to local files. <br>
Mitigation: Run it in a controlled Python environment with pinned dependencies and review output paths before saving results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicolassantos23/picoclaw-finance) <br>
- [Project homepage](https://github.com/nicolasteofilo/opencode-skills) <br>
- [Support issues](https://github.com/nicolasteofilo/opencode-skills/issues) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Files, Guidance] <br>
**Output Format:** [CLI text, Python dictionaries, JSON files, CSV files, and Markdown guidance with shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save scraped job listings locally as CSV or JSON.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
