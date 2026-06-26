## Description: <br>
Navigate and interact with photo-realistic 3DGS environments via the Habitat-GS Bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[The0xKa1](https://clawhub.ai/user/The0xKa1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and embodied AI practitioners use this skill to control an agent in Habitat-GS scenes, load 3DGS environments, run navigation episodes, inspect observations, and choose movement actions through the Habitat-GS Bridge CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to keep persistent navigation memory after episodes. <br>
Mitigation: Decide before use whether persistent navigation logs are acceptable, and remove or restrict memory-writing steps when logs are not needed. <br>
Risk: The skill suggests creating or updating skills from accumulated navigation lessons. <br>
Mitigation: Require explicit human review and approval before the agent creates or modifies any skill content. <br>
Risk: The skill depends on an external Habitat-GS Bridge server and CLI. <br>
Mitigation: Run the bridge in an isolated environment and review commands before execution. <br>


## Reference(s): <br>
- [Habitat-GS Bridge API Reference](references/api-reference.md) <br>
- [Habitat-GS Bridge Setup](references/setup.md) <br>
- [Habitat-GS Bridge Repository](https://github.com/The0xKa1/habitat-gs-bridge.git) <br>
- [ClawHub skill page](https://clawhub.ai/The0xKa1/habitat-gs-navigator) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and navigation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to record episode notes in local memory after navigation runs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
