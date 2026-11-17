## Description:

Ops Deck Lite helps agents set up local semantic code search and a reusable prompt library for developer productivity workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure local code search and prompt-library services that help agents find relevant code by meaning and reuse prompt templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead users to index broad local codebases and generate summaries without enough scoping guidance.

Mitigation: Index only repositories where local indexing and summaries are acceptable, and exclude secrets and sensitive directories before running the service.

Risk: The documented cron and PM2 setup can create persistent background re-indexing and services.

Mitigation: Enable persistence only intentionally, document the installed PM2 and crontab entries, and provide a clear removal path.

Risk: Unpinned dependencies and global installs can make local setup harder to audit or reproduce.

Mitigation: Prefer a virtual environment and pinned dependency versions before installing or running the services.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
