## Description: <br>
Liuyan Feiyu runs a Chinese-language AI counseling-style CLI that switches among five counselor personas and periodically analyzes conversation history to produce self-reflection and personality-profile outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macaubigh](https://clawhub.ai/user/macaubigh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill for Chinese-language emotional conversation, self-exploration, non-clinical psychological support, and personality-pattern reflection. Operators can run the included CLI with an OpenAI-compatible model provider to support guided dialogue and structured self-reflection outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process emotional disclosures and infer personality traits from conversation history. <br>
Mitigation: Use clear consent and disclosure, minimize sensitive details, and restrict storage or sharing of conversation history. <br>
Risk: Conversation history is sent to an external OpenAI-compatible model provider. <br>
Mitigation: Review the configured provider, base URL, retention terms, and access controls before use. <br>
Risk: The counseling-style behavior could be mistaken for crisis care or clinical advice. <br>
Mitigation: Do not use the skill for crisis care or clinical decision-making; route self-harm or emergency cases to qualified professional support. <br>
Risk: The artifact uses broad dependency ranges for runtime packages. <br>
Mitigation: Pin and review dependencies before operational deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/macaubigh/liuyan-feiyu) <br>
- [Counselor personas](references/counselors.md) <br>
- [Personality analysis specification](references/personality-analysis.md) <br>
- [API integration guide](references/api-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance, Shell commands, Configuration] <br>
**Output Format:** [Simplified Chinese conversational text, JSON personality analysis, and Markdown setup guidance with shell commands and environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an OpenAI-compatible chat-completions provider and may produce structured personality summaries at conversation milestones.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
