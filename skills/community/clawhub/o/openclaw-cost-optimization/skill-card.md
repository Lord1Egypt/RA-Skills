## Description: <br>
OpenClaw cost optimization guidance for lowering AI API spending for cost-sensitive users and enterprise deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, teams, and OpenClaw users use this skill to select lower-cost models, configure caching and context limits, set budgets, and monitor API usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence flags the release as suspicious because a bundled autoreview helper may launch nested Codex with full filesystem and network authority. <br>
Mitigation: Review the skill before installing, avoid full-access sandbox bypass for routine review tasks, and use the autoreview helper with `--no-yolo` unless elevated authority is intentionally required. <br>
Risk: The moderation-related security guidance assumes use from an authenticated staff environment with explicit targets and reasons. <br>
Mitigation: Limit moderation workflows to authorized staff contexts and require explicit target and reason details before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/openclaw-cost-optimization) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter remains 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
