## Description: <br>
Browserless helps an agent fetch rendered HTML content and generate PDFs or screenshots through Browserless via an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to run Browserless connector actions for fetching fully rendered page content, PDFs, and screenshots without handling raw Browserless credentials directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Browserless account and may use sensitive credentials managed outside the agent. <br>
Mitigation: Install it only when Browserless access is intended, connect only the account and scopes needed for the task, and avoid repeating authentication or connection setup unless a command fails for that reason. <br>
Risk: Generated PDFs, screenshots, and fetched pages may consume Browserless or OOMOL credits. <br>
Mitigation: Treat connector outputs as billable data operations and resolve billing errors before retrying failed commands. <br>
Risk: First-time CLI setup includes shell installation commands. <br>
Mitigation: Review the oo CLI install command before running it and use the platform-specific installation path documented by OOMOL. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-browserless) <br>
- [Browserless Homepage](https://www.browserless.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return rendered HTML text or base64-encoded PDF and screenshot data through the Browserless connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
