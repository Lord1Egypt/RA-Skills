## Description: <br>
Automates desktop GUI workflows via computer use API with screenshot capture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to run opt-in computer-use workflows that inspect GUI state through screenshots and drive mouse or keyboard actions for desktop and browser tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshot capture can expose private information visible on the desktop. <br>
Mitigation: Run the workflow in a sandbox, VM, or controlled display session and close sensitive applications before use. <br>
Risk: Synthesized mouse and keyboard actions can change application state or trigger real-world effects. <br>
Mitigation: Keep the skill opt-in, use human approval for consequential actions, and prefer dry-run or confirmation steps where available. <br>
Risk: Long-running computer-use loops can consume API budget or continue acting after a task becomes ambiguous. <br>
Mitigation: Set iteration caps and review progress between steps, especially for workflows involving credentials, package installs, or production systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-phantom-computer-control) <br>
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/phantom) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include screenshot-informed action plans, environment checks, and confirmation guidance.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
