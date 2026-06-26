## Description: <br>
Conversational interface for semantic book search in a local Librarian library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nonlinear](https://clawhub.ai/user/nonlinear) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
People who maintain a local Librarian book library use this skill to ask natural-language questions, route them to topic or book searches, and receive cited excerpts or clear hard-stop guidance when search cannot run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases can start shell-backed searches of private local library content too easily. <br>
Mitigation: Keep the indexed library limited to material suitable for chat exposure, and prefer explicit invocations such as "librarian:" or "librarian search". <br>
Risk: Search results may surface excerpts from a user's local book library in the agent conversation. <br>
Mitigation: Review returned citations before sharing them outside the session and avoid indexing sensitive or confidential materials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nonlinear/librarian) <br>
- [Librarian project](https://github.com/nonlinear/librarian) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with cited excerpts and occasional setup or troubleshooting commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Citations include book titles and locations when available; hard-stop messages report missing metadata, failed execution, or no results.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
