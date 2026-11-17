## Description:

Discovers, audits, and tracks external AI agent skills across GitHub, ClawHub, SkillHub, and Skills.sh with security scanning and recurring trend reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muippt](https://clawhub.ai/user/muippt)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to find external skills, compare candidates across multiple registries, audit candidates before installation, and generate scheduled skill discovery reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports risky automatic install paths and unpinned command execution patterns.

Mitigation: Review generated shell commands before running them, avoid curl-to-bash and unpinned npx paths, and prefer pinned or manually inspected installation steps.

Risk: The security evidence warns about weak GitHub token handling and persistent profile behavior.

Mitigation: Use least-privilege tokens, avoid storing broad tokens in shell startup files for this tool, and remove credentials when they are no longer needed.

Risk: The security evidence notes scheduled reporting behavior.

Mitigation: Confirm cron setup, destination, cadence, and message contents before enabling recurring reports.

Risk: The security evidence says scanner output should be treated as heuristic rather than a safety guarantee.

Mitigation: Use scanner results as one review input and perform manual inspection for high-impact or sensitive installations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/muippt/skills/mu-skill-hunter)
- [Search Guide](artifact/references/search-guide.md)
- [Security Levels](artifact/references/security-levels.md)
- [Weekly Report Template](artifact/references/weekly-report-template.md)
- [ClawHub](https://clawhub.ai)
- [SkillHub](https://skillhub.cn)
- [Skills.sh](https://skills.sh)
- [GitHub REST API Documentation](https://docs.github.com/en/rest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown summaries with tables, shell command examples, configuration guidance, and optional JSON scan or search output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and report outputs are intended for human review before installation or scheduling decisions.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter and changelog state 2.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
