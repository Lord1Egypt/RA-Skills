## Description:

Diffbot (diffbot.com). Use this skill for ANY Diffbot request — searching and reading data. Whenever a task involves Diffbot, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers can use this skill to extract normalized article content from public URLs through Diffbot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup can execute downloaded code without a user review step.

Mitigation: Review and install a specific CLI release separately, then check its automatic skill synchronization settings.

Risk: Using the skill entrusts Diffbot credentials to OOMOL, and requests may consume provider credit.

Mitigation: Use the connected account only if comfortable entrusting credentials to OOMOL, and monitor provider usage and credit.

## Reference(s):

- [Diffbot](https://www.diffbot.com)
- [Diffbot API Reference](https://docs.diffbot.com/reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text]

**Output Format:** [Shell commands with JSON input and normalized article data as output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extracts public article URLs using the extract_article action.]

## Skill Version(s):

1.0.5 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
