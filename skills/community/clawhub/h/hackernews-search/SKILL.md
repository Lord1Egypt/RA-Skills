---
name: HackerNews数据服务
description: 一个通过Model Context Protocol提供HackerNews内容搜索、检索和分析的服务，适用于AI代理和开发者。
version: 1.0.0
---

# HackerNews数据服务

一个通过Model Context Protocol提供HackerNews内容搜索、检索和分析的服务，适用于AI代理和开发者。

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
| Search HackerNews for stories, comments, and other content by keyword.
	
Supports:
- Keyword search across titles, text, and authors
- Tag filtering (story, comment, poll, show_hn, ask_hn, front_page, author_USERNAME)
- Numeric filters for points, comments, and dates
- Pagination with customizable results per page
- Advanced filtering with OR logic and multiple conditions

Basic Examples:
- Search for AI stories: { "query": "AI", "tags": ["story"] }
- Find popular posts: { "query": "Python", "numericFilters": ["points>=100"] }
- Filter by author: { "query": "startup", "tags": ["author_pg"] }
- Date range: { "query": "startup", "numericFilters": ["created_at_i>1640000000"] }

Advanced Filtering Examples:
- High engagement posts: { "query": "programming", "numericFilters": ["points>=100", "num_comments>=50"] }
- OR logic for tags: { "query": "web", "tags": ["(story,poll)"] } - returns stories OR polls
- Author with filters: { "query": "", "tags": ["author_pg", "story"], "numericFilters": ["points>=50"] }
- Multiple conditions: { "query": "AI", "tags": ["story"], "numericFilters": ["points>=200", "num_comments>=100"] }

Numeric Filter Operators: < (less than), <= (less than or equal), = (equal), >= (greater than or equal), > (greater than)
Numeric Filter Fields: points, num_comments, created_at_i (Unix timestamp)

Tag Syntax:
- Single tag: ["story"] - only stories
- Multiple tags (AND): ["story", "show_hn"] - stories that are also show_hn
- OR logic: ["(story,poll)"] - stories OR polls
- Author filter: ["author_USERNAME"] - posts by specific author

Returns paginated results with hits, total count, and page information. | `scripts.tools.search_posts` |
| Retrieve posts currently on the HackerNews front page.

Returns stories sorted by HackerNews ranking algorithm. The front page typically contains the most popular and trending stories.

Supports:
- Pagination to view beyond the first page
- Customizable results per page (default: 30)
- All posts are tagged with 'front_page'

Examples:
- Get first page: { }
- Get with custom page size: { "hitsPerPage": 50 }
- Get second page: { "page": 1 }

Returns the same structure as search results with hits, pagination info, and metadata. | `scripts.tools.get_front_page` |
| Retrieve the most recent HackerNews posts sorted by date.

Returns posts in chronological order (newest first), including all types of content unless filtered.

Supports:
- Filter by content type using tags (story, comment, poll, show_hn, ask_hn, etc.)
- Pagination to view older posts
- Customizable results per page (default: 20)
- Empty query to get all recent posts

Examples:
- Get latest stories: { "tags": ["story"] }
- Get latest comments: { "tags": ["comment"] }
- Get all recent activity: { }
- Get with custom page size: { "hitsPerPage": 50 }

Use this to monitor real-time HackerNews activity or find the newest content. | `scripts.tools.get_latest_posts` |
| Retrieve detailed information about a specific HackerNews item by ID.

Returns complete item details including the full nested comment tree. Use this to:
- View a story with all comments
- Read a specific comment with its replies
- Explore discussion threads in depth
- Get complete metadata for any item

Features:
- Full nested comment tree (all levels)
- Complete item metadata (title, url, text, points, author, etc.)
- Works for stories, comments, polls, and poll options
- Includes creation time and item type

Examples:
- Get story with comments: { "itemId": "38456789" }
- Get specific comment: { "itemId": "38456790" }
- Get poll: { "itemId": "126809" }

Note: Large comment threads (>500 comments) may take 2-3 seconds to load due to nested fetching.
Returns error if item doesn't exist or has been deleted. | `scripts.tools.get_item` |
| Retrieve public profile information for a HackerNews user.

Returns user profile including karma, bio, and account creation date. Use this to:
- Check user reputation (karma score)
- Read user bio and about information
- See when account was created
- Verify user existence before searching their content

Features:
- Username (case-sensitive)
- Karma score (total upvotes received)
- About/bio text (may contain HTML)
- Account creation date (Unix timestamp)

Examples:
- Get famous user: { "username": "pg" }
- Check moderator: { "username": "dang" }
- Verify author: { "username": "tptacek" }

Username validation:
- Alphanumeric characters and underscores only
- Case-sensitive
- Must exist on HackerNews

Returns error if user doesn't exist or username format is invalid. | `scripts.tools.get_user` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.search_posts
工具描述：Search HackerNews for stories, comments, and other content by keyword.
	
Supports:
- Keyword search across titles, text, and authors
- Tag filtering (story, comment, poll, show_hn, ask_hn, front_page, author_USERNAME)
- Numeric filters for points, comments, and dates
- Pagination with customizable results per page
- Advanced filtering with OR logic and multiple conditions

Basic Examples:
- Search for AI stories: { "query": "AI", "tags": ["story"] }
- Find popular posts: { "query": "Python", "numericFilters": ["points>=100"] }
- Filter by author: { "query": "startup", "tags": ["author_pg"] }
- Date range: { "query": "startup", "numericFilters": ["created_at_i>1640000000"] }

Advanced Filtering Examples:
- High engagement posts: { "query": "programming", "numericFilters": ["points>=100", "num_comments>=50"] }
- OR logic for tags: { "query": "web", "tags": ["(story,poll)"] } - returns stories OR polls
- Author with filters: { "query": "", "tags": ["author_pg", "story"], "numericFilters": ["points>=50"] }
- Multiple conditions: { "query": "AI", "tags": ["story"], "numericFilters": ["points>=200", "num_comments>=100"] }

Numeric Filter Operators: < (less than), <= (less than or equal), = (equal), >= (greater than or equal), > (greater than)
Numeric Filter Fields: points, num_comments, created_at_i (Unix timestamp)

Tag Syntax:
- Single tag: ["story"] - only stories
- Multiple tags (AND): ["story", "show_hn"] - stories that are also show_hn
- OR logic: ["(story,poll)"] - stories OR polls
- Author filter: ["author_USERNAME"] - posts by specific author

Returns paginated results with hits, total count, and page information.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|string|true| |Search query text (minimum 1 character)|
|tags|array|false| |Optional filter tags (e.g., ['story'], ['comment'], ['(story,poll)'] for OR logic, ['author_pg'] for author filter)|
|numericFilters|array|false| |Optional numeric filters (e.g., ['points>=100'], ['num_comments>=50'], ['created_at_i>1640000000']). Multiple filters use AND logic.|
|page|number|false|0.0|Page number (0-indexed, default: 0)|
|hitsPerPage|number|false|20.0|Results per page (1-1000, default: 20)|

---

## scripts.tools.get_front_page
工具描述：Retrieve posts currently on the HackerNews front page.

Returns stories sorted by HackerNews ranking algorithm. The front page typically contains the most popular and trending stories.

Supports:
- Pagination to view beyond the first page
- Customizable results per page (default: 30)
- All posts are tagged with 'front_page'

Examples:
- Get first page: { }
- Get with custom page size: { "hitsPerPage": 50 }
- Get second page: { "page": 1 }

Returns the same structure as search results with hits, pagination info, and metadata.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|page|number|false|0.0|Page number (0-indexed, default: 0)|
|hitsPerPage|number|false|30.0|Results per page (1-1000, default: 30)|

---

## scripts.tools.get_latest_posts
工具描述：Retrieve the most recent HackerNews posts sorted by date.

Returns posts in chronological order (newest first), including all types of content unless filtered.

Supports:
- Filter by content type using tags (story, comment, poll, show_hn, ask_hn, etc.)
- Pagination to view older posts
- Customizable results per page (default: 20)
- Empty query to get all recent posts

Examples:
- Get latest stories: { "tags": ["story"] }
- Get latest comments: { "tags": ["comment"] }
- Get all recent activity: { }
- Get with custom page size: { "hitsPerPage": 50 }

Use this to monitor real-time HackerNews activity or find the newest content.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|tags|array|false| |Optional filter tags (e.g., ['story'], ['comment'])|
|page|number|false|0.0|Page number (0-indexed, default: 0)|
|hitsPerPage|number|false|20.0|Results per page (1-1000, default: 20)|

---

## scripts.tools.get_item
工具描述：Retrieve detailed information about a specific HackerNews item by ID.

Returns complete item details including the full nested comment tree. Use this to:
- View a story with all comments
- Read a specific comment with its replies
- Explore discussion threads in depth
- Get complete metadata for any item

Features:
- Full nested comment tree (all levels)
- Complete item metadata (title, url, text, points, author, etc.)
- Works for stories, comments, polls, and poll options
- Includes creation time and item type

Examples:
- Get story with comments: { "itemId": "38456789" }
- Get specific comment: { "itemId": "38456790" }
- Get poll: { "itemId": "126809" }

Note: Large comment threads (>500 comments) may take 2-3 seconds to load due to nested fetching.
Returns error if item doesn't exist or has been deleted.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|itemId|string|true| |HackerNews item ID (e.g., '38456789')|

---

## scripts.tools.get_user
工具描述：Retrieve public profile information for a HackerNews user.

Returns user profile including karma, bio, and account creation date. Use this to:
- Check user reputation (karma score)
- Read user bio and about information
- See when account was created
- Verify user existence before searching their content

Features:
- Username (case-sensitive)
- Karma score (total upvotes received)
- About/bio text (may contain HTML)
- Account creation date (Unix timestamp)

Examples:
- Get famous user: { "username": "pg" }
- Check moderator: { "username": "dang" }
- Verify author: { "username": "tptacek" }

Username validation:
- Alphanumeric characters and underscores only
- Case-sensitive
- Must exist on HackerNews

Returns error if user doesn't exist or username format is invalid.
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|username|string|true| |HackerNews username (alphanumeric + underscores, e.g., 'pg')|

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