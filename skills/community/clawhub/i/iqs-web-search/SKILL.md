---
name: iqs-web-search
description: "阿里云 IQS 联网搜索引擎：通过 HTTP API 调用阿里云信息查询服务，获取实时网络搜索结果。用于需要联网检索信息的场景。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["curl", "jq"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "jq",
              "bins": ["jq"],
              "label": "Install jq (brew)",
            },
          ],
        "env":
          [
            {
              "name": "TONGXIAO_API_KEY",
              "description": "阿里云 IQS API Key，从控制台获取：https://ipaas.console.aliyun.com/api-key",
              "required": true,
            },
          ],
      },
  }
---

# IQS Search Skill - 阿里云联网搜索

调用阿里云信息查询服务 (IQS WebSearch) 进行实时网络搜索。适用于需要获取最新网络信息、新闻、知识等场景。

## 前置准备

### 1. 获取 API Key

前往 [阿里云控制台](https://ipaas.console.aliyun.com/api-key) 创建并获取 `X-API-Key`。

### 2. 设置环境变量

```bash
export TONGXIAO_API_KEY='your-api-key-here'
```

建议添加到 `~/.zshrc` 或 `~/.bashrc`：

```bash
echo "export TONGXIAO_API_KEY='your-api-key-here'" >> ~/.zshrc
source ~/.zshrc
```

---

## 使用方法

### CLI 直接调用

```bash
# 基础搜索
~/.openclaw/skills/iqs-search/scripts/iqs-search.sh "阿里巴巴最新财报"

# 搜索新闻
~/.openclaw/skills/iqs-search/scripts/iqs-search.sh "2026 年 AI 技术趋势"

# 搜索技术文档
~/.openclaw/skills/iqs-search/scripts/iqs-search.sh "Kubernetes 部署最佳实践"
```

### 在 Agent 中使用

当用户需要联网检索信息时，调用此 skill：

```bash
# 示例：搜索最新新闻
export TONGXIAO_API_KEY='xxx'
~/.openclaw/skills/iqs-search/scripts/iqs-search.sh "今日科技新闻"
```

---

## 输出格式

搜索结果以结构化格式输出：

```
---
标题：{网页标题}
链接：{网页 URL}
摘要：{搜索摘要}
正文：{网页主要内容}
---
标题：{网页标题}
链接：{网页 URL}
...
```

---

## API 说明

### 端点

- **通用搜索**: `https://cloud-iqs.aliyuncs.com/search/genericSearch`
- **统一搜索**: `https://cloud-iqs.aliyuncs.com/search/unified`

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 是 | 搜索查询语句 (2-100 字符) |
| engineType | string | 否 | 搜索引擎类型 (业务透传) |

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| pageItems | array | 搜索结果列表 |
| pageItems[].title | string | 网页标题 |
| pageItems[].link | string | 网页 URL |
| pageItems[].snippet | string | 搜索摘要 |
| pageItems[].mainText | string | 网页正文内容 |
| pageItems[].publishTime | number | 发布时间 (毫秒时间戳) |

---

## 集成示例

### 在 Agent 平台中使用

此 skill 可集成到以下 Agent 平台：

- **阿里云百炼**: 创建自定义插件，配置 HTTP 请求节点
- **Dify**: 使用工作流 + HTTP 请求节点
- **LangChain/OpenAI**: 作为 Function Call 工具

### Python 调用示例

```python
import os
import requests

def iqs_search(query: str) -> str:
    """调用阿里云 IQS 搜索"""
    url = f"https://cloud-iqs.aliyuncs.com/search/genericSearch?query={query}"
    headers = {"X-API-Key": os.getenv("TONGXIAO_API_KEY")}
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    results = response.json().get("pageItems", [])
    return "\n---\n".join([
        f"标题：{r.get('title', '')}\n链接：{r.get('link', '')}\n摘要：{r.get('snippet', '')}"
        for r in results
    ])
```

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `TONGXIAO_API_KEY 未设置` | 缺少环境变量 | 设置 `export TONGXIAO_API_KEY='xxx'` |
| `HTTP 401` | API Key 无效 | 检查 Key 是否正确，或前往控制台重新生成 |
| `HTTP 429` | 请求超限 | 降低请求频率，参考配额文档 |
| `HTTP 400` | 参数错误 | 检查 query 长度 (2-100 字符) |
| `timeout` | 请求超时 | 检查网络连接，或增加 TIMEOUT 值 |

---

## 配额与限制

- **QPS 限制**: 参考 [配额文档](https://help.aliyun.com/zh/document_detail/2870259.html)
- **Query 长度**: 2-100 字符
- **超时时间**: 默认 10 秒

---

## 相关文档

- [接入搜索 HTTP API](https://help.aliyun.com/zh/document_detail/2871439.html)
- [创建并查看凭证](https://help.aliyun.com/zh/document_detail/2872258.html)
- [查询响应时间与配额](https://help.aliyun.com/zh/document_detail/2870259.html)
- [阿里云 IQS 控制台](https://ipaas.console.aliyun.com/api-key)

---

_MickeMIN · 技能库 · IQS Web Search_
