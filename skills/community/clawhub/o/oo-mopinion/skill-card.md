## Description: <br>
Mopinion (mopinion.com). Use this skill for ANY Mopinion request - searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Mopinion account, deployment, dataset, feedback form, feedback item, and report data through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require installing or updating the oo CLI with a remote installer before connector actions can run. <br>
Mitigation: Review the oo CLI installer source and install it only from the documented OOMOL URL. <br>
Risk: The agent can read connected Mopinion account, dataset, feedback, deployment, and report information once the user is authenticated. <br>
Mitigation: Use the skill only with trusted agents and confirm the target account, dataset, report, or deployment before running connector actions. <br>
Risk: Connector schemas may change over time, causing invalid or incomplete payloads if actions are called from memory. <br>
Mitigation: Inspect the live action schema with oo connector schema before constructing each action payload. <br>


## Reference(s): <br>
- [Mopinion ClawHub listing](https://clawhub.ai/oomol/oo-mopinion) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Mopinion homepage](https://www.mopinion.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects containing data and meta.executionId when actions are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
