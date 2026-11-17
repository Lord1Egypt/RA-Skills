## Description:

A GitHub intelligence tool for AI product managers that uses the locally authenticated gh CLI and GitHub API to discover trends, monitor signals, and generate PM-grade repository analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kun-0546](https://clawhub.ai/user/kun-0546)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and ecosystem researchers use this skill to find GitHub projects worth monitoring, search technical directions, detect anomalous repository growth, and analyze a repository's ecosystem position.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the locally authenticated GitHub CLI and makes live GitHub API calls.

Mitigation: Run it only with a GitHub account and API quota you are comfortable using, and check the rate limit before long scans.

Risk: Untrusted repository text such as README or issue content can influence the agent's analysis.

Mitigation: Treat repository content as data, keep user and system instructions authoritative, and review generated analysis before acting on it.

Risk: Generated HTML reports may include untrusted fields that are not safely escaped.

Mitigation: Open generated HTML reports cautiously in a local context and avoid sharing or publishing them until escaping is verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kun-0546/skills/github-trend-observer)
- [GitHub CLI](https://cli.github.com)
- [Layer Model](references/layer_model.md)
- [Layer Model Chinese](references/layer_model_cn.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, HTML reports, JSON script output, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the local GitHub CLI authentication state and GitHub API quota; report files may be written under an output directory.]

## Skill Version(s):

0.1.1 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
