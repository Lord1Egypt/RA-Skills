## Description:

Generates Chinese-language Markdown drafts of GPU compute lease agreements from client, GPU model, quantity, price, and duration inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, sales engineers, and operations teams can use this skill to draft GPU compute lease agreements for review and negotiation. The generated draft covers service scope, pricing, SLA, data security, intellectual property, confidentiality, liability, term, termination, and dispute resolution sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated contract drafts may be mistaken for finalized legal advice or execution-ready agreements.

Mitigation: Treat each draft as a starting template and require legal review before use.

Risk: The output embeds PRC-law dispute terms and fixed SLA, security, payment, and liability clauses that may not match the intended transaction.

Mitigation: Review and adapt jurisdiction, dispute venue, SLA, security, payment, and liability terms for the specific deal.

Risk: The optional --output path can create or overwrite a file.

Mitigation: Use --output only with a path that is intended for the generated Markdown draft.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dashiming/skills/pans-contract-generator)
- [standard_gpu_lease.md](references/templates/standard_gpu_lease.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown contract draft, either printed to stdout or written to a user-specified file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires client name, GPU model, GPU count, monthly per-card price, and lease duration; optional output path may create or overwrite a Markdown file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
