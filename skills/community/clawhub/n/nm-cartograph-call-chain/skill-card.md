## Description: <br>
Traces execution paths through the code graph with criticality scoring and Mermaid charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect how a function or entry point propagates through a codebase, visualize the call chain, and assess criticality factors such as file spread, security sensitivity, external calls, test gaps, and depth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects local repository code and may use an existing gauntlet plugin from the user's Claude plugins directory. <br>
Mitigation: Use it only in repositories the user is comfortable having analyzed by their coding agent, and review proposed commands before execution. <br>
Risk: When gauntlet graph data is unavailable, static search fallback can produce incomplete or approximate call-chain analysis. <br>
Mitigation: Treat fallback results as review aids and verify important call paths against source code before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/athola/skills/nm-cartograph-call-chain) <br>
- [Cartograph Homepage](https://github.com/athola/claude-night-market/tree/master/plugins/cartograph) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Code] <br>
**Output Format:** [Markdown with shell command examples and Mermaid diagrams] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use an existing gauntlet graph query helper when available, or static search fallback when graph data is unavailable.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
