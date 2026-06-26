## Description: <br>
Atomic node skill to read a specific email via Gmail using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when they need to retrieve the headers, body, and metadata for a specific Gmail message by message ID through the configured gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Retrieved Gmail messages can contain sensitive headers, body text, authentication links, financial details, or other private content. <br>
Mitigation: Use the skill only for intentional retrieval of a specific email, trust the configured gog CLI and Gmail account, and avoid unnecessary sharing or logging of full message contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/gmail-retrieve-email) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON returned by the gog CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Retrieves a single Gmail message identified by message ID.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
