## Description: <br>
GitHub Copilot CLI - AI code analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[biuyx](https://clawhub.ai/user/biuyx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to install and invoke GitHub Copilot CLI for code analysis questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The usage example depends on a GitHub Copilot token, and poor token handling could expose the secret through plaintext files, shell history, or process arguments. <br>
Mitigation: Treat the token as a secret; prefer an official login flow, OS keychain, or environment variable, and avoid commands that expose tokens in shell history or process arguments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
