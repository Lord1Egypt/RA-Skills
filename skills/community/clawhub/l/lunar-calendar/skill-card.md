## Description:

Provides structured Chinese lunar calendar queries, including solar-to-lunar conversion, lunar-to-solar conversion, almanac suitability checks, zodiac stems and branches, leap-month handling, and solar-term lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hehuibiao](https://clawhub.ai/user/hehuibiao)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill when an agent needs deterministic Chinese lunar calendar conversion, almanac guidance, traditional festival data, or solar-term information instead of relying on model memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled GitHub publishing and setup scripts may expose code or persist a GitHub token.

Mitigation: Use only the lunar calendar runtime needed for calendar queries; ignore or remove publishing scripts and do not provide GitHub credentials to this package.

Risk: Downloaded archives or dependency versions may not match the reviewed release.

Mitigation: Verify release archive hashes and dependency versions before installation.

## Reference(s):

- [Fortune Rules](references/fortune_rules.md)
- [Solar Terms](references/solar_terms.md)
- [ClawHub Skill Page](https://clawhub.ai/hehuibiao/skills/lunar-calendar)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Structured XML-style text with optional Markdown and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs agents to call bundled scripts for supported dates from 1900 to 2100 and to return deterministic calendar fields rather than free-form estimates.]

## Skill Version(s):

0.9.0 (source: SKILL.md frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
