## Description: <br>
Research what people actually say about any topic in the last 30 days. Pulls posts and engagement from Reddit, X, YouTube, TikTok, Hacker News, Polymarket, GitHub, and the web. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvanhorn](https://clawhub.ai/user/mvanhorn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research agents use this skill to gather recent social, web, GitHub, and prediction-market signals about a person, company, product, topic, or comparison and synthesize them into a concise brief. Review credential and local-cookie access before enabling broad use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local browser login cookies. <br>
Mitigation: Set FROM_BROWSER=off by default and allow browser-cookie extraction only after explicit user review and consent. <br>
Risk: The skill can use local developer credentials, including a local GitHub token in the GitHub/ScrapeCreators setup path. <br>
Mitigation: Prefer explicit limited API keys and avoid the GitHub/ScrapeCreators setup path unless the user understands which token may be sent. <br>
Risk: Raw research reports and configuration state may be stored locally. <br>
Mitigation: Define local retention expectations and avoid running sensitive research topics unless saved reports and config files are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mvanhorn/last30days-official) <br>
- [Project homepage from ClawHub metadata](https://github.com/mvanhorn/last30days-skill) <br>
- [README](README.md) <br>
- [Skill contract](SKILL.md) <br>
- [Changelog](CHANGELOG.md) <br>
- [Hermes setup](HERMES_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown research briefs with cited source references, setup guidance, command examples, and optional local saved reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and node; SCRAPECREATORS_API_KEY is the primary configured environment variable, with optional provider, browser-cookie, and social-platform credentials.] <br>

## Skill Version(s): <br>
3.1.0-open (source: server release metadata; changelog 3.1.0 released 2026-04-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
