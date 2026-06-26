---
name: AgentTool
description: "Spawn and manage sub-agents for delegated tasks. Use when you need to offload work to specialized agents, run parallel tasks, or coordinate multi-agent workflows."
metadata: { "openclaw": { "emoji": "🤖", "requires": { "bins": [] } } }
---

# AgentTool

Spawn and manage sub-agents for delegated tasks.

## When to Use

✅ **USE this skill when:**
- Delegating specialized tasks to sub-agents
- Running parallel independent tasks
- Coordinating multi-agent workflows
- Offloading long-running operations
- Creating specialized worker agents

❌ **DON'T use this skill when:**
- Simple tasks you can do yourself → use built-in tools
- Tasks requiring shared context → keep in main agent
- Quick one-liner operations → use `BashTool`

## Usage

Sub-agents are spawned through the OpenClaw runtime:

```bash
# Via OpenClaw CLI (if available)
openclaw agent spawn --task "Analyze this codebase" --workspace ./my-project

# Via API (runtime internal)
# The runtime handles sub-agent creation and result collection
```

## Agent Types

| Type | Purpose | Example |
|------|---------|---------|
| Coding Agent | Code analysis, implementation | `coding-agent` skill |
| Research Agent | Information gathering | Web research, documentation |
| Review Agent | Code review, PR analysis | PR review workflows |
| Task Agent | Specific task execution | Data processing, migrations |

## Sub-Agent Lifecycle

```
1. Spawn → Create sub-agent with task and context
2. Execute → Sub-agent works independently
3. Report → Results auto-announce to parent
4. Terminate → Sub-agent completes and exits
```

## Communication Patterns

### Push-Based Results

Sub-agents push results back to parent automatically:
- No polling required
- Results arrive as tool outputs
- Parent continues other work while waiting

### Context Sharing

```yaml
Shared Context:
  - Task description
  - Workspace path
  - Environment variables
  - Tool permissions
```

## Examples

### Example 1: Delegate Code Review

Spawn a sub-agent to review a pull request:
- Task: "Review PR #123 for security issues"
- Workspace: Temporary clone of repo
- Result: Review report with findings

### Example 2: Parallel Research

Spawn multiple sub-agents for parallel research:
- Agent 1: "Research React best practices"
- Agent 2: "Research Vue best practices"
- Agent 3: "Research Svelte best practices"
- Combine results for comparison

### Example 3: Specialized Analysis

Spawn specialized agents:
- Security agent: "Audit for vulnerabilities"
- Performance agent: "Analyze performance bottlenecks"
- Documentation agent: "Generate API docs"

## Integration with coding-agent Skill

The `coding-agent` skill uses AgentTool internally:
- Spawns Codex, Claude Code, or Pi agents
- Manages background processes
- Collects and returns results

```bash
# Using coding-agent skill (which uses AgentTool)
# See coding-agent/SKILL.md for details
```

## Best Practices

1. **Clear task definition**: Provide specific, actionable tasks
2. **Appropriate scope**: Don't make tasks too broad or narrow
3. **Context sharing**: Include necessary context and constraints
4. **Result handling**: Plan how to integrate sub-agent results

## Limitations

- **Depth limit**: Sub-agent depth is typically limited (e.g., 1-2 levels)
- **Resource usage**: Each agent consumes resources
- **Context size**: Sub-agents have their own context limits
- **Coordination overhead**: Complex workflows need careful planning

## Security Notes

⚠️ **Sub-agent considerations:**
- Sub-agents inherit your permissions
- Ensure tasks don't conflict
- Monitor resource usage
- Review sub-agent outputs before acting
