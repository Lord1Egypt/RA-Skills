# OpenClaw 调用参考

## 1. 前置条件

- 启动命令：`node main.js`
- `settings.js` 推荐：
  - `external_controller_only: true`
  - `mindserver_port: 8080`
- Minecraft 世界可连通（本地 LAN 示例：`127.0.0.1:55916`）

## 2. 接口定义

### GET `/api/v1/agents`

用途：列出可控 bot 与连接状态。  
成功响应示例：

```json
{
  "success": true,
  "agents": [
    {
      "name": "andy",
      "in_game": true,
      "socket_connected": true,
      "viewer_port": 3000
    }
  ]
}
```

---

### GET `/api/v1/agents/:agentName/state`

用途：读取结构化状态（位置、血量、饥饿、背包、邻近实体等）。

响应结构核心字段（示例）：

```json
{
  "success": true,
  "state": {
    "name": "andy",
    "gameplay": {
      "position": { "x": 1.2, "y": 64, "z": -3.4 },
      "health": 20,
      "hunger": 20
    },
    "action": { "current": "Idle", "isIdle": true },
    "inventory": { "counts": { "oak_log": 4 } }
  }
}
```

---

### GET `/api/v1/agents/:agentName/actions/schema`

用途：查询全部命令及参数规格。建议调用方缓存。

响应示例：

```json
{
  "success": true,
  "commands": [
    {
      "name": "!goToCoordinates",
      "category": "action",
      "description": "Go to the given x, y, z location.",
      "blocked": false,
      "params": [
        { "name": "x", "type": "float", "domain": [-Infinity, Infinity] },
        { "name": "y", "type": "float", "domain": [-64, 320] },
        { "name": "z", "type": "float", "domain": [-Infinity, Infinity] },
        { "name": "closeness", "type": "float", "domain": [0, Infinity] }
      ]
    }
  ]
}
```

---

### POST `/api/v1/agents/:agentName/actions/execute`

用途：执行单个动作或查询命令。

请求体：

```json
{
  "command": "!stats",
  "args": []
}
```

成功响应：

```json
{
  "success": true,
  "command": "!stats",
  "args": [],
  "result": "..."
}
```

失败响应（示例）：

```json
{
  "success": false,
  "error": "Agent 'andy' is not connected in game."
}
```

## 3. 编排建议（OpenClaw）

- 先获取 `schema` 再执行，避免参数错误。
- 任何动作后都读取 `state` 校验结果。
- 若动作冲突或卡住：先执行 `!stop`，再恢复流程。
- 对采集/移动任务使用循环策略：
  - `execute` -> `state` -> 判断目标是否达成 -> 未达成则继续。

## 4. 安全与约束

- 外控模式默认无 LLM，但动作仍会与真实游戏世界交互。
- 建议在私有/本地世界验证自动化流程后再扩大范围。
- 若需要并发控制多个 bot，用 `/agents` 按 `name` 分开调度。
