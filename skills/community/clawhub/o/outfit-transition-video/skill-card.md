## Description: <br>
Generate vertical shorts of anthropomorphic outfit changes on beat using WeryAI, including one-second cuts, style jumps, and accessory detail beats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate short vertical fashion-transition videos through WeryAI from a brief, optional public image URLs, and confirmed generation parameters. It is suited for outfit transition reels, look-change clips, and beat-synced accessory macro videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WERYAI_API_KEY, and generation can consume paid WeryAI credits. <br>
Mitigation: Use a scoped or dedicated API key where possible, keep the key out of source control, and confirm parameters before starting paid generation. <br>
Risk: If local image paths are used, the helper can read the local file and upload it to WeryAI to obtain a public image URL. <br>
Mitigation: Prefer public HTTPS image URLs. Only use local paths after reviewing the script and getting explicit user consent for the upload. <br>
Risk: Video generation depends on WeryAI network services and model-specific parameter constraints. <br>
Mitigation: Run with Node.js 18+, verify the selected model supports the requested duration, aspect ratio, and fields, and surface API errors with parameter-fix guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/outfit-transition-video) <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>
- [WeryAI video API host](https://api.weryai.com) <br>
- [WeryAI model and upload API host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request parameters and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return WeryAI task status details, error messages, and playable video URLs after API completion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
