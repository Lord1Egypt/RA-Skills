## Description: <br>
Create and manage Google Jules AI coding sessions via the Jules REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arthbhalodiya](https://clawhub.ai/user/arthbhalodiya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to start, monitor, guide, and inspect Google Jules coding sessions against connected GitHub repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Jules API key tied to connected GitHub repositories and can initiate coding sessions that change repository content. <br>
Mitigation: Install only when this access is intended, keep the API key scoped and protected, and review generated plans and diffs before accepting changes. <br>
Risk: AUTO_CREATE_PR can allow autonomous pull request creation after a session completes. <br>
Mitigation: Use AUTO_CREATE_PR only for repositories and tasks where autonomous PR creation is acceptable; prefer plan approval for important repositories. <br>
Risk: Deleting or messaging the wrong session could affect an unrelated Jules task. <br>
Mitigation: Verify session IDs before destructive actions or follow-up messages. <br>


## Reference(s): <br>
- [Google Jules API Reference](https://jules.google/docs/api/reference/) <br>
- [Google Jules](https://jules.google) <br>
- [ClawHub Skill Page](https://clawhub.ai/arthbhalodiya/jules-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JULES_API_KEY and curl to call the Jules REST API; jq is used by the helper script for JSON construction and optional formatting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
