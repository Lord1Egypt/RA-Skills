## Description: <br>
Investigates a username across 1000+ social media platforms and websites using social-analyzer, with additional lookup support for Bilibili, Zhihu, and Weibo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guleguleguru](https://clawhub.ai/user/guleguleguru) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and investigators use this skill to check whether a username appears on public social platforms, summarize likely profile matches, and support lawful self-auditing, security research, journalism, or similar public OSINT workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Username queries may be sent to many public websites where requests can be logged or rate-limited. <br>
Mitigation: Use the skill only for lawful, consent-aware public OSINT and limit scan scope when appropriate. <br>
Risk: Installing social-analyzer can modify the user's Python environment. <br>
Mitigation: Prefer installing dependencies in an isolated Python environment. <br>
Risk: Public profile matches can be misinterpreted as identity confirmation. <br>
Mitigation: Present confidence tiers and require human confirmation before treating a match as the same person. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guleguleguru/osint-social) <br>
- [Platform coverage reference](references/platforms.md) <br>
- [social-analyzer](https://github.com/qeeqbox/social-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summary with shell commands and structured findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should prioritize confidence tiers, public profile links, relevant metadata, failed-request notes, and a privacy and ethics reminder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
