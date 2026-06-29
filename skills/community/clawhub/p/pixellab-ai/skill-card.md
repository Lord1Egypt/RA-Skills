## Description: <br>
PixelLab AI helps agents plan and run PixelLab asset workflows for pixel-art images, conversions, rotations, animations, layered sprites, tilesets, UI assets, prompt enhancement, and consistent game-art packs using the user's own PixelLab API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uncmatteth](https://clawhub.ai/user/uncmatteth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, game artists, and agent users use this skill to turn PixelLab-named asset requests into scoped visual briefs, manifests, API payloads, live PixelLab runs, downloaded candidates, approval galleries, and validation reports for game-ready pixel art. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PixelLab API requests can send prompts, payload JSON, and optional user-provided reference images to PixelLab. <br>
Mitigation: Install only when intending to use PixelLab, review payloads before live runs, and avoid including sensitive or unapproved inputs in prompts, payloads, or reference images. <br>
Risk: PIXELLAB_API_KEY grants access to the user's PixelLab account for live generation. <br>
Mitigation: Keep the key in a local environment variable or secret manager, do not paste it into chat or commit it, and use only the official PixelLab API base unless testing a trusted endpoint explicitly. <br>
Risk: Live runs with explicit approval can spend PixelLab credits. <br>
Mitigation: Use manifest planning, linting, budget checks, and balance preflight before running commands with --yes. <br>
Risk: Generated and downloaded assets are written to local output folders. <br>
Mitigation: Use a dedicated output folder, inspect candidates and approval galleries, and validate sprites before treating assets as game-ready. <br>


## Reference(s): <br>
- [PixelLab AI ClawHub Release](https://clawhub.ai/uncmatteth/skills/pixellab-ai) <br>
- [PixelLab Account](https://www.pixellab.ai/) <br>
- [PixelLab API Token Page](https://api.pixellab.ai/mcp) <br>
- [PixelLab MCP/API Documentation](https://api.pixellab.ai/mcp/docs) <br>
- [Endpoint Mapping](artifact/references/endpoint-mapping.md) <br>
- [API Coverage Matrix](artifact/references/api-coverage-matrix.md) <br>
- [Install And Secrets](artifact/references/install-and-secrets.md) <br>
- [Prompt Cheatsheet](artifact/references/prompt-cheatsheet.md) <br>
- [Sprite Animation Layering](artifact/references/sprite-animation-layering.md) <br>
- [YouTube Workflow Playbook](artifact/references/youtube-workflow-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls, Files] <br>
**Output Format:** [Markdown guidance with JSON manifests, shell commands, configuration snippets, and local file paths or result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live runs require PIXELLAB_API_KEY and write manifests, payloads, results, logs, downloads, galleries, approvals, and reports under the selected output folder.] <br>

## Skill Version(s): <br>
1.5.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
