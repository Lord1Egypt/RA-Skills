## Description: <br>
Skill Forge automates skill creation by analyzing a request and existing skills, then generating fusion plans, SKILL.md scaffolds, test scripts, agent configuration, workflows, deployment scripts, and optional ClawHub publish metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeman88-tch](https://clawhub.ai/user/freeman88-tch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use Skill Forge to turn natural-language requirements into generated or optimized OpenClaw skill assets and deployable agent templates. It is suited to active skill factory workflows where generated files are reviewed before use or publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite local skill files and generated assets, including batch optimization of a skill workspace. <br>
Mitigation: Run it in a backed-up or test workspace and review generated diffs before adopting the results. <br>
Risk: Publishing options can send generated artifacts to ClawHub with weak review and confirmation boundaries. <br>
Mitigation: Avoid publish flags until content, metadata, permissions, and destination account are checked. <br>
Risk: The release requires sensitive credentials for some workflows. <br>
Mitigation: Use least-privilege or test accounts for browser and publishing workflows, and do not store production secrets in generated files. <br>


## Reference(s): <br>
- [Skill Forge ClawHub release](https://clawhub.ai/freeman88-tch/lobster-skill-forge) <br>
- [Publisher profile: freeman88-tch](https://clawhub.ai/user/freeman88-tch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown, JSON configuration files, Python-generated skill files, shell scripts, and console guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or rewrite local skill files and can prepare or trigger ClawHub publishing when publish options are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
