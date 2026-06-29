## Description: <br>
Fireberry lets an agent read, list, query, create, update, and delete Fireberry account and contact records through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Fireberry account and contact records through an OOMOL-connected account, including reads, paginated lists, v3 queries, and confirmed write or destructive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write and destructive Fireberry actions can change or delete account and contact records. <br>
Mitigation: Confirm the exact action, target record, payload, and expected effect with the user before running any action tagged write or destructive. <br>
Risk: The skill depends on an external Fireberry connection and OOMOL account permissions. <br>
Mitigation: Before installation or use, review the skill listing and confirm that requested permissions, credentials, and external services match the intended task. <br>


## Reference(s): <br>
- [ClawHub Fireberry skill listing](https://clawhub.ai/oomol/skills/oo-fireberry) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Fireberry homepage](https://www.fireberry.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions may return JSON data with meta.executionId when executed through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
