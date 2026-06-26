## Description: <br>
Atomic node skill to update a Google Doc using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to write, insert, or replace text in an existing Google Doc through the configured gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Google Docs through the user's configured gog access. <br>
Mitigation: Before approving use, confirm the Google account, exact document ID or URL, and the text to write or replace. <br>
Risk: Shared or sensitive documents may be changed unintentionally if the target is not verified. <br>
Mitigation: Verify the target document and requested edit before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-docs-update-document) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text] <br>
**Output Format:** [Shell command with a JSON object or confirmation string] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured gog CLI access to Google Docs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
