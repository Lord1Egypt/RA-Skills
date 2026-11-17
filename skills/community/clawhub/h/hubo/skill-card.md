## Description:

Implements and tests code while an independent reviewer challenges every change until all findings are reconciled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h0ngcha0](https://clawhub.ai/user/h0ngcha0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Hubo for programming tasks that benefit from a dedicated implementation lineage and an independent review lineage that iterates until every review finding is closed, withdrawn, or escalated for a real user decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed diffs, commands, evidence, and review commentary may appear in the conversation transcript.

Mitigation: Use the skill only when that level of repository detail is acceptable in the conversation, and avoid highly sensitive repositories unless this disclosure is acceptable.

Risk: The work lineage may edit task-relevant files while coordinating with a read-only reviewer.

Mitigation: Inspect the reported diffs and require the review lineage to return CLEAR, with every finding closed or withdrawn, before accepting the result.

## Reference(s):

- [Hubo workflow](references/workflow.md)
- [Host adapters](references/hosts.md)
- [Karpathy-inspired coding discipline](https://github.com/multica-ai/andrej-karpathy-skills)
- [Ponytail](https://github.com/DietrichGebert/ponytail)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown conversation reports with code changes, diffs, shell command results, review findings, and final guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a chronological work and review exchange in the conversation; the exchange is not stored in a file.]

## Skill Version(s):

0.4.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
