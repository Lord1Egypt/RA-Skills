## Description: <br>
Automates desktop GUI workflows via computer use API with screenshot capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to automate visual desktop workflows, test web applications through GUI interaction, fill forms, navigate menus, and verify actions from screenshots when CLI or API paths are not sufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose desktop contents through screenshots and control the keyboard and mouse. <br>
Mitigation: Install only when intentional, run it in an isolated VM, container, or display session, and close private applications before use. <br>
Risk: Automated GUI actions can affect sensitive accounts or produce real-world consequences. <br>
Mitigation: Avoid banking or other sensitive services and require human confirmation before consequential actions. <br>
Risk: Long-running agent loops can continue taking actions or incur API cost. <br>
Mitigation: Use iteration caps and monitor runs during desktop automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-phantom-computer-control) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/phantom) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include safety guidance for sandboxing, iteration limits, and human confirmation before consequential GUI actions.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
