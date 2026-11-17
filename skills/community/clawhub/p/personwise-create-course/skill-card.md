## Description:

Create, refine, resume, publish, or query polished PersonWise courses from topics, supplied text, documents, or reference images using the PersonWise CLI and browser OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[personwiseai](https://clawhub.ai/user/personwiseai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through staged PersonWise course authoring, including blueprint design, document upload, checkpoint review, visual QA, publishing or access setup, and completion evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update a user-local PersonWise CLI and requires browser OAuth.

Mitigation: Use only the bundled pinned bootstrap or service-provided update command, require explicit approval for install or update, and never handle passwords, tokens, authorization codes, cookies, or other secrets.

Risk: Course creation can upload selected materials and consume existing course credits.

Mitigation: Upload only user-named, attached, selected, or explicitly approved files; run readiness before new course creation; stop on insufficient credit; and never purchase credits automatically.

Risk: Link access, publishing, or Topics submission can expose course content beyond the authoring account.

Mitigation: Default new courses to private unless broader access is requested, require fresh state before access changes, and report only URLs whose returned state proves the intended access mode and playability.

## Reference(s):

- [Connect and authorize the PersonWise CLI](references/connection-and-auth.md)
- [Design a high-quality PersonWise course](references/course-design.md)
- [Course classes, teaching archetypes, and editorial authority](references/course-archetypes.md)
- [PersonWise CLI workflow and recovery](references/workflow.md)
- [Capability-aware visual quality](references/visual-quality.md)
- [ClawHub skill page](https://clawhub.ai/personwiseai/skills/personwise-create-course)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with JSON command inputs and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include secret-free course blueprints, review findings, CLI commands, access-state summaries, and completion evidence.]

## Skill Version(s):

2.1.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
