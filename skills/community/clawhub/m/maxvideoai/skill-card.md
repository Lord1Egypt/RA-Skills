## Description:

Helps users plan AI video projects, compare current models, obtain and approve exact MaxVideoAI generation quotes, and recover results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camgraphe](https://clawhub.ai/user/camgraphe)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users can compare live AI video models, estimate project budgets, obtain an exact quote, and request a single approved generation through MaxVideoAI. They can also track jobs and present completed results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paid generation could proceed without approval of the current exact quote or after the request changes.

Mitigation: Show the fresh exact quote and request, wait for explicit approval, and require a new quote and approval for any replacement or changed request.

Risk: Credentials, payment details, or private reference material could be exposed in chat or temporary links.

Mitigation: Keep account and payment information in MaxVideoAI account screens; use owned assets for private references and do not put private bytes or temporary upload links in chat.

Risk: Repeating confirmation after a timeout could unintentionally initiate another paid attempt.

Mitigation: Recover the existing job by its ID or recent history, follow returned retry instructions, and do not reconfirm to resolve an ambiguous response.

## Reference(s):

- [MaxVideoAI ClawHub listing](https://clawhub.ai/camgraphe/skills/maxvideoai)
- [Safe generation boundary](references/safe-generation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model comparisons, budgets, exact quotes, job status, and result destinations; paid generation requires explicit approval.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
