## Description: <br>
Create and manage AI agent tasks via Manus API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvanhorn](https://clawhub.ai/user/mvanhorn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to create, monitor, and retrieve deliverables from Manus autonomous AI tasks through the Manus API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and files sent to Manus are handled by an external service. <br>
Mitigation: Use the skill only for data Manus is approved to process, and avoid sending secrets or regulated information unless that use has been reviewed. <br>
Risk: Shareable links and downloaded task outputs can expose or carry untrusted content. <br>
Mitigation: Handle share links carefully, download outputs directly when needed, and review or scan files before opening or redistributing them. <br>
Risk: The skill requires a Manus API key. <br>
Mitigation: Store MANUS_API_KEY securely and avoid committing or sharing it in prompts, logs, or configuration files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mvanhorn/manus) <br>
- [Manus API documentation](https://open.manus.ai/docs) <br>
- [Manus documentation](https://manus.im/docs) <br>
- [Manus homepage](https://manus.im) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MANUS_API_KEY and may download files produced by Manus tasks.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
