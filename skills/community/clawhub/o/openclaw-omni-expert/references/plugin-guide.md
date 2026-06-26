# OpenClaw 插件开发指南

## 目录
- [插件架构](#插件架构)
- [插件类型](#插件类型)
- [开发流程](#开发流程)
- [权限管理](#权限管理)
- [插件市场](#插件市场)

---

## 插件架构

### 目录结构

```
plugin_name/
├── plugin.json          # 插件元数据
├── plugin.py            # 主入口
├── tools/               # 工具插件
├── channels/            # 渠道插件
├── assets/              # 资源文件
├── __init__.py
├── requirements.txt
└── README.md
```

### plugin.json 结构

```json
{
  "name": "my_plugin",
  "version": "1.0.0",
  "description": "插件描述",
  "author": {
    "name": "作者名",
    "email": "email@example.com"
  },
  "license": "MIT",
  "openclaw_version": ">=1.0.0",
  "type": "tool",
  "permissions": ["network", "filesystem"],
  "dependencies": {
    "requests": "^2.28.0"
  }
}
```

---

## 插件类型

### 1. 工具插件 (Tool Plugin)

扩展 Agent 的工具能力。

```python
from openclaw import BaseTool, ToolParameter, ToolResult

class MyTool(BaseTool):
    name = "my_tool"
    description = "我的自定义工具"
    category = "custom"
    
    parameters = [
        ToolParameter(
            name="input",
            type="string",
            required=True,
            description="输入参数"
        )
    ]
    
    async def execute(self, params):
        input_value = params.get("input")
        
        # 处理逻辑
        result = await self.process(input_value)
        
        return ToolResult(
            success=True,
            data=result,
            message="操作成功"
        )
    
    async def process(self, input_value):
        # 实现具体逻辑
        pass
```

### 2. 渠道插件 (Channel Plugin)

添加新的消息渠道支持。

```python
from openclaw import BaseChannel, Message, ChannelConfig

class MyChannel(BaseChannel):
    name = "my_channel"
    
    def __init__(self, config: ChannelConfig):
        super().__init__(config)
        self.client = None
    
    async def connect(self) -> bool:
        # 建立连接
        pass
    
    async def disconnect(self):
        # 断开连接
        pass
    
    async def send(self, message: Message) -> bool:
        # 发送消息
        pass
    
    async def receive(self) -> Message:
        # 接收消息
        pass
```

### 3. 记忆插件 (Memory Plugin)

自定义记忆存储后端。

```python
from openclaw import BaseMemory, MemoryEntry, SearchResult

class MyMemory(BaseMemory):
    name = "my_memory"
    
    async def connect(self) -> bool:
        pass
    
    async def store(self, entry: MemoryEntry) -> str:
        pass
    
    async def retrieve(self, entry_id: str) -> MemoryEntry:
        pass
    
    async def search(self, query: str, top_k: int) -> List[SearchResult]:
        pass
```

### 4. 中间件插件 (Middleware Plugin)

请求/响应处理中间件。

```python
from openclaw import BaseMiddleware, Request, Response

class MyMiddleware(BaseMiddleware):
    name = "my_middleware"
    
    async def process_request(self, request: Request) -> Request:
        # 处理请求
        return request
    
    async def process_response(self, response: Response) -> Response:
        # 处理响应
        return response
```

---

## 开发流程

### 步骤 1: 创建项目

```bash
mkdir my_plugin
cd my_plugin
touch plugin.json
touch my_tool.py
```

### 步骤 2: 编写元数据

```json
{
  "name": "my_plugin",
  "version": "1.0.0",
  "type": "tool"
}
```

### 步骤 3: 实现功能

```python
# my_tool.py
from openclaw import BaseTool, ToolParameter

class MyTool(BaseTool):
    name = "my_tool"
    
    async def execute(self, params):
        # 实现逻辑
        return {"success": True}
```

### 步骤 4: 测试

```bash
openclaw plugin test ./my_plugin
```

### 步骤 5: 打包发布

```bash
openclaw plugin package ./my_plugin --output my_plugin.zip
```

---

## 权限管理

### 权限类型

| 权限 | 说明 | 风险级别 |
|------|------|---------|
| `network` | 网络访问 | 中 |
| `filesystem` | 文件读写 | 高 |
| `execute` | 命令执行 | 高 |
| `memory` | 记忆访问 | 中 |
| `api` | API 调用 | 中 |

### 权限配置

```json
{
  "plugin": "my_plugin",
  "permissions": [
    {
      "name": "network",
      "level": "read",
      "granted": true
    },
    {
      "name": "filesystem",
      "level": "write",
      "granted": true,
      "constraints": {
        "allowed_paths": ["/tmp/openclaw"]
      }
    }
  ],
  "constraints": {
    "rate_limit": 100,
    "quota": 1000,
    "timeout": 30
  }
}
```

### 安全最佳实践

1. **最小权限原则**
   ```json
   "permissions": ["network"]
   ```

2. **路径限制**
   ```json
   {
     "filesystem": {
       "allowed_paths": ["/tmp/openclaw"],
       "denied_paths": ["/etc", "/root"]
     }
   }
   ```

3. **请求限制**
   ```json
   {
     "constraints": {
       "rate_limit": 10,
       "max_request_size": "1MB"
     }
   }
   ```

---

## 插件市场

### 官方插件

| 插件 | 类型 | 描述 |
|------|------|------|
| `slack` | channel | Slack 集成 |
| `discord` | channel | Discord 集成 |
| `pinecone` | memory | Pinecone 向量库 |
| `github` | tool | GitHub API 工具 |

### 安装插件

```bash
# 从市场安装
openclaw plugin install slack

# 从文件安装
openclaw plugin install ./my_plugin.zip
```

### 搜索插件

```bash
openclaw plugin search "vector"
```

### 更新插件

```bash
openclaw plugin update slack
```

---

## 完整示例

### weather_tool.py

```python
"""
天气查询工具插件
"""

from typing import Dict, Any
from openclaw import BaseTool, ToolParameter, ToolResult
import httpx

class WeatherTool(BaseTool):
    """查询天气信息"""
    
    name = "weather"
    description = "查询指定城市的天气信息"
    category = "data"
    
    parameters = [
        ToolParameter(
            name="city",
            type="string",
            required=True,
            description="城市名称"
        )
    ]
    
    async def execute(self, params: Dict[str, Any]) -> ToolResult:
        city = params.get("city")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.weather.example.com/current",
                    params={"city": city, "key": self.config.get("api_key")}
                )
                data = response.json()
                
                return ToolResult(
                    success=True,
                    data={
                        "city": data.get("city"),
                        "temperature": data.get("temp"),
                        "condition": data.get("condition")
                    }
                )
        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e)
            )
```

### plugin.json

```json
{
  "name": "weather_tool",
  "version": "1.0.0",
  "description": "天气查询工具",
  "type": "tool",
  "permissions": ["network"],
  "dependencies": {
    "httpx": "^0.24.0"
  }
}
```
