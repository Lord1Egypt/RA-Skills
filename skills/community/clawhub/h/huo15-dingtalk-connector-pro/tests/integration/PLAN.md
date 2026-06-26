# integration（端到端链路）测试方案

## 1. 目标

该套件用于验证插件在**真实钉钉环境**下的端到端链路（鉴权、发送消息、AI Card 创建/更新/结束、媒体上传等）。它与单元测试不同：依赖真实凭证与外部网络，因此默认会被跳过。

## 2. 运行前置条件

- **环境变量**
  - `DINGTALK_CLIENT_ID`：钉钉应用 clientId
  - `DINGTALK_CLIENT_SECRET`：钉钉应用 clientSecret
  - `DINGTALK_TEST_USER_ID`：用于接收消息的测试用户（可选，未设置时会用占位值导致相关用例可能失败/无效）

- **运行命令**

```bash
npm run test:integration
```

当未配置 `DINGTALK_CLIENT_ID` 或 `DINGTALK_CLIENT_SECRET` 时，测试会被 `describe.skipIf(...)` 跳过，仅保留一个“说明性测试”用于提示需要哪些环境变量（实现位于 `integration.test.ts` 顶部，通过 `plugin.__testables` 调用真实函数）。

## 3. 覆盖用例（按当前测试文件）

### 3.1 Authentication

| 序号 | 场景 | 期望 |
|------|------|------|
| 1 | 使用真实凭证获取 access token | 返回非空 token |
| 2 | 使用错误凭证 | promise reject |

### 3.2 Message Sending

| 序号 | 场景 | 期望 |
|------|------|------|
| 3 | 发送 text 给用户 | `ok=true` 且 `processQueryKey` 存在 |
| 4 | 发送 markdown 给用户 | `ok=true` |
| 5 | 发送 AI Card 给用户 | `ok=true` 且 `cardInstanceId` 存在 |

### 3.3 Card Operations

| 序号 | 场景 | 期望 |
|------|------|------|
| 6 | 创建 AI Card | `cardInstanceId` 存在 |
| 7 | stream 更新 AI Card | 返回非空结果 |
| 8 | finish 结束 AI Card | 返回非空结果 |

### 3.4 Media Upload

| 序号 | 场景 | 期望 | 说明 |
|------|------|------|------|
| 9 | 上传一张临时 PNG | 返回非空 mediaId | 用最小 1x1 PNG 作为测试文件 |

### 3.5 Error Handling

| 序号 | 场景 | 期望 |
|------|------|------|
| 10 | 非法 userId | 不抛异常，返回结构化结果 |
| 11 | 快速发送多条消息（模拟限流） | 全部 promise 完成且不抛异常 |

## 4. 风险与注意事项

- **幂等与副作用**：会真实给测试用户发消息/创建卡片，建议使用专门测试账号与群。
- **配额/限流**：钉钉接口可能限流；相关用例仅保证“不抛异常”，不保证每条都成功。
- **网络波动**：外部依赖导致偶发失败，建议在 CI 中单独分组且允许重试（如需要）。

