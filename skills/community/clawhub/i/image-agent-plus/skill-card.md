## Description: <br>
Use image-agent-plus CLI to generate images, prioritizing image2 for high-quality text and prompt-following, with Codex/Gemini fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webkubor](https://clawhub.ai/user/webkubor) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent users use this skill to invoke image-agent-plus for prompt-based image generation, choosing image2 when OpenAI credentials are available and falling back to Codex or Gemini local runtimes when appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Direct provider mode can require sensitive OpenAI credentials. <br>
Mitigation: Use dedicated, appropriately scoped credentials through the user's normal shell or agent secret manager, and prefer local Codex or Gemini runtimes when direct API access is not needed. <br>
Risk: The security scan reports a review helper that defaults to nested Codex with full filesystem sandbox bypass. <br>
Mitigation: Install only in a trusted maintainer environment, review the helper before use, and disable full-access mode with --no-yolo or the documented environment override when possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/webkubor/image-agent-plus) <br>
- [Project Homepage](https://github.com/webkubor/image-agent-plus) <br>
- [Showcase Image](https://raw.githubusercontent.com/webkubor/image-agent-plus/main/skills/image-agent-plus/assets/ai-era-editorial-poster.png) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; generated image files are written by the CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports prompt, provider, filename, aspect ratio, model, and output-count options; direct image2 API mode may require OpenAI credentials.] <br>

## Skill Version(s): <br>
2.0.5 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
