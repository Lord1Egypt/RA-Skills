## Description: <br>
Generates structured Obsidian markdown lecture notes from lectures, articles, videos, URLs, transcripts, and PDFs, including a hub note, recursive atomic notes, glossary entries, Mermaid diagrams, comparison tables, bilingual terms, and wikilinks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SchaeferAnjon](https://clawhub.ai/user/SchaeferAnjon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, educators, researchers, and knowledge workers use this skill to convert source material into an Obsidian-ready study vault with a main hub note, recursive concept notes, glossary entries, review questions, diagrams, and optional chart assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes note files and optional chart assets to local directories, including the configured Obsidian vault path. <br>
Mitigation: Use a test folder first, review the planned file tree and destination path, and confirm the output directory before allowing writes. <br>
Risk: The skill can process URLs, videos, PDFs, transcripts, and documents, which may expose private material if external extraction or model tools are used. <br>
Mitigation: Avoid sending private URLs or documents through external extraction or model tools unless that processing is acceptable. <br>
Risk: Generated study notes may need human review for accuracy, placeholders, and source fidelity before they are used for coursework or exam preparation. <br>
Mitigation: Review generated notes, diagrams, glossary entries, and review questions against the original source material before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SchaeferAnjon/lecture-notes-master) <br>
- [Publisher profile](https://clawhub.ai/user/SchaeferAnjon) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Usage examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Obsidian Markdown files with YAML frontmatter, Mermaid diagrams, wiki-links, tables, and optional PNG chart assets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured or user-specified output paths and may create local directories, note files, glossary files, and visualization assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
