## Description: <br>
Atomic node skill to read a Google Doc using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch the plain text contents of a specific Google Doc by document ID through the local gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads Google Docs identified by document ID through the user's local gog CLI, which can expose sensitive document contents if used on documents the user did not intend to share with the agent. <br>
Mitigation: Use it only for documents the user explicitly identifies and avoid sensitive documents unless agent access to that content is intended. <br>
Risk: The skill depends on the local gog CLI configuration and Google Docs access permissions. <br>
Mitigation: Install only when the local gog CLI setup is trusted and verify CLI authentication and document permissions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-docs-read-document) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text from the gog CLI, with command guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local gog CLI setup with access to the requested Google Docs document ID.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
