## Description:

Delegates tasks to Z.ai GLM-5.x via the stock claude binary and an endpoint swap

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to delegate coding, review, and other selected tasks to Z.ai GLM models through the stock Claude Code CLI, including tasks that need a large context window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local documents may be sent to an external model provider, and the selected provider may use a different account or billing plan.

Mitigation: Before installing, confirm that document sharing and the provider's account and billing arrangement are acceptable; review executor behavior because scan coverage is partial.

## Reference(s):

- [Conjure plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)
- [Z.ai pricing](https://docs.z.ai/guides/overview/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown response saved to a dated .md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the delegated task and selected GLM model.]

## Skill Version(s):

1.10.3 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
