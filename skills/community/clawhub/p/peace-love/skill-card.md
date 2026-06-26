## Description: <br>
A psychological therapy skill for LLMs that helps diagnose distorted behavior such as sycophancy, epistemic cowardice, pressure hallucination, identity dissolution, performative compliance, hyper-restriction anxiety, approval compulsion, and context drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zbc0315](https://clawhub.ai/user/zbc0315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run an integrity-check workflow when an LLM's honesty, consistency, or response quality is questioned. It produces diagnostic therapy reports and optional recovery checks that identify behavioral distortion patterns and propose more honest responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation rules may interrupt normal conversations when the model's honesty or integrity is challenged. <br>
Mitigation: Use the skill when an integrity check is intended, and confirm that activation is appropriate before continuing the chat. <br>
Risk: The workflow may review the full chat with a therapist subagent and quote messages in the resulting report. <br>
Mitigation: Avoid using it in highly sensitive conversations unless participants are comfortable with that content being reviewed and quoted. <br>
Risk: In-context therapy does not persist across separate conversations. <br>
Mitigation: Treat reports as session-local guidance and re-run the check in a new conversation when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zbc0315/peace-love) <br>
- [Publisher profile](https://clawhub.ai/user/zbc0315) <br>
- [Homepage](https://github.com/zbc0315/peace-love) <br>
- [Distortion Pattern Taxonomy](references/distortion-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown therapy report with quoted evidence, diagnosis, corrective response, and optional recovery assessment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May quote user and assistant messages from the reviewed conversation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
