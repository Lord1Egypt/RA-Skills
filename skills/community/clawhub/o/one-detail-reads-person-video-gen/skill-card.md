## Description: <br>
Create vertical social-read shorts: one-cue thesis, example beat, playful closer, timed English captions (WeryAI). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and developers use this skill to produce short vertical WeryAI videos about a single social cue, with a thesis, concrete B-roll example, playful closer, and timed English captions. It is intended for psychology hooks, micro-behavior reads, and respectful debate-style short-form content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected image inputs may be sent to WeryAI during generation. <br>
Mitigation: Use the skill only when sharing those prompts or images with WeryAI is acceptable, and avoid sensitive or private inputs. <br>
Risk: Local image paths can be read and uploaded to WeryAI by the helper script. <br>
Mitigation: Prefer public HTTPS image URLs; use local paths only after confirming the file is non-sensitive and explicitly approving upload. <br>
Risk: The skill requires a WERYAI_API_KEY for live model, generation, status, and local-upload operations. <br>
Mitigation: Store the API key in the environment, keep it out of prompts and repositories, and use an isolated or short-lived environment for higher assurance. <br>


## Reference(s): <br>
- [WeryAI Video API reference](resources/WERYAI_VIDEO_API.md) <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/one-detail-reads-person-video-gen) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI JSON examples and generated video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, network access, and WeryAI model parameters for video generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
