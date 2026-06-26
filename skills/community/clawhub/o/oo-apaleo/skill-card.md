## Description: <br>
apaleo enables agents to read, create, update, and delete apaleo data through the OOMOL oo CLI connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage apaleo properties, units, unit groups, and unit attributes through an OOMOL-connected account. It supports read workflows and clearly marked write or destructive apaleo actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a suspicious security verdict for the broader scanned skill set. <br>
Mitigation: Review the skill before installation and install it only in a trusted development environment. <br>
Risk: Write and destructive apaleo actions can change or delete live account data. <br>
Mitigation: Confirm the target resource, payload, and expected effect before running actions marked write or destructive. <br>
Risk: The skill depends on an authenticated OOMOL account and connected apaleo provider. <br>
Mitigation: Use the first-time setup paths only after an auth or connection failure, and verify the apaleo connection scope before retrying. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/oomol/oo-apaleo) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [apaleo homepage](https://apaleo.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands produce JSON responses from the oo connector when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
