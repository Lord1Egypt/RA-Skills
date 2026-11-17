## Description:

Debug and troubleshoot common issues with the Orderly SDK including errors, WebSocket issues, authentication problems, and trading failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarnadas](https://clawhub.ai/user/tarnadas)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to troubleshoot Orderly SDK browser integrations, including build setup, WebSocket status, authentication, order submission, deposits, withdrawals, and hook debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Console logging snippets can reveal wallet or account state, balances, and trading context in development logs.

Mitigation: Use the snippets only in development, avoid collecting sensitive logs, and remove debug panels before production use.

Risk: Transaction examples cover deposits, withdrawals, and order submission flows that can involve real funds.

Mitigation: Review and test transaction code in a non-production environment or with limited funds before using it with real accounts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tarnadas/skills/orderly-sdk-debugging)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, CSS, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes troubleshooting checklists and development-only debugging snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
