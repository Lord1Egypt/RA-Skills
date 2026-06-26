# 调用示例

## PowerShell 示例

### 1) 获取 agent 列表

```powershell
Invoke-RestMethod "http://localhost:8080/api/v1/agents"
```

### 2) 获取状态

```powershell
Invoke-RestMethod "http://localhost:8080/api/v1/agents/andy/state"
```

### 3) 获取动作 schema

```powershell
Invoke-RestMethod "http://localhost:8080/api/v1/agents/andy/actions/schema"
```

### 4) 执行命令（!stats）

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8080/api/v1/agents/andy/actions/execute" `
  -ContentType "application/json" `
  -Body '{"command":"!stats","args":[]}'
```

### 5) 执行命令（!goToCoordinates）

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8080/api/v1/agents/andy/actions/execute" `
  -ContentType "application/json" `
  -Body '{"command":"!goToCoordinates","args":[100,64,100,1.5]}'
```

### 6) 紧急停止（!stop）

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8080/api/v1/agents/andy/actions/execute" `
  -ContentType "application/json" `
  -Body '{"command":"!stop","args":[]}'
```

---

## Python 示例（OpenClaw 调用层可直接复用）

```python
import requests

BASE = "http://localhost:8080"
AGENT = "andy"

def api_get(path: str):
    r = requests.get(BASE + path, timeout=30)
    r.raise_for_status()
    return r.json()

def api_post(path: str, payload: dict):
    r = requests.post(BASE + path, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()

def run_action(command: str, args: list):
    return api_post(
        f"/api/v1/agents/{AGENT}/actions/execute",
        {"command": command, "args": args}
    )

def get_state():
    return api_get(f"/api/v1/agents/{AGENT}/state")

if __name__ == "__main__":
    print(api_get("/api/v1/agents"))
    print(api_get(f"/api/v1/agents/{AGENT}/actions/schema")["success"])
    print(run_action("!stats", []))
    print(get_state()["state"]["gameplay"]["position"])
```

---

## 任务编排示例（采集 4 个橡木原木）

1. `!collectBlocks("oak_log", 4)`
2. 轮询 `/state` 查看 `inventory.counts.oak_log`
3. `< 4` 则继续尝试
4. `>= 4` 即成功

建议在每轮执行前后调用 `!stats` 记录上下文，便于故障追踪。
