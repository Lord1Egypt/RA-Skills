## Description: <br>
提示词架构师专业版 helps Chinese-language prompt engineering teams design, test, budget, and orchestrate agent prompts, including few-shot generation, token planning, DAG task decomposition, A/B testing, hallucination checks, and context-quality diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, prompt engineers, and AI agent team leads use this skill to create structured prompts, generate and evaluate few-shot examples, plan token budgets, coordinate multi-agent workflows, and test prompt quality before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares read, exec, and write-style agent tools for prompt testing and validation. <br>
Mitigation: Keep command execution, file writes, generated test scripts, and validation runs under explicit user control. <br>
Risk: The skill may involve network checks, external APIs, or credential setup when users extend its prompt-testing workflows. <br>
Mitigation: Require user confirmation for network access, external API use, and credential configuration; avoid storing credentials in skill files. <br>
Risk: Prompt tests, hallucination checks, token estimates, and optimization advice can still produce incomplete or misleading guidance. <br>
Mitigation: Review generated prompts, test cases, and recommendations before using them in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/prompt-architect-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with text examples, JSON schemas, code snippets, and shell-command suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated few-shot examples, DAG task plans, prompt test cases, token budget estimates, diagnostic reports, and review recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
