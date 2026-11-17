## Description:

Scrapes a public Letterboxd user's watchlist into a CSV or JSONL list of titles and film URLs without logging in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xnuminous](https://clawhub.ai/user/0xnuminous)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to export a public Letterboxd watchlist into a local CSV or JSONL file for watch-next queues, mirrors, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes public requests to letterboxd.com.

Mitigation: Use it only when public Letterboxd requests are acceptable for the intended environment.

Risk: The user-provided output path could overwrite an existing local file.

Mitigation: Choose a normal new output filename and review the path before execution.

Risk: Best-effort HTML scraping can stop working if Letterboxd changes its page markup.

Mitigation: Review the generated CSV or JSONL output and update the scraper pattern if expected watchlist entries are missing.

## Reference(s):

- [Letterboxd](https://letterboxd.com)
- [ClawHub skill page](https://clawhub.ai/0xnuminous/skills/letterboxd-watchlist)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, files]

**Output Format:** [Markdown guidance with bash commands; generated watchlist data is CSV or JSONL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a public Letterboxd username and a user-provided output path ending in .csv or .jsonl.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
