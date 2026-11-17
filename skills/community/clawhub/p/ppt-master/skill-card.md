## Description:

AI-driven multi-format SVG content generation system for presentations, social media graphics, and marketing materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzfxxx](https://clawhub.ai/user/lzfxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content teams use this skill to turn Markdown, PDF, or URL source material into SVG-based presentations, social media graphics, posters, and PPTX exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic URL fetching can expose internal networks or retrieve untrusted content.

Mitigation: Run URL conversion only in an isolated environment and avoid cloud or internal-network contexts unless egress and target URLs are controlled.

Risk: Privileged install guidance using curl piped to sudo can execute remote scripts with elevated permissions.

Mitigation: Use trusted package-manager packages, pinned installers, or a sandboxed environment instead of piping remote scripts into a privileged shell.

Risk: Watermark removal can raise rights, attribution, or policy concerns for generated images.

Mitigation: Review image ownership, usage rights, and organizational policy before removing marks or publishing derived assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lzfxxx/skills/ppt-master)
- [GitHub Pages online preview](https://hugohe3.github.io/ppt-master/)
- [README_EN.md](artifact/README_EN.md)
- [Tools guide](artifact/tools/README.md)
- [Role definitions](artifact/roles/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and generated SVG, image, Markdown, and PPTX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project plans, SVG pages, image prompts or assets, speaker notes, and optional PPTX exports through local tools.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
