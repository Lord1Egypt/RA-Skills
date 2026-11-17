## Description:

Lingxing (lingxing.com). Use this skill for ANY Lingxing request — searching and reading data. Whenever a task involves Lingxing, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can query and read Lingxing ERP data, including products, inventory, shipments, listings, advertising reports, and profitability metrics, through the connected Lingxing account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A missing CLI dependency can trigger remote software installation without a separate approval step; the remote installers and hosted connector implementation were not verified.

Mitigation: Review and approve CLI installation separately, preferably using a reviewed, pinned release. Check automatic skill synchronization before allowing persistent changes across agents, and connect only the intended Lingxing account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-lingxing)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Lingxing API documentation](https://apidoc.lingxing.com/docs/Guidance/newInstructions)
- [Lingxing homepage](https://www.lingxing.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Analysis, Guidance]

**Output Format:** [Shell commands with JSON request payloads and JSON connector responses, summarized with Markdown guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Lingxing account and the selected action's input schema.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
