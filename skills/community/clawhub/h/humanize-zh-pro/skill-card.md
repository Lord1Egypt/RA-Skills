## Description: <br>
中文去AI味 Pro helps agents transform mechanical AI-generated Chinese text into more natural human-facing writing across Zhihu, Xiaohongshu, WeChat public account, Moments, and general casual styles, with local AI-taste scoring prompts and style guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaryn-hs](https://clawhub.ai/user/aaryn-hs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content teams, and developers use this skill to prepare Chinese rewrite prompts, style-specific drafting guidance, and local AI-taste checks for text intended to sound less formulaic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated rewrite prompts or style guidance may preserve inaccurate, misleading, or unsuitable claims from the original draft. <br>
Mitigation: Review the rewritten text for factual accuracy, tone, and audience fit before publishing or sharing it. <br>
Risk: Using an output path can overwrite an existing local file. <br>
Mitigation: Choose output paths deliberately and keep backups of important drafts before running the scripts. <br>
Risk: Private drafts could be exposed if a user sends generated prompts or source text to an external AI service. <br>
Mitigation: Do not submit confidential text to external services unless that sharing is approved and intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaryn-hs/humanize-zh-pro) <br>
- [Homepage](https://github.com/renyetu/humanize-zh-pro) <br>
- [Deep style guide](references/style-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and shell output containing rewrite prompts, style guidance, and AI-taste score reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read text from files or stdin and may write generated prompt text to a requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
