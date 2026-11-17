## Description:

Guides setup of Loudkit voice notes for an existing agent and messenger using a local companion on an Apple Silicon Mac.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pepinu](https://clawhub.ai/user/pepinu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users assess compatibility, configure local speech for their existing agent and messenger, and verify a voice-note round trip without replacing the agent's session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running setup on an unintended machine or without required local resources may disrupt the intended workflow.

Mitigation: Review the companion repository, check Mac prerequisites and disk space, and run setup only on the intended Mac.

Risk: Changing agent or messenger configuration may expose credentials or disrupt an existing connection.

Mitigation: Keep credentials in local configuration, back up changed files, preserve agent sessions and tools, and use only a bridge compatible with the user's account.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/pepinu/skills/loudkit-voice)
- [Loudkit agent setup guide](https://loudkit.loudreader.io/agents/llms.txt)
- [Loudkit Voice companion README](https://github.com/loudreader/loudkit-voice#readme)
- [Hermes voice documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/voice-mode)
- [OpenClaw audio documentation](https://docs.openclaw.ai/nodes/audio)
- [OpenClaw TTS configuration](https://docs.openclaw.ai/tools/tts/configuration)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports compatibility blockers and distinguishes local speech tests from verified messenger delivery.]

## Skill Version(s):

0.1.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
