## Description: <br>
Builds and searches a local index of OpenClaw memory and knowledge files, returning ranked snippets with file paths and line numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to search local memory, memory folder, and knowledge files from the command line and retrieve the most relevant snippets for a query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory and knowledge file contents may be embedded by the local Ollama service and stored persistently in ~/.openclaw/memory_index.json. <br>
Mitigation: Review indexed paths before building the index, avoid storing secrets in those files, and delete the index when that retained content is no longer needed. <br>
Risk: The release under-discloses its indexing and persistence behavior. <br>
Mitigation: Review the artifact behavior before deployment and run it only where local memory content is appropriate to process and retain. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text command output with ranked snippets and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes similarity scores, relative file paths, line ranges, and short content previews.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
