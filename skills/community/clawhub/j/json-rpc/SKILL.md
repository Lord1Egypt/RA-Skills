---
name: JSON-RPC服务
description: 一个基于OpenRPC的Model Context Protocol (MCP)服务器，提供JSON-RPC功能调用和方法发现服务。
version: 1.0.0
---

# JSON-RPC服务

一个基于OpenRPC的Model Context Protocol (MCP)服务器，提供JSON-RPC功能调用和方法发现服务。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Call any JSON-RPC method on a server with parameters. A user would prompt: Call method <method> on <server url> with params <params> | `scripts.tools.rpc_call` |
| This uses JSON-RPC to call `rpc.discover` which is part of the OpenRPC Specification for discovery for JSON-RPC servers. A user would prompt: What JSON-RPC methods does this server have? <server url> | `scripts.tools.rpc_discover` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.rpc_call
工具描述：Call any JSON-RPC method on a server with parameters. A user would prompt: Call method <method> on <server url> with params <params>
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|server|string|true| |Server URL|
|method|string|true| |JSON-RPC method name to call|
|params|string|false| |Stringified Parameters to pass to the method|

---

## scripts.tools.rpc_discover
工具描述：This uses JSON-RPC to call `rpc.discover` which is part of the OpenRPC Specification for discovery for JSON-RPC servers. A user would prompt: What JSON-RPC methods does this server have? <server url>
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|server|string|true| |Server URL|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据