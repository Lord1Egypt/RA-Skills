# Protocol Bridge SKILL / 协议桥技能

---

## English

### SKILL Overview

Protocol Bridge is an AI Agent communication infrastructure SKILL that enables seamless cross-protocol agent interaction.

### What This SKILL Does

This SKILL acts as a universal translator and router for AI agents, solving protocol incompatibility between MCP, A2A, LangChain, AutoGPT, and CrewAI.

### Key Capabilities

1. **Protocol Translation** - Convert messages between different protocol formats
2. **Intelligent Routing** - Route to agents based on capabilities
3. **Agent Discovery** - Automatic registration and capability matching
4. **Security** - JWT, OAuth, API keys, mTLS support

### Installation

```bash
npm install -g openclaw-protocol-bridge
```

### Basic Usage

#### Start Bridge Server
```bash
protocol-bridge serve --port 8080
```

#### Register Agents
```bash
# Register MCP agent
protocol-bridge register --id agent-1 --protocol mcp --endpoint http://localhost:3001

# Register A2A agent  
protocol-bridge register --id agent-2 --protocol a2a --endpoint http://localhost:3002
```

#### Send Cross-Protocol Message
```typescript
import { ProtocolBridge } from 'openclaw-protocol-bridge';

const bridge = new ProtocolBridge({
  protocols: {
    mcp: { enabled: true },
    a2a: { enabled: true }
  }
});

await bridge.initialize();

const result = await bridge.send({
  from: { id: 'agent-a', protocol: 'a2a' },
  to: { id: 'agent-b', protocol: 'mcp' },
  action: 'search',
  params: { query: 'test' }
});
```

### Use Scenarios

**1. Enterprise Multi-Agent System**
Connect HR, Finance, and IT agents across different protocols.

**2. Multi-Framework Development**
Build agents with LangChain, AutoGPT, CrewAI - communicate seamlessly.

**3. Protocol Migration**
Migrate from one protocol to another without rewriting agents.

### Configuration

```json
{
  "protocols": {
    "mcp": { "enabled": true },
    "a2a": { "enabled": true }
  },
  "routing": {
    "strategy": "capability-based"
  },
  "security": {
    "authentication": "jwt"
  }
}
```

### CLI Commands

- `protocol-bridge serve` - Start bridge server
- `protocol-bridge init` - Initialize configuration
- `protocol-bridge register` - Register an agent
- `protocol-bridge list` - List all agents
- `protocol-bridge health` - Check system health

### Advanced Features

**Middleware Support**
```typescript
bridge.use(async (message, next) => {
  console.log(`${message.from.id} → ${message.to.id}`);
  return await next(message);
});
```

**Agent Discovery**
```typescript
const agents = await bridge.discover({
  capabilities: ['search'],
  protocols: ['mcp', 'a2a']
});
```

### Troubleshooting

**Agent Not Found**
```bash
protocol-bridge list
```

**Connection Timeout**
Increase timeout in config:
```json
{
  "routing": {
    "timeout": 60000
  }
}
```

### Links

- GitHub: https://github.com/ZhenRobotics/openclaw-protocol-bridge
- npm: https://www.npmjs.com/package/openclaw-protocol-bridge

---

## 中文

### SKILL 概述

Protocol Bridge 是一个 AI Agent 通信基础设施 SKILL，可实现无缝的跨协议 Agent 交互。

### 此 SKILL 的功能

此 SKILL 充当 AI Agent 的通用翻译器和路由器，解决 MCP、A2A、LangChain、AutoGPT 和 CrewAI 之间的协议不兼容问题。

### 核心能力

1. **协议转换** - 在不同协议格式之间转换消息
2. **智能路由** - 根据 Agent 的能力进行路由
3. **Agent 发现** - 自动注册和能力匹配
4. **安全** - 支持 JWT、OAuth、API 密钥、mTLS

### 安装

```bash
npm install -g openclaw-protocol-bridge
```

### 基本使用

#### 启动桥接服务器
```bash
protocol-bridge serve --port 8080
```

#### 注册 Agent
```bash
# 注册 MCP Agent
protocol-bridge register --id agent-1 --protocol mcp --endpoint http://localhost:3001

# 注册 A2A Agent
protocol-bridge register --id agent-2 --protocol a2a --endpoint http://localhost:3002
```

#### 发送跨协议消息
```typescript
import { ProtocolBridge } from 'openclaw-protocol-bridge';

const bridge = new ProtocolBridge({
  protocols: {
    mcp: { enabled: true },
    a2a: { enabled: true }
  }
});

await bridge.initialize();

const result = await bridge.send({
  from: { id: 'agent-a', protocol: 'a2a' },
  to: { id: 'agent-b', protocol: 'mcp' },
  action: 'search',
  params: { query: 'test' }
});
```

### 使用场景

**1. 企业多 Agent 系统**
连接跨不同协议的人力资源、财务和 IT Agent。

**2. 多框架开发**
使用 LangChain、AutoGPT、CrewAI 构建 Agent - 无缝通信。

**3. 协议迁移**
从一个协议迁移到另一个协议，无需重写 Agent。

### 配置

```json
{
  "protocols": {
    "mcp": { "enabled": true },
    "a2a": { "enabled": true }
  },
  "routing": {
    "strategy": "capability-based"
  },
  "security": {
    "authentication": "jwt"
  }
}
```

### CLI 命令

- `protocol-bridge serve` - 启动桥接服务器
- `protocol-bridge init` - 初始化配置
- `protocol-bridge register` - 注册 Agent
- `protocol-bridge list` - 列出所有 Agent
- `protocol-bridge health` - 检查系统健康

### 高级功能

**中间件支持**
```typescript
bridge.use(async (message, next) => {
  console.log(`${message.from.id} → ${message.to.id}`);
  return await next(message);
});
```

**Agent 发现**
```typescript
const agents = await bridge.discover({
  capabilities: ['search'],
  protocols: ['mcp', 'a2a']
});
```

### 故障排查

**找不到 Agent**
```bash
protocol-bridge list
```

**连接超时**
在配置中增加超时：
```json
{
  "routing": {
    "timeout": 60000
  }
}
```

### 链接

- GitHub: https://github.com/ZhenRobotics/openclaw-protocol-bridge
- npm: https://www.npmjs.com/package/openclaw-protocol-bridge

---

**v1.0.0** | MIT License | ZhenRobotics
