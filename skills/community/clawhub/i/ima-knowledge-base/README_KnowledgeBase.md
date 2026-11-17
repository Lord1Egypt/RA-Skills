# IMA 知识库操作指南

## 📌 关键结论

**IMA 和 WorkBuddy 同源，但使用不同 API 层！**

| | OpenAPI (Client ID+API Key) | Cookie 认证 (/cgi-bin/) |
|---|---|---|
| 认证方式 | Client ID + API Key | 浏览器 Cookie |
| 接口前缀 | `/openapi/` | `/cgi-bin/` |
| 支持功能 | 仅个人笔记 | **完整知识库操作** |
| 知识库问答 | ❌ | ✅ |
| 订阅知识库 | ❌ | ✅ |

---

## 🚀 快速开始

### 第一步：获取 IMA Cookie（3步完成）

#### 方法A：Playwright 自动获取（推荐有界面时使用）

```bash
cd ./skills/ima_knowledge_base
python get_ima_cookie_playwright.py
```

> 会打开浏览器窗口，请用微信扫码登录

#### 方法B：手动获取

1. 打开 https://ima.qq.com ，用微信扫码登录
2. 按 **F12** → 切换到 **Network（网络）** 标签 → 刷新页面
3. 点击任意请求（如 get_home_page_data）→ 在 **Headers** 中复制 **Cookie**

### 第二步：验证 Cookie

```bash
cd ./skills/ima_knowledge_base
python test_cookie.py "你的_Cookie_字符串"
```

验证成功后会：
- 自动保存到 `~/.hermes/.env` 作为 `IMA_COOKIE`
- 显示你的知识库列表
- 测试接口可用性

---

## 📂 脚本说明

| 文件 | 说明 |
|------|------|
| `test_cookie.py` | ⭐ **推荐先用这个** - Cookie验证+接口测试一体化 |
| `test_knowledge_base.py` | 简单测试脚本 |
| `get_ima_cookie_playwright.py` | Playwright自动化获取Cookie |
| `get_ima_cookie_guide.py` | 完整功能测试脚本（含详细指南） |
| `ima_sdk.py` | IMA OpenAPI SDK（仅笔记操作） |

---

## 🔌 /cgi-bin/ 接口清单

### 已验证可用接口

#### 1. 获取首页数据（知识库列表）
- **URL**: `POST https://ima.qq.com/cgi-bin/knowledge_tab_reader/get_home_page_data`
- **Headers**:
  ```javascript
  {
    'x-ima-cookie': '你的_Cookie',
    'x-ima-bkn': '212004022',
    'From_browser_ima': '1',
    'Extension_version': '999.999.999',
    'Content-Type': 'application/json'
  }
  ```
- **请求体**:
  ```json
  {
    "knowledge_base_id": "",
    "need_folder_number": true,
    "need_default_cover": false
  }
  ```
- **响应**:
  ```json
  {
    "ret": 0,
    "data": {
      "main_knowledge_base_info": {
        "id": "个人知识库ID",
        "name": "我的知识库"
      },
      "followed_knowledge_base": [
        {"id": "订阅知识库ID", "name": "知识库名"}
      ],
      "recent_public_knowledge_base": []
    }
  }
  ```

#### 2. 笔记搜索
- **URL**: `POST https://ima.qq.com/cgi-bin/note/search_note_book`
- **Headers**: 同上
- **请求体**:
  ```json
  {
    "search_type": 0,
    "query_info": {"title": "搜索关键词"},
    "start": 0,
    "end": 20
  }
  ```

#### 3. 知识库问答（待验证）
- **URL**: `POST https://ima.qq.com/cgi-bin/assistant/qa`
- 使用 SSE 流式返回

#### 4. 获取笔记内容
- **URL**: `POST https://ima.qq.com/cgi-bin/note/get_note_content`
- **Headers**: 同上

#### 5. 创建/更新笔记
- **URL**: `POST https://ima.qq.com/cgi-bin/note/save_note`

### Headers 模板（通用）

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

---

## 🔐 OpenAPI 接口清单（备用）

使用 Client ID + API Key 认证，仅支持个人笔记：

| 接口 | 说明 |
|------|------|
| `/openapi/note/v1/import_doc` | 创建/导入笔记（支持markdown） |
| `/openapi/note/v1/append_doc` | 追加笔记内容 |
| `/openapi/note/v1/search_note_book` | 搜索笔记本 |

---

## 💡 使用示例

### Python 调用示例

```python
import requests
import json

# 读取 Cookie
with open(Path.home() / '.hermes' / '.env') as f:
    content = f.read()
    cookie = re.search(r'IMA_COOKIE=["\'](.+?)["\']', content).group(1)

headers = {
    'x-ima-cookie': cookie,
    'x-ima-bkn': '212004022',
    'From_browser_ima': '1',
    'Content-Type': 'application/json'
}

# 获取知识库列表
resp = requests.post(
    'https://ima.qq.com/cgi-bin/knowledge_tab_reader/get_home_page_data',
    headers=headers,
    json={"knowledge_base_id": "", "need_folder_number": True}
)

data = resp.json()
print(json.dumps(data, ensure_ascii=False, indent=2))
```

---

## ⚠️ 常见问题

### Q: Cookie 获取失败？
- 确保从 **Request Headers** 复制，不是 Response Headers
- Cookie 应该包含 `IMA-TOKEN=`
- 尝试刷新页面后重新获取

### Q: 接口返回 401/403？
- Cookie 可能已过期，需要重新登录获取

### Q: x-ima-bkn 是什么？
- 这是 IMA 的一个校验参数，当前固定值为 `212004022`

---

## 📝 更新日志

- **2026-05-10**: 创建 /cgi-bin/ 接口文档，整理完整Headers模板
