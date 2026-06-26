## Description: <br>
Isolate and coordinate sub-agent memory in OpenClaw with Hippocampus using scoped IDs, bounded merge-back, and explicit cross-agent imports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cezexPL](https://clawhub.ai/user/cezexPL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when OpenClaw spawns sub-agents that need isolated Hippocampus memory namespaces. It helps return bounded summaries or artifacts to a parent agent and import only explicitly approved child-agent memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child-agent context may include sensitive or excessive information if full transcripts are merged into parent memory. <br>
Mitigation: Import only explicitly approved summaries, artifacts, and references; avoid merging full child-agent transcripts. <br>
Risk: Persistent memory may retain sensitive data longer than intended. <br>
Mitigation: Keep sensitive data out of persistent memory unless storage is intentional and approved. <br>
Risk: Incorrect child-agent outputs could be promoted into parent memory without review. <br>
Mitigation: Review child-agent summaries and artifacts before importing them into parent memory. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with ordered workflow steps, bullets, and inline configuration identifiers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution; provides memory-isolation guidance for scoped sub-agent contexts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
