## Description: <br>
Turns books, long articles, research reports, and papers into a connected Zettelkasten-style knowledge network of structure notes, atomic notes, method notes, and index notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikonos](https://clawhub.ai/user/mikonos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Readers, analysts, researchers, and knowledge workers use this skill to deeply digest long-form source material and build a linked knowledge vault rather than a simple summary. It guides an agent through planning, structure extraction, index design, atomic note creation, method-note consolidation, and network review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow writes, moves, and cross-links Markdown notes in a knowledge vault, including index notes that may already exist. <br>
Mitigation: Confirm the daily-record and index paths before running it, keep backups, and review diffs before accepting edits to existing notes. <br>
Risk: The workflow may call companion skills such as structure-note, index-note, file-organize, or workflow-audit when they are available. <br>
Mitigation: Review companion skills before use and run the workflow manually when a companion skill is missing or untrusted. <br>
Risk: Source material without full text can lead to weaker case fidelity if the agent relies only on summaries or memory. <br>
Mitigation: Provide the original source when possible; when only summaries are available, require the notes to mark source limitations and avoid invented details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikonos/mikonos-deep-reading) <br>
- [README](README.md) <br>
- [Expert personas reference](references/expert_personas.md) <br>
- [Luhmann Scan workflow](references/luhmann_scan.md) <br>
- [Structure note template](templates/structure_note_template.md) <br>
- [Atomic note template](templates/atomic_note_template.md) <br>
- [Method note template](templates/method_note_template.md) <br>
- [Index note template](templates/index_note_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown notes, task checklists, YAML frontmatter, and wikilinks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates knowledge-vault notes in daily and index directories; outputs may include structure, atomic, method, index, task, and review notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
