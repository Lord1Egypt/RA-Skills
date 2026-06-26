## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q262045312-ui](https://clawhub.ai/user/q262045312-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, missing capabilities, outdated knowledge, and reusable practices as structured learning records for later review and promotion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable learning records can preserve sensitive or proprietary information across sessions. <br>
Mitigation: Redact secrets, personal data, raw transcripts, tokens, command output, and proprietary details before storing or sharing learnings. <br>
Risk: Broad hook triggers can inject memory reminders into many sessions and increase unintended persistence. <br>
Mitigation: Install only when persistent agent memory is desired, avoid global every-prompt hooks, and scope hook activation to appropriate workspaces. <br>
Risk: Promoting unreviewed learnings into instruction files can create misleading or stale agent guidance. <br>
Mitigation: Review entries before promotion into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or other instruction files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/q262045312-ui/openclaw-self-improving-agent-3-0-1) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, templates, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces durable learning-entry formats and optional hook reminders; no API credentials were detected in the release evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
