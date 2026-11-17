## Description:

Searches LinkedIn, Poslovi Infostud, and HelloWorld.rs for jobs matching target roles, scores listings against a resume PDF, and can produce chat results, optional email digests, optional daily scheduling, and cover letters on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanishsidhu](https://clawhub.ai/user/tanishsidhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and job seekers use this skill to find Serbia and remote job listings that match configured target roles, compare them with a resume, and receive scored results. It can also help draft cover letters for user-selected opportunities while leaving all applications under user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional email feature stores a Gmail App Password in plaintext in the skill directory.

Mitigation: Enable email only when the user accepts that storage model; prefer a dedicated sending account or secret store, restrict file access, and revoke the app password if the config is shared.

Risk: External job data is rendered into the optional email digest without escaping.

Mitigation: Review digest content before enabling or sending email, and treat links and listing text as untrusted external content.

Risk: Daily cron automation can run searches repeatedly without the user being present.

Mitigation: Enable cron only after confirming the schedule, timezone, and deletion path with the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanishsidhu/skills/job-search-skill)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with job summaries, scoring justifications, optional HTML email digest content, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces job-search summaries and cover-letter text for the agent to present; scripts may also write JSON, SQLite, and email-digest artifacts during use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
