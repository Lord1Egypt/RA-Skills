# AgentUI Guardrails

## Public API only

- 只从 `orbcafe-ui` 导入：
  - `AgentPanel`
  - `StdChat`
  - `CopilotChat`
  - `type ChatMessage`
  - `type AgentUICardHooks`
- 不要指导业务代码直接从 `src/components/AgentUI/...` 引内部实现。

## Message state contract

- `messages` 是单一消息源。
- `ChatMessage.timestamp` 按当前实现应传 `Date`。
- 用户发送时先 append user message，再处理 assistant。
- assistant 流式输出时设置 `isStreaming: true`。
- 在 `onMessageStreamingComplete(messageId)` 里把对应消息改回 `isStreaming: false`。

## Card hooks contract

- 卡片动作统一使用 `cardHooks.onCardEvent`。
- 事件对象至少关注：
  - `messageId`
  - `cardType`
  - `action`
  - `payload`
- 不要把业务逻辑直接绑到 `MarkdownRenderer` 或 `DynamicCardRenderer`。

## Copilot shell boundary

- `CopilotChat` 不负责：
  - 悬浮按钮
  - 打开/关闭状态
  - 绝对定位
  - 拖拽
  - 吸附角
  - resize
- 这些必须由页面外壳负责。

## Resizable copilot constraint

如果做可拖拽/可缩放 copilot：

- resize 期间关闭 transition。
- resize 期间避免 `ResizeObserver` 回写尺寸状态。
- pointer up 后再恢复 observer 同步。

否则容易出现“位置变了，尺寸又被改回去”的假象。

## Voice input boundary

- `VoiceInputButton` 内部依赖 `AINav` 的 `useVoiceInput`。
- 这不是 AgentUI 对外稳定 hook，不要让业务代码直接依赖这条内部链路。
