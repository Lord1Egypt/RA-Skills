## Description: <br>
Kit (kit.com) skill for reading, creating, and updating data through the OOMOL Kit connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to operate Kit accounts through OOMOL-connected credentials, including listing forms, tags, and subscribers, reading account details, and creating or updating subscribers after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update Kit subscriber records. <br>
Mitigation: Confirm the exact write payload and expected effect with the user before running create_subscriber or update_subscriber. <br>
Risk: The skill requires access to a connected Kit account through OOMOL. <br>
Mitigation: Install only if the user trusts OOMOL with Kit account access and use the documented connection flow when authentication or connection errors occur. <br>
Risk: First-time CLI setup includes remote install commands. <br>
Mitigation: Verify the OOMOL CLI install URL before running setup commands. <br>


## Reference(s): <br>
- [Kit homepage](https://kit.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-kit) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OOMOL server-side credentials for Kit actions; write actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
