## Description:

Creates and manages autonomous Manus tasks through the Manus API, including task creation, status polling, and retrieval of generated files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvanhorn](https://clawhub.ai/user/mvanhorn)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to delegate research, document creation, coding, and other multi-step work to Manus, then poll task status and collect generated deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shareable Manus task links may expose task context or results beyond the intended audience.

Mitigation: Avoid shareable links unless access scope and duration are understood, and avoid using sensitive prompts or documents unless this risk is acceptable.

Risk: Remote agent-generated files are downloaded locally with weak safeguards.

Mitigation: Use a dedicated empty output directory and inspect downloaded files before opening, executing, or sharing them.

## Reference(s):

- [Manus API Reference](https://open.manus.ai/docs)
- [Manus Docs](https://manus.im/docs)
- [ClawHub Skill Page](https://clawhub.ai/mvanhorn/skills/manus)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Files, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MANUS_API_KEY; may download remote Manus-generated output files locally.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
