## Description:

Immigration provides privacy-conscious process guidance and application organization for visa, work permit, residency, citizenship, document, deadline, and interview preparation workflows without providing legal advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to organize immigration applications, generate document checklists, track deadlines and application status, and prepare for interviews while preserving local-only privacy boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive immigration plans, application notes, checklists, and deadlines may be saved in plaintext local files.

Mitigation: Store only necessary data, avoid passport numbers, receipt numbers, financial details, and private case facts, and delete local records when no longer needed.

Risk: Immigration guidance may be incomplete, outdated, or mistaken for legal advice.

Mitigation: Verify visa rights, restrictions, deadlines, fees, and eligibility questions with official government sources or a licensed immigration professional before acting.

## Reference(s):

- [Application Status Tracking](references/application-status.md)
- [Deadline and Timeline Tracker](references/deadline-tracker.md)
- [Document Checklist Generator](references/document-checklist.md)
- [Visa Interview Preparation](references/interview-prep.md)
- [Pathway Finder](references/pathway-finder.md)
- [Post-Approval Planning](references/post-approval.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with local JSON records and Python script command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write plaintext local JSON under ~/.openclaw/workspace/memory/immigration when scripts are used.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
