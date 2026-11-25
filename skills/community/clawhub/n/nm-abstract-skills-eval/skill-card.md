## Description:

Evaluate Claude skill quality through auditing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining Claude skills use this framework to audit skill structure and quality, find opportunities to improve performance and token use, and plan or verify changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery guidance may not clearly limit which processes or temporary files and caches should be stopped or cleared; the security analysis reports partial coverage.

Mitigation: Review each recovery action before running it and limit process stops or cleanup to specifically identified targets.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-abstract-skills-eval)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown evaluation findings and improvement guidance, with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on the target skill and available project tooling.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
