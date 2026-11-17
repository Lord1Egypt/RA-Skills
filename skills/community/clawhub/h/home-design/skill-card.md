## Description:

Home Design helps agents produce home renovation planning outputs from floor-plan and requirements evidence, including layout analysis, style guidance, room image prompts, construction-document drafts, electrical and plumbing plans, and material lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yqrpaul](https://clawhub.ai/user/yqrpaul)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect home renovation requirements, analyze a floor plan, propose room layouts and design styles, generate image prompts or optional room renderings, and draft construction, electrical, plumbing, materials, and budget planning documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated construction, electrical, plumbing, material, and code-compliance outputs may be incomplete or unsuitable for real renovation work.

Mitigation: Treat those outputs as conceptual drafts and have licensed local professionals verify them before procurement, permitting, or construction.

Risk: Floor plans, client details, and private room data may be exposed when using remote image-generation services.

Mitigation: Avoid sending sensitive property or client data to remote services unless the user has reviewed and accepted those providers' terms.

Risk: Optional setup guidance includes third-party installation or system commands that may affect the user's environment.

Mitigation: Review third-party setup steps and any privileged commands before running them.

## Reference(s):

- [Home Design ClawHub listing](https://clawhub.ai/yqrpaul/skills/home-design)
- [Construction standards reference](artifact/references/construction.md)
- [Ergonomics reference](artifact/references/ergonomics.md)
- [Materials selection guide](artifact/references/materials.md)
- [Interior style guide](artifact/references/style_guide.md)
- [Stable Diffusion WebUI](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [LiblibAI](https://www.liblib.ai/)
- [TusiArt](https://tusiart.com/)
- [SeaArt](https://www.seaart.ai/)
- [Tongyi Wanxiang](https://wanxiang.aliyun.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON material lists and prompt files, shell commands, configuration snippets, and optional PNG room renderings when an image backend is configured.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are planning drafts; construction, electrical, plumbing, code-compliance, and material recommendations require local professional review before real-world use.]

## Skill Version(s):

2.0.1 (source: server release evidence and artifact/skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
