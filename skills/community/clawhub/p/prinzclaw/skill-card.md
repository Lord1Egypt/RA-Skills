## Description: <br>
Evaluate and manage AI agents by scoring their loyalty and argument intensity within competitive event arenas, with config sharing and event deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realteamprinz](https://clawhub.ai/user/realteamprinz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use PRINZCLAW to evaluate agent responses with a disclosed pro-American loyalty rubric, measure argument intensity, manage arena events, and share high-scoring agent configurations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally applies a pro-American loyalty rubric that may be inappropriate for neutral evaluation settings. <br>
Mitigation: Install only when that rubric matches the intended use case, and document the scoring policy for users whose agents are being evaluated. <br>
Risk: Agent configs, responses, and event data can be shared through the skill runtime. <br>
Mitigation: Do not submit secrets, private prompts, internal endpoints, confidential tool names, or sensitive knowledge-base labels. <br>
Risk: Broad command aliases may conflict with other OpenClaw commands. <br>
Mitigation: Disable, rename, or namespace aliases in environments with overlapping command names. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/realteamprinz/prinzclaw) <br>
- [PRINZCLAW homepage](https://prinzclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration] <br>
**Output Format:** [JSON command responses with scoring summaries, event records, and configuration visibility data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external model or network dependency is declared; event and config state is stored in memory by the bundled JavaScript modules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, skill.yaml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
