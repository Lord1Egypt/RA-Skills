## Description: <br>
Atomic node skill to create a Google Doc using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user needs a new Google Docs document created through the local gog CLI. It is suited to workflows that can confirm the document title and intended Google account before creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates Google Docs through the local gog CLI using its configured Google account. <br>
Mitigation: Use it only where the gog CLI and configured Google account are trusted, and confirm the intended account before execution. <br>
Risk: Automated workflows could create a document with an unintended title. <br>
Mitigation: Confirm the requested document title before running the creation command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-docs-create-document) <br>
- [Publisher profile](https://clawhub.ai/user/zvirb) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, json] <br>
**Output Format:** [Markdown guidance with an example shell command; the invoked CLI returns JSON document details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog binary and its configured Google account.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
