## Description: <br>
DocsAutomator (docsautomator.co). Use this skill for ANY DocsAutomator request - reading, creating, and updating data. Whenever a task involves DocsAutomator, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate DocsAutomator through an OOMOL-connected account for listing automations, inspecting templates, generating documents, and checking queued document jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires trust in OOMOL and DocsAutomator with the connected account. <br>
Mitigation: Install only when the user trusts OOMOL and DocsAutomator with the account and workspace being connected. <br>
Risk: The first-time CLI setup includes a remote installer command. <br>
Mitigation: Review the official installer or installation guide before running the pipe-to-shell command. <br>
Risk: Document-generation actions can change DocsAutomator state. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>


## Reference(s): <br>
- [DocsAutomator homepage](https://www.docsautomator.co) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-docsautomator) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before building action payloads; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
