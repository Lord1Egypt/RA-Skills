# Subagent Toolset - Constrained Subagent Tool Sets

## Purpose

When spawning a sub-agent, select the appropriate tool subset based on task type and add it to the task prompt to constrain its behavior.

## Tool Subsets

### Explore
For information gathering, code reading, file analysis.
- read_file: Read file contents
- glob_search: Path pattern search
- grep_search: Content search
- WebFetch: Fetch web page content
- WebSearch: Web search
- Skill: Invoke other skills
- StructuredOutput: Structured output

**Forbidden:** exec, sessions_spawn, edit, write

### Plan
For task breakdown, planning, scheme design.
- read_file: Read files
- glob_search: Path search
- grep_search: Content search
- WebFetch: Fetch reference material
- TodoWrite: Write task list
- SendUserMessage: Send messages
- StructuredOutput: Structured output

**Forbidden:** exec, sessions_spawn, edit, write

### Verification
For testing, verification, result confirmation.
- bash: Execute commands (read-only verification commands only)
- read_file: Read files
- glob_search: Path search
- grep_search: Content search
- WebFetch: Fetch reference material
- TodoWrite: Record results
- StructuredOutput: Structured output
- PowerShell: Windows commands

**Forbidden:** sessions_spawn, edit (dangerous write operations)

### Coding
For code writing, debugging, fixing.
- read_file: Read files
- write_file: Write files
- edit_file: Edit files
- glob_search: Path search
- grep_search: Content search
- bash: Execute commands for verification
- TodoWrite: Task tracking
- StructuredOutput: Structured output
- WebFetch: Fetch reference material

**Full tool access (high privilege)**

### Secretary
For document organization, summarization, report generation.
- read_file: Read files
- glob_search: Path search
- TodoWrite: Write task list
- SendUserMessage: Send messages
- StructuredOutput: Structured output

**Forbidden:** exec, sessions_spawn, edit, write, glob_search, grep_search

## Usage

When spawning a sub-agent, read the corresponding tool subset from this skill and prepend it to the task prompt:

```
You are an Explore-type sub-agent.
You may only use the following tools: read_file, glob_search, grep_search, WebFetch, WebSearch, Skill
Forbidden: exec, sessions_spawn, edit, write

[Your task follows...]
```

## Notes

- Tool subsets are soft constraints (LLM compliance), not hard restrictions
- For dangerous operations (file deletion, config modification), explicit prohibition is required
- High-privilege tasks (Coding type) should be used with caution
