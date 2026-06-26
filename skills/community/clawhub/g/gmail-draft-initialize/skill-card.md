## Description: <br>
Atomic node skill to initialize a Gmail draft with recipients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users composing Gmail messages use this skill to create a new empty Gmail draft addressed to specified recipients, leaving the subject and body for later update steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates Gmail drafts in the account configured for the gog CLI. <br>
Mitigation: Use it only with a trusted gog CLI configuration and review drafts before sending. <br>
Risk: An unclear or incorrect recipient list can create a draft addressed to unintended recipients. <br>
Mitigation: Confirm the intended recipients before running the draft creation command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/gmail-draft-initialize) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with an inline shell command and a JSON draft creation result] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates an empty Gmail draft with recipients only; subject and body are excluded.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
