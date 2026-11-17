# HSCIQ MCP - 海关编码查询服务

多国海关编码查询、公告检索与归类服务（支持 CN/JP/US/EU/VN/MY/BR/MX/ID/CA 10 国编码）。

> **传输协议**：本技能通过**标准 MCP 协议**（JSON-RPC over Stateless Streamable HTTP）与服务端通信，端点 `POST /mcp/rpc`，认证头 `X-API-Key`（或 `Authorization: Bearer`）。所有 CLI 命令对上层调用方式不变。

## 功能

- 搜索海关编码 - 按商品名称查询 HS 编码（10 国）
- 获取编码详情 - 税率、申报要素、监管条件
- 搜索归类实例 - 查看历史归类案例
- 统一搜索 - CIQ 项目/危化品/港口信息（危化品默认按名称检索，可用 `--searchType` 切换 CAS/编码）
- 创建归类咨询 - AI 自动提交产品信息与产品图片（必填至少 1 张），发起人工专家复核，可选指定行业分类
- 查看咨询详情 - 获取归类咨询单的完整详情（字段对话、归类结论）
- 咨询单列表 - 查看我的归类咨询单分页列表
- 咨询讨论 - 在归类单字段上新建讨论或回复已有讨论（支持 `--parentMessageId` 回复指定消息）
- 行业分类列表 - 获取可用的行业分类（用于创建归类咨询单时选择 categoryId）
- 海关公告 - 检索/详情/按 HS 编码反查中国海关公告（含 3 组关联编码）
- 船公司公告 - 船公司清单、公告检索与详情（仅最近 30 天，返回原文）

## 快速开始

### 配置 API Key

创建配置文件 `~/.openclaw/workspace/hsciq-mcp-config.json`：

```json
{
  "baseUrl": "https://www.hsciq.com",
  "apiKey": "your_api_key"
}
```

或使用环境变量：
```bash
export HSCIQ_API_KEY=your_api_key
```

### 使用示例

**Node.js:**
```bash
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js search-code --keywords "塑料软管"
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js get-guilei-form --formId "abc123..."
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js list-my-guilei-forms
```

**Python:**
```bash
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py search-code --keywords "塑料软管"
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py get-guilei-form --formId "abc123..."
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py add-guilei-dialog-message --formId "abc..." --fieldKey "ProductNameCn" --content "追问"
```

## 命令参考

| 命令 | 说明 |
|------|------|
| `search-code` | 搜索海关编码 |
| `get-detail` | 获取编码详情 |
| `search-instance` | 搜索归类实例 |
| `search-unified` | 统一搜索 |
| `create-guilei-form` | 创建归类咨询单（图片必填，AI → 人工复核，可选 `--categoryId`） |
| `get-guilei-form` | 获取归类咨询单详情 |
| `list-my-guilei-forms` | 查看我的归类咨询单列表 |
| `add-guilei-dialog-message` | 归类单字段讨论（新建/回复，支持 `--parentMessageId`） |
| `list-guilei-categories` | 获取行业分类列表（用于 create-guilei-form 的 categoryId） |
| `search-gonggao` | 检索海关公告（CN，支持关键词与发布日期范围） |
| `get-gonggao-detail` | 海关公告详情（含 created/updated/deleted 3 组关联编码） |
| `get-gonggao-by-code` | 按 HS 编码反查海关公告（附 changeType） |
| `list-ocean-carriers` | 船公司清单（SCAC 代码/名称） |
| `search-ocean-carrier-notice` | 检索船公司公告（仅最近 30 天） |
| `get-ocean-carrier-notice-detail` | 船公司公告详情（原文，仅最近 30 天） |
| `list-tools` | 列出服务器公布的全部 MCP 工具（标准 tools/list） |

## API 文档

完整文档：https://www.hsciq.com/MCP/Docs

## License

MIT
