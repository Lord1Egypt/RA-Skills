---
name: notion
description: Notion 集成。搜索页面和数据库，创建/更新/归档页面，读取/追加区块内容，查询数据库。通过 MorphixAI 代理安全访问 Notion API。
metadata:
  openclaw:
    emoji: "📝"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# Notion

通过 `mx_notion` 工具管理 Notion 工作区：搜索、页面管理、数据库查询、内容读写。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接 Notion 账号，或通过 `mx_link` 工具链接（app: `notion`）
5. 在 Notion 中将需要访问的页面/数据库与集成共享

## 核心操作

### 查看当前用户

```
mx_notion:
  action: get_me
```

### 搜索页面和数据库

```
mx_notion:
  action: search
  query: "会议纪要"
  filter_type: "page"
  page_size: 10
```

> `filter_type` 可选值：`page`、`database`。省略则搜索全部类型。

### 获取页面详情

```
mx_notion:
  action: get_page
  page_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 创建页面

```
mx_notion:
  action: create_page
  parent_type: "page"
  parent_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  title: "新页面标题"
  children:
    - type: "paragraph"
      paragraph:
        rich_text:
          - type: "text"
            text:
              content: "页面内容"
```

### 更新页面属性

```
mx_notion:
  action: update_page
  page_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  properties:
    title:
      title:
        - text:
            content: "更新后的标题"
```

### 归档页面

```
mx_notion:
  action: archive_page
  page_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 读取页面内容（区块）

```
mx_notion:
  action: get_block_children
  block_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  page_size: 50
```

### 追加内容到页面

```
mx_notion:
  action: append_blocks
  block_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  children:
    - type: "paragraph"
      paragraph:
        rich_text:
          - type: "text"
            text:
              content: "追加的新段落"
```

### 查询数据库

```
mx_notion:
  action: query_database
  database_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
  filter:
    property: "Status"
    select:
      equals: "进行中"
  sorts:
    - property: "Created"
      direction: "descending"
  page_size: 20
```

## 常见工作流

### 知识库搜索

```
1. mx_notion: search, query: "API 设计规范", filter_type: "page"
2. mx_notion: get_page, page_id: "xxx"  → 查看页面元信息
3. mx_notion: get_block_children, block_id: "xxx"  → 读取具体内容
```

### 项目管理（数据库）

```
1. mx_notion: search, filter_type: "database"  → 找到项目数据库
2. mx_notion: query_database, database_id: "xxx", filter: { status = "进行中" }
3. mx_notion: create_page, parent_type: "database", parent_id: "xxx"  → 创建新任务
```

## 注意事项

- Notion 集成只能访问已明确共享给它的页面和数据库
- 页面 ID 为 UUID 格式（含连字符）
- 搜索结果支持分页：`has_more: true` 时使用 `start_cursor` 获取下一页
- 数据库页面的 `properties` 格式取决于数据库的字段定义
- `account_id` 参数通常省略，工具自动检测已链接的 Notion 账号
