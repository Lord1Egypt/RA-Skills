## Description:

Runs OpenClaw on low-RAM machines (2-4 GB) by trimming context, throttling skills, and checking memory before heavy operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirajmahmudul](https://clawhub.ai/user/mirajmahmudul)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users enable this skill on low-RAM machines to reduce memory pressure before heavy operations, keep responses compact, and throttle browser or image workflows when available RAM is low.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically stop tasks, trim conversation context, or disable browser and image workflows when memory is low.

Mitigation: Enable it only for low-memory sessions and review user-facing notices so affected users understand when capabilities were skipped or context was trimmed.

Risk: Short responses and context trimming may omit details from long-running work.

Mitigation: Ask the agent to preserve critical decisions before trimming and re-send important context after gateway restarts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirajmahmudul/skills/lite-mode)
- [Project Homepage](https://github.com/mirajmahmudul/openclaw-lite-mode)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown responses with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps default replies short, emits memory status when requested, and may recommend temporary tool throttling or gateway restart steps.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
