## Description: <br>
Generates Mermaid and ASCII diagrams of palace structure, knowledge topology, and synapse connectivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect memory palace structure, knowledge topology, entity relationships, and synapse strength through Mermaid diagrams or inline ASCII overviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger terms such as memory, diagram, and graph may activate the skill for requests that are not specifically about memory-palace visualization. <br>
Mitigation: Confirm the request is about inspecting or presenting a memory palace before using the skill, and prefer a more specific skill for unrelated diagrams or knowledge search. <br>
Risk: The artifact states the skill contract is not yet wired into a command or agent flow, so generated guidance may require manual execution through the memory palace renderer. <br>
Mitigation: Use the documented PalaceRenderer workflow directly and review generated Mermaid or ASCII output before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-memory-palace-palace-diagram) <br>
- [Memory Palace plugin source](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Mermaid flowcharts or ASCII text, typically presented in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a memory palace knowledge graph and may use Mermaid rendering for diagram output.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
