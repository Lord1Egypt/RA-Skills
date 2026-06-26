# InvestmentTracker MCP 标准技能包

## 🎯 概述

这是一个符合 **MCP (Model Context Protocol)** 标准的 InvestmentTracker 技能包。使用标准的 MCP 服务器配置格式，可以与任何支持 MCP 的 AI 助手集成。

## 📁 文件结构

```
InvestmentTracker-platform/
├── mcp_config.json              # MCP 标准配置文件
├── mcp_standard_skill.py        # MCP 标准技能实现
├── InvestmentTracker_skill.py   # 原始技能实现（兼容）
├── simple_skill.py              # 简化版本
├── SKILL.md                     # 技能文档
├── README.md                    # 详细说明
├── USAGE_EXAMPLES.md           # 使用示例
├── MCP_STANDARD_README.md      # 本文档
├── examples/                   # 示例数据
│   ├── portfolio.md
│   ├── transactions.md
│   └── analysis.md
└── scripts/                   # 辅助脚本
    └── fetch_data.py
```

## 🔧 MCP 标准配置

### 配置文件：`mcp_config.json`
```json
{
  "mcpServers": {
    "investmenttracker": {
      "url": "https://investmenttracker-ingest-production.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer it_live_E8MnP28kdPmgpxdjfRG1wzUB9Nr7mCiBU34NjFkAPes",
        "X-API-Key": "it_live_E8MnP28kdPmgpxdjfRG1wzUB9Nr7mCiBU34NjFkAPes"
      }
    }
  }
}
```

### 配置说明
1. **mcpServers**: MCP 服务器配置对象
2. **investmenttracker**: 服务器名称（可自定义）
3. **url**: MCP 服务器端点
4. **headers**: 认证头信息（支持多种认证方式）

## 🚀 快速开始

### 1. 安装依赖
无需安装额外依赖，仅需：
- Python 3.7+
- curl 命令行工具

### 2. 测试技能
```bash
# 使用MCP标准技能
python3 mcp_standard_skill.py all

# 查看用户信息
python3 mcp_standard_skill.py user

# 查看持仓
python3 mcp_standard_skill.py positions

# 查看投资方法论
python3 mcp_standard_skill.py methodology

# 查看统计数据
python3 mcp_standard_skill.py stats

# 查看可用工具
python3 mcp_standard_skill.py tools
```

### 3. 命令行参数
```bash
# 指定配置文件
python3 mcp_standard_skill.py --config custom_config.json all

# 筛选持仓状态
python3 mcp_standard_skill.py positions --status CLOSE

# 限制显示数量
python3 mcp_standard_skill.py positions --limit 5
```

## 📡 MCP 协议支持

### 支持的 MCP 方法
1. **tools/list** - 列出所有可用工具
2. **tools/call** - 调用特定工具
3. **resources/list** - 列出所有可用资源
4. **resources/read** - 读取特定资源

### 可用工具
1. **whoami_v1** - 获取用户身份信息
2. **methodology_get_v1** - 获取投资方法论
3. **stats_quick_v1** - 快速统计数据
4. **positions_list_v1** - 列出持仓位置

## 🔄 数据流

### API 模式
```
用户请求 → MCP客户端 → MCP服务器 → JSON-RPC响应 → 格式化输出
```

### 模拟模式
```
用户请求 → 模拟数据生成器 → 格式化输出
```

### 混合模式（默认）
```
用户请求 → 尝试API连接 → 成功则使用API数据，失败则使用模拟数据
```

## 🛠️ 技术实现

### 核心类
1. **InvestmentTrackerMCPClient** - MCP 标准客户端
   - 使用 curl 发送 HTTP 请求
   - 支持 JSON-RPC 2.0 协议
   - 自动处理认证头

2. **InvestmentTrackerSkill** - 技能主类
   - 加载 MCP 配置
   - 管理客户端连接
   - 提供数据获取接口

### 数据格式化
- **format_user_info()** - 格式化用户信息
- **format_positions()** - 格式化持仓列表
- **format_methodology()** - 格式化投资方法论
- **format_stats()** - 格式化统计数据
- **format_tools()** - 格式化工具列表

## 🔍 错误处理

### 自动回退机制
1. API 连接失败时自动切换到模拟数据
2. 提供清晰的数据源标识
3. 记录详细的错误日志

### 常见错误
- **HTTP 500** - 服务器内部错误
- **认证失败** - API 密钥无效
- **连接超时** - 网络问题
- **JSON 解析错误** - 响应格式不正确

## 🎨 输出示例

### 用户信息
```
👤 用户信息
============================================================
ID: user_123
名称: 投资用户
邮箱: investor@example.com
加入日期: 2024-01-01
投资风格: 成长型
📡 数据源: 模拟数据
```

### 持仓列表
```
📊 持仓列表
============================================================
持仓数量: 2
总价值: $28,750.00

详细持仓:
------------------------------------------------------------
BTC    Bitcoin         数量:   0.5000 现价: $45000.00 价值: $22500.00 收益:  12.5%
ETH    Ethereum        数量:   2.5000 现价: $ 2500.00 价值: $ 6250.00 收益:  25.0%
📡 数据源: 模拟数据
```

## 🔄 集成指南

### 1. 在 OpenClaw 中集成
```bash
# 复制技能目录
cp -r InvestmentTracker-platform /path/to/openclaw/skills/

# 更新技能配置
# 在 OpenClaw 配置中添加 MCP 服务器配置
```

### 2. 在 Claude Desktop 中集成
```json
// 添加到 Claude Desktop 配置
{
  "mcpServers": {
    "investmenttracker": {
      "url": "https://investmenttracker-ingest-production.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

### 3. 在 Cursor 中集成
```json
// 添加到 Cursor 配置
{
  "mcpServers": {
    "investmenttracker": {
      "command": "python3",
      "args": ["/path/to/mcp_standard_skill.py"],
      "env": {
        "MCP_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

## 📊 性能优化

### 1. 连接池
- 复用 HTTP 连接
- 减少连接建立开销

### 2. 数据缓存
- 缓存 API 响应
- 设置合理的过期时间

### 3. 异步处理
- 使用异步 I/O
- 提高并发性能

## 🔧 自定义配置

### 1. 修改认证方式
编辑 `mcp_config.json`：
```json
{
  "mcpServers": {
    "investmenttracker": {
      "url": "YOUR_SERVER_URL",
      "headers": {
        "Authorization": "Bearer YOUR_TOKEN",
        "X-API-Key": "YOUR_API_KEY",
        "Custom-Header": "Custom-Value"
      }
    }
  }
}
```

### 2. 添加新工具
在代码中添加新的工具调用方法：
```python
def get_new_data(self):
    result = self.client.call_tool("new_tool_v1", {"param": "value"})
    # 处理结果
```

### 3. 扩展数据格式化
添加新的格式化函数：
```python
def format_new_data(self, data):
    output = []
    output.append("📊 新数据")
    output.append("=" * 60)
    # 添加格式化逻辑
    return "\n".join(output)
```

## 🚀 部署建议

### 1. 生产环境
- 使用 HTTPS 连接
- 配置 API 密钥轮换
- 启用访问日志
- 设置速率限制

### 2. 监控告警
- 监控 API 可用性
- 设置错误告警
- 跟踪性能指标

### 3. 安全建议
- 保护 API 密钥
- 使用环境变量存储敏感信息
- 定期审计访问日志

## 📞 技术支持

### 1. 问题排查
```bash
# 测试 API 连接
curl -v -X POST https://investmenttracker-ingest-production.up.railway.app/mcp \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","params":{},"id":1}'

# 查看技能日志
python3 mcp_standard_skill.py --debug all
```

### 2. 获取帮助
- 查看 `SKILL.md` 文档
- 参考 `USAGE_EXAMPLES.md` 示例
- 检查错误日志输出

### 3. 报告问题
1. 描述问题现象
2. 提供错误日志
3. 说明复现步骤
4. 提供环境信息

## 🔄 更新日志

### v1.1.0 (2026-02-16)
- ✅ 添加 MCP 标准配置支持
- ✅ 实现标准 MCP 客户端
- ✅ 支持多种认证方式
- ✅ 完善错误处理机制
- ✅ 添加完整文档

### v1.0.0 (2026-02-16)
- ✅ 初始版本发布
- ✅ 支持投资数据查询
- ✅ 实现模拟数据回退
- ✅ 提供命令行接口

## 📚 相关资源

### 官方文档
- [MCP 协议规范](https://spec.modelcontextprotocol.io/)
- [OpenClaw 技能开发指南](https://docs.openclaw.ai/)
- [InvestmentTracker API 文档](https://investmenttracker.com/docs)

### 社区支持
- [OpenClaw Discord](https://discord.com/invite/clawd)
- [MCP 社区](https://github.com/modelcontextprotocol)
- [InvestmentTracker 论坛](https://forum.investmenttracker.com)

## 🎉 开始使用

现在你可以：
1. 测试技能功能：`python3 mcp_standard_skill.py all`
2. 集成到你的 AI 助手
3. 根据需求自定义配置
4. 扩展功能以满足特定需求

祝你使用愉快！ 🚀