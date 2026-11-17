## Description:

Contribute to the OpenClaw core repository using the repo's own CONTRIBUTING.md rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manjaroblack](https://clawhub.ai/user/manjaroblack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and contributors use this skill when working in openclaw/openclaw or a fork to triage issues, plan focused fixes, choose validation commands, prepare AI-assisted PRs, and route work to appropriate maintainers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may recommend local git and project validation commands that take time or run against the wrong checkout if the repository path is incorrect.

Mitigation: Confirm the target OpenClaw checkout, inspect the recommended commands, and run only the checks appropriate for the intended change.

Risk: Generated PR text or maintainer routing hints may be incomplete or unsuitable for a specific contribution.

Mitigation: Review generated PR bodies, AI-assistance disclosures, testing notes, and maintainer hints before publishing.

## Reference(s):

- [OpenClaw Contributor ClawHub Page](https://clawhub.ai/manjaroblack/skills/openclaw-contributor)
- [OpenClaw Contribution Checklist](references/contributing-checklist.md)
- [OpenClaw PR Template Guide](references/pr-template.md)
- [Example Perplexity Check Plan](references/example-perplexity-check-plan.txt)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and optional generated PR-body Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit JSON validation recommendations when the bundled recommender is run with --json.]

## Skill Version(s):

0.1.1 (source: evidence.release.version and artifact/CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
