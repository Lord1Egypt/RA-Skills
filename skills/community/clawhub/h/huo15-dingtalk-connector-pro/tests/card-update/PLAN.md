# card-update（AI Card 更新）测试方案

## 1. 目的与覆盖范围

该套件定位为 **AI Card“更新链路”的轻量回归集**，目标是用较少用例覆盖最容易被改坏、但线上影响大的关键契约：

- **被动场景创建卡片**：`createAICard(config, data, log?)` 会根据 `conversationType` 正确选择 user/group 目标并完成投放。
- **流式状态机**：`streamAICard(card, content, finished?, log?)` 首次会先切换到 INPUTING，再写入 streaming；后续调用不应重复 INPUTING。
- **结束流程**：`finishAICard(card, content, log?)` 会 finalize streaming 并设置 FINISHED。

说明：

- 本套件**不再**覆盖 `sendAICardInternal/sendAICardToUser/sendAICardToGroup` 或 `buildMsgPayload`，这些更适合放在 `tests/ai-card` 与 `tests/proactive`（避免重复与耦合）。

## 2. 用例表（覆盖现有测试）

| 序号 | 场景 | 期望 | 说明 |
|------|------|------|------|
| 1 | createAICard：单聊（conversationType='1'） | 成功创建并投放到 `dtv1.card//IM_ROBOT.<userId>` | user 目标选择正确 |
| 2 | createAICard：群聊（conversationType='2'） | 成功创建并投放到 `dtv1.card//IM_GROUP.<openConversationId>` | group 目标选择正确 |
| 3 | streamAICard：首次调用 | 先 PUT INPUTING，再 PUT streaming；并把 `card.inputingStarted=true` | 状态机契约 |
| 4 | streamAICard：后续调用 | 仅 PUT streaming（不再重复 INPUTING） | 避免多余状态切换 |
| 5 | finishAICard | streaming `isFinalize=true`，并 PUT FINISHED（flowStatus='3'） | 完成闭环 |

## 3. 预期正确输出与潜在错误

- **正确**：create 时目标选择与投放 `openSpaceId` 正确；stream/finish 的状态机顺序正确且不会重复 INPUTING；finish 会 finalize streaming 并设置 FINISHED。
- **潜在错误原因**：conversationType 判断反了导致 user/group 投放错；streamAICard 忘记先 INPUTING 或重复 INPUTING；finishAICard 未 finalize streaming；flowStatus 值写错导致客户端状态异常。

