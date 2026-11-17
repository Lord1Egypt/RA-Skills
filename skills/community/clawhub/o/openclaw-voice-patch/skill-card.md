## Description:

Patches the OpenClaw Control UI with a single microphone button that supports short-click auto-send voice input, hold-for-continuous dictation, live interim transcript display, and state-aware tooltips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elzershark](https://clawhub.ai/user/elzershark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to reapply or validate a Control UI voice-input patch after OpenClaw updates overwrite bundled frontend assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt broad filesystem searches to locate OpenClaw's bundled frontend file.

Mitigation: Confirm the OpenClaw installation path first and prefer a known package location or exact target path over a root-level recursive search.

Risk: The skill text includes a recursive ownership-change command for OpenClaw's dist directory.

Mitigation: Do not run the recursive chown command as written; copy only the exact target file or perform the edit with administrator review while preserving original ownership and permissions.

Risk: The patch edits a minified OpenClaw frontend asset and can break the Control UI if the asset changed between OpenClaw versions.

Mitigation: Back up the target file, verify every documented compatibility pattern before editing, verify all post-patch markers after editing, and use the documented rollback if validation fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elzershark/skills/openclaw-voice-patch)
- [Publisher profile](https://clawhub.ai/user/elzershark)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline code blocks and exact patch strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes compatibility checks, backup and rollback steps, restart guidance, and troubleshooting notes.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
