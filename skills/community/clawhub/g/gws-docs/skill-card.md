## Description: <br>
Read and write Google Docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect Google Docs commands, read document content, create blank documents, and apply validated document updates through the gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to read or modify Google Docs through the external gws tool. <br>
Mitigation: Confirm the Google account, scopes, target document ID, and requested parameters before running write or batch-update actions. <br>
Risk: Document updates may affect shared or business-critical content. <br>
Mitigation: Inspect method schemas with gws schema and review proposed params or JSON payloads before execution. <br>


## Reference(s): <br>
- [Gws Docs on ClawHub](https://clawhub.ai/googleworkspace-bot/gws-docs) <br>
- [gws docs CLI help](gws docs --help) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and a Google account with the intended Docs scopes.] <br>

## Skill Version(s): <br>
1.0.12 (source: release evidence; skill metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
