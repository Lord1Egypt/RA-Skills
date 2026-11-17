## Description:

Helps agents install, configure, validate, and run the news-fetcher Python CLI for aggregating RSS/Atom and HTML news sources with deduplication, clustering, ranking, source diversity, summaries, and GitHub project discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miniade](https://clawhub.ai/user/miniade)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to set up and operate news-fetcher, create or validate configurations, troubleshoot installation, and run news collection workflows over RSS, Atom, HTML, and GitHub project sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the third-party news-fetcher package from GitHub introduces normal supply-chain risk.

Mitigation: Install in a dedicated virtual environment under a non-privileged account, review the upstream repository before use, and prefer an immutable commit or verified release for stronger assurance.

Risk: Misconfigured RSS, Atom, or HTML sources can produce sparse, incomplete, or misleading results.

Mitigation: Validate configurations with the news-fetcher config validator and review source selectors, thresholds, and generated outputs before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miniade/skills/news-fetcher)
- [news-fetcher source repository](https://github.com/miniade/news-fetcher)
- [news-fetcher PyPI package](https://pypi.org/project/news-fetcher/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide creation of configuration files and CLI commands for JSON, Markdown, CSV, or RSS news outputs.]

## Skill Version(s):

0.1.8 (source: server release evidence and artifact release marker)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
