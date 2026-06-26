# AI Card 模块测试方案

## 1. 模块划分与职责

本套件覆盖 AI Card 相关能力（创建/流式更新/结束/投放与回退），主要围绕以下通过 `plugin.__testables` 暴露的函数：

- **buildDeliverBody(cardInstanceId, target, robotCode)**：构建投放请求体（核心契约：`openSpaceId` 与 deliver model）。
- **createAICardForTarget(config, target, log?)**：通用创建+投放，返回 `{ cardInstanceId, accessToken, inputingStarted }` 或 null。
- **createAICard(config, data, log?)**：被动回复场景创建卡片（从 DingTalk 回调 `data` 推导 target 后委托给 createAICardForTarget）。
- **streamAICard(card, content, finished?, log?)**：流式更新（首次会切换 INPUTING；失败会 throw）。
- **finishAICard(card, content, log?)**：结束卡片（finalize streaming + 设置 FINISHED；FINISHED 写入失败会记录日志但不抛异常）。
- **sendAICardInternal / sendAICardToUser / sendAICardToGroup**：主动发送 AI Card（失败可按策略回退到普通消息）。

## 2. 用例表（覆盖现有测试）

### 2.1 buildDeliverBody

| 序号 | 场景 | mock/输入 | 期望 | 说明 |
|------|------|-----------|------|------|
| 1 | user target | target={type:'user', userId:'u1'} | openSpaceId 为 `dtv1.card//IM_ROBOT.u1` | deliver model 正确 |
| 2 | group target | target={type:'group', openConversationId:'c1'} | openSpaceId 为 `dtv1.card//IM_GROUP.c1` | deliver model 正确 |

### 2.2 createAICardForTarget

| 序号 | 场景 | mock/输入 | 期望 | 说明 |
|------|------|-----------|------|------|
| 3 | user 创建投放成功 | POST instances + deliver 成功 | 返回 cardInstanceId/accessToken | 并投放到 IM_ROBOT |
| 4 | group 创建投放成功 | 同上 | 返回非空 | 并投放到 IM_GROUP |
| 5 | create 失败 | axios.post reject | 返回 null | 错误收敛 |
| 6 | deliver 失败 | deliver reject | 返回 null | 错误收敛 |

### 2.3 streamAICard / finishAICard

| 序号 | 场景 | 输入 | 期望 | 说明 |
|------|------|------|------|------|
| 7 | 首次 stream | inputingStarted=false | 先 INPUTING 再 streaming | INPUTING 失败会 throw |
| 8 | 后续 stream | inputingStarted=true | 仅 streaming | 不重复 INPUTING |
| 9 | finish | - | finalize streaming + FINISHED | FINISHED 失败记录 error 不 throw |

### 2.4 sendAICardInternal / sendAICardToUser / sendAICardToGroup

| 序号 | 场景 | mock/输入 | 期望 | 说明 |
|------|------|-----------|------|------|
| 10 | internal 用户发送成功 | gettoken + create + put 成功 | `ok=true` | 主流程 |
| 11 | internal 群发送成功 | 同上 | `ok=true` | 主流程 |
| 12 | internal 创建失败 | create 抛错 | `ok=false` + `error` | 错误返回 |
| 13 | toUser 带回退 | 卡片失败、普通消息成功（若实现有回退） | `ok=true` | 体现“回退不影响 ok” |
| 14 | toGroup 带回退 | 同上 | `ok=true` |  |

## 3. 预期正确输出与潜在错误

- **正确**：deliver body 的 `openSpaceId/robotCode` 契约稳定；createAICardForTarget 返回结构稳定；stream/finish 状态机顺序正确；外部错误被收敛为 null/throw（按函数契约）。
- **潜在错误原因**：openSpaceId 拼错（IM_ROBOT/IM_GROUP）；deliver model 字段缺失；stream 首次未切 INPUTING；把应 throw 的路径吞掉导致上层误判成功。

