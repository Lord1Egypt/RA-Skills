## Description:

AI-powered personal finance management system - track expenses, manage budgets, analyze spending patterns, and get smart financial recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to record income and expenses, manage category budgets, analyze spending, and generate personal finance reports through the Personal CFO CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an external finance CLI from npm or GitHub, which can introduce supply-chain risk if the package or lifecycle scripts are not reviewed.

Mitigation: Pin a reviewed npm version or Git commit, review the package source and lifecycle scripts before installation, and install only in environments where that dependency is acceptable.

Risk: The skill manages sensitive personal finance records in local JSON files.

Mitigation: Keep the data directory permissions appropriate for financial records, choose a controlled data directory with CFO_DATA_DIR when needed, and avoid unintentional cloud sync or sharing.

Risk: Ambiguous user requests could cause an agent to record inaccurate amounts, categories, descriptions, or budget changes.

Mitigation: Confirm transaction and budget details with the user before adding or modifying records, especially when currency, category, or intent is unclear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/personal-cfo)
- [GitHub Repository](https://github.com/ZhenRobotics/openclaw-personal-cfo)
- [npm Package](https://www.npmjs.com/package/openclaw-personal-cfo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate on local JSON finance records through the CLI after user confirmation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
