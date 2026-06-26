## Description: <br>
Converts Markdown articles into platform-ready content for WeChat Official Accounts, Zhihu, and Toutiao, with code formatting, AI writing assistance, AI cover image generation, and draft publishing support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuesf](https://clawhub.ai/user/yuesf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and content operators use this skill to convert Markdown into publication-ready drafts, generate or revise article content, create cover images, and send drafts to WeChat Official Accounts, Zhihu, or Toutiao. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use real WeChat, Zhihu, and Toutiao credentials to create drafts or publish content. <br>
Mitigation: Prefer test accounts, limit credential scope where possible, and review each generated or converted article before publication. <br>
Risk: Drafts, prompts, and article content may be sent to configured AI or conversion providers. <br>
Mitigation: Avoid sending confidential content to external providers unless approved, and configure providers according to the user's data handling requirements. <br>
Risk: The AI de-tracing feature can be misused to obscure AI authorship or bypass platform disclosure expectations. <br>
Mitigation: Do not use de-tracing to evade disclosure, authorship, or platform policy requirements. <br>
Risk: Account cookies and API keys are needed for several workflows. <br>
Mitigation: Avoid storing browser cookies in plaintext configuration and rotate credentials if local configuration files are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuesf/multi-writing-skills) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Skill tutorial](docs/skill-tutorial.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, HTML, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or HTML content, CLI command guidance, configuration values, generated image outputs, and platform draft or publish results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call configured publishing platforms and AI providers, and may write converted articles or generated assets to local files.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
