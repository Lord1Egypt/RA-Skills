## Description:

Propose a canonical home, concrete consumers, and any justified runtime home for a reusable tool, library, skill, document, or workflow. Use after building a reusable capability or when asked where it should live; execution requires approval of exact targets and actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to decide where reusable work should live, which authorized projects should consume it, and whether any runtime host is actually needed before approving concrete actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned npx installation example may run whatever version the package resolver selects at install time.

Mitigation: Use a trusted, already-approved skills CLI or pin and verify the installer source and version before installation.

Risk: Distribution proposals can lead to unintended cross-repository changes, publication, deployment, or credential movement if approval is ambiguous.

Mitigation: Approve only exact repositories, paths, versions, and actions, and verify each approved target before reporting it as handled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antreasantoniou/skills/propagate)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown proposal with concrete approved actions when execution is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposal-first workflow; execution requires exact user-approved targets and actions.]

## Skill Version(s):

1.0.0 (source: changelog, released 2026-09-05; ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
