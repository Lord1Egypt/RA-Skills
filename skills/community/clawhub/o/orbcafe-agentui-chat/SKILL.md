---
name: orbcafe-agentui-chat
description: Build ORBCAFE chat and copilot experiences with AgentPanel, StdChat, CopilotChat, ChatMessage typing flow, and AgentUICardHooks using official examples patterns. Use for full-page chat, floating copilot, streaming replies, markdown/cards rendering, and when chat UI appears but send, stream, card actions, drag, or resize behavior has no effect.
---

# ORBCAFE AgentUI Chat

## Workflow

1. 先对照 `skills/orbcafe-ui-component-usage/references/module-contracts.md`，确认这是 `Component-first` 模块。
2. 用 `references/component-selection.md` 选择 `AgentPanel` / `StdChat` / `CopilotChat`。
3. 执行安装与最小接入。
4. 用 `references/recipes.md` 输出最小可运行代码。
5. 用 `references/guardrails.md` 检查消息状态、streaming、card hooks 和 copilot 外壳边界。
6. 输出验收步骤与“没效果”排障。

## Installation and Bootstrapping (Mandatory)

```bash
npm install orbcafe-ui @mui/material @mui/icons-material @mui/x-date-pickers @emotion/react @emotion/styled dayjs
```

本仓库联调：

```bash
npm run build
cd examples
npm install
npm run dev
```

参考实现：
- `examples/app/chat/ChatExampleClient.tsx`
- `examples/app/copilot/CopilotExampleClient.tsx`
- `src/components/AgentUI/README.md`

## Output Contract

0. `Mode`: `Component-first`.
1. `Chat decision`: 选择 `AgentPanel` / `StdChat` / `CopilotChat` 并说明依据。
2. `Minimal code`: 一个可直接粘贴的最小片段，只允许从 `orbcafe-ui` 导入公共 API。
3. `State shape`: `messages`、`isResponding` 以及 copilot 外壳状态的最小结构。
4. `Verify`: 至少 3 条可执行验收步骤，覆盖发送、streaming、card action；如果是 copilot，还要覆盖打开/关闭和拖拽/缩放。
5. `Troubleshooting`: 至少 3 条“UI 看得到但没有效果”的排查项。

## Examples-Based Experience Summary

- `StdChat` 是标准聊天布局层，负责消息区和输入区，不负责标题、浮窗、拖拽和缩放。
- `AgentPanel` 是 `StdChat` 的带头部封装，适合工作台或整页聊天。
- `CopilotChat` 只负责 copilot 面板内容层；浮动按钮、定位、吸附、拖拽和 resize 必须在页面壳层实现。
- assistant typing flow 的稳定基线是：append assistant message with `isStreaming: true`，然后在 `onMessageStreamingComplete` 中改回 `false`。
- 卡片交互统一走 `AgentUICardHooks.onCardEvent`，不要直接耦合内部 renderer。
