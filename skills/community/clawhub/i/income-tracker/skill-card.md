## Description:

Income Tracker helps freelancers, creators, side-business operators, and small teams record multi-source income, summarize earnings, and generate trend and source analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as freelancers, creators, side-business operators, and small teams use this skill to log income, review daily, weekly, monthly, or yearly totals, analyze income sources, view trends, forecast earnings, and export records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Income records are stored in a local plaintext JSON file.

Mitigation: Use a private data path, restrict filesystem permissions, avoid shared machines for this data, and do not store sensitive details that require encryption.

Risk: Dependency hardening issues are noted in the security evidence.

Mitigation: Regenerate dependencies from a trusted HTTPS npm registry and review lockfile changes before running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/income-tracker)
- [Skill Homepage](https://clawhub.com/skills/income-tracker)
- [Publisher Profile](https://clawhub.ai/user/onlyloveher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses, CSV or JSON exports, and plain-text or ASCII chart summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user income records in a local JSON file and can export filtered record data.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
