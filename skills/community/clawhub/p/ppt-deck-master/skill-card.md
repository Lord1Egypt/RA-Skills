## Description: <br>
Ppt Deck Master helps an agent turn a presentation request into a polished slide deck workflow, covering planning, copy, visual direction, AI image generation, QA iteration, and delivery with Ofox or OpenRouter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dizhu](https://clawhub.ai/user/dizhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external consultants, and creators use this skill to plan, write, visually specify, generate, and iterate product demos, pitch decks, sales materials, training materials, and client reports. It is especially oriented toward high-quality Chinese-language decks that need controlled prompts, page-by-page QA, and reproducible single-slide regeneration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Slide prompts may be sent to Ofox or OpenRouter and could expose sensitive client or business information. <br>
Mitigation: Avoid secrets and sensitive client data in prompts; use approved data handling practices before sending content to third-party APIs. <br>
Risk: The skill requires API credentials for image generation. <br>
Mitigation: Use dedicated API keys with spending limits and keep credentials in environment variables rather than slide files or prompts. <br>
Risk: The workflow includes commands that copy, overwrite, or remove generated slide files during iteration. <br>
Mitigation: Review commands before running them and preserve any accepted outputs before rerunning or deleting individual slides. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dizhu/ppt-deck-master) <br>
- [Brainstorming template](references/Brainstorming模板.md) <br>
- [Prompt guide](references/Prompt指南.md) <br>
- [QA fix mode](references/QA修复模式.md) <br>
- [Writing principles](references/写作原则.md) <br>
- [Self-review checklist](references/自审清单.md) <br>
- [Visual strategy](references/视觉策略.md) <br>
- [Ofox image generation endpoint](https://api.ofox.ai/v1/images/generations) <br>
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with JSON slide specifications and shell commands; generated assets are JPG slide images and a PPTX when the included script is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OFOX_API_KEY or OPENROUTER_API_KEY; python-pptx is optional for PPTX assembly.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
