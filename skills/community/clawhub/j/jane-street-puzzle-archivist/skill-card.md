## Description: <br>
Use when solving, organizing, or reviewing Jane Street monthly puzzles, especially when bootstrapping a new puzzle month, comparing against prior public solutions, capturing reusable solving patterns, submitting answers, or updating the long-lived puzzle archive and knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aznikline](https://clawhub.ai/user/aznikline) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, puzzle solvers, and archive maintainers use this skill to organize Jane Street monthly puzzle work, compare against public reference repositories, create reproducible solver artifacts, and preserve reusable solving notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow instructs agents to run local repository scripts for current puzzle metadata and reference indexing. <br>
Mitigation: Confirm the repository is trusted and review the referenced local scripts before execution. <br>
Risk: The workflow may create or update puzzle folders, solver scripts, notes, README entries, submission metadata, and shared archive knowledge files. <br>
Mitigation: Review proposed file changes and scan generated scripts before running, committing, or publishing them. <br>


## Reference(s): <br>
- [Reference Repositories](references/reference-repos.md) <br>
- [Solving Patterns](references/solving-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aznikline/jane-street-puzzle-archivist) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, generated solver code, archive files, and JSON submission metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update puzzle folders, solver scripts, notes, README entries, submission metadata, and shared archive knowledge files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
