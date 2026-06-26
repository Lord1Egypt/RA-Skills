## Description: <br>
Use this skill for Fillout (fillout.com) requests involving reading, creating, updating, and deleting data through the OOMOL connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a connected Fillout workspace through OOMOL, including listing forms, reading form metadata and submissions, creating submissions, and deleting individual submissions after approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on OOMOL-brokered access to a connected Fillout account. <br>
Mitigation: Install and use it only when the user trusts OOMOL to broker account access. <br>
Risk: The skill can create submissions and delete individual submissions in the connected Fillout workspace. <br>
Mitigation: Review write and delete requests carefully and require explicit approval before running state-changing actions. <br>
Risk: Connector action inputs may drift from static documentation. <br>
Mitigation: Inspect the live action schema before constructing payloads for connector actions. <br>


## Reference(s): <br>
- [Fillout homepage](https://www.fillout.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub Fillout skill](https://clawhub.ai/oomol/oo-fillout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before action execution; write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
