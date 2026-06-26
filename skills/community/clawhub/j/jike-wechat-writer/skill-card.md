## Description: <br>
Guides an agent through the full WeChat public-account article workflow, including topic discovery, style analysis, drafting, image planning, and styled HTML rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzoob](https://clawhub.ai/user/mzoob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to plan, draft, revise, illustrate, and format WeChat public-account articles. It helps agents call the bundled 100City-backed tools for trend search, WeChat style analysis, image generation, and Markdown-to-HTML rendering when the required API key is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send search terms, URLs, prompts, and image-generation requests to the 100City API. <br>
Mitigation: Use only when that data sharing is acceptable, configure the API key through the environment where possible, and ask before submitting sensitive or third-party URLs. <br>
Risk: The skill gives the agent broad permission to remember user preferences. <br>
Mitigation: Ask before writing memory and keep remembered content limited to preferences or reusable writing context the user has agreed to store. <br>
Risk: The skill may overwrite draft files during article generation or formatting. <br>
Mitigation: Require confirmation before overwriting existing drafts and preserve a copy when revising user-provided work. <br>
Risk: The key-check command may reveal partial API-key information in shared logs. <br>
Mitigation: Avoid running key checks in shared transcripts or logs, and prefer environment-based secret management. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mzoob/jike-wechat-writer) <br>
- [Module A: Topic and Direction Confirmation](references/module-a-topic.md) <br>
- [Module B: Memory Adaptation](references/module-b-memory.md) <br>
- [Module C: Style Following](references/module-c-style.md) <br>
- [Module D: Drafting and Iteration](references/module-d-writing.md) <br>
- [Module E: Image Strategy](references/module-e-image.md) <br>
- [Module F: WeChat Styling](references/module-f-styling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown drafts, command guidance, JSON-capable CLI output, and styled HTML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a 100CITY_API_KEY or configured API key for API-backed search, style analysis, and image generation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
