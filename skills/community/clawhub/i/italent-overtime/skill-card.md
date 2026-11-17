## Description:

Italent Overtime helps agents authenticate with Beisen iTalent and push, query, or cancel employee overtime records through the iTalent open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zjm1226](https://clawhub.ai/user/zjm1226)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, HR operators, and agents use this skill to manage Beisen iTalent overtime workflows, including submitting overtime, querying employee overtime records, and requesting cancellation of submitted overtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles iTalent AppKey/AppSecret values and saved access tokens.

Mitigation: Use non-shared credentials, avoid entering secrets into shell history, rotate any credential-shaped values found in the package, and store saved tokens with strict local permissions or a credential store.

Risk: The skill can submit or revoke HR overtime records in a real iTalent tenant.

Mitigation: Require explicit human confirmation and review target employee, time range, and overtime ID before push or cancel actions.

Risk: The security verdict is suspicious for this release.

Mitigation: Review and scan the package before installing it in any real HR environment.

## Reference(s):

- [API docs](references/api-docs.md)
- [Troubleshooting guide](references/troubleshooting.md)
- [Beisen iTalent open platform](https://open.italent.cn)
- [iTalent OpenAPI endpoint](https://openapi.italent.cn)
- [ClawHub skill page](https://clawhub.ai/zjm1226/skills/italent-overtime)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or JSON CLI output with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied iTalent AppKey/AppSecret and employee identifiers; can submit or revoke HR overtime records.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
