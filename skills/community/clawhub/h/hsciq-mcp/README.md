# HSCIQ MCP - 海关编码查询服务

专业的中国商品海关编码查询与归类服务。

## 功能

- 搜索海关编码 - 按商品名称查询 HS 编码
- 获取编码详情 - 税率、申报要素、监管条件
- 搜索归类实例 - 查看历史归类案例
- 统一搜索 - CIQ 项目/危化品/港口信息
- 创建归类咨询 - AI 自动提交产品信息与图片，发起人工专家复核
- 查看咨询详情 - 获取归类咨询单的完整详情（字段对话、归类结论）
- 咨询单列表 - 查看我的归类咨询单分页列表
- 咨询讨论 - 在归类单字段上新建讨论或回复已有讨论

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
| `create-guilei-form` | 创建归类咨询单（AI → 人工复核） |
| `get-guilei-form` | 获取归类咨询单详情 |
| `list-my-guilei-forms` | 查看我的归类咨询单列表 |
| `add-guilei-dialog-message` | 归类单字段讨论（新建/回复） |

## API 文档

完整文档：https://www.hsciq.com/MCP/Docs

## License

MIT
