# OpenClaw Agent 创建与飞书路由绑定（中文流程）

## 1. 目标

本技能只做两件事：
- 创建 OpenClaw Agent。
- 将 Agent 绑定到飞书路由（重点是 `bindings.match.peer.id`）。

其中 `peer.id` 就是飞书会话 ID：
- 群聊通常是 `oc_xxx`
- 私聊是对应用户会话 ID

## 1.1 运行前提与权限说明
- 必须具备本地命令：
  - `openclaw`
  - `python`（3.x）
- 建议先检查：
```bash
openclaw --version
python --version
```
- 本技能会读取并可能写入本地 `openclaw.json`（如 `agents.list[]`、`bindings[]`）。
- `openclaw.json` 可能包含敏感配置（凭据等），仅在受信任环境执行。

## 2. 必填信息

### A. Agent 信息
- Agent 职责边界：做什么、不做什么
- `agentId`
- `workspace`
- `model`
- `agents.list[]` 中必须使用 `identity` 对象（参考当前配置写法）

示例（推荐）：
```json
{
  "id": "data-analyst",
  "workspace": "C:\\Users\\Administrator\\.openclaw\\workspace-dataAnalysis",
  "agentDir": "C:\\Users\\Administrator\\.openclaw\\agents\\data-analyst\\agent",
  "identity": {
    "name": "data-analyst"
  }
}
```

### B. 飞书路由信息
- `match.channel = feishu`
- `match.accountId`（例如 `main`）
- `match.peer.kind`（常见 `group`）
- `match.peer.id`（飞书会话 ID）

强约束：
- `match.accountId` 只能是飞书账号键（例如 `main`）。
- `oc_xxx` 这类群会话 ID 只能放在 `match.peer.id`，不能放在 `match.accountId`。

## 3. 四步确认机制（必须按顺序）

### 确认 1：确认要创建什么 Agent
确认项：
- 目标职责
- 输出风格
- 禁止范围

输出模板：
```text
Agent 目标确认：
- 角色：
- 主要职责：
- 不做事项：
请确认是否正确（是/否）。
```

### 确认 2：确认 Agent 配置参数
确认项：
- `agentId`
- `workspace`
- `model`
- `name/emoji/theme`（如有）

输出模板：
```text
Agent 配置确认：
- agentId:
- workspace:
- model:
- identity(name/emoji/theme):
请确认是否正确（是/否）。
```

### 确认 3：确认飞书路由参数
确认项：
- `accountId`
- `peer.kind`
- `peer.id`（明确说明这是飞书会话 ID）

输出模板：
```text
飞书路由确认：
- channel: feishu
- accountId:
- peer.kind:
- peer.id:
请确认是否正确（是/否）。
```

### 确认 4：最终执行确认
在真正写入前做一次总确认。

输出模板：
```text
最终执行确认：
将创建 Agent 并写入路由绑定，摘要如下：
- agentId:
- workspace:
- model:
- route: feishu/<accountId>/<peer.kind>/<peer.id>
请确认执行（执行/取消）。
```

## 4. 执行流程（SOP）

1. 读取现状
```bash
openclaw agents list
openclaw config get agents.list --json
openclaw config get channels.feishu.accounts --json
openclaw directory groups list --channel feishu --account <account-id> --query "<群关键词>" --json
openclaw config get bindings --json
```

2. 创建 Agent
```bash
openclaw agents add <agent-id> \
  --non-interactive \
  --workspace <workspace-dir> \
  --model <provider/model-id> \
  --json
```

3. 设置身份（推荐）
```bash
openclaw agents set-identity --agent <agent-id> --name "<display-name>" --emoji "🦞" --json
```
说明：你的规范是 `agents.list[]` 里使用 `identity` 对象，不要只写顶层 `name`。

4. 绑定路由
- 账户级（可选）：
```bash
openclaw agents bind --agent <agent-id> --bind feishu:<account-id> --json
```
- 会话级（重点）：在 `bindings[]` 中写入 `match.peer.id = <飞书会话ID>`

示例：
```json
{
  "agentId": "product-ops",
  "match": {
    "channel": "feishu",
    "accountId": "main",
    "peer": { "kind": "group", "id": "oc_xxx" }
  }
}
```

反例（错误）：
```json
{
  "agentId": "product-ops",
  "match": {
    "channel": "feishu",
    "accountId": "oc_xxx"
  }
}
```

5. 验收
```bash
python -X utf8 .\scripts\validate_feishu_bindings.py --config C:\Users\Administrator\.openclaw\openclaw.json
openclaw config validate --json
openclaw config get agents.list --json
openclaw config get bindings --json
```

验收标准：
- 新 Agent 已存在
- 对应 `peer.id` 的绑定项存在且字段准确
- 无 schema 校验错误
- 自动检查脚本返回 `[OK]`

## 5. 排障与回滚

### 常见问题
- 绑定到了错误群：检查 `peer.id` 是否填错
- `accountId` 写成了 `oc_xxx`：这是字段混淆，必须改为账号键（如 `main`），并把 `oc_xxx` 放入 `peer.id`
- 命中了错误 Agent：检查 `bindings` 顺序（精确规则应优先）
- 配置不生效：先 `config validate` 再按你部署策略重载网关
- 群里仍走 `main`：通常是当前消息的真实 `peer.id` 与配置不一致，或网关尚未加载最新配置
- Agent 已创建但显示/路由异常：检查 `agents.list[]` 是否包含 `identity.name`

### 回滚原则
- 变更前先保存 `bindings` 快照
- 回滚时恢复上一个可用 `bindings`，再次校验

## 6. 操作纪律

- 没有完成 4 次确认，不执行写操作
- 每次写操作后必须做读回校验
- 统一保留 JSON 变更记录，便于审计与交接
