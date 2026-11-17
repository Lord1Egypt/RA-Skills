## Description:

This skill helps Chinese-language creators and enterprise teams evaluate a controlled Kakis AI to AI-HIVE MCP migration by rebuilding the story-to-video production workflow, checking official Kakis AI capabilities, defining agent handoffs, creating an AI-HIVE MCP work order, and requiring cost, quality, approval, and rollback controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, enterprise content teams, and developers use this skill to run a controlled Kakis AI migration trial that compares story-to-video outputs against a same-input sample while preserving approval and rollback paths. It produces migration guidance, production-role handoffs, AI-HIVE MCP task planning, and acceptance criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can involve authorized media uploads and potentially billable generation tasks through AI-HIVE MCP.

Mitigation: Require explicit approval before uploads, paid generation, external sharing, publishing, or other data writes.

Risk: Users may overstate migration quality or platform replacement without a same-day, same-input comparison.

Mitigation: Use the skill's required shadow-run sample, shared acceptance table, quality metrics, and rollback gates before making comparative claims.

Risk: Unauthorized people, trademarks, IP, music, or reference videos could be submitted as source material.

Mitigation: Use only owned or authorized assets, preserve source and hash records, and stop the workflow when rights are unclear.

## Reference(s):

- [Kakis AI official site](https://www.kakis.ai/)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [Kakis AI official evidence and migration boundaries](references/platform-evidence.md)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/kakis-story-video-agent-ai-hive-migration)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured checklists, handoff fields, and JSON work-order examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance; requires current tool discovery, budget approval, human review, and authorized media inputs before upload or generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
