## Description:

Before saying a coding task is done, fixed, working or passing, run the project's real tests, build, typecheck and lint, show the real output, and inspect the change for the quiet ways "done" is not done (skipped or weakened tests, test commands that cannot fail, swallowed errors, hardcoded results, files outside the task, broken project rules, debug leftovers, secrets, dependency and migration mistakes). Use it at the end of every coding task, before committing or opening a PR, and whenever someone asks "did you test it?", "is it really done?" or "prove it". Also use it when the person corrects a mistake ("don't do that again") to turn the correction into a rule checked on every later proof.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shashwat14m](https://clawhub.ai/user/shashwat14m)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill at the end of coding tasks to run and report real project checks, review changes for issues that checks may miss, and record recurring mistakes as project rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this skill suspicious because scanners report unsafe command execution and file handling risks; analysis was partial, and the evidence does not establish malicious intent.

Mitigation: Consider avoiding installation until the command execution and write risks are addressed and the partial analysis is completed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/shashwat14m/skills/prove-it-works)
- [GitHub source repository (server-resolved provenance)](https://github.com/shashwat14m/shipsnag-skills/tree/main/skills/prove-it-works)
- [Review checklist](references/review-checklist.md)
- [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [A proof report with check commands and real output, plus optional project rule or ledger files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports checks as passed, not run, or failed; Never Twice rules and the optional ledger are stored under .shipsnag.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
