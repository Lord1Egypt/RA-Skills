## Description:

PixelLab AI helps agents plan and run PixelLab asset workflows for pixel-art images, conversions, rotations, animations, layered sprites, modular outfits and equipment, tilesets, UI assets, prompt enhancement, and consistent game-art packs using a user-provided PixelLab API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uncmatteth](https://clawhub.ai/user/uncmatteth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, game creators, and technical artists use this skill to turn asset briefs into PixelLab payloads, manifests, live API runs, downloaded candidates, galleries, approvals, and sprite validation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic asset downloads can fetch unvalidated URLs returned by the PixelLab service and may exceed the declared network scope.

Mitigation: Review before installing, use the default PixelLab API endpoint, and do not enable automatic downloads from untrusted or custom PixelLab endpoints until asset URL validation is added.

Risk: Live generation requires a PixelLab API key and can send prompts, payload JSON, and optional user-provided reference images to PixelLab.

Mitigation: Use only a PixelLab API key you control, keep it in local environment or secret configuration, and avoid pasting or packaging the key.

Risk: Live runs can spend PixelLab credits.

Mitigation: Review generated manifests, payloads, and budget output before using run commands that require explicit generation approval.

## Reference(s):

- [PixelLab AI ClawHub Skill](https://clawhub.ai/uncmatteth/skills/pixellab-ai)
- [PixelLab Account](https://www.pixellab.ai/)
- [PixelLab API Token and MCP](https://api.pixellab.ai/mcp)
- [PixelLab MCP Documentation](https://api.pixellab.ai/mcp/docs)
- [API Coverage Matrix](references/api-coverage-matrix.md)
- [Endpoint Mapping](references/endpoint-mapping.md)
- [Install And Secrets](references/install-and-secrets.md)
- [Prompt Cheatsheet](references/prompt-cheatsheet.md)
- [Sprite Animation Layering](references/sprite-animation-layering.md)
- [YouTube Workflow Playbook](references/youtube-workflow-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON manifests and payload files, compact JSON results, image asset files, and HTML or PNG galleries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live generation requires PIXELLAB_API_KEY; dry-run planning can produce manifests without spending PixelLab credits.]

## Skill Version(s):

1.5.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
