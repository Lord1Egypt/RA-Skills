## Description: <br>
Pre-ship risk report for OpenClaw PRs that dynamically explores the codebase to assess module risk, blast radius, and version-specific gotchas, then scores each finding by severity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glucksberg](https://clawhub.ai/user/Glucksberg) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and maintainers use this skill to inspect OpenClaw pull request diffs before shipping and produce an evidence-backed risk report with severity-scored findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may include local diffs or grep output that contain secrets or sensitive repository details. <br>
Mitigation: Review generated reports for sensitive content before sharing them outside the local review context. <br>
Risk: The included update-pipeline test script is intended for maintainer workflow validation, not normal PR review. <br>
Mitigation: Do not run scripts/test-update-pipeline.sh unless you specifically intend to validate the maintainer update or cron workflow. <br>
Risk: The skill is scoped to OpenClaw pull requests and may produce misleading findings on other repositories. <br>
Mitigation: Use the skill only in an OpenClaw repository and review the current branch diff against main. <br>


## Reference(s): <br>
- [Pr Ship on ClawHub](https://clawhub.ai/Glucksberg/pr-ship) <br>
- [STABLE-PRINCIPLES.md](references/STABLE-PRINCIPLES.md) <br>
- [ARCHITECTURE-MAP.md](references/ARCHITECTURE-MAP.md) <br>
- [CURRENT-CONTEXT.md](references/CURRENT-CONTEXT.md) <br>
- [EXPLORATION-PLAYBOOK.md](references/EXPLORATION-PLAYBOOK.md) <br>
- [VISION-GUIDELINES.md](references/VISION-GUIDELINES.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown risk report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include branch, base, changed file count, touched modules, module risk summary, findings, final alert score, and executive summary.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
