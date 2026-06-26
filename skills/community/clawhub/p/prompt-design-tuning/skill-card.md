## Description: <br>
Collaboratively design, evaluate, iterate on, and recommend a final launch candidate for a target prompt under a human-gated, agent-executed workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abysscat-yj](https://clawhub.ai/user/abysscat-yj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prompt engineers use this skill to turn prompt design and tuning into a reviewable workflow with task specifications, target prompts, judge prompts, evaluation plans, controlled iteration, and final recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Execution mode may share evaluation data with selected model providers and incur API costs. <br>
Mitigation: Confirm provider data-sharing rules, redact secrets or sensitive data, use scoped test API keys, set budget and rate limits, and require approval before high-cost iteration loops. <br>
Risk: Generated scripts, prompts, or evaluation recommendations may be incorrect or unsuitable for launch without review. <br>
Mitigation: Review generated scripts before running them, keep target and judge prompt changes separated, maintain an experiment log, and require human review for the final launch candidate. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with optional code blocks and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-gated prompt-tuning artifacts, evaluation scripts, reports, and final recommendation material.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
