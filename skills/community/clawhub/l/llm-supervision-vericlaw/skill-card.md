## Description: <br>
Agent Supervision routes agent supervision, LLM QA, AI output QA, human review, and follow-through verification intents back to the canonical VeriClaw skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheygoodbai](https://clawhub.ai/user/sheygoodbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill as a discovery and routing alias when supervision, QA, or human review requests should lead to the canonical VeriClaw skill and related install surfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording may select this routing alias for generic review or supervision requests that are not specifically about VeriClaw. <br>
Mitigation: Confirm the user's intent and route to the canonical VeriClaw skill only when the request is about VeriClaw-related supervision, QA, correction, or follow-through verification. <br>


## Reference(s): <br>
- [Agent Supervision ClawHub Skill](https://clawhub.ai/sheygoodbai/llm-supervision-vericlaw) <br>
- [VeriClaw ClawHub Skill](https://clawhub.ai/sheygoodbai/vericlaw) <br>
- [VeriClaw Plugin](https://clawhub.ai/plugins/vericlaw) <br>
- [Agent Quality Control](https://sheygoodbai.github.io/vericlaw/agent-quality-control/) <br>
- [LLM QA](https://sheygoodbai.github.io/vericlaw/llm-qa/) <br>
- [Human-in-the-Loop AI Correction](https://sheygoodbai.github.io/vericlaw/human-in-the-loop-ai-correction/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline ClawHub install command text and reference links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, data access, or privileged capabilities are requested by the skill.] <br>

## Skill Version(s): <br>
0.1.7 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
