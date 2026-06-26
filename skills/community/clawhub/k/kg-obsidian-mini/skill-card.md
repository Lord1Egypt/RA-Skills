## Description: <br>
A compact Obsidian knowledge-graph note workflow that analyzes notes before editing, creates execution checklists, classifies four note types, normalizes direct links, fills relationships, deduplicates notes, and previews enrichment with YAML-oriented Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realpda](https://clawhub.ai/user/realpda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize an Obsidian vault into a small knowledge-graph note system while preserving original note text and requiring review before modifications. It supports note classification, relationship-note creation, duplicate cleanup planning, YAML validation, and enrichment preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify, rename, move, or delete local notes during execution. <br>
Mitigation: Use it only on a backed-up vault, require dry-run or checklist previews before file-changing operations, and approve each proposed change before execution. <br>
Risk: The enrichment workflow may use web search or remote image checks that expose note-derived topics or URLs. <br>
Mitigation: Approve each external search or remote image check only when sharing the related note topic or URL is acceptable. <br>
Risk: Incorrect classification, relationship creation, or deduplication could alter the meaning or structure of a knowledge graph. <br>
Mitigation: Review generated execution checklists and final change summaries before accepting edits, especially for relationship notes and duplicate removal. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realpda/kg-obsidian-mini) <br>
- [Publisher profile](https://clawhub.ai/user/realpda) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, execution checklists, note edits, and JSON previews from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, move, rename, patch, or delete local Obsidian notes after analysis and user review; helper scripts read local Markdown files and validate YAML frontmatter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
