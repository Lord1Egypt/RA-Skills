## Description:

Unified log search across Loki, Elasticsearch, and CloudWatch that translates natural language into LogQL, Elasticsearch DSL, or CloudWatch filter patterns while keeping operations read-only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkuehnl](https://clawhub.ai/user/tkuehnl)

### License/Terms of Use:

MIT

## Use Case:

Developers, SREs, and incident responders use this skill to search configured log backends, correlate errors across services, and produce concise timelines, root-cause hypotheses, and recommended actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell argument handling could allow crafted inputs to execute local commands.

Mitigation: Install only after the maintainer fixes numeric validation for --since and --limit, and review command construction before enabling execution.

Risk: Returned logs can contain PII, secrets, tokens, and internal infrastructure details.

Mitigation: Use least-privilege read-only backend credentials, treat returned logs as sensitive, and summarize findings instead of exposing raw log output.

Risk: Authenticated backend queries over weakly protected networks can expose credentials or sensitive log data.

Mitigation: Prefer HTTPS for authenticated backends and avoid production AWS profiles during testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tkuehnl/skills/log-dive)
- [README](README.md)
- [Security Policy](SECURITY.md)
- [Testing Guide](TESTING.md)
- [Grafana Loki logcli install guide](https://grafana.com/docs/loki/latest/tools/logcli/)
- [AWS CLI install guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown incident summaries with inline shell commands and structured JSON backend results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only log search output should be summarized, not dumped raw; default result limit is 200 entries.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata; artifact frontmatter, changelog, and scripts report 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
