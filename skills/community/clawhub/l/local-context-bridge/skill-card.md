## Description: <br>
Searches local personal and internal Word, Excel, PDF, and Markdown documents with semantic keywords and returns relevant snippets and file paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whyischen](https://clawhub.ai/user/whyischen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to locate information in approved local or internal document folders and decide whether retrieved snippets are enough to answer a user request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search selected local or internal folders that may contain private or sensitive documents. <br>
Mitigation: Limit watched directories to approved locations and avoid adding folders that contain secrets, personal records, or highly sensitive material. <br>
Risk: Automatic local search can expose private document snippets without clear consent boundaries. <br>
Mitigation: Configure workflows so the agent asks before searching or reading private documents, and review snippets before using them in responses. <br>
Risk: The skill depends on an external local package for indexing and search behavior. <br>
Mitigation: Review the cbridge-agent package before installation or updates and install only versions approved for the environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/whyischen/local-context-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and retrieved text snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include local file paths and excerpts from indexed documents.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
