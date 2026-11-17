## Description:

Uses a local llama.cpp-compatible model to translate PDF, Markdown, and TXT documents on Windows, supporting eight language codes and Markdown output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and document-heavy users use this skill to batch translate local documents through a local llama.cpp-compatible translation server while keeping the normal endpoint on localhost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document text and the configured bearer key may be sent outside the machine if the API URL is changed from localhost to a remote endpoint.

Mitigation: Keep the API URL on localhost for private documents, and use a remote service only when it is trusted to receive the full document text and key.

Risk: The skill depends on local Python packages, llama-server, and a compatible GGUF model that are not bundled with the release.

Mitigation: Use a virtual environment, pin dependencies where practical, and confirm missing installs with the user before downloading or installing components.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-local-pdf-translate)
- [Publisher profile](https://clawhub.ai/user/43622283)
- [README.md](artifact/README.md)
- [Default configuration](artifact/config/default.json)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [Markdown files and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs translated documents as target-language Markdown files; connection checks and configuration commands produce terminal text.]

## Skill Version(s):

2.0.4 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
