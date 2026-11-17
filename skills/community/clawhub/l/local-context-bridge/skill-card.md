## Description:

Searches local personal and internal Word, Excel, PDF, and Markdown documents with semantic keywords and returns relevant snippets and file paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyischen](https://clawhub.ai/user/whyischen)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and agent developers use this skill to retrieve relevant context from local or internal document collections without manually browsing files. It is suited for questions where the answer may exist in private documents already added to ContextBridge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local document searches can expose private or business data from watched directories.

Mitigation: Use a narrowly scoped document folder, avoid credential stores or unrelated private records, and require confirmation before searches that may touch sensitive local or business data.

Risk: Unpinned package installation and update behavior can change the reviewed software version.

Mitigation: Review the cbridge-agent package and version before installing or updating.

## Reference(s):

- [ContextBridge GitHub repository](https://github.com/whyischen/context-bridge)
- [ClawHub skill page](https://clawhub.ai/whyischen/skills/local-context-bridge)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local search result snippets with file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pip and the cbridge-agent CLI; searches only directories the user adds to ContextBridge.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
