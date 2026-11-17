## Description:

Turns dependency changes into a deterministic PASS, WARN, or FAIL verdict for CI checks and pull request comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salemalem](https://clawhub.ai/user/salemalem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to gate dependency pull requests from before-and-after manifests or named version upgrades. It produces a concise verdict and reasons suitable for a CI check or pull request comment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports an undisclosed transfer of dependency snapshots to a third-party service.

Mitigation: Before installing, review the data flow and decide whether sending complete dependency manifests and lockfiles to npmscan is acceptable.

Risk: ClawScan reports a conflict in the documented security gate policy and incomplete scan coverage.

Mitigation: Review the gate policy and test it against representative dependency changes; interpret results cautiously while the scan evidence remains incomplete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/salemalem/skills/npmscan-ci-pr-gate)
- [npmscan MCP server](https://npmscan.com/api/mcp)
- [Test prompts](references/test-prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown with a PASS, WARN, or FAIL verdict and a package findings table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces text for a CI check or pull request comment; it does not itself post comments or enforce merges.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
