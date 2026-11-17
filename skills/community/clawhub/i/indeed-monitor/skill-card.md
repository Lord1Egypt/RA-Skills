## Description:

Monitor Indeed job postings for businesses hiring receptionists, customer service representatives, or front desk staff in target areas and output enriched leads with company, location, salary and posting details when available, job URL, and pain point summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayjjimenez](https://clawhub.ai/user/jayjjimenez)

### License/Terms of Use:


## Use Case:

Sales and operations teams use this skill to identify businesses with active front-desk, receptionist, customer service, or office-manager hiring signals and produce enriched lead records for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a local Chrome profile through a browser relay.

Mitigation: Run it with an isolated browser profile rather than a personal Chrome profile.

Risk: Using --save can append scraped lead text to a hard-coded master lead file.

Mitigation: Review and change the output path before saving, and inspect generated Markdown before sharing.

Risk: Scraped job listing content may be untrusted or inaccurate.

Mitigation: Treat saved leads as untrusted until verified against the source job posting and sanitize Markdown output before reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jayjjimenez/skills/indeed-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown lead list with job posting fields and pain point summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append scraped leads to a hard-coded local Markdown file when run with --save; browser mode requires an active Chrome relay.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
