## Description:

Planeja, cria e edita campanhas no Meta Ads com racional documentado e padrao operacional, usando qualquer MCP de Meta Ads conectado ao agente.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moskoweb](https://clawhub.ai/user/moskoweb)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, operators, and developers use this skill to turn campaign briefings into Meta Ads campaign, ad set, ad, and creative builds through a connected Meta Ads MCP. It supports planning, paused-by-default creation, controlled edits, readiness checks, naming, UTM, and launch review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect a connected Meta Ads account, including campaign structure, budgets, targeting, tracking, and publish or resume actions.

Mitigation: Install only when the agent should operate a Meta Ads account, and review account selection, budgets, targeting, tracking, and any resume or publish action before allowing changes.

Risk: Campaigns or edits could be launched with incorrect strategy, naming, UTM, creative, readiness, or tracking assumptions.

Mitigation: Use the paused-by-default workflow, require rationale and final checklist review, and validate readiness, account setup, and tracking before publishing.

Risk: The source guidance is primarily in Portuguese, which may be misread by reviewers or operators who do not read Portuguese.

Mitigation: Ask the agent to translate the guidance before review or execution when the operator is not comfortable reading Portuguese.

## Reference(s):

- [Campaign Build Playbooks](artifact/references/campaign-build-playbooks.md)
- [Ad Set Structures](artifact/references/adset-structures.md)
- [Creative Assembly](artifact/references/creative-assembly.md)
- [Launch Checklist](artifact/references/launch-checklist.md)
- [Editing Guidelines](artifact/references/editing-guidelines.md)
- [Official Meta Build Guidelines](artifact/references/official-meta-build-guidelines.md)
- [Meta Performance Marketing](https://www.facebook.com/business/ads/performance-marketing)
- [Meta Advantage+ Placements](https://www.facebook.com/business/ads/meta-advantage-plus/placements)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with suggested MCP tool operations, naming and UTM details, rationale, and launch checklists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Meta Ads account changes through a connected MCP; creation starts paused and budget, publish, resume, targeting, tracking, and account-selection actions should be reviewed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
