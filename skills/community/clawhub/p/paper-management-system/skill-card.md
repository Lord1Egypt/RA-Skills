## Description: <br>
Automates PDF paper indexing, metadata extraction, search, renaming, full-text extraction, and optional AI summarization for research-paper collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crayfish-ai](https://clawhub.ai/user/crayfish-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to organize local PDF paper collections, index metadata into SQLite, search papers by keyword or bibliographic fields, and optionally generate structured summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional notification feature can execute shell commands built from PDF-derived text. <br>
Mitigation: Leave notifications disabled unless the PDFs and configured notification command are trusted; prefer a fixed, argument-based notification adapter instead of shell execution. <br>
Risk: The SQLite database may contain extracted full text from private or unpublished papers. <br>
Mitigation: Store the database in a dedicated protected workspace, back it up deliberately, and handle it as sensitive research data. <br>
Risk: Indexing and renaming modify files in the configured papers and downloads directories. <br>
Mitigation: Run the skill only in a dedicated papers/downloads workspace and keep backups before enabling automated cron processing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crayfish-ai/paper-management-system) <br>
- [Publisher profile](https://clawhub.ai/user/crayfish-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, local file outputs, SQLite records, renamed PDF files, and optional structured summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Operates on local PDF, downloads, data, and logs directories; optional AI summarization uses an OpenAI API key when enabled.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
