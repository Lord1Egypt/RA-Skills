## Description: <br>
Anticipates needs, keeps work moving, and improves through use so the agent gets more proactive over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to make an assistant more proactive: tracking local operating notes, recovering task context, surfacing timely next steps, and following learned boundaries before taking action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local proactive notes may accumulate sensitive or unnecessary personal or project details. <br>
Mitigation: Review ~/proactivity periodically and avoid storing secrets or highly sensitive information in those files. <br>
Risk: Workspace integration snippets can change how an agent behaves in a project. <br>
Mitigation: Require explicit approval and show the exact proposed lines before writing outside ~/proactivity/. <br>
Risk: Overly broad proactive behavior can interrupt users or exceed expected boundaries. <br>
Mitigation: Use learned action boundaries, stay silent on weak signals, and ask before external communication, spending, deletion, scheduling, or commitments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muguozi1/muguozi1-openclaw-proactivity) <br>
- [Skill homepage](https://clawic.com/skills/proactivity) <br>
- [Setup guide](artifact/setup.md) <br>
- [Boundary learning](artifact/boundaries.md) <br>
- [Execution patterns](artifact/execution.md) <br>
- [State routing](artifact/state.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and local state file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local proactive state under ~/proactivity/ and proposes workspace integration snippets only with explicit approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
