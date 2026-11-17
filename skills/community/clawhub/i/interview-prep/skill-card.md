## Description:

Generate a structured interview prep doc for any company -- pulls context from Gmail, Notion, and existing notes, then writes a timeline.md to the interviewGPT folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyuan99](https://clawhub.ai/user/chenyuan99)

### License/Terms of Use:

MIT-0

## Use Case:

Job candidates and career-focused users use this skill to assemble interview preparation notes for a target company, combining interview logistics, company context, technical practice topics, behavioral prompts, and day-of checklist items into a standardized Markdown document.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private interview-related Gmail, Notion, tracker, profile, and local note data.

Mitigation: Install and run it only when that data access is acceptable, and review the requested data sources before execution.

Risk: The generated prep document can store sensitive interview codes, meeting links, and personal contact emails in plaintext.

Mitigation: Confirm the exact output path and omit access codes, meeting links, or personal contact emails unless they are intentionally being saved.

Risk: Company names and output paths influence file creation and updates.

Mitigation: Use trusted company-name input, confirm the target path before writing, and review existing notes before merge or update operations.

## Reference(s):

- [FastPrep Practice Dashboard](https://www.fastprep.io/dashboard/problems)
- [ClawHub Skill Page](https://clawhub.ai/chenyuan99/skills/interview-prep)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown document with tables, checklists, bullet lists, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes or updates a company-specific timeline.md prep document and may preserve existing user-authored notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
