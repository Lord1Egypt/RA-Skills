# Agent Harness — Architecture Overview
> Based on Anthropic's "Effective Harnesses for Long-Running Agents"

```mermaid
graph TB
    subgraph SHARED["📦 Shared State (Persists Across Sessions)"]
        FL["📄 feature_list.json<br/>• Feature ID & Description<br/>• Test Steps<br/>• passes: true/false"]
        CP["📝 claude-progress.txt<br/>• Session log<br/>• What was done / broken / next"]
        GIT["🔀 Git History<br/>• Descriptive commits<br/>• Revert capability"]
        INIT["⚙️ init.sh<br/>• Start/Stop dev server<br/>• Environment setup"]
    end

    USER["👤 User"] -->|1. harness init &lt;desc&gt;| INIT_AGENT
    INIT_AGENT["🟢 Initializer Agent<br/><i>runs once</i>"]
    CODER1["🟡 Coding Agent #1"]
    CODER2["🟡 Coding Agent #2"]
    CODERN["🟡 Coding Agent #N"]

    INIT_AGENT -->|Creates| FL
    INIT_AGENT -->|Creates| CP
    INIT_AGENT -->|Creates| INIT
    INIT_AGENT -->|Initial commit| GIT

    INIT_AGENT -->|Handoff via shared state| CODER1

    CODER1 -->|Reads & updates| FL
    CODER1 -->|Reads & appends| CP
    CODER1 -->|Commits| GIT
    CODER1 -->|Starts server| INIT

    CODER1 -->|Handoff via shared state| CODER2

    CODER2 -->|Reads & updates| FL
    CODER2 -->|Reads & appends| CP
    CODER2 -->|Commits| GIT

    CODER2 -->|... repeat until done| CODERN
    CODERN -->|All features pass ✓| DONE["🎉 Complete"]

    style INIT_AGENT fill:#a5d6a7
    style CODER1 fill:#fff9c4
    style CODER2 fill:#fff9c4
    style CODERN fill:#fff9c4
    style USER fill:#bbdefb
    style SHARED fill:#f5f5f5
    style DONE fill:#c8e6c9
```

## Failure Modes & Solutions

| Problem | Initializer Agent | Coding Agent |
|---------|------------------|--------------|
| Declares victory too early | Set up comprehensive feature_list.json | Read feature list, pick ONE feature per session |
| Leaves broken state | Create progress file + git repo | Read progress + git log, smoke test first, fix before build |
| Marks features done without testing | Define concrete test steps | Self-verify end-to-end before marking passes=true |
| Doesn't know how to run app | Write init.sh | Read init.sh at session start |
