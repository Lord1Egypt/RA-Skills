## Description:

Helps users assess whether a technical idea is novel, patentable, or already disclosed in prior art.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Inventors, R&D teams, and patent professionals use this skill to compare an invention disclosure with prior art before filing or project decisions, and to prepare a novelty-search report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weaknesses in endpoint validation, redirect handling, or paid-key storage could expose access credentials.

Mitigation: Review endpoint validation and redirect handling before use; provide a restricted key outside chat and avoid shared plaintext storage.

Risk: Confidential invention material may be sent to PatentMax for processing.

Mitigation: Confirm PatentMax's confidentiality terms before submission and limit sensitive details where appropriate.

Risk: A paid search may incur charges.

Mitigation: Review and approve the quoted charge before submission.

## Reference(s):

- [PatentMax skill release on ClawHub](https://clawhub.ai/ip930/skills/patent-novelty-cn)
- [PatentMax publisher profile](https://clawhub.ai/user/ip930)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [Workflow reference](references/workflow.md)
- [Technical solution writing guide](references/solution-guide.md)

## Skill Output:

**Output Type(s):** [text, guidance, document]

**Output Format:** [Prior-art comparisons and a novelty assessment, with an optional downloadable Word (.docx) report.]

**Output Parameters:** [Technical solution, search purpose, search depth, and target regions.]

**Other Properties Related to Output:** [Search-based findings are not a guarantee of patentability and do not replace a formal novelty search by a qualified institution.]

## Skill Version(s):

1.1.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
