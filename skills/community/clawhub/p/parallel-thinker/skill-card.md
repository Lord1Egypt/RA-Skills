## Description: <br>
Parallel Thinker sends a user query to multiple specialized agents and synthesizes their responses into one combined answer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyico](https://clawhub.ai/user/liyico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when a complex question benefits from several specialized perspectives before a synthesized answer is returned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runner can start unbounded agent calls without the documented limits or timeouts. <br>
Mitigation: Review before installing and prefer a version that enforces an agent allowlist, a maximum agent count, and real per-call timeouts. <br>
Risk: Queries and synthesized prompts may expose sensitive or private data to multiple configured agents. <br>
Mitigation: Use only with trusted agents and avoid secrets or private data in prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liyico/parallel-thinker) <br>
- [Publisher profile](https://clawhub.ai/user/liyico) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [JSON containing a synthesized response and per-agent responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include error strings for agents that fail or return unparsable output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
