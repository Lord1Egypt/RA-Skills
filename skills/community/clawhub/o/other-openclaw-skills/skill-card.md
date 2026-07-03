## Description: <br>
Routes requests across Meitu image and video workflows, including poster generation, stickers, visual try-on, product editing, video generation, upscaling, ID photos, cutouts, carousels, beauty enhancement, platform adaptation, and direct Meitu CLI execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongjie-oss](https://clawhub.ai/user/dongjie-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill pack to route image and video generation or editing requests to the appropriate Meitu scene skill or CLI-backed workflow. It supports creative, commerce, identity-photo, portrait, background-removal, adaptation, and direct command-execution tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API credentials may be exposed if users follow prompts that ask them to paste AK/SK into chat. <br>
Mitigation: Configure credentials through environment variables or a protected local credentials file, and avoid sharing secrets in conversation. <br>
Risk: Personal photos, profile facts, and visual preferences may persist across tasks through shared visual memory behavior. <br>
Mitigation: Review and limit stored visual memory and reference photos before use, especially for sensitive personal, biometric, business, or client images. <br>
Risk: Image and video workflows depend on Meitu API processing and local credential access. <br>
Mitigation: Use the skill only for content that is appropriate to process with Meitu services, and restrict credential file permissions in shared or CI environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongjie-oss/other-openclaw-skills) <br>
- [Security model](SECURITY.md) <br>
- [Meitu tools execution hub](meitu-tools/SKILL.md) <br>
- [Visual workflow guide](skills/meitu-visual-me/references/workflows.md) <br>
- [Poster output formats](skills/meitu-poster/references/output-formats.md) <br>
- [Product-view e-commerce specs](skills/meitu-product-view/references/ecommerce-specs.md) <br>
- [ID photo specification database](skills/meitu-id-photo/references/spec-database.md) <br>
- [Image adaptation platform presets](skills/meitu-image-adapt/references/platform-presets.md) <br>
- [Meitu Open Platform](https://www.miraclevision.com/open-claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets and shell command examples; direct tool execution can return JSON fields with task IDs, media URLs, and results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media is returned through Meitu CLI workflows when execution succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
