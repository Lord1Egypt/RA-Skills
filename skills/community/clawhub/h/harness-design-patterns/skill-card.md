## Description: <br>
A documentation-only knowledge base for agent harness architecture patterns, including handoffs, compaction memory extraction, denial tracking, memory consolidation, hook brackets, delegation modes, adaptive complexity, and hook runtime profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent-system designers use this skill to choose harness patterns for multi-stage context transfer, multi-agent coordination, hook architecture, and task-complexity controls. It provides design guidance and directs users to separate implementation skills when executable hooks or operational monitoring are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary flags under-scoped guidance around bypassing permission checks in agent workflows. <br>
Mitigation: Avoid permission-bypass mode except in isolated test environments, and require normal review for any workflow that can modify files, run commands, or affect production systems. <br>
Risk: The release security summary notes hook patterns that read session data. <br>
Mitigation: Review hook scripts and settings before enabling them, restrict transcript and shared-memory directory access, and apply cleanup and file-permission controls to generated session state. <br>
Risk: Examples describe hook and state-management behavior that can be copied into executable workflows. <br>
Mitigation: Treat examples as design guidance until independently reviewed, tested, and scoped to the target environment. <br>


## Reference(s): <br>
- [Pattern 2: Handoff Documents](references/02-handoff.md) <br>
- [Pattern 6: Atomic File Writes](references/06-atomic-write.md) <br>
- [Pattern 8: Compaction Memory Extraction](references/08-compaction-extract.md) <br>
- [Pattern 9: Denial Circuit Breaker](references/09-denial-tracking.md) <br>
- [Pattern 10: Memory Consolidation](references/10-memory-consolidation.md) <br>
- [Pattern 11: Hook Pair Bracket](references/11-hook-bracket.md) <br>
- [Pattern 12: Component-Scoped Hooks](references/12-scoped-hooks.md) <br>
- [Pattern 14: Delegation Modes](references/14-delegation-modes.md) <br>
- [Pattern 16: Adaptive Complexity Scoring](references/16-adaptive-complexity.md) <br>
- [Pattern 18: Hook Runtime Profiles](references/18-hook-profiles.md) <br>
- [Distillation Methodology](references/distillation-methodology.md) <br>
- [Prompt Hardening Integration](references/prompt-hardening-integration.md) <br>
- [Quality Pipeline Integration](references/quality-pipeline-integration.md) <br>
- [Anthropic: Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) <br>
- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) <br>
- [Oh My ClaudeCode](https://github.com/Yeachan-Heo/oh-my-claudecode) <br>
- [Agentic Harness Patterns Skill](https://github.com/keli-wen/agentic-harness-patterns-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with tables and occasional JSON or shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable code is installed by the skill itself.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and metadata.json; SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
