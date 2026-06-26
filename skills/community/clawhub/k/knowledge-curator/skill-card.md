## Description: <br>
Knowledge Curator saves explicitly requested web links into a local Markdown knowledge base, summarizes and categorizes entries, and supports search, listing, deletion, statistics, and export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mayuyang-study](https://clawhub.ai/user/Mayuyang-study) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn saved links from supported platforms into searchable local Markdown knowledge-base entries for later retrieval and export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted links may be fetched and saved into a local knowledge base, including content the user did not intend to persist if save intent is ambiguous. <br>
Mitigation: Use explicit save commands, avoid private or authenticated URLs, and review saved entries before sharing or exporting. <br>
Risk: The skill can delete or export stored knowledge-base entries. <br>
Mitigation: Review target IDs and exported content before running delete or export commands, and keep backups of the knowledge-base folder. <br>
Risk: Fetched content and generated summaries may be incomplete, inaccurate, or affected by platform access limits. <br>
Mitigation: Check source links and stored Markdown entries before relying on them for decisions. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/Mayuyang-study/knowledge-curator) <br>
- [README.md](artifact/README.md) <br>
- [QUICKSTART.md](artifact/QUICKSTART.md) <br>
- [examples.md](artifact/references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown knowledge-base entries with text command responses; exports may be Markdown, JSON, or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores entries in a local knowledge-base folder and maintains an index file; fetches user-submitted links when save intent is explicit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
