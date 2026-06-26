## Description: <br>
Create AI images with GPT Image, Gemini Nano Banana, FLUX, Imagen, and top providers using prompt engineering, style control, and smart editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creative teams use this skill to choose image generation and editing providers, write stronger prompts, configure provider access, and plan model-specific workflows for AI visuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images may be sent to the selected third-party image provider. <br>
Mitigation: Use only providers trusted for the content being processed, and remove confidential details from prompts or reference assets before generation. <br>
Risk: API keys could be exposed if pasted into chat or stored in ordinary text. <br>
Mitigation: Keep provider keys in environment variables or platform secret configuration, and avoid including secrets in prompts, memory, or logs. <br>
Risk: Local memory may contain sensitive project context or provider preferences. <br>
Mitigation: Periodically review or delete ~/image-generation/memory.md when it contains confidential or stale context. <br>
Risk: Model names, aliases, and benchmark rankings can drift over time. <br>
Mitigation: Resolve aliases to current provider model IDs and recheck current rankings before quality-critical generation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/image-generation-zhouli) <br>
- [Skill homepage](https://clawic.com/skills/image-generation) <br>
- [Setup guide](setup.md) <br>
- [API patterns](api-patterns.md) <br>
- [Benchmark snapshot](benchmarks-2026.md) <br>
- [Image prompting guide](prompting.md) <br>
- [GPT Image](gpt-image.md) <br>
- [Google Image Models](gemini.md) <br>
- [FLUX](flux.md) <br>
- [Stable Diffusion](stable-diffusion.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, API request examples, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer to local memory in ~/image-generation/ and selected provider APIs; the skill itself does not persist generated images unless the user asks to save them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
