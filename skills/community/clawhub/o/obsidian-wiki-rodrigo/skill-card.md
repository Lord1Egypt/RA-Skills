## Description: <br>
Work with Rodion's Obsidian vault via Nextcloud, including ingest, query, and lint workflows for a Karpathy-style wiki pattern. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rodrigo09313](https://clawhub.ai/user/rodrigo09313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage an Obsidian knowledge base stored in Nextcloud by ingesting source material, querying indexed wiki pages, checking wiki health, and syncing file changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently modify and sync Obsidian or Nextcloud vault content. <br>
Mitigation: Define the exact vault path before use and require explicit confirmation before ingesting content, updating indexes or logs, linting with writes, or syncing changes. <br>
Risk: Incorrect ingest or lint output could add misleading summaries, entities, concepts, or cross-references to the knowledge base. <br>
Mitigation: Review generated Markdown changes before sync and keep raw source material immutable for comparison. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rodrigo09313/obsidian-wiki-rodrigo) <br>
- [Wiki Operations](references/operations.md) <br>
- [Nextcloud Sync](references/sync.md) <br>
- [Wiki Structure](references/wiki-structure.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Markdown wiki files, append log entries, and propose or run Nextcloud sync commands when authorized.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
