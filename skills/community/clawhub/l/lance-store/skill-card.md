## Description: <br>
Persist and retrieve structured data using the Lance columnar format for cross-session storage, querying, and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vitorhugoze](https://clawhub.ai/user/vitorhugoze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Lance Store to persist structured outputs, conversation context, research records, and knowledge-base data across sessions, then inspect or query those datasets through local CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, read, overwrite, back up, and delete local datasets. <br>
Mitigation: Use it only when local persistent dataset management is intended, run it from the intended working directory, and make backups before update, delete, or drop operations. <br>
Risk: Stored datasets may contain secrets, credentials, personal data, or regulated information if users provide them. <br>
Mitigation: Avoid storing sensitive or regulated data unless separate access controls, retention rules, and handling procedures are in place. <br>
Risk: Some write paths are broader than the documentation suggests. <br>
Mitigation: Use simple dataset names without path characters, review backup paths before execution, and keep operations scoped to a controlled workspace. <br>
Risk: Lance field types are fixed by the first inserted record, so later appends with different types can fail. <br>
Mitigation: Inspect existing datasets with list-datasets-info and plan the schema before the first append. <br>


## Reference(s): <br>
- [Lance Store on ClawHub](https://clawhub.ai/vitorhugoze/lance-store) <br>
- [vitorhugoze ClawHub Profile](https://clawhub.ai/user/vitorhugoze) <br>
- [Lance Columnar Format](https://github.com/lance-format/lance) <br>
- [Lance Documentation](https://lance.org) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [JSON command responses plus concise Markdown or bash guidance for invoking the CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and modifies local Lance dataset directories and metadata in the current working directory.] <br>

## Skill Version(s): <br>
1.0.12 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
