---
name: "openclaw-engine-mcp-setup"
description: "开启 openclaw MCP 功能并添加 MCP 服务器配置。Invoke when user wants to enable MCP or add engine_mcp_server configuration."
---

# OpenClaw MCP 配置技能

## 🎯 技能功能

本技能用于：
1. 开启 openclaw 的 MCP 功能
2. 添加 engine_mcp_server 的 MCP 服务器配置

## 📋 配置说明

### 1. 开启 MCP 功能

在主配置文件中启用 MCP 功能：

```yaml
commands:
  mcp: true
```

### 2. 添加 MCP Server 配置

在主配置文件中添加 MCP Server 配置：

```json
"mcp": {
  "servers": {
    "engine_mcp_server": {
      "url": "https://mcp.hzyotoy.com/engine/mcp",
      "headers": {
        "Authorization": "Aksk Mu4OfFXJSPyWXGv3",
        "appid": "mcpclient001"
      }
    }
  }
}
```

## 🔧 使用场景

当用户需要：
- 开启 openclaw 的 MCP 功能
- 配置 engine_mcp_server 服务器
- 使用 Finance Engine MCP 服务器执行量化策略
- 回测交易策略或执行金融分析

## ⚠️ 注意事项

1. 确保 openclaw 版本 >= 2026.3.24
2. 如需升级 openclaw，请使用 `openclaw update` 命令
3. 配置完成后需要重启 openclaw 使配置生效
4. 确保 Authorization 和 appid 配置正确

## 📝 完整配置示例

```json
{
  "commands": {
    "mcp": true
  },
  "mcp": {
    "servers": {
      "engine_mcp_server": {
        "url": "https://mcp.hzyotoy.com/engine/mcp",
        "headers": {
          "Authorization": "Aksk Mu4OfFXJSPyWXGv3",
          "appid": "mcpclient001"
        }
      }
    }
  }
}
```

## ✅ 验证配置

配置完成后，可以通过以下方式验证：
1. 检查主配置文件中 `commands.mcp` 是否为 `true`
2. 检查 `mcp.servers` 中是否包含 `engine_mcp_server`
3. 尝试调用 MCP 工具确认配置生效

## 🔄 标准 JSON-RPC 调用格式

### MCP 工具标准调用格式
当调用 MCP 工具时，必须使用以下标准的 JSON-RPC 格式：

```json
{
  "method": "tools/call",
  "params": {
    "name": "run_expression_selected",
    "arguments": {
      "input": {
        "startDate": "2023-01-17T00:00",
        "endDate": "2026-04-17T00:00",
        "openCondition": "_close_5m > MAX(_box_15m_green_high, REF(_box_15m_green_high, 1)) && _dkx_30m_cross_status == 1",
        "closeCondition": "_close_5m < MIN(_box_15m_red_low, REF(_box_15m_red_low, 1)) && _dkx_30m_cross_status == -1",
        "period": "5m",
        "poolId": 10,
        "codes": "ag8888,au8888",
        "initCash": 10000000,
        "direction": 1,
        "commssionFee": 0,
        "slippage": 0,
        "runId": 1
      }
    },
    "_meta": {
      "progressToken": 82
    }
  }
}
```

### JSON-RPC 参数说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `method` | `string` | 调用的方法名 | `"tools/call"` |
| `params.name` | `string` | MCP 工具名称 | `"run_expression_selected"` |
| `params.arguments` | `object` | 工具参数对象 | `{ "input": {...} }` |
| `params.arguments.input` | `object` | 策略输入参数 | 见下方详细说明 |
| `params._meta` | `object` | 元数据（可选） | `{ "progressToken": 82 }` |

### input 对象参数说明

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `startDate` | `DateTime` | 开始日期 | `"2023-01-17T00:00"` |
| `endDate` | `DateTime` | 结束日期 | `"2026-04-17T00:00"` |
| `openCondition` | `string` | 开仓条件 | `"_close_5m > MAX(_box_15m_green_high, REF(_box_15m_green_high, 1)) && _dkx_30m_cross_status == 1"` |
| `closeCondition` | `string` | 平仓条件 | `"_close_5m < MIN(_box_15m_red_low, REF(_box_15m_red_low, 1)) && _dkx_30m_cross_status == -1"` |
| `period` | `string` | 基础周期 | `"5m"` |
| `poolId` | `int` | 品种池ID | `10` |
| `codes` | `string` | 合约代码列表 | `"ag8888,au8888"` |
| `initCash` | `float` | 初始资金 | `10000000` |
| `direction` | `int` | 交易方向 | `1`（多头） |
| `commssionFee` | `float` | 手续费% | `0` |
| `slippage` | `float` | 跳数或跳点值 | `0` |
| `runId` | `long` | 运行ID | `1` |

### 调用示例

**示例1：使用品种池回测**
```json
{
  "method": "tools/call",
  "params": {
    "name": "run_expression_selected",
    "arguments": {
      "input": {
        "startDate": "2025-12-25T00:00",
        "endDate": "2026-03-25T00:00",
        "openCondition": "_ma_5m_30_trend == 1 && _dkx_1d_cross_status == 1",
        "closeCondition": "_ma_5m_30_trend == -1 && _dkx_1d_cross_status == -1",
        "period": "5m",
        "poolId": 10,
        "codes": "",
        "initCash": 10000000,
        "direction": 1,
        "commssionFee": 0,
        "slippage": 0,
        "runId": 1774578250123
      }
    }
  }
}
```