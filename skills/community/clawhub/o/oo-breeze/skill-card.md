## Description: <br>
Breeze helps an agent search and read Breeze CHMS data through the OOMOL-connected breeze connector and oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve Breeze people, profile-field, tag-folder, and tag data through their connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected Breeze account, so use can expose Breeze data to the agent during requested reads. <br>
Mitigation: Install and invoke it only when connector-backed Breeze access is intended, and review requested data retrieval before running commands. <br>
Risk: The trigger wording is broad and may activate for casual Breeze-related discussion. <br>
Mitigation: Confirm the task needs live Breeze connector access before executing oo CLI commands. <br>
Risk: First-time setup may involve CLI installation or account-connection steps. <br>
Mitigation: Review installation and connection prompts before approving them, and only connect the Breeze account required for the task. <br>


## Reference(s): <br>
- [ClawHub Breeze skill page](https://clawhub.ai/oomol/oo-breeze) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Breeze homepage](https://www.breezechms.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Breeze connector actions and returns connector responses as JSON when commands are executed.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
