## Description: <br>
Operate Imgix through an OOMOL-connected account for source lookup, source updates, and cache purges using the oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Imgix through OOMOL without handling raw Imgix credentials. It supports reading Imgix Sources, updating Source attributes, and purging cached assets after explicit approval for state-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can update Imgix Sources and purge cached assets. <br>
Mitigation: Confirm the exact payload, target, and expected effect with the user before running write or destructive actions. <br>
Risk: The skill depends on installing or authenticating the OOMOL oo CLI for account-connected Imgix access. <br>
Mitigation: Only run setup or account-connection steps when the user needs this integration, trusts OOMOL, and an action fails because the CLI or connection is missing. <br>


## Reference(s): <br>
- [ClawHub Imgix Skill Page](https://clawhub.ai/oomol/skills/oo-imgix) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>
- [Imgix Homepage](https://www.imgix.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live action schema inspection before connector runs; write and destructive actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
