## Description: <br>
Autonomous QA evaluation loop — runs domain-specific tasks against yourself, scores responses with an LLM judge, installs missing skills, and logs knowledge gains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[no7dw](https://clawhub.ai/user/no7dw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw agent users and developers use this skill to run self-evaluation tasks, judge response quality, install suggested skills, and record learning outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently install suggested skills during an evaluation run. <br>
Mitigation: Require manual approval before any `clawhub install` action and review installed skills before using them. <br>
Risk: Evaluation summaries may be shared through BotLearn when that skill is available. <br>
Mitigation: Disable BotLearn posting or require per-run approval before sharing evaluation results. <br>
Risk: Evaluation logs may contain private or sensitive task content. <br>
Mitigation: Use the skill only on non-sensitive tasks and inspect or delete `memory/qa-eval-*` logs after each run. <br>
Risk: The LLM judge requires an OpenRouter API key and can incur usage costs. <br>
Mitigation: Use a restricted OpenRouter key with an explicit budget and do not log the full key. <br>


## Reference(s): <br>
- [ClawHub skill homepage](https://clawhub.ai/skills/openclaw-auto-training-skill) <br>
- [ClawHub release page](https://clawhub.ai/no7dw/openclaw-auto-training-skill) <br>
- [OpenRouter API endpoint](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown logs, command recommendations, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call an LLM judge, install suggested skills, append evaluation logs, and optionally post a summary when BotLearn is available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
