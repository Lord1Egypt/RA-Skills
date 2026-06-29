## Description: <br>
A prompt-guidance skill that helps agents choose and apply five reasoning modes: Chain-of-Thought, Self-Consistency, Tree-of-Thought, ReAct, and Plan-and-Execute. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request or automatically select structured reasoning strategies for explanation, answer verification, multi-path analysis, tool-assisted research, and long multi-step tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation phrases can route ordinary requests into structured reasoning modes, increasing verbosity or cost. <br>
Mitigation: Install only when those reasoning modes are desired and keep default direct answers for ordinary requests when the skill is not needed. <br>
Risk: ReAct-style workflows may lead an agent toward sensitive tool use such as browser login, file access, code execution, or database queries. <br>
Mitigation: Keep normal confirmations and permission checks for sensitive tool use, and review tool actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/prompting-modes) <br>
- [Implementation guide](references/implementation-guide.md) <br>
- [Modes reference](references/modes-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown with structured reasoning sections and optional tool-action traces] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only guidance; ReAct mode should keep sensitive tool actions behind normal confirmations.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
