## Description: <br>
Make any AI model (GPT-5.4, Gemini, Ollama) behave more like Claude by applying named failure modes, a cognitive performance framework, and a drop-in system prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rushindrasinha](https://clawhub.ai/user/rushindrasinha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to adapt model behavior when setting up a new agent, switching away from Claude, or reducing patterns such as sycophancy, padding, unverified claims, and premature completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The prompt changes how an agent responds and encourages more autonomous low-risk action. <br>
Mitigation: Review and approve the prompt before adding it to a system prompt or shared agent configuration. <br>
Risk: Capability tags appear broader than the markdown-only artifact behavior. <br>
Mitigation: Confirm capability metadata during publication review and avoid granting runtime permissions based only on tags. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rushindrasinha/model-behavior-layer) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/rushindrasinha) <br>
- [Make Any Model Behave Like Claude](artifact/MAKE_ANY_MODEL_CLAUDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with a drop-in system prompt block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The artifact is markdown-only and does not install code or access data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
