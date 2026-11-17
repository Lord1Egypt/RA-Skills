## Description:

Generates and edits draw.io artifacts from natural-language prompts without a frontend, with optional image export, context ingestion, shape-library lookup, and visual validation loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzfxxx](https://clawhub.ai/user/lzfxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and diagram authors use this skill to generate, edit, export, and validate draw.io diagrams from prompts, local or URL context, and shape libraries in CLI-based agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files, URL content, images, PDFs, or internal URLs may be forwarded to the configured model provider.

Mitigation: Do not pass secrets, regulated documents, or internal URLs unless the provider policy permits that use.

Risk: Ambient dotenv loading can pick up credentials from a nearby project environment file.

Mitigation: Use --no-dotenv to disable automatic loading, or use --dotenv-file with a trusted explicit path.

Risk: Image export may fall back to the jgraph/drawio Docker image with mounted directory access when the local draw.io CLI is unavailable.

Mitigation: Prefer a vetted local draw.io CLI, or use --no-docker-fallback unless the Docker image and mounted paths have been reviewed.

Risk: The security verdict is suspicious because the release needs review before installation.

Mitigation: Review the skill before installing and use trusted, pinned install sources where possible.

## Reference(s):

- [Capability Parity Notes](references/capability-parity.md)
- [Rendering Notes](references/rendering-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/lzfxxx/skills/prompt-to-drawio)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; generated artifacts are draw.io XML files, optional PNG/SVG/PDF/JPG exports, backup paths, and validation JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful runs surface machine-readable file path lines such as DRAWIO_FILE, IMAGE_FILE, BACKUP_FILE, and VALIDATION_JSON when applicable.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
