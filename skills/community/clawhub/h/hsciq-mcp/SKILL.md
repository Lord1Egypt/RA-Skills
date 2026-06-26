---
name: hsciq-mcp
description: HS Code Lookup for Chinese Products. Query customs codes, tariff rates, declaration elements, and regulatory requirements via HSCIQ MCP API. Create classification consultation requests with image upload for expert review.
license: MIT
tags:
  - HS Code Lookup for Chinese Products
  - Tariff Classification
  - Customs
  - Trade
  - China
  - MCP
env:
  HSCIQ_API_KEY:
    description: "HSCIQ API key for accessing the customs code lookup service"
    required: true
  HSCIQ_BASE_URL:
    description: "HSCIQ API base URL (default: https://www.hsciq.com)"
    required: false
    default: "https://www.hsciq.com"
credentials:
  - name: HSCIQ API Key
    description: "Free API key from https://www.hsciq.com"
    required: true
    url: https://www.hsciq.com
---

# ⚠️ 使用前必读：需要 API 密钥

**本技能需要 HSCIQ API 密钥才能正常工作。**

## 获取 API 密钥

1. 访问 [https://www.hsciq.com](https://www.hsciq.com)
2. 注册账号并登录
3. 在控制台申请 API 密钥
4. 将密钥配置到本地（见下方"配置"章节）

**没有 API 密钥将无法查询海关编码。**

---



# HSCIQ MCP - 海关编码查询服务

专业的中国商品海关编码查询与归类服务，基于 HSCIQ MCP API。

## 功能

- **search_code** - 按关键词搜索海关编码（支持中国/日本/美国）
- **get_code_detail** - 获取海关编码详情（税率、申报要素、监管条件等）
- **search_instance** - 按商品名称检索归类实例（输入具体商品名如"自行车"、"手机壳"，非描述性短语）
- **search_unified** - 统一搜索（CIQ 项目/危化品/港口信息）
- **create_guilei_form** - 创建 HS 归类咨询单（支持产品信息与图片上传，提交给平台专业归类师人工审核）
- **get_guilei_form** - 获取归类咨询单详情（含字段对话、归类结论、修改历史）
- **list_my_guilei_forms** - 获取当前用户的归类咨询单分页列表
- **add_guilei_dialog_message** - 在归类单字段上创建新讨论或回复已有讨论

## 触发条件

用户提到以下关键词时自动触发：
- "海关编码"、"HS 编码"、"税号"、"商品编码"
- "查询税率"、"申报要素"、"监管条件"
- "CIQ"、"危化品"、"港口代码"
- "归类实例"、"商品归类"
- "归类咨询"、"人工复核"、"提交审核"、"专家确认"、"帮我提交归类"
- "我的咨询单"、"咨询详情"、"咨询回复"、"归类结果"

## 配置

配置文件位于 `~/.openclaw/workspace/hsciq-mcp-config.json`：
```json
{
  "baseUrl": "https://www.hsciq.com",
  "apiKey": "your_api_key",
  "authHeader": "X-API-Key"
}
```

**注意**：API Key 也可以通过环境变量设置：
```bash
export HSCIQ_API_KEY=your_api_key
export HSCIQ_BASE_URL=https://www.hsciq.com
```

## 命令

```bash
# 搜索海关编码
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js search-code --keywords "塑料软管" --country CN

# 获取编码详情
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js get-detail --code "3926909090" --country CN

# 搜索归类实例
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js search-instance --keywords "自行车" --country CN

# 统一搜索（CIQ/危化品/港口）
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js search-unified --keywords "食品" --type ciq

# 创建归类咨询单（AI 自动提交人工复核）
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js create-guilei-form \
  --productNameCn "智能手机壳" \
  --uses "手机保护" \
  --ingredients "硅胶" \
  --images ./front.jpg ./back.jpg

# 获取归类咨询单详情
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js get-guilei-form --formId "abc123..."

# 查看我的归类咨询单列表
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js list-my-guilei-forms --pageIndex 1 --pageSize 20

# 在归类单上发起讨论或回复
node ~/.openclaw/skills/hsciq-mcp/hsciq-client.js add-guilei-dialog-message \
  --formId "abc123..." \
  --fieldKey "ProductNameCn" \
  --content "请问这个产品的材质是什么？"
```

## 使用示例

### 示例 1: 查询商品的海关编码
```
用户：帮我查一下"塑料软管"的海关编码
→ 调用 search_code，返回编码列表和税率信息
```

### 示例 2: 获取编码详情
```
用户：3926909090 这个编码的税率是多少
→ 调用 get_code_detail，返回完整税率、申报要素、监管条件
```

### 示例 3: 搜索归类实例
```
用户：看看别人是怎么归类"蓝牙耳机"的
→ 调用 search_instance，输入商品名称关键词"蓝牙耳机"（非短语），返回历史归类案例
```

### 示例 4: AI 拿不准时提交人工复核
```
用户：帮我查一下这个产品的 HS 编码，我不太确定 AI 给的结果对不对
→ AI 在用 search_code 查询后，如果用户对结果有疑问
→ 调用 create_guilei_form，自动提交产品信息与图片，生成归类咨询单
→ 平台专业归类师审核后给出权威结论
```

### 示例 5: 查看归类咨询单结果
```
用户：我之前提交的归类咨询有结果了吗？
→ 调用 list_my_guilei_forms 获取用户的归类咨询单列表
→ 找到目标单后调用 get_guilei_form 获取详情（含归类结论、字段对话）
```

### 示例 6: 在归类单上追问
```
用户：之前在归类单上问过的问题，我想补充信息
→ 调用 add_guilei_dialog_message
→ 传入 formId + fieldKey + content，在指定字段上发起新讨论或回复已有讨论
```

## API 端点说明

所有工具调用统一使用以下端点：

| 端点 | 说明 |
|------|------|
| `POST https://www.hsciq.com/mcp/tools/list` | 列出可用工具 |
| `POST https://www.hsciq.com/mcp/tools/call` | 调用任意工具（通过 `toolName` 参数区分） |

**调用格式示例**：
```json
{
  "toolName": "search_code",
  "arguments": {
    "keywords": "塑料软管",
    "country": "CN",
    "pageIndex": 1,
    "pageSize": 10
  }
}
```

### create_guilei_form 调用示例
```json
{
  "toolName": "create_guilei_form",
  "arguments": {
    "productNameCn": "智能手机壳",
    "productNameEn": "Smartphone Case",
    "uses": "手机保护",
    "ingredients": "硅胶",
    "brand": "某品牌",
    "model": "X1",
    "images": [
      { "fileName": "front.jpg", "data": "base64编码的图片数据..." }
    ]
  }
}
```

**图片限制**：最多 3 张，每张 ≤ 1MB，支持 JPG/PNG/GIF/WebP。每人每天最多创建 5 次（可配置）。

### get_guilei_form 调用示例
```json
{
  "toolName": "get_guilei_form",
  "arguments": {
    "formId": "00000000-0000-0000-0000-000000000001"
  }
}
```

返回完整的归类咨询单详情，包含产品字段、字段对话、归类结论（如有）等信息。

### list_my_guilei_forms 调用示例
```json
{
  "toolName": "list_my_guilei_forms",
  "arguments": {
    "pageIndex": 1,
    "pageSize": 20
  }
}
```

返回当前用户的归类咨询单分页列表，包含表单状态、创建时间等摘要信息。

### add_guilei_dialog_message 调用示例
```json
{
  "toolName": "add_guilei_dialog_message",
  "arguments": {
    "formId": "00000000-0000-0000-0000-000000000001",
    "fieldKey": "ProductNameCn",
    "content": "这个产品的准确材质是什么？",
    "dialogId": null,
    "messageType": null
  }
}
```

- `formId` / `fieldKey` / `content` 为必填
- `dialogId`：不为空时回复已有对话；为空时新建对话
- `messageType`：可选的消息类型

## API 文档

完整 API 说明：https://www.hsciq.com/MCP/Docs

## Python 客户端

也可以使用 Python 脚本直接调用：

```bash
# 搜索海关编码
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py search-code --keywords "塑料软管" --country CN

# 获取编码详情
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py get-detail --code "3926909090"

# 搜索归类实例
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py search-instance --keywords "自行车"

# 统一搜索
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py search-unified --keywords "食品" --type ciq

# 创建归类咨询单
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py create-guilei-form \
  --productNameCn "智能手机壳" --uses "手机保护" --ingredients "硅胶" \
  --images ./front.jpg ./back.jpg

# 获取归类咨询单详情
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py get-guilei-form --formId "abc123..."

# 查看归类咨询单列表
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py list-my-guilei-forms --pageIndex 1

# 归类单讨论
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py add-guilei-dialog-message \
  --formId "abc123..." --fieldKey "ProductNameCn" --content "追问内容"

# 列出可用工具
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py list-tools

# JSON 输出（便于程序处理）
python3 ~/.openclaw/skills/hsciq-mcp/hsciq_client.py search-code --keywords "软管" --json
```

### Python 代码集成

```python
from hsciq_client import HSCIQClient

client = HSCIQClient()

# 搜索编码
result = client.search_code("塑料软管", country="CN")
print(result)

# 获取详情
detail = client.get_code_detail("3926909090")
print(detail)

# 创建归类咨询（图片为文件路径，客户端自动 base64 编码）
result = client.create_guilei_form(
    productNameCn="智能手机壳",
    uses="手机保护",
    ingredients="硅胶",
    images=["./front.jpg", "./back.jpg"]
)
print(result)

# 获取归类咨询单详情
form = client.get_guilei_form("00000000-0000-0000-0000-000000000001")
print(form)

# 查看归类咨询单列表
forms = client.list_my_guilei_forms(pageIndex=1, pageSize=20)
print(forms)

# 在归类单上追问
reply = client.add_guilei_dialog_message(
    formId="00000000-0000-0000-0000-000000000001",
    fieldKey="ProductNameCn",
    content="请确认这个产品的材质"
)
print(reply)
```
