## Description: <br>
Extracts character personality from novels, scripts, and anime materials and generates SoulPod packages for Memory-Inhabit dialogue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evangeliona](https://clawhub.ai/user/evangeliona) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Memory Trace to turn character source materials into Memory-Inhabit SoulPod persona packages, including profiles, prompts, memory files, and voice configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can guide the agent to search the web, download media, and install a search dependency. <br>
Mitigation: Require a dry-run and explicit approval before any network access, download, or SkillHub install. <br>
Risk: Generated personas and assets may be deployed into Memory-Inhabit and may overwrite existing persona directories. <br>
Mitigation: Review generated files first, keep backups of existing personas, and approve each deployment or overwrite step explicitly. <br>
Risk: Character images, audio, recognizable voices, or real-person materials may raise licensing, likeness, or consent concerns. <br>
Mitigation: Use user-provided or licensed source materials and avoid cloning real people or recognizable voices without proper rights and consent. <br>
Risk: The skill creates persistent persona packages that can influence later conversations. <br>
Mitigation: Inspect the generated profile, prompts, memories, and configuration before making the package available to downstream agents. <br>


## Reference(s): <br>
- [Memory Trace product page](https://memory-series.github.io/#/product/trace) <br>
- [ClawHub Memory Trace release page](https://clawhub.ai/evangeliona/memory-trace) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/evangeliona) <br>
- [Origin material structure](origin/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, configuration, shell commands, files, guidance] <br>
**Output Format:** [SoulPod file package with JSON, Markdown/text prompts, configuration files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated packages may include profile.json, system_prompts.txt, config.json, raw_memories.json, universal_prompt.txt, story_baseline.txt, and optional image or audio assets.] <br>

## Skill Version(s): <br>
1.1.7 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
