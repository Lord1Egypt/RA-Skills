## Description:

Odu is a 256-state, 8-bit binary pattern recognition format for signal classification, state mapping, and action-oriented analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arosstale](https://clawhub.ai/user/arosstale)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to ask an agent for structured binary-pattern analysis of a situation, including channel scores, a decimal state, range classification, and recommended action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages automatic execution of mapped actions after classification.

Mitigation: Use it as an analysis and reporting format only; keep normal confirmation, safety, uncertainty, and authorization checks in place before any action.

Risk: The skill asks the agent to suppress deliberation and avoid second-guessing.

Mitigation: Require review before using outputs in workflows that can change files, call APIs, spend money, post content, or affect accounts.

## Reference(s):

- [Project homepage](https://github.com/arosstale/clawoney)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with binary pattern, decimal state, range, action, and channel-level notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill provides an analysis format and should not be treated as authority to act automatically.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
