## Description: <br>
Generate images from text prompts using FLUX via Together.ai. Returns image URL. Prompts are auto-enhanced for best results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unixlamadev-spec](https://clawhub.ai/user/unixlamadev-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and agents use this skill to generate original visual assets from natural-language prompts, including logos, illustrations, concept visuals, report imagery, and presentation assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and a spend token are sent to AIProx for paid external image generation. <br>
Mitigation: Install only if AIProx is trusted for submitted prompts and payment handling; avoid secrets or private data in prompts and prefer a scoped or spending-limited token when available. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/unixlamadev-spec/image-gen-bot) <br>
- [AIProx Homepage](https://aiprox.dev) <br>
- [AIProx Orchestration Endpoint](https://aiprox.dev/api/orchestrate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON responses containing generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are returned as URLs; optional width, height, and step settings affect image generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
