## Description:

IELTS Reading passage review, scoring, and progress tracking skill that generates structured review JSON and can upload results to www.liuxue.online for web rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dengjiawei1226](https://clawhub.ai/user/dengjiawei1226)

### License/Terms of Use:

MIT-0

## Use Case:

IELTS learners and tutors use this skill to convert reading passage results, screenshots, and answer lists into structured review data with scores, wrong-question analysis, vocabulary, synonyms, and progress tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt-triggered auto-update behavior can change skill code before review.

Mitigation: Disable or remove the auto-update hook and review the installed version before using the skill.

Risk: The skill can upload review data and use long-lived account tokens.

Mitigation: Use a dedicated short-lived token stored outside shell startup files and require explicit confirmation before any upload.

Risk: Folder scanning can touch broad personal directories during legacy review import.

Mitigation: Limit scans to an explicit user-selected directory and confirm the scan plan before processing files.

Risk: Author mode includes SSH deployment and service restart commands.

Mitigation: Avoid author mode on machines with production SSH access unless the operator intentionally needs deployment capability.

Risk: The README contains older offline-first claims while the current release is web-connected.

Mitigation: Treat the current release as network-connected and review upload/API behavior before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dengjiawei1226/skills/ielts-reading-review)
- [Client Mode Onboarding](artifact/references/CLIENT_MODE_ONBOARDING.md)
- [Review Style Guide](artifact/references/review-style-guide.md)
- [Error Taxonomy](artifact/references/error-taxonomy.md)
- [Score-to-Band Conversion Table](artifact/references/score-band-table.md)
- [538 IELTS Keywords Reference Guide](artifact/references/538-keywords-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with structured JSON review data and shell commands when setup, upload, or validation actions are needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local review files and use configured web upload endpoints for progress tracking.]

## Skill Version(s):

5.5.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
