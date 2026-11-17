## Description:

Searches and formats Indeed job listings and company information through Bright Data's Web Scraper API using Bash scripts that require BRIGHTDATA_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foreztgump](https://clawhub.ai/user/foreztgump)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and recruiting teams use this skill to search Indeed jobs and company pages, collect details from specific Indeed URLs, poll asynchronous Bright Data results, and present formatted recruiting research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A polling script accepts crafted timing options that can execute local shell commands.

Mitigation: Review before installing and do not allow untrusted prompts or inputs to control polling options until timeout and interval values are strictly validated.

Risk: Job searches, company URLs, and fetched results are sent to Bright Data and cached locally.

Mitigation: Use a narrowly scoped Bright Data API key, avoid sensitive queries where inappropriate, and clear ~/.config/indeed-brightdata/ when cached results should not persist.

Risk: The README includes an optional unpinned npx installation path.

Mitigation: Prefer a reviewed release artifact or pin and verify the installer package before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/foreztgump/skills/indeed-brightdata)
- [Bright Data Indeed API Reference](references/api-reference.md)
- [Keyword expansions](references/keyword-expansions.json)
- [Bright Data](https://brightdata.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands, Configuration]

**Output Format:** [Markdown summaries, JSON result objects, and CSV exports produced by shell scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and BRIGHTDATA_API_KEY; stores pending searches, cache history, and fetched results under ~/.config/indeed-brightdata/.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
