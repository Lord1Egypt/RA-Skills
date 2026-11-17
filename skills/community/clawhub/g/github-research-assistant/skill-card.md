## Description:

GitHub Research Assistant helps users analyze GitHub repositories across basic metadata, purpose, tech stack, usage examples, and technical architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luochang212](https://clawhub.ai/user/luochang212)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to quickly understand a GitHub repository before adoption, review, integration, or further technical investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository analysis may expose private repository metadata, source snippets, manifests, or configuration examples to the agent's available tools.

Mitigation: Use this skill only on repositories you are comfortable sharing with the agent environment, and avoid sensitive private repositories or configuration examples unless access is intended.

Risk: Repository summaries can omit context or mischaracterize architecture when only selected files are inspected.

Mitigation: Treat the generated report as a review aid and verify adoption, security, and integration decisions against the repository's authoritative documentation and source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luochang212/skills/github-research-assistant)
- [Chinese reference](references/skill-cn.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown repository analysis report with sections for basic information, purpose, tech stack, usage, and technical architecture.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is based on repository metadata and selected source, manifest, README, and configuration files available to the agent.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
