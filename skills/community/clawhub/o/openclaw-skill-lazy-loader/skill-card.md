## Description: <br>
Dramatically reduce per-session token usage by loading skills and context files only when needed, not at session start. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Asif2BD](https://clawhub.ai/user/Asif2BD) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to replace eager skill loading with a lightweight SKILLS catalog, task-based loading rules, and an optional local recommendation helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lazy-loading instructions could introduce incorrect or unwanted AGENTS.md behavior if merged without review. <br>
Mitigation: Review AGENTS.md changes before merging them into an agent workspace. <br>
Risk: A SKILLS catalog that references untrusted skill paths could cause an agent to load untrusted instructions. <br>
Mitigation: Keep SKILLS.md limited to trusted skill paths and treat helper recommendations as advisory. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/Asif2BD/openclaw-skill-lazy-loader) <br>
- [Publisher profile](https://clawhub.ai/user/Asif2BD) <br>
- [Project homepage](https://github.com/Asif2BD/openclaw-skill-lazy-loader) <br>
- [OpenClaw Token Optimizer](https://clawhub.ai/Asif2BD/openclaw-token-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, templates, and optional plain-text CLI recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory recommendations; users should review AGENTS.md changes and keep SKILLS.md limited to trusted skill paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
