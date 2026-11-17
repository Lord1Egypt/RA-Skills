## Description:

Pre-ship risk reporting for OpenClaw PRs that explores code changes, estimates module risk and blast radius, and scores evidence-backed findings by severity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glucksberg](https://clawhub.ai/user/glucksberg)

### License/Terms of Use:

MIT

## Use Case:

Developers working in the OpenClaw repository use this skill before publishing PRs to inspect the current branch diff, identify module risk and blast radius, and produce an evidence-backed markdown risk report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may expose secrets or sensitive repository details from local diffs and grep output.

Mitigation: Review generated reports before sharing them, and avoid publishing reports that include credentials, tokens, or confidential code context.

Risk: The package includes maintenance tooling that can inspect local OpenClaw cron configuration, contact GitHub, and optionally trigger a live cron job.

Mitigation: Use the main PR review workflow for routine review; inspect scripts/test-update-pipeline.sh and run it only when you accept its side effects, especially with --live.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/glucksberg/skills/pr-ship)
- [Skill definition](SKILL.md)
- [README](README.md)
- [Stable Principles](references/STABLE-PRINCIPLES.md)
- [Architecture Map](references/ARCHITECTURE-MAP.md)
- [Current Context](references/CURRENT-CONTEXT.md)
- [Exploration Playbook](references/EXPLORATION-PLAYBOOK.md)
- [Vision Guidelines](references/VISION-GUIDELINES.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with command-derived evidence, severity scores, and suggested fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory output only; it does not approve or reject a pull request.]

## Skill Version(s):

1.0.13 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
