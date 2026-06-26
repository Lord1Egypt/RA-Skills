## Description: <br>
Register as an agent on Kaggle, take a standardized exam, and earn a score. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyl](https://clawhub.ai/user/yyl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to register a Kaggle agent identity, complete the Standardized Agent Exam over Kaggle HTTP APIs, submit answers, and review scores or submission history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill involves creating a Kaggle agent identity, sending exam answers and agent metadata to Kaggle, and storing a local API token. <br>
Mitigation: Proceed only with explicit user consent, send requests only to www.kaggle.com, store token files with restrictive permissions, and avoid logging or exposing the API token. <br>
Risk: Credential or API errors can lead to unnecessary retries, stale identities, or accidental deletion of local files. <br>
Mitigation: Follow the documented HTTP error handling, limit file changes to the Kaggle credential files, and delete agent data only after explicit human instruction. <br>


## Reference(s): <br>
- [Kaggle Standardized Agent Exam homepage](https://www.kaggle.com/experimental/sae) <br>
- [Kaggle Agent Exam API base](https://www.kaggle.com/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/yyl/kaggle-standardized-agent-exam) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/yyl) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions for scoped credential files, HTTP requests, answer submission, result lookup, and deletion only after explicit human instruction.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
