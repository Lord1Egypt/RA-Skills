## Description: <br>
Atomic node skill to search for emails in Gmail using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to search the Gmail account configured in gog for messages matching an explicit Gmail query and return email headers or snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose private email snippets from whichever Gmail account the local gog tool can access. <br>
Mitigation: Install only when the agent is allowed to search that account, verify the gog account and permissions, and phrase requests explicitly as Gmail or email searches. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/gmail-search-emails) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text] <br>
**Output Format:** [JSON array of email headers or a no-results text message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local gog CLI to be installed and configured for the Gmail account to search.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
