## Description: <br>
RSS监控技能 - 监控RSS/Atom订阅源，检测更新，获取新内容。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and content teams use this skill to parse RSS/Atom feeds, check for new entries, filter categories, and monitor blogs, news, podcasts, or social media feeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetching arbitrary RSS/Atom URLs can contact untrusted, localhost, or private-network endpoints if the user provides them. <br>
Mitigation: Use trusted public feed URLs unless private-network access is intentional, and review new versions that add background polling, saved history, or broader network access. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/534422530/laosi-rss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch user-provided RSS/Atom URLs; examples require the Python feedparser package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
