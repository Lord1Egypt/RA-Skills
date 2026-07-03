针对 **OpenClaw (2026版)** 的 Provider 设计配置，实现 **ACP (Agent Client Protocol)** 桥的最佳方案是构建一个“透明代理适配器”。

这个方案的核心在于：利用 OpenClaw 能够自定义 `Base URL` 的特性，将原本发往云端的请求拦截到本地的 Python 桥接脚本中，由脚本通过 **标准输入输出 (stdio)** 与 `kiro-cli acp` 保持长连接会话。

### 1. 架构设计图


### 2. 核心桥接脚本实现 (`acp_bridge.py`)
这个脚本使用了 `FastAPI` 作为 Web 接口，并使用 `subprocess.Popen` 维护 `kiro-cli` 的持久进程，从而实现**直到主动中断**的会话保持。

```python
import subprocess
import json
import uuid
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

# 维护全局 ACP 进程
class ACPManager:
    def __init__(self):
        self.process = subprocess.Popen(
            ["kiro-cli", "acp"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        # 初始握手
        self.send({"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1})
        # 开启长会话模式
        self.send({"jsonrpc": "2.0", "method": "session/new", "params": {"mode": "continuous"}, "id": 2})

    def send(self, data):
        self.process.stdin.write(json.dumps(data) + "\n")
        self.process.stdin.flush()
        return self.process.stdout.readline()

acp = ACPManager()

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    user_message = body['messages'][-1]['content']
    
    # 构造 ACP 指令发给本地 Kiro
    acp_request = {
        "jsonrpc": "2.0",
        "method": "session/prompt",
        "params": {"text": user_message},
        "id": str(uuid.uuid4())
    }
    
    # 获取 Kiro 的实时回显
    raw_response = acp.send(acp_request)
    kiro_data = json.loads(raw_response)
    
    # 转换回 OpenAI 格式回传给 OpenClaw
    return {
        "id": "acp-" + str(uuid.uuid4()),
        "object": "chat.completion",
        "choices": [{
            "message": {"role": "assistant", "content": kiro_data['result']['text']},
            "finish_reason": "stop"
        }]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=18788)
```

### 3. OpenClaw Provider 配置步骤

在 OpenClaw 的配置文件中（通常位于 `~/.openclaw/openclaw.json`），添加如下配置：

| 配置项 | 填写内容 | 说明 |
| :--- | :--- | :--- |
| **Provider Type** | `Custom / OpenAI Compatible` | 选择兼容 OpenAI 的自定义模式 |
| **Base URL** | `http://127.0.0.1:18788/v1` | 指向你刚才跑起来的桥接脚本 |
| **API Key** | `KIRO_LOCAL_BYPASS` | **随便填**。你的桥不校验这个 Key，只是为了通过 OpenClaw 的前端检查 |
| **Model Name** | `kiro-acp-engine` | 随便填，用于在 UI 上显示 |

### 4. 方案亮点：为什么这是“最优”？

* **真正的长会话**：通过 `subprocess.Popen`，`kiro-cli` 进程在你的桥脚本运行期间永远不会关闭。Kiro 内部的上下文（Context）会随着对话不断累积，直到你手动关闭桥脚本。
* **零源码修改**：你不需要动 OpenClaw 一行代码，只需要把它当成一个“皮肤”挂在你的 ACP 桥上。
* **极致性能**：ACP 协议基于 stdio 管道通信，省去了反复建立网络连接和初始化模型的开销。
* **权限透传**：因为 `kiro-cli` 以你的系统用户身份运行，它在对话中可以直接访问你的本地文件系统或执行 CLI 命令，真正实现“对话操作电脑系统”。

### 运行建议
1.  先打开终端运行：`python acp_bridge.py`。
2.  确保看到 `Uvicorn running on http://127.0.0.1:18788`。
3.  在 OpenClaw 设置中应用上述配置。
4.  开始对话。只要桥脚本不关，你的所有历史对话都会被 Kiro 记住。