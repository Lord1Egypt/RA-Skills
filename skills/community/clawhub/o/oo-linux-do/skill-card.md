## Description: <br>
Helps an agent search and read Linux DO content through OOMOL's linux_do connector and oo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to discover and read Linux DO topics, posts, category feeds, tag feeds, group activity, badge grants, and user activity through read-only CLI actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party OOMOL oo CLI and includes installer commands for first-time setup. <br>
Mitigation: Install or authenticate the CLI only when needed, and use the installer only after deciding to trust OOMOL's distribution path. <br>
Risk: Linux DO feeds can return rate limits or 404 responses for private or anonymously inaccessible resources. <br>
Mitigation: Treat 404 responses as access ambiguity, retry rate-limited requests later, and avoid over-interpreting unavailable feed data. <br>


## Reference(s): <br>
- [ClawHub Linux DO Skill](https://clawhub.ai/oomol/oo-linux-do) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Linux DO](https://linux.do) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions are documented as read-only; the skill directs agents to inspect the live connector schema before sending JSON payloads.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
