## Description:

Knowledge Orchestrator is a compatibility-layer skill for coordinating knowledge search across Zotero, Obsidian, and IMA while directing users toward the unified knowledge entry point.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use this skill to search and coordinate research references and notes across Zotero, Obsidian, and IMA from an agent workflow. The current release preserves compatibility commands while recommending the unified knowledge search, sync, and link entry points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure from Zotero or IMA API keys stored in local configuration files.

Mitigation: Keep API keys out of shared repositories, restrict access to credential files, and rotate exposed credentials.

Risk: Private research notes or literature metadata may be sent to external services when cloud sync or upload features are used.

Mitigation: Review notes before enabling IMA sync or upload behavior and use the feature only when external service transfer is intended.

Risk: Search output can be incomplete when adjacent Zotero or Obsidian modules or credentials are unavailable.

Mitigation: Verify the dependent local modules and configuration files before relying on aggregated search results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/knowledge-orchestrator)
- [Publisher profile](https://clawhub.ai/user/jirboy)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Aggregates search output from configured local knowledge sources; IMA search and sync behavior is described as in development or compatibility-layer behavior.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
