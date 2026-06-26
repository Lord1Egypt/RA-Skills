## Description: <br>
Cautious curation, classification, review, and migration planning for Obsidian or Markdown vaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thenerdforge](https://clawhub.ai/user/thenerdforge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and knowledge workers use this skill to organize Obsidian or Markdown vaults, classify notes, identify canonical pages, preserve historical context, and plan small reviewable cleanup or migration slices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads targeted areas of an Obsidian or Markdown vault and may propose or make small Markdown edits. <br>
Mitigation: Use bounded slices, keep backups, and review diffs before applying any write slice. <br>
Risk: Vault notes may contain secrets, credentials, PII, internal identifiers, or operational data. <br>
Mitigation: Avoid targeting notes with sensitive material unless local review is intended; treat sensitive findings as hypotheses and verify exact note text in the main agent before escalation or edits. <br>
Risk: Classification, frontmatter, move, rename, or canonical-page changes can make vault navigation or backlinks misleading if applied too broadly. <br>
Mitigation: Inventory first, keep writes serialized within 3-10 related notes, and run frontmatter and link checks after each write slice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thenerdforge/obsidian-vault-curator) <br>
- [Status schema](references/status-schema.md) <br>
- [Classification rubric](references/classification-rubric.md) <br>
- [Workflow](references/workflow.md) <br>
- [Subagent model](references/subagents.md) <br>
- [Subagent packet examples](references/subagent-packets.md) <br>
- [Output and merge format](references/output-format.md) <br>
- [Bases and review views](references/bases-views.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON reports, shell commands, and small configuration or frontmatter snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bounded read-only review passes by default and proposes serialized 3-10 note write slices when edits are appropriate.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
