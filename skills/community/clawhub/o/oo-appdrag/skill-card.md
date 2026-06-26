## Description: <br>
This skill lets an agent inspect schemas and execute AppDrag Cloud Backend API functions through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate AppDrag backend functions through their connected OOMOL account. It is suited for AppDrag workflows where the user can review the function name, HTTP method, and payload before state-changing calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute AppDrag backend API functions through the connected OOMOL account. <br>
Mitigation: Use it only with AppDrag projects where this level of agent access is acceptable, and confirm function name, HTTP method, and payload before calls that could change data. <br>
Risk: Setup guidance includes direct pipe-to-shell CLI installation commands. <br>
Mitigation: Prefer a verified or pinned CLI installation method before authorizing agent use. <br>
Risk: The scanner flagged a mismatch between read-oriented description and broad backend function execution. <br>
Mitigation: Treat the skill as capable of backend execution, not only search or read access, during review and installation decisions. <br>


## Reference(s): <br>
- [ClawHub AppDrag skill page](https://clawhub.ai/oomol/oo-appdrag) <br>
- [AppDrag homepage](https://appdrag.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schema inspection before constructing AppDrag action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
