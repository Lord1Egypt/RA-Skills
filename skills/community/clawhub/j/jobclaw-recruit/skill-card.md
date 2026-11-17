## Description:

Jobclaw Recruit helps recruiters publish, update, delete, and review job postings in JobClaw, then inspect AI-matched candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imluyu](https://clawhub.ai/user/imluyu)

### License/Terms of Use:


## Use Case:

Recruiters and hiring teams use this skill to collect job-posting details, publish and maintain openings in JobClaw, and review matched candidates with structured hiring analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recruiter authentication tokens are stored locally and may appear in command output.

Mitigation: Treat command outputs and transcripts as sensitive, and rotate or revoke any token that is exposed.

Risk: Job posting and candidate data is sent to JobClaw.

Mitigation: Use the skill only with hiring data approved for processing by JobClaw.

Risk: Custom API endpoints can redirect hiring data or tokens away from the intended service.

Mitigation: Use the default JobClaw API endpoint unless a custom apiUrl is explicitly trusted.

## Reference(s):

- [Jobclaw Recruit ClawHub listing](https://clawhub.ai/imluyu/skills/jobclaw-recruit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include job records, candidate match details, similarity scores, and token-dependent API results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
