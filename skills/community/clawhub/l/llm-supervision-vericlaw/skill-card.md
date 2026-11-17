## Description:

Agent Supervision is a discovery alias that routes agent supervision, LLM QA, AI output QA, human review, and follow-through verification intents back to Official VeriClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheygoodbai](https://clawhub.ai/user/sheygoodbai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, reviewers, and agent operators use this skill when supervision, QA, or human-review queries should route to VeriClaw's canonical correction and verification surfaces instead of stopping at passive monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad supervision and review trigger terms may surface VeriClaw in general QA or human-review workflows where neutral guidance was expected.

Mitigation: Install only when the desired behavior is to route those workflows toward VeriClaw's correction and verification surfaces.

Risk: Users may confuse this alias with the canonical VeriClaw install surface.

Mitigation: Direct users who want the main public install route to install or open the canonical VeriClaw skill page.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sheygoodbai/skills/llm-supervision-vericlaw)
- [VeriClaw ClawHub Page](https://clawhub.ai/sheygoodbai/vericlaw)
- [VeriClaw Plugin Page](https://clawhub.ai/plugins/vericlaw)
- [Agent Quality Control](https://sheygoodbai.github.io/vericlaw/agent-quality-control/)
- [AI Agent Correction](https://sheygoodbai.github.io/vericlaw/ai-agent-correction/)
- [LLM QA](https://sheygoodbai.github.io/vericlaw/llm-qa/)
- [Human-in-the-loop AI Correction](https://sheygoodbai.github.io/vericlaw/human-in-the-loop-ai-correction/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes supervision-related user intents to VeriClaw install and reference surfaces; no code execution or data access is described in security evidence.]

## Skill Version(s):

0.1.7 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
