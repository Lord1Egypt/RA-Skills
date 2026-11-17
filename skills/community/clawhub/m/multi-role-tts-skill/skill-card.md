## Description:

Multi-role TTS Skill helps agents generate multi-character dialogue audio with configurable Edge TTS voices and FFmpeg-based audio merging and spatial effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsun4414](https://clawhub.ai/user/johnsun4414)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn role-labeled dialogue scripts into generated voice audio for training, service simulations, education, entertainment, and accessibility workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer steps may make global system changes, including package installation and copying files into OpenClaw or system paths.

Mitigation: Review install.sh before use, install dependencies manually where possible, and avoid sudo unless global installation is intended.

Risk: Dialogue text is submitted to Edge TTS for audio generation.

Mitigation: Do not process sensitive, confidential, or regulated text unless the external TTS service is approved for that data.

Risk: The main shell generator appears broken or truncated in security evidence, which may cause reliability issues.

Mitigation: Test the generator with non-sensitive sample scripts before production use and prefer the Python generator if the shell script fails validation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnsun4414/skills/multi-role-tts-skill)
- [Edge TTS package](https://github.com/rany2/edge-tts)
- [FFmpeg documentation](https://ffmpeg.org/documentation.html)
- [OpenClaw](https://openclaw.ai)
- [Usage guide](docs/usage-guide.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Audio files and Markdown or terminal guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires edge-tts and ffmpeg; generated audio may include temporary intermediate files unless cleanup is enabled.]

## Skill Version(s):

1.0.1 (source: server release metadata, frontmatter metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
