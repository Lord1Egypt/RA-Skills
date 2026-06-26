## Description: <br>
Generates Chinese CEO-style daily briefings by fetching current technology, AI, finance, social, and GitHub sources, normalizing them to JSON, and producing Markdown analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhlorra](https://clawhub.ai/user/yhlorra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect public news and discussion sources, then generate Chinese daily briefings for executive review across technology, finance, AI, social trends, and GitHub activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches many external sites and uses browser scraping, including anti-bot behavior. <br>
Mitigation: Install and run it only when those network behaviors are acceptable, and avoid sensitive internal URLs or private feeds. <br>
Risk: Fetched content or repository metadata may be sent to MiniMax or OpenRouter when credentials are present. <br>
Mitigation: Review API-key handling before use and avoid providing credentials when third-party model processing is not intended. <br>
Risk: The skill writes local reports and cache files. <br>
Mitigation: Use --no-save where supported and inspect generated reports or caches before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yhlorra/lorra-ceo-briefing) <br>
- [README](artifact/README.md) <br>
- [General briefing instructions](artifact/references/briefing_general.md) <br>
- [Finance briefing instructions](artifact/references/briefing_finance.md) <br>
- [Technology briefing instructions](artifact/references/briefing_tech.md) <br>
- [AI daily briefing instructions](artifact/references/briefing_ai_daily.md) <br>
- [GitHub briefing instructions](artifact/references/briefing_github.md) <br>
- [Social briefing instructions](artifact/references/briefing_social.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with intermediate JSON data files and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports and cache files may be saved locally; some commands support --no-save.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
