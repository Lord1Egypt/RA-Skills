## Description:

Generates terminal recordings using VHS tape scripts and produces GIF outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create terminal demo recordings for documentation and tutorials. It guides them through preparing and running VHS tape scripts and checking the resulting recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tape scripts can run commands in the recording environment.

Mitigation: Review the tape commands before execution and run them in a restricted environment when appropriate.

Risk: The optional --publish flag makes recordings public.

Mitigation: Use --publish only when public sharing is intended, and check recordings for sensitive content before publishing.

## Reference(s):

- [Scry plugin project](https://github.com/athola/claude-night-market/tree/master/plugins/scry)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-scry-vhs-recording)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [VHS tape files and terminal recordings, typically GIFs, with Markdown guidance and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recording output format and appearance depend on the VHS tape directives.]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
