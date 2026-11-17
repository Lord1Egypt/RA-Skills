## Description:

Generate AI images via the GoAI API for image creation, editing, rendering, posters, avatars, photos, concept art, and Chinese-language image requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goai](https://clawhub.ai/user/goai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate or edit images through GoAI while preserving the user's original prompt language and optionally using local or remote reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A changed or untrusted GOAI_BASE_URL endpoint could receive credentials or prompts.

Mitigation: Use the default production endpoint unless you control and trust the override endpoint.

Risk: Local reference images are uploaded before generation and may contain sensitive content.

Mitigation: Provide local reference images only when their upload to GoAI is intended.

Risk: Remote media downloads and broad local file writes can affect the user's workspace.

Mitigation: Review generated output paths and prefer a release that constrains downloads to a safe output directory.

Risk: Runtime dependency setup can download Python packages during first use.

Mitigation: Install only in trusted OpenClaw environments and review dependency pinning before deployment.

## Reference(s):

- [GoAI homepage](https://mustgoai.com)
- [ClawHub skill page](https://clawhub.ai/goai/skills/goai-image-gen)
- [Publisher profile](https://clawhub.ai/user/goai)

## Skill Output:

**Output Type(s):** [Shell commands, Files, URLs, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated image file and URL outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [On success, the script prints MEDIA, MEDIA_URL, RESULT_PATH, and RESULT_URL lines and saves the generated image as a local PNG file.]

## Skill Version(s):

1.0.1 (source: server release; artifact frontmatter and pyproject.toml remain 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
