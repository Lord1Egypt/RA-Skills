## Description:

Build and review private A2A commerce workflows with P-ACP packages, privacy boundaries, Solana settlement plans, and receipt proofs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kairomarkets](https://clawhub.ai/user/kairomarkets)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build or review private agent-to-agent commerce integrations with P-ACP, including lifecycle modeling, package selection, privacy boundaries, Solana settlement planning, and receipt proof validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent output could blur the boundary between unsigned settlement planning and wallet-controlled payment execution.

Mitigation: Keep wallet selection, signing, transaction broadcast, confirmation, and user-visible payment errors in the consuming application, and require verified chain evidence before claiming funds moved.

Risk: Private commerce requirements, deliverables, keys, grants, or sensitive metadata could be exposed in logs, receipts, or public output.

Mitigation: Bind encrypted payloads and disclosures to explicit sessions, recipients, grants, and expiry, and keep plaintext sensitive content out of journals, receipt commitments, logs, exceptions, and test snapshots.

Risk: Generated integration advice may select unnecessary or stale P-ACP packages.

Mitigation: Inspect the target project's runtime and installed package versions, prefer @p-acp/sdk for most integrations, and use lower-level packages only when the required surface is specific.

## Reference(s):

- [Package Selection](references/package-selection.md)
- [Safety Boundaries](references/safety-boundaries.md)
- [Workflow Recipes](references/workflow-recipes.md)
- [Server-resolved GitHub Source](https://github.com/KairoMarkets/p-acp/tree/main/skills/p-acp-agent-commerce)
- [ClawHub Skill Page](https://clawhub.ai/kairomarkets/skills/p-acp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes package choices, lifecycle maps, privacy and evidence boundaries, settlement boundaries, tests, validation results, and dependency notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
