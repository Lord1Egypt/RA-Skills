## Description: <br>
Detect if AI responses contain hallucinations by analyzing tool usage and response quality. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JDChi](https://clawhub.ai/user/JDChi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to review AI responses for likely hallucinations, missing verification, and invalid-premise handling. It can run on demand or, when explicitly enabled, append fact-check output after each response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When invoked or enabled, the skill may review and summarize prior chat context, which can expose sensitive details from earlier turns. <br>
Mitigation: Keep automatic mode off unless ongoing fact-check blocks are desired, and avoid invoking it in chats where summarizing earlier sensitive context would be inappropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JDChi/is-bullshit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown fact-check summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the user's language when reporting per-round verdicts.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
