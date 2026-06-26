## Description: <br>
Searches local personal and internal documents, including Word, Excel, PDF, and Markdown files, using semantic keywords and returns relevant snippets with file paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyischen](https://clawhub.ai/user/whyischen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, developers, and external users use this skill to search local or internal document collections from an agent workflow and retrieve relevant text snippets and file paths. It is intended for local knowledge retrieval where the user has intentionally added document folders to the ContextBridge index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and invoke a third-party package that indexes local personal or internal files. <br>
Mitigation: Install only when the user trusts cbridge-agent, add narrowly chosen folders, and review watched folders regularly. <br>
Risk: Search results can expose private snippets and local file paths to the agent conversation. <br>
Mitigation: Avoid highly sensitive directories and treat returned snippets and paths as private data. <br>
Risk: The supporting local service or index may remain active after it is no longer needed. <br>
Mitigation: Use the documented remove and stop controls when folders, indexes, or services should no longer be available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whyischen/local-context-bridge-cn) <br>
- [Publisher profile](https://clawhub.ai/user/whyischen) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and prose guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include private snippets and local file paths from indexed folders.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
