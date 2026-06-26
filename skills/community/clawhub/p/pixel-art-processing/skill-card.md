## Description: <br>
Pixel Art Processing helps agents guide pixel art and sprite sheet workflows including video frame extraction, GIF and frame conversion, sprite sheet composition and splitting, matting, pixelation, resizing, cropping, and watermark removal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anlinxi](https://clawhub.ai/user/anlinxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, artists, and game creators use this skill to process pixel art, game assets, RPG Maker sprites, GIFs, video frames, and sprite sheets. It supports agent-guided workflows for local image conversion, matting, layout math, and deployment steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backend and deployment helpers can execute local code and may affect unrelated local services. <br>
Mitigation: Review the backend directory and helper scripts before running them, and prefer browser or local Python processing paths for trusted files. <br>
Risk: Exposing the API on a public interface without controls can make processing endpoints reachable by others. <br>
Mitigation: Keep the API bound to localhost unless authentication and firewall rules are in place. <br>
Risk: Watermark or provenance mark removal can create legal or policy issues. <br>
Mitigation: Remove watermarks or provenance marks only when the user has explicit rights to do so. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anlinxi/pixel-art-processing) <br>
- [API Reference](references/api.md) <br>
- [RPG Maker Workflow](references/rpgmaker.md) <br>
- [Sprite Sheet Math](references/sprite_math.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks, command examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in local image, GIF, sprite sheet, ZIP, or JSON index files when users run the included tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
