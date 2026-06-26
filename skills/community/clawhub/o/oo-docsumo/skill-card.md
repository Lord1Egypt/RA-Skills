## Description: <br>
Docsumo (docsumo.com). Use this skill for ANY Docsumo request: reading, creating, and updating data through the OOMOL Docsumo connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect Docsumo account information, document metadata, document summaries, extracted document data, filtered document lists, and upload a public file URL for a selected document type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a user's connected Docsumo account through OOMOL and requires sensitive credentials to be configured server-side. <br>
Mitigation: Install it only when Docsumo account access through OOMOL is intended, and run first-time account connection steps only when authentication or connection errors require them. <br>
Risk: The upload action changes Docsumo state by submitting a public file URL for processing. <br>
Mitigation: Confirm the exact upload payload and expected effect with the user before running write actions. <br>
Risk: Connector schemas may vary by live Docsumo configuration or OOMOL connector version. <br>
Mitigation: Inspect the live action schema before building each connector payload. <br>


## Reference(s): <br>
- [Docsumo homepage](https://www.docsumo.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-docsumo) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill instructs the agent to inspect live connector schemas before forming action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
