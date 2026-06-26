## Description: <br>
Hermes Agent coordinates multi-agent task routing, OpenClaw session integration, opt-in local memory, and GEPA-style skill evolution for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[briefness](https://clawhub.ai/user/briefness) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to register specialized sub-agents, route tasks by topic, retain opt-in local workflow memory, and derive reusable skill patterns from successful executions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: When persistence is enabled, task inputs, outputs, step results, and reusable examples may be stored locally without broad redaction or retention controls. <br>
Mitigation: Keep persistence disabled for sensitive work, or enable it only with non-secret task data until stronger redaction, retention, deletion, and data-separation controls are added. <br>
Risk: Session fallback logging can expose more task payload detail if configured for full logs. <br>
Mitigation: Use the default summary logging or set fallback logging to off for sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/briefness/hermes-agent-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/briefness) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and Python examples, runtime task messages, configuration snippets, and optional local SQLite-backed memory and skill records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persistence is disabled by default and must be explicitly enabled through environment variables or runtime configuration.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
