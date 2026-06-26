## Description: <br>
Fast filesystem catalog for finding files by name, date, type, or size; it indexes metadata only and uses SQLite for quick lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lookupmark](https://clawhub.ai/user/lookupmark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to build or update a local metadata index and find files by filename, extension, size, or modified date without indexing file contents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local SQLite catalog can contain filenames, full paths, sizes, and dates from indexed folders. <br>
Mitigation: Review the configured folders before rebuilding or scheduling updates, and avoid placing sensitive filenames or symlinks in indexed locations when path privacy matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lookupmark/lookupmark-file-indexer) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Indexes local file metadata such as path, filename, extension, size, and modified date; it does not index file contents.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
