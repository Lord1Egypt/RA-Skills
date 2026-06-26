## Description: <br>
Deterministic verification and reputation scoring for AI sub-agents, with code gates for coding work and a structural, grounding, and LLM-council pipeline for open-ended tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nefas11](https://clawhub.ai/user/Nefas11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to spawn sub-agents, verify claimed completion, score reliability over time, and apply supervision levels based on observed results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spawn local agent CLIs and run configured verification commands. <br>
Mitigation: Use it only in trusted workspaces, review task contracts before execution, and keep spawned agents constrained to intended working directories and credentials. <br>
Risk: HTTP mode and grounding checks can make outbound or local URL requests. <br>
Mitigation: Keep endpoints local or trusted, avoid sensitive internal URLs unless intended, and use network-disabling configuration when URL checks are not needed. <br>
Risk: The skill stores task and reputation metadata locally. <br>
Mitigation: Review the configured workspace and database path, avoid storing sensitive task content when unnecessary, and clean state between unrelated projects. <br>
Risk: Direct spawn or self-reporting paths may not prove that every advertised verification gate ran. <br>
Mitigation: Inspect recorded verification results and prefer deterministic gates or council verdicts that explicitly show which checks executed and passed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Nefas11/governed-agents) <br>
- [Source Repository](https://github.com/Nefas11/governed-agents) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and shell examples, JSON task-result schemas, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate verification prompts, structured verdict summaries, local reputation records, and subprocess commands for configured agent CLIs.] <br>

## Skill Version(s): <br>
0.1.11 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
