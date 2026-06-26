## Description: <br>
Measure and display AI model response latency when the user types /ping or /ping followed by a model name, with formatted timing output and optional model comparison. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[dofbi](https://clawhub.ai/user/dofbi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users can run this skill to display ping-style timing output for the current or named model. Based on the security evidence, its current latency results should be treated as demonstration formatting rather than real benchmark data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present simulated latency numbers as if they were real model measurements. <br>
Mitigation: Treat the output as demo formatting only; do not use it for model selection, routing, incident diagnosis, or performance claims until actual model-call timing is implemented and clearly labeled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dofbi/ping-model) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text with fixed ping and comparison layouts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node; prints timestamps, formatted duration, and optional comparison ranking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
