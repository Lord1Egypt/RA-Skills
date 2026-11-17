## Description:

Pre-build idea validator that checks competition across GitHub, Hacker News, npm, PyPI, and Product Hunt before writing code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and product builders use this skill before implementation to evaluate whether an idea appears crowded across open source, community, package, product, and China-market channels. It provides a reality_signal score, competitor summary, and differentiation guidance to support go, pivot, or stop decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned external code through `uvx idea-reality-mcp`.

Mitigation: Review and pin the external `idea-reality-mcp` package before installation or execution.

Risk: The bundled validator presents mock, random results as market validation.

Mitigation: Treat `npm run validate` output as demonstration data unless it is replaced with verified competitive research from live sources.

Risk: The validator writes status to a hardcoded local persistent memory path.

Mitigation: Do not run the validator until the path is removed, reviewed, or made configurable for the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/idea-reality-validator)
- [ClawHub publisher profile](https://clawhub.ai/user/sunnyhot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-style guidance with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a numeric reality_signal score, competitor list, and differentiation suggestions.]

## Skill Version(s):

1.0.0 (source: evidence release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
