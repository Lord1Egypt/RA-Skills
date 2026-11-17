---
name: ima-knowledge-base
description: 腾讯IMA知识库技能。封装IMA智能知识库的完整接口，支持OpenAPI和Cookie两种认证方式。功能包括知识库管理、笔记CRUD、RAG问答、文件夹操作、订阅知识库管理等。
---

# IMA 知识库技能

## 概述

本技能封装了腾讯 IMA 智能知识库的完整接口，支持两种认证方式：

| 认证方式 | 接口前缀 | 功能范围 |
|---------|---------|---------|
| **OpenAPI** (Client ID + API Key) | `/openapi/` | 仅个人笔记操作 |
| **Cookie** 认证 | `/cgi-bin/` | 完整知识库 + 问答 |

## 功能特性

### Cookie 认证（全功能）
- ✅ **获取知识库列表** - 个人、订阅、公开知识库
- ✅ **知识库问答** - 基于知识库的 RAG 问答
- ✅ **笔记搜索** - 搜索笔记本和笔记内容
- ✅ **文件夹管理** - 创建/读取文件夹结构
- ✅ **订阅知识库操作** - 操作他人分享的知识库

### OpenAPI 认证（基础功能）
- ✅ **创建笔记** - 将内容保存到 IMA 知识库
- ✅ **读取笔记** - 获取知识库中的笔记内容
- ✅ **追加内容** - 向已有笔记追加新内容

## 快速开始

### 第一步：获取 Cookie（激活完整功能）

```bash
cd ./skills/ima_knowledge_base

# 方案A：Playwright 自动获取
python get_ima_cookie_playwright.py

# 方案B：手动获取后验证
python test_cookie.py "你的_Cookie_字符串"
```

#### 手动获取 Cookie（3步）
1. 打开 https://ima.qq.com ，用微信扫码登录
2. 按 **F12** → **Network** → 刷新页面
3. 点击任意请求 → 复制 **Headers** 中的 **Cookie**

### 第二步：测试接口

```bash
# 验证 Cookie + 查看知识库
python test_cookie.py "你的_Cookie"

# 批量测试所有端点
python test_endpoints.py "你的_Cookie"
```

### 第三步：环境变量持久化

验证成功后，Cookie 自动保存到 `~/.hermes/.env`

```bash
# 或者手动添加
echo 'IMA_COOKIE="你的_Cookie"' >> ~/.hermes/.env
```

## 使用方法

### Python SDK - Cookie 认证

```python
import requests
import re
from pathlib import Path

# 读取 Cookie
env_file = Path.home() / ".hermes" / ".env"
content = env_file.read_text()
cookie = re.search(r'IMA_COOKIE=["\'](.+?)["\']', content).group(1)

# 通用 Headers
headers = {
    'x-ima-cookie': cookie,
    'x-ima-bkn': '212004022',
    'From_browser_ima': '1',
    'Content-Type': 'application/json'
}

# 1. 获取知识库列表
resp = requests.post(
    'https://ima.qq.com/cgi-bin/knowledge_tab_reader/get_home_page_data',
    headers=headers,
    json={"knowledge_base_id": "", "need_folder_number": True}
)
data = resp.json()
print(f"知识库列表: {data['data']}")

# 2. 知识库问答
resp = requests.post(
    'https://ima.qq.com/cgi-bin/assistant/qa',
    headers=headers,
    json={"query": "你的问题", "knowledge_base_id": "知识库ID"}
)
# 返回 SSE 流式数据
```

### Python SDK - OpenAPI 认证

```python
from ima_sdk import IMAKnowledgeBase

# 初始化客户端
ima = IMAKnowledgeBase(
    client_id="your_client_id",
    api_key="your_api_key"
)

# 1. 创建笔记
result = ima.create_note(
    content="# 我的笔记\n\n这是笔记内容...",
    title="笔记标题"
)
note_id = result["data"]["note_id"]

# 2. 读取笔记
note = ima.get_note(note_id)
print(note["data"]["content"])

# 3. 追加内容
ima.append_note(note_id, "\n\n## 新增章节\n\n追加的内容...")
```

## API 接口列表

### /cgi-bin/ 接口（Cookie 认证）

| 接口 | 方法 | 说明 |
|------|------|------|
| `/cgi-bin/knowledge_tab_reader/get_home_page_data` | POST | 获取首页数据（知识库列表） |
| `/cgi-bin/knowledge_tab_reader/get_knowledge_base_info` | POST | 获取知识库详情 |
| `/cgi-bin/knowledge_tab_reader/list_knowledge_bases` | POST | 列出知识库 |
| `/cgi-bin/knowledge_tab_reader/search_knowledge` | POST | 搜索知识库内容 |
| `/cgi-bin/knowledge_tab_reader/get_folder_list` | POST | 获取文件夹列表 |
| `/cgi-bin/note/search_note_book` | POST | 搜索笔记本 |
| `/cgi-bin/note/get_note_content` | POST | 获取笔记内容 |
| `/cgi-bin/note/save_note` | POST | 保存笔记 |
| `/cgi-bin/assistant/qa` | POST | 知识库问答（SSE流） |

### /openapi/ 接口（OpenAPI 认证）

| 接口 | 方法 | 说明 |
|------|------|------|
| `/openapi/note/v1/import_doc` | POST | 创建/导入笔记（支持markdown） |
| `/openapi/note/v1/get_doc_content` | POST | 获取笔记内容 |
| `/openapi/note/v1/append_doc` | POST | 追加笔记内容 |

## 请求头

### Cookie 认证 Headers

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Content-Type': 'application/json',
    'From_browser_ima': '1',
    'Extension_version': '999.999.999',
    'Referer': 'https://ima.qq.com/wikis',
    'x-ima-bkn': '212004022',
    'x-ima-cookie': '你的_Cookie',
    'accept': 'application/json',
}
```

### OpenAPI 认证 Headers

```
ima-openapi-clientid: {CLIENT_ID}
ima-openapi-apikey: {API_KEY}
Content-Type: application/json; charset=utf-8
```

## 配置文件

### 环境变量

```bash
# Cookie 认证（完整功能）
IMA_COOKIE="你的_Cookie"

# OpenAPI 认证（仅笔记）
IMA_CLIENT_ID="your_client_id"
IMA_API_KEY="your_api_key"
```

## 典型场景

### 场景1：自动搜集 + 存入知识库

```python
# 让 WorkBuddy 每天自动搜索行业动态并存入 IMA
# 1. 搜索公众号文章
# 2. 筛选相关内容
# 3. 调用 /cgi-bin/note/save_note 保存到知识库
```

### 场景2：知识库 RAG 问答

```python
# 基于知识库内容回答问题
resp = requests.post(
    'https://ima.qq.com/cgi-bin/assistant/qa',
    headers=headers,
    json={
        "query": "上周会议的主要结论是什么？",
        "knowledge_base_id": "你的知识库ID"
    },
    stream=True
)

# 解析 SSE 流
for line in resp.iter_lines():
    if line:
        data = json.loads(line.decode('utf-8').replace('data: ', ''))
        print(data.get('content', ''), end='', flush=True)
```

### 场景3：定时推送摘要

```python
# 设置每日自动化任务：
# 1. 读取知识库最新内容
# 2. 生成摘要
# 3. 推送到微信/企微
```

## 常见问题

### Q: Cookie 获取失败？
- 从 **Request Headers** 复制，不是 Response Headers
- Cookie 应包含 `IMA-TOKEN=`
- 尝试刷新页面后重新获取

### Q: 接口返回 401/403？
- Cookie 已过期，需要重新登录获取

### Q: x-ima-bkn 是什么？
- IMA 校验参数，当前固定值：`212004022`

### Q: Cookie 和 OpenAPI 如何选择？
- 需要**知识库问答**或**订阅知识库**：必须用 Cookie
- 仅操作个人笔记：两者皆可，OpenAPI 更稳定

## 文件说明

| 文件 | 说明 |
|------|------|
| `test_cookie.py` | ⭐ Cookie 验证 + 知识库查看 |
| `test_endpoints.py` | 批量测试 /cgi-bin/ 端点 |
| `get_ima_cookie_playwright.py` | Playwright 自动获取 Cookie |
| `test_knowledge_base.py` | 简单测试脚本 |
| `get_ima_cookie_guide.py` | 完整功能测试 |
| `ima_sdk.py` | OpenAPI SDK（仅笔记） |
