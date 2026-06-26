## Description: <br>
Create, update, and maintain structured identity entries for every person, org, or group mentioned in conversation, with support for human and AI entity subtypes, group dynamics, pairwise member relations, and enforced soul/memory write-through. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyber-bye](https://clawhub.ai/user/cyber-bye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workspace users and agent operators use this skill to maintain persistent identity records for people, organizations, groups, and AI personas mentioned in conversation. It is intended for agents that need structured identity context, relationship tracking, group defaults, and auditable memory write-through across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically create long-lived identity records from ordinary mentions of people, groups, organizations, and AI personas. <br>
Mitigation: Install only when persistent identity memory is desired, set IDENTITY_AUTO_SCAN=false before use unless automatic scanning is intended, and review created entries regularly. <br>
Risk: Identity entries, hook logs, and soul context files persist in the workspace until the owner manually removes or edits them. <br>
Mitigation: Audit and delete or trim identity/, memory/hook_log.jsonl, and soul/identity_context.md according to the workspace owner's retention needs. <br>
Risk: The skill may store sensitive relationship or contact context if the agent records information from conversation. <br>
Mitigation: Use the bundled privacy rules, avoid storing credentials or regulated identifiers, and review sensitive entries before sharing or syncing the workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cyber-bye/identity-manager) <br>
- [ClawHub metadata homepage](https://clawhub.ai/skills/identity-manager) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Agent guardrails](artifact/AGENT.md) <br>
- [Identity memory schema](artifact/memory/schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown identity entries, JSON memory indexes and logs, and response warnings when sync breaches occur] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and appends local workspace files under identity/, memory/, and soul/; no external credentials are required.] <br>

## Skill Version(s): <br>
2.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
