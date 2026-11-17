## Description:

Adversarial review of code quality findings with source-anchored counter-evidence and structured verdicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumingtao](https://clawhub.ai/user/yumingtao)

### License/Terms of Use:

MIT

## Use Case:

Developers and code reviewers use this skill to check findings from code reviews, static analysis, or security scans against accessible source and design evidence, then report whether each finding is overturned, weakened, or confirmed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious with medium confidence because it found a potentially misleading verdict validator and could not fully inspect it.

Mitigation: Review the validator's complete source and the scan guidance before installing or relying on its verdicts.

## Reference(s):

- [Insight Challenge on ClawHub](https://clawhub.ai/yumingtao/skills/insight-challenge)
- [Challenge Protocol](specs/challenge-protocol.en.md)
- [Verdict Schema](specs/verdict-schema.en.md)
- [Usage Guide](README.en.md)

## Skill Output:

**Output Type(s):** [JSON, Markdown]

**Output Format:** [Markdown report with an embedded JSON verdict; raw JSON can be requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdicts include a confidence score and may include counter-evidence, supporting evidence, adjusted severity, and a recommendation.]

## Skill Version(s):

1.7.1 (source: ClawHub release metadata; SKILL.en.md frontmatter lists 1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
