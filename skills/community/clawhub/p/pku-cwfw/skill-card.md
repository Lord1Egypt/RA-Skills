## Description:

PKU CWFW helps agents use the cwfw CLI for Peking University's financial information portal, including IAAA login, session management, and payment, salary, and reimbursement queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjsoj](https://clawhub.ai/user/wjsoj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate and troubleshoot the cwfw CLI for PKU financial portal workflows, including authenticated access to personal payment, salary, and reimbursement information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI accesses sensitive payroll and reimbursement data, and saved sessions may remain on the local machine.

Mitigation: Use the skill only on a trusted machine/account, avoid shared environments, and use the CLI's logout or session controls when finished.

Risk: Command output may reveal personal financial information.

Mitigation: Review account context before running queries and avoid sharing terminal output that contains personal payment, salary, or reimbursement details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wjsoj/skills/pku-cwfw)
- [PKU financial information portal](https://cwfw.pku.edu.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese CLI command output and guidance that uses local cwfw session configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
