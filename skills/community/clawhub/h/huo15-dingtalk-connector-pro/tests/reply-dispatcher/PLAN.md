# reply-dispatcher 模块测试方案

## 1. 目的与覆盖范围

`tests/reply-dispatcher` 覆盖回复分发器的核心功能，负责处理 AI 回复的生命周期管理，包括流式输出、状态回调、以及异步模式下的响应累积。

主要覆盖（以测试文件实际引用为准）：

- 指令归一：**normalizeSlashCommand**
- 分发器创建：**createDingtalkReplyDispatcher**
- 流式生命周期回调：**onReplyStart / deliver / onError / onIdle / onCleanup**
- 异步模式响应累积：**asyncMode / getAsyncModeResponse**

## 2. 用例表（覆盖现有测试）

### 2.1 normalizeSlashCommand

| 序号 | 输入 | 期望 |
|------|------|------|
| 1 | `/reset` | 归一化为 `/new` |
| 2 | `新会话` | 归一化为 `/new` |
| 3 | `hello` | 原样返回 |

### 2.2 创建分发器与流式生命周期

| 序号 | 场景 | 期望 |
|------|------|------|
| 4 | onReplyStart 触发 | 调用 createAICardForTarget 创建卡片 |
| 5 | deliver block 分片 | 调用 streamAICard 流式更新 |
| 6 | deliver final 完成 | 调用 finishAICard 结束卡片 |
| 7 | onError 处理 | 正常执行错误回调 |
| 8 | onIdle / onCleanup | 正常执行空闲和清理回调 |
| 9 | onPartialReply | 触发部分回复处理 |

### 2.3 异步模式

| 序号 | 场景 | 期望 |
|------|------|------|
| 10 | asyncMode=true | 不执行流式输出 |
| 11 | onPartialReply 累积 | 响应文本被累积 |
| 12 | getAsyncModeResponse | 返回累积的完整响应 |

## 3. 预期正确输出与潜在错误

- **正确**：指令归一逻辑清晰；流式生命周期按顺序执行（创建→流式更新→结束）；异步模式下正确累积响应而不流式输出；所有回调函数正常触发。
- **潜在错误原因**：流式生命周期顺序错误（如未先创建卡片就流式更新）；异步模式下仍执行流式输出导致行为混乱；回调函数未正确触发或抛出异常导致流程中断。
