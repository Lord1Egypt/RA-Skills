## Description: <br>
Plume NoteCard helps agents convert topics, long-form text, reference images, and slide-deck requests into generated information-card images through the Plume service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dake6767](https://clawhub.ai/user/dake6767) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to plan, create, retry, package, and deliver notecards or image-based notecard slide decks from user-provided topics, articles, or reference images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User text and selected reference images are sent to Plume for processing. <br>
Mitigation: Avoid sensitive documents or images unless that transfer is acceptable for the use case. <br>
Risk: The skill requires a PLUME_API_KEY and can be affected by local EXTEND.md configuration. <br>
Mitigation: Use a revocable API key and review .plume-notecard/EXTEND.md or ~/.plume-notecard/EXTEND.md before use. <br>
Risk: The skill keeps local task history and generated media paths. <br>
Mitigation: Treat local history and generated files as user data and clear them according to the deployment's retention policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dake6767/plume-notecard) <br>
- [Publisher profile](https://clawhub.ai/user/dake6767) <br>
- [Plume notecard service](https://design.useplume.app/notecard) <br>
- [Template gallery](https://design.useplume.app/notecard/templates?lang=en) <br>
- [Notecard modes and parameters](references/modes.md) <br>
- [Workflow examples](references/workflows.md) <br>
- [Error codes reference](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Files, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command results; generated artifacts are image files, PDFs, or ZIP archives.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PLUME_API_KEY and may store local task history and generated media paths.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence, created 2026-04-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
