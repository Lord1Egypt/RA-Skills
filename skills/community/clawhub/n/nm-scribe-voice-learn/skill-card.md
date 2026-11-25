## Description:

Improves a voice profile by learning from manual edits. Use after editing generated text to refine registers and close voice drift over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and developers use this skill after manually editing generated text to identify recurring voice and style patterns and propose profile updates. Proposed changes are reviewed and approved before they are applied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan could not resolve local learning/accumulator.json references, so evidence about those references is incomplete.

Mitigation: Before use, check that the unresolved references are expected and review their contents.

## Reference(s):

- [Scribe plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/scribe)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, JSON]

**Output Format:** [Markdown pattern analysis and proposals, with JSON accumulator records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile updates require user approval; recurring patterns are checked against an evidence threshold.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
