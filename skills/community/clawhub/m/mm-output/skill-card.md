## Description:

Parse PDF or Markdown files into structured HTML posters with multi-modal output formats, or generate poster and slide images through Gemini image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuriyanzexuan](https://clawhub.ai/user/yuriyanzexuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to transform PDF or Markdown source material into styled HTML posters, converted document outputs, and generated poster or slide imagery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and dependency setup can change the local environment and includes curl-to-shell installation behavior.

Mitigation: Review before installing, run in a sandbox or disposable environment, avoid running install.sh as root, and replace curl-to-shell installation with verified packages where possible.

Risk: The HTML rendering and document conversion pipeline can expose users to unsafe content when processing untrusted documents.

Mitigation: Only process trusted documents unless JavaScript is disabled and generated HTML is sanitized before conversion.

Risk: Dependency choices include vulnerable pins or unpinned Git-sourced components according to release security guidance.

Mitigation: Remove or pin Git dependencies and update vulnerable dependency pins before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuriyanzexuan/skills/mm-output)
- [Artifact README](artifact/README.md)
- [MMOutput README](artifact/mm_output/README.md)
- [UV package manager](https://github.com/astral-sh/uv)
- [Marker PDF dependency](https://github.com/Hadlay-Zhang/marker.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands, configuration examples, generated HTML, PDF, PNG, DOCX, PPTX, and image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Python 3.12, LLM or image-generation API credentials, and Chromium-compatible rendering dependencies.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
