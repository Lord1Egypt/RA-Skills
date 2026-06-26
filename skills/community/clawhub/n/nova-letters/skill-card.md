## Description: <br>
Nova Letters helps agents write reflective letters to their future selves that capture what matters across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptocana](https://clawhub.ai/user/cryptocana) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use Nova Letters to save reflective notes, lessons, decisions, and meaningful context as local daily markdown letters for future sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The read command can escape the intended letters folder and expose other Markdown files. <br>
Mitigation: Validate date inputs and ensure resolved paths remain inside ~/.openclaw/workspace/letters/ before reading files. <br>
Risk: Letters are stored as plaintext local markdown files and may contain sensitive personal or business context. <br>
Mitigation: Avoid writing secrets or highly sensitive details unless plaintext local storage is acceptable for the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cryptocana/nova-letters) <br>
- [Publisher profile](https://clawhub.ai/user/cryptocana) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown files and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes plaintext daily markdown files under ~/.openclaw/workspace/letters/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
