## Description: <br>
Organizes local knowledge bases by helping merge related content, standardize file names, remove duplicates, and update directory indexes for Markdown documents, scripts, and configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheney87](https://clawhub.ai/user/cheney87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, documentation maintainers, and agents use this skill to reorganize local knowledge-base folders, consolidate overlapping Markdown content, apply a consistent numbered naming scheme, and keep README indexes aligned with the resulting file structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File rename, merge, or deletion workflows can remove information or make local documentation harder to recover. <br>
Mitigation: Use --dry-run first, keep the target knowledge base under version control or backed up, and review proposed rm and mv actions before allowing changes. <br>
Risk: Over-aggressive duplicate-content consolidation can omit useful non-duplicate context. <br>
Mitigation: Compare source files before merging and preserve non-duplicate content with clear section headings. <br>


## Reference(s): <br>
- [Knowledge Base Organizer release page](https://clawhub.ai/cheney87/knowledge-base-organizer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and file-organization conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file merges, renames, removals, and README index updates; use dry-run or review steps before applying changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
