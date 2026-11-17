## Description:

Money helps an agent advise on personal-finance sequencing decisions, including debt payoff, emergency funds, affordability, housing, retirement readiness, shocks, windfalls, credit problems, fees, and savings rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to decide where money should go next, size buffers and goals, evaluate financial trade-offs, and record durable personal-finance decisions. It is advisory only and does not move money, open accounts, transact, or submit forms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically saves and edits detailed financial records in shared local files without asking first.

Mitigation: Install only when durable local financial memory is desired, and use an agent policy that confirms writes and deletions before ending a session.

Risk: Local financial memory may include account balances, debts, income, contacts, fraud history, and decisions in plaintext.

Mitigation: Review the configured ~/Clawic/data paths, keep them private and backed up, and avoid storing credentials or authentication secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/money)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)
- [Money skill homepage](https://clawic.com/skills/money)
- [Skill definition](artifact/SKILL.md)
- [Memory template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown responses and local Markdown/YAML notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist agreed financial facts, plans, and decisions to configured local Clawic data paths.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
