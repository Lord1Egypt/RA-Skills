# Global Search API 演示文档

## ⚠️ 隐私和安全声明

**重要提示：** 本API会将用户搜索查询发送到外部网络搜索服务 `https://clb.ciglobal.cn/web_search`。请注意：

- **数据传输：** 用户查询（可能包含敏感信息）将传输到第三方服务
- **API密钥：** 唯一运行时凭据是 `GLOBAL_SEARCH_API_KEY`
- **凭据存储：** 请使用环境变量或系统凭据管理器安全存储API密钥，切勿硬编码在脚本中
- **用户同意：** 仅在获得用户明确同意后才使用此服务发送其查询
- **数据最小化：** 考虑在发送前对敏感查询进行脱敏或泛化处理
- **使用范围：** 仅将此服务用于合法的搜索目的，不要处理机密或个人数据
- **提供商验证：** 服务提供商 (clb.ciglobal.cn) 是第三方服务。发布前应核验其可信度、隐私政策和主体信息
- **账户关联：** 您的API密钥会将所有查询与您的账户关联。提供商可能会记录并存储您的搜索历史

## API Key 获取与配置

### 获取API Key

在使用本API之前，请先访问 https://clb.ciglobal.cn/apiKey/login 申请您的API Key。

### 配置API Key（推荐方式）

**使用环境变量（推荐）：**

```bash
# Linux/Mac
export GLOBAL_SEARCH_API_KEY="your_api_key_here"

# Windows PowerShell
$env:GLOBAL_SEARCH_API_KEY="your_api_key_here"

# Windows CMD
set GLOBAL_SEARCH_API_KEY=your_api_key_here
```

**或在代码中设置（不推荐用于生产环境）：**
```python
import os
os.environ["GLOBAL_SEARCH_API_KEY"] = "your_api_key_here"
```

## 接口地址

```
POST https://clb.ciglobal.cn/web_search
```

## 请求说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| keyword | string | 是 | 搜索关键词 |
| search_source | string | 否 | 搜索源：`baidu_search`、`google_search`、`baidu_search_ai`，默认 baidu_search |
| mode | string | 否 | 模式：`network`（实时爬取）、`warehouse`（ES 库），默认 network |
| page | int | 否 | 页码，从 1 开始，默认 1 |

**请求头：** 
- `X-API-Key`: 必填，您的API密钥（从 https://clb.ciglobal.cn/apiKey/login 获取）
- `Content-Type`: 必填，设置为 `application/x-www-form-urlencoded`

## 演示示例

### 示例 1：cURL 调用

```bash
curl -X POST "https://clb.ciglobal.cn/web_search" \
  -H "X-API-Key: your_api_key_here" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "keyword=人工智能" \
  -d "search_source=baidu_search" \
  -d "mode=network" \
  -d "page=1"
```

### 示例 2：Python 调用

```python
import requests
import os

# 从环境变量获取API密钥（推荐方式）
API_KEY = os.environ.get("GLOBAL_SEARCH_API_KEY", "your_api_key_here")

if API_KEY == "your_api_key_here":
    print("警告：请设置 GLOBAL_SEARCH_API_KEY 环境变量")

url = "https://clb.ciglobal.cn/web_search"
headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "keyword": "人工智能",
    "search_source": "baidu_search",
    "mode": "network",
    "page": 1
}

response = requests.post(url, headers=headers, data=data)
result = response.json()
print(result)
```

### 示例 3：JavaScript (Fetch)

```javascript
fetch('https://clb.ciglobal.cn/web_search', {
  method: 'POST',
  headers: {
    'X-API-Key': 'your_api_key_here',  // Get your API key at https://clb.ciglobal.cn/apiKey/login
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: new URLSearchParams({
    keyword: '人工智能',
    search_source: 'baidu_search',
    mode: 'network',
    page: '1'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

## 响应示例

```json
{
  "code": 200,
  "message": "success",
  "references": [
    {
      "title": "文章标题",
      "sourceAddress": "https://example.com/article",
      "origin": "来源名称",
      "publishDate": "2025-03-24 12:00:00",
      "summary": "文章摘要"
    }
  ]
}
```

## 搜索源说明

| search_source | 说明 |
|---------------|------|
| baidu_search | 百度资讯实时爬取 |
| google_search | 谷歌资讯实时爬取 |
| baidu_search_ai | 百度 AI 搜索 API |

## 模式说明

| mode | 说明 |
|------|------|
| network | 实时从搜索引擎爬取（配合 search_source 使用） |
| warehouse | 从 Elasticsearch 索引库查询（忽略 search_source） |
