## Description:

Convert text, images, PDFs, websites, or YouTube videos into multilingual AI-generated podcast audio using Podcastfy's open-source Python toolkit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-11even](https://clawhub.ai/user/mr-11even)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to install and run Podcastfy workflows that turn source material into podcast audio or transcripts through CLI and Python examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Podcast generation can send source material to cloud LLM or text-to-speech providers.

Mitigation: Avoid processing sensitive, medical, dental, confidential, or regulated documents unless consent and compliance approval are in place; use local or transcript-only options where appropriate.

Risk: Installing Podcastfy and FFmpeg introduces normal package supply-chain and system package trust considerations.

Mitigation: Install in a virtual environment, consider pinning Podcastfy to a reviewed version, and only grant sudo for FFmpeg installation when the system package source is trusted.

## Reference(s):

- [Podcastfy GitHub Repository](https://github.com/souzatharsis/podcastfy)
- [Podcastfy Documentation](https://podcastfy.readthedocs.io/)
- [Podcastfy PyPI Package](https://pypi.org/project/podcastfy/)
- [Podcastfy Web App](https://openpod.fly.dev/)
- [ClawHub Skill Page](https://clawhub.ai/mr-11even/skills/podcastfy-openclaw-skill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands and scripts that generate MP3 audio files or TXT transcripts through Podcastfy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
