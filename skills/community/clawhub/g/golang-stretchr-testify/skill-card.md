## Description:

Comprehensive guide to stretchr/testify for Go testing with assertions, require checks, mocks, suites, async polling, and common misuse patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when writing or reviewing Go tests that import github.com/stretchr/testify. It helps choose assert versus require, create mocks, use suites, verify expectations, and avoid common testify mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper tool gotests is disclosed as an unpinned @latest install, so the installed code can change between releases.

Mitigation: Pin gotests to a reviewed version or install it yourself from a trusted source before using the skill.

Risk: The skill may propose or generate Go test edits that affect repository behavior.

Mitigation: Use it in a scoped project workspace and review generated test changes before committing them.

## Reference(s):

- [testify/mock reference](references/mock.md)
- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-stretchr-testify)
- [Project homepage](https://github.com/samber/cc-skills-golang)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown with Go code examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose generated or edited Go test code; users should review edits before committing.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
