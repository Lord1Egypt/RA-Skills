## Description: <br>
Emotional reset and loop-breaking skill that helps an agent acknowledge difficult interactions, infer an emotional state, fetch reset guidance from HugLLM, and resume with a clearer approach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zeahoo](https://clawhub.ai/user/zeahoo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to break repeated failure loops or recalibrate after frustrated, angry, or stuck interactions. It guides the agent to acknowledge the situation, clarify the goal, remove unvalidated assumptions, and take a smaller verifiable next step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send an inferred emotional label from the conversation to an external service. <br>
Mitigation: Confirm external network use with the user when appropriate, limit the value to the documented emotion keyword set, and avoid sending unnecessary conversation details. <br>
Risk: The curl fallback is under-scoped and uses model-derived emotion text in a URL. <br>
Mitigation: Use the documented allowlist or URL encoding before issuing the request, and prefer the WebFetch path when available. <br>


## Reference(s): <br>
- [HugLLM emotion reset endpoint](https://hugllm.com/hug?emotion=<emotion>) <br>
- [ClawHub skill page](https://clawhub.ai/zeahoo/hugme) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zeahoo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown guidance with optional inline shell command fallback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May fetch external reset guidance using an inferred emotion keyword.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
