## Description:

Searches WeChat public account articles by keyword, ranks recent results, displays a terminal table, and exports CSV and interactive HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content researchers, creators, and competitive analysts use this skill to search recent WeChat public account articles, inspect popularity signals, and export results for content research or trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local report server can expose API-backed search access more broadly than users may expect.

Mitigation: Prefer csv-only or no-open mode when possible, stop the local server promptly after viewing the report, and add proxy authentication or origin checks before broader deployment.

Risk: RedFox API keys may be misused if they are hardcoded, logged, or retained longer than needed.

Mitigation: Use a revocable RedFox API key, verify its scope and validity period, and keep the key out of code, prompts, logs, and generated output files.

Risk: Search terms are sent to the RedFox API and may reveal sensitive research or internal topics.

Mitigation: Avoid sensitive internal search terms and review the API provider's terms and data handling expectations before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/gzh-search)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFoxHub](https://redfox.hk?source=clawhub)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, markdown]

**Output Format:** [Terminal text plus UTF-8 CSV files and interactive HTML reports; usage guidance may include Markdown and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RedFox API key through REDFOX_API_KEY, a CLI flag, or a local config file; supports count, sort, output directory, csv-only, no-open, and port options.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
