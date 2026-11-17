## Description:

Audits shell scripts for correctness, portability, and common pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review shell scripts used in CI/CD, hooks, wrappers, build automation, and pre-commit workflows for exit-code handling, portability, safety, and structure issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad shell-related triggers may activate the skill in contexts where script review was not intended.

Mitigation: Install it only for agents expected to review shell scripts, and confirm activation context before applying recommendations.

Risk: Package-manager and xtrace snippets could be copied into CI or secret-handling scripts without enough review.

Mitigation: Treat snippets as review examples; inspect and adapt commands before use, and avoid xtrace where secrets may appear in logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-shell-review)
- [ClawHub metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown review report with shell command examples and file:line findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a recommendation such as Approve, Approve with actions, or Block.]

## Skill Version(s):

1.9.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
