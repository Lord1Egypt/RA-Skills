## Description:

Automates the iGOT Karmayogi portal with an OpenClaw-managed Playwright browser for course enrollment, video playback, assessments, progress tracking, and certificate downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koppakanagaharsha-lang](https://clawhub.ai/user/koppakanagaharsha-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Learners and account holders use this skill to automate iGOT Karmayogi coursework in an authenticated browser session, including enrollment, course playback, assessment submission, progress checks, and certificate download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can autonomously operate an authenticated iGOT account, including enrolling in courses and submitting assessments.

Mitigation: Install only when this automation is explicitly wanted and permitted by the relevant organization; prefer requiring confirmation before enrollment and assessment submission.

Risk: The skill persists session state and can resume account actions with limited user control.

Mitigation: Avoid shared machines and review state, session, certificate download, and resume behavior before deployment.

## Reference(s):

- [iGOT Portal Selectors Reference](artifact/references/selectors.md)
- [iGOT Known Course IDs](artifact/references/course-ids.md)
- [iGOT Karmayogi Portal](https://portal.igotkarmayogi.gov.in/page/home)
- [ClawHub Skill Page](https://clawhub.ai/koppakanagaharsha-lang/skills/igot-karmayogi)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown instructions with browser actions and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local state and download certificate PDFs during agent execution.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
