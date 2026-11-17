## Description:

Quality review of a diff: bugs, security, real load, missing tests, speed, and what to delete. Each finding says what goes wrong and how to fix it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dietrichgebert](https://clawhub.ai/user/dietrichgebert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review a code change for bugs, security issues, load concerns, missing tests, performance problems, and unnecessary code. It returns a findings report with concrete fixes and does not apply changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A review finding or proposed fix could be incorrect or misleading.

Mitigation: Check each finding against the affected code and tests before applying its proposed fix; the skill reports recommendations but does not change files.

## Reference(s):

- [Project homepage](https://github.com/DietrichGebert/ponytail)
- [ClawHub skill page](https://clawhub.ai/dietrichgebert/skills/ponytail-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Numbered findings with explanations and proposed fixes; no code changes are made.]

## Skill Version(s):

5.3.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
