## Description:

Structures meeting transcripts into formal minutes with summaries, decisions, and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers can use this skill to turn supplied meeting transcript text into structured minutes, including decisions and action items. It is especially positioned for medical or research meeting workflows that need explicit assumptions and bounded outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical compliance wording may be mistaken for proof that generated minutes satisfy regulatory requirements.

Mitigation: Treat FDA and ICH E6 references as drafting context only; have qualified reviewers verify clinical, legal, or official records before use.

Risk: Broad routing language and stress-case audit results indicate the skill can drift outside its declared meeting-minutes scope.

Mitigation: Confirm the transcript, meeting type, scope limits, and acceptance criteria before use, and stop when required inputs or boundaries are unclear.

Risk: Generated action items or decisions may be incomplete or incorrect for complex transcripts.

Mitigation: Compare generated minutes against the source transcript and manually correct decisions, action owners, deadlines, and unresolved items.

## Reference(s):

- [Meeting Minutes References](artifact/references/guidelines.md)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/meeting-minutes-aipoch)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON with structured minutes, decisions, action items, assumptions, risks, and next checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be manually reviewed before use in clinical, legal, or official records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
