## Description: <br>
Health, eval, and regression system for continuously improving OpenClaw skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw maintainers use this skill to audit skill registries, run routing evaluations, and maintain recurring health reports for duplicates, dark skills, stale skills, and routing regressions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local agent transcript logs outside the selected workspace and stores derived usage data. <br>
Mitigation: Run it only in trusted local environments, review generated .learnings reports before sharing, and avoid committing reports that contain usage-derived information. <br>
Risk: The daily heartbeat constructs shell commands from the workspace path. <br>
Mitigation: Use trusted absolute workspace paths and review the scripts before scheduling unattended runs. <br>
Risk: Health and routing reports can produce false positives or approximate recommendations. <br>
Mitigation: Manually review duplicate, dark, stale, and routing findings before deleting, deprecating, or changing skills. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/x-rayluan/openclaw-skill-self-improvement) <br>
- [Routing evaluation cases](references/routing-evals.json) <br>
- [ClawLite](https://clawlite.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON report file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [When scripts run, they write local .learnings JSON reports, history snapshots, and daily text summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
