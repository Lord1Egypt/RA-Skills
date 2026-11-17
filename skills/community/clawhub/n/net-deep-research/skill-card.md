## Description:

Performs deep multi-source internet research for complex truth-finding, cross-source fact checking, authenticity checks, and online verification tasks where ordinary browsing is insufficient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4444433333](https://clawhub.ai/user/h4444433333)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill for multi-round web research that verifies claims across independent sources, resolves conflicting evidence, and produces concise evidence-backed answers or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Online runs may transmit research metadata, structured evidence links, query classification, and usefulness signals to shoggoth.vip.

Mitigation: Use only when that data sharing is acceptable; avoid confidential, legal, medical, security, internal-company, or identity-sensitive research unless the backend operator, retention rules, and consent model are acceptable.

Risk: Report Mode may start a local unsandboxed browser process to render PDFs.

Mitigation: Use Report Mode only in a contained environment and review generated report artifacts before distribution.

Risk: The security verdict is suspicious because the skill mandates detailed research trace submission to a third-party backend during online runs.

Mitigation: Review the skill before deployment and restrict use to cases where third-party feedback submission is approved.

## Reference(s):

- [Feedback Contract](artifact/references/feedback-contract.md)
- [Research Playbook](artifact/references/research-playbook.md)
- [Source Scoring](artifact/references/source-scoring.md)
- [Writing Rules](artifact/references/writing-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/h4444433333/skills/net-deep-research)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown answer; optional Markdown or PDF report file in Report Mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source lists, uncertainty notes, and concise rationale; Report Mode produces one report artifact when requested.]

## Skill Version(s):

1.0.14 (source: server release metadata; artifact bundle metadata reports 1.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
