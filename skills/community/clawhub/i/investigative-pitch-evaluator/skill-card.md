## Description:

Investigative Pitch Evaluator turns a tip, FOIA return, document drop, or reporting anomaly into a draft investigative pitch packet with source-tier evidence mapping, rubric scoring, an editorial verdict, and next reporting steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Reporters, freelancers, investigative editors, and newsroom intake desks use this skill to structure leads into editor-ready draft pitch packets and decide whether to commit reporting time, legal review, or travel budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive reporting material, source identities, sealed records, or embargoed documents.

Mitigation: Use it only in an appropriate environment for the material; avoid sharing protected details, use redacted source descriptors, and keep confidential material out of tool calls or searches.

Risk: The generated pitch packet could be mistaken for a final editorial or legal decision.

Mitigation: Keep the output labeled as DRAFT and require independent reporter, editor, and legal review before sending a pitch or committing reporting resources.

Risk: Weak, anonymous-only, or social-source claims could create misleading pitch recommendations.

Mitigation: Apply the source-tier evidence map, flag unsupported load-bearing claims as NOT YET PUBLISHABLE, require corroboration, and preserve right-of-reply planning for criticized subjects.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/investigative-pitch-evaluator)
- [Feedback and Contributions](https://github.com/archlab-space/Open-Skill-Hub/issues)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft pitch packet with structured tables and rubric scoring]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a DRAFT label, source-tier evidence map, legal and ethics checklist, Greenlight / Develop / Park / Decline verdict, next-reporting-steps plan, and human sign-off line.]

## Skill Version(s):

0.1.2 (source: server release metadata and CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
