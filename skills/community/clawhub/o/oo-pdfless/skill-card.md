## Description: <br>
Pdfless (pdfless.com). Use this skill for ANY Pdfless request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to inspect a connected Pdfless workspace and list document templates through OOMOL-managed Pdfless connector actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on OOMOL-managed credentials for Pdfless access. <br>
Mitigation: Install and use it only when OOMOL is an acceptable credential broker for the target Pdfless workspace. <br>
Risk: First-time setup may involve running shell installer commands for the oo CLI. <br>
Mitigation: Verify the oo CLI install source before running curl or PowerShell installer commands. <br>
Risk: Future connector actions may add write-capable behavior. <br>
Mitigation: Review connector schemas and confirm any write or destructive payload with the user before execution. <br>


## Reference(s): <br>
- [Pdfless skill page](https://clawhub.ai/oomol/oo-pdfless) <br>
- [Pdfless homepage](https://pdfless.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects with data and meta.executionId when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
