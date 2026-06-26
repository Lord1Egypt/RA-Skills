## Description: <br>
Generate and edit draw.io artifacts from natural-language prompts without a frontend. Use when the user asks for prompt-to-diagram workflows that need `.drawio` output, optional image export (`png`/`svg`/`pdf`/`jpg`), context ingestion (image/PDF/text/URL), shape-library lookup, or visual validation loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzfxxx](https://clawhub.ai/user/lzfxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, edit, export, and validate draw.io diagrams from natural-language prompts, local context files, URLs, and shape-library references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, selected files, URL-derived text, diagram XML, and validation images may be sent to the configured model provider. <br>
Mitigation: Use only an approved provider for sensitive work and avoid confidential diagrams or attachments unless that provider is authorized. <br>
Risk: The runtime can auto-load nearby .env files. <br>
Mitigation: Use --no-dotenv or an explicit minimal --dotenv-file when running in projects with unrelated secrets. <br>
Risk: Image export or validation can fall back to Docker when local draw.io is unavailable. <br>
Mitigation: Use --no-docker-fallback when Docker execution is not acceptable. <br>


## Reference(s): <br>
- [Capability Parity Notes](references/capability-parity.md) <br>
- [Rendering Notes](references/rendering-notes.md) <br>
- [Shape Library References](https://raw.githubusercontent.com/DayuanJiang/next-ai-draw-io/main/docs/shape-libraries) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated .drawio files, optional image exports, and validation JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated paths are surfaced as DRAWIO_FILE, IMAGE_FILE, BACKUP_FILE, and VALIDATION_JSON when applicable.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
