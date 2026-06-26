# PRE Engineering Skill (English)

"Three humble cobblers surpass one Zhuge Liang" (三个臭皮匠，顶个诸葛亮) — A Chinese proverb reminding us that multiple ordinary agents, working together, can outperform a single genius. PRE Engineering is the embodiment of this wisdom.

The three agent roles — **P**lan, **R**eview, **E**xecute — form the acronym **PRE**. This also echoes "preparation": this skill provides the essential materials for a project to take flight — role guides, collaboration protocols, and workflow configuration.

## What It Does

When triggered, this skill guides the user through a 2-step interactive process to collect project requirements, then generates 5 core documents for running a PRE collaborative project:

1. **Project Goals Document** (`project-goals.md`) — Requirements and constraints (only humans can modify)
2. **Collaboration Log** (`collaboration-log.md`) — Agent communication medium with initial PLN_WAIT entry
3. **Planner Guide** (`planner-guide.md`) — Planner role behavior specification
4. **Executor Guide** (`executor-guide.md`) — Executor role behavior specification
5. **Reviewer Guide** (`reviewer-guide.md`) — Reviewer role behavior specification

After generation, the skill provides startup instructions for launching three agents in separate terminals using `/loop` commands.

## Trigger Conditions

Use this skill when the user wants to:
- Initialize a multi-agent collaborative project
- Set up PRE system / Plan-Review-Execute workflow
- Create Planner/Executor/Reviewer guide documents
- Start a collaboration log-driven multi-agent workflow
- Expresses multi-agent collaboration intent (even without explicitly mentioning PRE)

## File Structure

```
skills/pre-engineering/
├── SKILL.md                          ← Skill definition (this directory's entry point)
├── README.md                         ← This file
└── references/
    ├── planner-guide-template.md     ← Planner agent guide template
    ├── executor-guide-template.md    ← Executor agent guide template
    ├── reviewer-guide-template.md    ← Reviewer agent guide template
    ├── collaboration-log-format-reference.md  ← Log format examples
    └── state-system-reference.md     ← 7-state system reference
```

## How to Use

1. **Install the skill**: Place the `skills/pre-engineering/` directory into your Claude Code skills directory
2. **Trigger the skill**: Express multi-agent collaboration intent in Claude Code, for example:
   - "I want to initialize a multi-agent collaborative project"
   - "Help me set up a PRE system"
   - "Start PRE Engineering"
   - Or simply mention roles like "Planner", "Executor", "Reviewer"
3. **Interactive requirement collection**: The skill guides you through a 2-step interactive process to collect and confirm project information
4. **Document generation**: After confirmation, 5 `.pre/` collaboration documents are generated in your project directory
5. **Baseline commit**: Run `git add .pre/ && git commit` to create a baseline before starting agents
6. **Launch agents**: Follow the provided instructions to start three agents in separate terminals using `/loop` commands

## Author

张战罗 (zhangzhanluo) — zhangzhanluo@outlook.com

## Related Repository

- **Chinese version repository**: [pre-engineering-cn](https://github.com/zhangzhanluo/pre-engineering-cn) — PRE Engineering Skill in Chinese, with documentation and templates in Chinese

## Key Mechanisms

- **Loop Prevention**: 3 consecutive rejections trigger blockage, reverting to PLN_WAIT
- **Version Recording**: Reviewer manages git stash after planning approval and git commit after execution approval
- **Code Conciseness**: Reviewer enforces strict quality standards against code bloat
- **Timezone**: Confirmed with user during initialization, used consistently in all log entries