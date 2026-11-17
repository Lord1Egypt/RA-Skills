## Description:

Generates Mandarin dual-host podcast scripts from topics, URLs, or PDFs, with optional persona styling and stereo TTS audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liaozicen666-tech](https://clawhub.ai/user/liaozicen666-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn articles, PDFs, or free-form topics into Mandarin two-host podcast content. It supports configurable dialogue styles, persona selection or extraction, and optional text-to-speech audio generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe URL fetching can expose the runtime to untrusted web content or unintended network destinations.

Mitigation: Install and run the skill in an isolated local environment, avoid internal network access, and do not pass untrusted URLs.

Risk: Broad local file writes can create or overwrite generated podcast outputs in user-selected directories.

Mitigation: Use a dedicated output directory with least-privilege filesystem access and review generated files before sharing or deploying them.

Risk: Plaintext credential handling can expose API or TTS credentials if they are stored in local files.

Mitigation: Prefer environment variables or a credential manager, rotate or remove embedded TTS credentials, and avoid saving private secrets in the skill directory.

Risk: Hidden process-wide proxy changes can affect network behavior for the running agent process.

Mitigation: Run in an isolated process and review network configuration before use in production or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liaozicen666-tech/skills/personalized-podcast-mandarin)
- [README](README.md)
- [Development guide](DEVELOPMENT.md)
- [External research agent](agents/external-research-agent.md)
- [Research package example](examples/research_package_example.py)
- [High-efficiency delivery style](references/¸ßÐ§´«´ï.md)
- [Divergent conversation style](references/·¢É¢ÂþÌ¸.md)
- [Deep dialogue style](references/Éî¶È¶ÔÌ¸.md)
- [Viewpoint debate style](references/¹Ûµã½»·æ.md)
- [Comedy style](references/Ï²¾ç·ç¸ñ.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, audio files]

**Output Format:** [Markdown, JSON, and optional MP3 files, with command-line and Python API guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include podcast session metadata, research summaries, dialogue scripts, and optional stereo TTS audio when credentials are configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
