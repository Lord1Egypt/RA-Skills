# Quickstart / 快速开始

Advisor. Read-only guidance for new ideas, drifting projects and repository
health reviews.

## Install / 安装

```bash
openclaw skills install project-lifecycle-navigator
```

## When to use / 什么时候用

- 有个新想法，不知道该不该做
- 项目做偏了，需要纠偏
- 想给现有代码做一次只读体检

## Try it in 30 seconds / 30 秒验证

Say to your agent / 对 agent 说：

```text
我有个想法，帮我看看该不该做、最小第一版是什么
```

You should get / 你应该得到:

- startup gates — if the four questions cannot be answered, it says do not
  start yet;
- a go / no-go score;
- concrete next steps and a handoff.

## Safety / 安全

- Read-only. It never modifies product code or governance state.
- Distinguishes a green build from real runtime behaviour — a passing build is
  not accepted as proof that the flow works.
- Stores no API keys, tokens or credentials.
