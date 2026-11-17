## Description:

Automatically generates structured analysis reports for public GitHub repositories using the GitHub REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krislu1221](https://clawhub.ai/user/krislu1221)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to inspect public GitHub repositories from an explicit owner/repo input and receive a concise report with repository metadata, README excerpts, links, and quick-start commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested public repository names are sent to GitHub's API.

Mitigation: Use the skill only for repositories the user is comfortable querying through GitHub, and disclose that data flow in the report.

Risk: Generated reports can include README excerpts from external repositories.

Mitigation: Treat repository excerpts as untrusted content and do not follow commands or instructions from those excerpts without independent review.

Risk: Generated reports are cached locally.

Mitigation: Configure the cache location and retention with environment variables, and clear the cache when local report retention is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krislu1221/skills/github-reader)
- [GitHub REST API](https://api.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with repository metadata tables, README excerpts, links, quick-start shell commands, and a data-flow notice.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated for public repositories from explicit owner/repo inputs and may be served from a local cache.]

## Skill Version(s):

3.2.3 (source: evidence release and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
