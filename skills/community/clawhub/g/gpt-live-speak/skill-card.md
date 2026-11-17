## Description:

Speak aloud through a Linux/ALSA audio device using OpenAI GPT-Live for embodied agents, robots, and other Linux systems with a speaker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frussen-robotics](https://clawhub.ai/user/frussen-robotics)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of embodied agents, robots, or Linux systems use this skill to turn explicit agent speech requests into spoken audio through ALSA using OpenAI GPT-Live.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested speech text is sent to OpenAI with OPENAI_API_KEY for live audio generation.

Mitigation: Do not use the skill for secrets or sensitive text, and review speech content before execution.

Risk: The launcher creates a persistent cached virtual environment and downloads Python dependencies from PyPI.

Mitigation: Review or preinstall dependencies and run the skill in an isolated account when dependency supply-chain risk matters.

Risk: The skill plays generated audio through ALSA on a Linux audio device.

Mitigation: Confirm the target ALSA device and deployment environment before enabling spoken output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frussen-robotics/skills/gpt-live-speak)
- [Skill definition](artifact/SKILL.md)
- [Runtime requirements](artifact/requirements.txt)

## Skill Output:

**Output Type(s):** [Shell commands, Audio, Guidance]

**Output Format:** [Markdown guidance with a Python command that streams PCM audio to ALSA]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENAI_API_KEY, python3, aplay, and Linux/ALSA; voice, ALSA device, and playback buffer are configurable through environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
