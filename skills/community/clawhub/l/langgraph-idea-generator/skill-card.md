## Description: <br>
Langgraph Idea Generator turns a one-sentence coding request into a three-line executable implementation plan using a LangGraph classification, complexity, and planning pipeline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colbertlee](https://clawhub.ai/user/colbertlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation-focused users use this skill to quickly classify a coding idea, estimate its complexity, and get a compact implementation plan with a command, scenario, and suggested script path. It is also useful as a LangGraph state-machine example. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user prompt and a small local list of OpenClaw script filenames to the MiniMax API. <br>
Mitigation: Avoid entering secrets, confidential client or project names, and remove sensitive filenames from the scanned scripts directory before use. <br>
Risk: Generated coding plans may be incomplete or unsuitable for a particular environment. <br>
Mitigation: Review generated commands, file paths, and implementation guidance before creating or running code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/colbertlee/langgraph-idea-generator) <br>
- [Publisher profile](https://clawhub.ai/user/colbertlee) <br>
- [MiniMax Anthropic-compatible API endpoint](https://api.minimaxi.com/anthropic) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Code, Guidance] <br>
**Output Format:** [Plain text CLI output, or JSON when IDEA_GEN_JSON=1] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes category, complexity, a three-line implementation plan, and local script filename context used for deduplication.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
