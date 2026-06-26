## Description: <br>
Create AI images with GPT Image, Gemini Nano Banana, FLUX, Imagen, and top providers using prompt engineering, style control, and smart editing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to choose image-generation providers, write stronger prompts, plan edits, and manage cost-aware fallback workflows across hosted and local image models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images can be sent to external image providers selected by the user. <br>
Mitigation: Use only providers approved for the content, avoid confidential material in prompts or references, and confirm provider data-handling terms before use. <br>
Risk: API keys and provider access can create unintended spend or expose broader account privileges. <br>
Mitigation: Use scoped or budget-limited API keys and rotate or revoke keys that are no longer needed. <br>
Risk: Local memory and optional history files may contain sensitive project context. <br>
Mitigation: Review, redact, or delete ~/image-generation/memory.md and history.md when they may contain sensitive information. <br>
Risk: Model names, aliases, availability, and leaderboard rankings can change quickly. <br>
Mitigation: Resolve aliases to official provider model IDs and recheck current provider documentation or rankings before quality-critical work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/image-generation) <br>
- [Skill Homepage](https://clawic.com/skills/image-generation) <br>
- [Setup - AI Image Generation](artifact/setup.md) <br>
- [API Patterns (2026)](artifact/api-patterns.md) <br>
- [Benchmark Snapshot (2025-2026)](artifact/benchmarks-2026.md) <br>
- [Image Prompting Guide (2026)](artifact/prompting.md) <br>
- [GPT Image (OpenAI)](artifact/gpt-image.md) <br>
- [Google Image Models (Gemini + Imagen)](artifact/gemini.md) <br>
- [FLUX (Black Forest Labs)](artifact/flux.md) <br>
- [Stable Diffusion (Local)](artifact/stable-diffusion.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, configuration snippets, and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider selection guidance, prompt templates, fallback chains, local memory setup, and cost-control recommendations.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
