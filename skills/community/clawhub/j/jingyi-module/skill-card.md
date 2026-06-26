## Description: <br>
Help users use Jingyi Module in E-language by searching command names, fetching official docs, and generating directly runnable code that the user can copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junqianglu3-netizen](https://clawhub.ai/user/junqianglu3-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users building Jingyi Module assistants use this skill to find relevant commands, fetch official command documentation, and generate copyable E-language code grounded in those docs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command documentation lookups may send command ids or names to ec.ijingyi.com. <br>
Mitigation: Use the lookup only when external documentation access is acceptable, and avoid sensitive query terms. <br>
Risk: Search may fail if the advertised command index is not supplied or rebuilt. <br>
Mitigation: Provide or rebuild the command index before relying on search results, and verify important commands by fetching the official document. <br>
Risk: Generated E-language code can still be wrong if documentation is incomplete or the selected command is not the intended one. <br>
Mitigation: Review the selected command, parameters, and return type before running generated code. <br>


## Reference(s): <br>
- [Jingyi Module official documentation](https://ec.ijingyi.com/sub.htm) <br>
- [ClawHub skill page](https://clawhub.ai/junqianglu3-netizen/jingyi-module) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with concise explanation and E-language code blocks; helper scripts may return JSON command lookup results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated code should start with the E-language version directive and should be based on fetched command signatures.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
