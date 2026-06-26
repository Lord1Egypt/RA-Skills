## Description: <br>
Guides OpenClaw skill authors through publishing and updating skills on ClawHub while keeping GitHub Releases, metadata, changelogs, and review checklists aligned. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aliramw](https://clawhub.ai/user/aliramw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this documentation skill to prepare OpenClaw skill releases, publish them to ClawHub, create matching GitHub Releases, and troubleshoot common metadata or CLI publishing issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents a manual API publishing workaround that may involve handling a locally stored ClawHub token. <br>
Mitigation: Prefer the normal clawhub login, publish, and sync workflows; only handle local tokens deliberately in a trusted environment and avoid copying, printing, or reusing them. <br>
Risk: Manual workspace synchronization writes skill files into the agent workspace. <br>
Mitigation: Run workspace synchronization only as an explicit action in a trusted local environment after reviewing the target path. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aliramw/marila-skill-publish) <br>
- [ClawHub Review Checklist](references/clawhub-review-checklist.md) <br>
- [dingtalk-ai-table Homepage](https://github.com/aliramw/dingtalk-ai-table) <br>
- [ClawHub Skill Format Specification](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md) <br>
- [ClawHub Security Guidelines](https://github.com/openclaw/clawhub/blob/main/docs/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes publishing checklists, versioning guidance, troubleshooting steps, and security cautions.] <br>

## Skill Version(s): <br>
1.0.8 (source: server evidence, SKILL.md frontmatter, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
