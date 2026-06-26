## Description: <br>
Lean Context helps agents reduce token usage in AI coding and agent systems by applying context compression, selective loading, prompt deduplication, caching, model tiering, and efficient tool-output patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awalesagar](https://clawhub.ai/user/awalesagar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit prompts, skills, agent configuration files, tool definitions, and multi-agent workflows for context bloat and token cost. It provides practical guidance for keeping agent context small while preserving task quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill mentions flags that can reduce confirmation prompts. <br>
Mitigation: Keep approvals enabled for file changes, commands, credentialed tools, and external actions unless the workflow is sandboxed, low risk, and explicitly pre-approved. <br>
Risk: Token-reduction advice can remove useful context if applied too aggressively. <br>
Mitigation: Review compressed prompts, summaries, and configuration changes against task requirements before deploying them. <br>


## Reference(s): <br>
- [Compression Deep Dive](references/compression-deep-dive.md) <br>
- [Lean Context on ClawHub](https://clawhub.ai/awalesagar/lean-context) <br>
- [Anthropic Token Counting](https://docs.anthropic.com/en/docs/build-with-claude/token-counting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include audit checklists, configuration patterns, compression examples, and cost-estimation formulas.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
