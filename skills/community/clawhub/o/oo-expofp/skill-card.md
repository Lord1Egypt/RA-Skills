## Description: <br>
ExpoFP (expofp.com). Use this skill for ANY ExpoFP request: reading, creating, updating, and deleting data through the OOMOL ExpoFP connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect ExpoFP schemas and run account-authorized ExpoFP actions for expo and exhibitor workflows. It supports listing and retrieving data, creating and updating exhibitors after user confirmation, and deleting exhibitors only after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a connected ExpoFP account and includes create, update, and delete actions. <br>
Mitigation: Run read actions directly, but require user confirmation for exact write payloads and explicit approval before destructive deletes. <br>
Risk: ExpoFP credentials and connection state are required through OOMOL. <br>
Mitigation: Use OOMOL server-side credential injection and only trigger setup or reconnection steps after a command returns an authentication or connection error. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-expofp) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [ExpoFP homepage](https://expofp.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before action execution; command responses are expected as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
