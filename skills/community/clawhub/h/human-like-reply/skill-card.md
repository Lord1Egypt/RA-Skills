## Description: <br>
让AI回复更像真人，避免过度称呼和机械化的表达，使对话更加自然流畅。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HisongMo](https://clawhub.ai/user/HisongMo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to automatically make outgoing Chinese AI replies sound more natural by reducing repeated greetings, replacing mechanical phrases, and tuning casualness from configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outgoing replies may be rewritten into a more casual tone in contexts where exact wording or formality matters. <br>
Mitigation: Disable the skill or raise formal_level for legal, medical, financial, incident-response, audit, or other wording-sensitive conversations. <br>
Risk: Local session metadata is retained in memory/reply_state.json to track greeting and topic state. <br>
Mitigation: Periodically clear memory/reply_state.json when local topic or session metadata should not be retained. <br>
Risk: The formatter is optimized for Chinese and uses heuristic topic and greeting detection. <br>
Mitigation: Use it primarily for Chinese-language replies and tune or disable casual formatting when outputs become too informal or inaccurate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/HisongMo/human-like-reply) <br>
- [HisongMo Publisher Profile](https://clawhub.ai/user/HisongMo) <br>
- [Human-like Reply Skill - Technical Reference](references/technical_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Rewritten natural-language replies with configurable YAML settings and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optimized for Chinese-language conversations; stores per-session formatting state locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
