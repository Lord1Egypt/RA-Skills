## Description:

Audits the DSA problem bank for coverage gaps and proposes new YAML entries

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to compare DSA problem bank counts with the category manifest, identify coverage gaps, and prepare YAML entries for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because five referenced local files were unavailable, so behavior connected to them was not assessed.

Mitigation: Review the referenced files and their behavior before relying on the coverage report or proposed entries.

## Reference(s):

- [Gauntlet plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, YAML configuration]

**Output Format:** [Markdown coverage report with proposed YAML entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposals are presented for human review and are not written directly into the problem bank.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
