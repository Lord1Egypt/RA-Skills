## Description: <br>
Query ad platform data (Meta, Google, LinkedIn, Reddit) using the Hopkin CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nemo](https://clawhub.ai/user/nemo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query read-only advertising account, campaign, ad set, ad, and performance data across supported paid media platforms through Hopkin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external Hopkin CLI and npm package @hopkin/cli. <br>
Mitigation: Install the CLI only when Hopkin and the package source are trusted, and review the package before using it with sensitive ad-account data. <br>
Risk: Hopkin API keys may expose access to advertising account data if mishandled. <br>
Mitigation: Use limited-scope keys when available, avoid sharing keys in chat or logs, and rotate any key that may have been exposed. <br>
Risk: Advertising account and campaign queries can return sensitive business performance data. <br>
Mitigation: Review Hopkin's local credential storage and caching behavior before querying sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nemo/hopkin-paid-ads) <br>
- [Hopkin API key settings](https://app.hopkin.ai/settings/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides read-only Hopkin CLI queries and recommends JSON, CSV, or TSV output formats where appropriate.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
