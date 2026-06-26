## Description: <br>
Multi-model AI debate platform. Submit a topic and multiple AIs deliberate across rounds, producing structured insights and a polished research report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DreamArc77](https://clawhub.ai/user/DreamArc77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to send research, analysis, debate, or investigation topics to LLM Conclave, where multiple AI models deliberate across rounds and return structured conclusions and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided topics to an external AI-debate service and may spend account credits. <br>
Mitigation: Require explicit confirmation before each debate, including model choice, estimated credit cost, locale, and external data sharing. <br>
Risk: The skill requests a bearer API key and the evidence notes unclear secret-handling limits. <br>
Mitigation: Provide the API key only through a secure secret mechanism, do not store it in long-term memory or logs, and rotate it if it was pasted into ordinary chat. <br>
Risk: The artifact asks agents to remember a broad trigger for research, analysis, debate, or investigation topics. <br>
Mitigation: Do not accept the broad long-term memory trigger as written; treat LLM Conclave use as an explicit per-session user decision. <br>


## Reference(s): <br>
- [LLM Conclave homepage](https://llmconclave.com) <br>
- [LLM Conclave skill source](https://llmconclave.com/skill.md) <br>
- [LLM Conclave package metadata](https://llmconclave.com/skill.json) <br>
- [ClawHub skill page](https://clawhub.ai/DreamArc77/llmconclave) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown and text responses with API request examples and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Debate runs use Server-Sent Events, bearer authentication, model selection, round count, locale, and credit balance checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
