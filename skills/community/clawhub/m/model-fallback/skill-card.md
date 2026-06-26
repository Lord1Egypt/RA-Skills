## Description: <br>
Monitors model availability and falls back to backup MiniMax, Kimi, Zhipu, or other OpenAI-compatible models when the primary model fails, slows down, or hits rate limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[azure5100](https://clawhub.ai/user/azure5100) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external OpenClaw users use this skill to configure automatic model failover, health checks, logging, and task routing across approved providers when primary models are unavailable, slow, rate-limited, or too expensive for simple tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fallback may send prompts to alternate model providers. <br>
Mitigation: Configure only approved providers for the intended data classification, and disable or narrow fallback for confidential or regulated prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/azure5100/model-fallback) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference provider routing decisions, health checks, and fallback logs; provider configuration controls where prompts are sent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md Version section) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
