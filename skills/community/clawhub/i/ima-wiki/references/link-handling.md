# 链接处理（阶段 3 详细）

> **前置要求**：链接处理必须在编译前完成，不得在编译阶段临时获取。

## 1. 链接特性预获取流程

### 步骤 1：收集文件列表

获取文件夹中的所有文件，提取每个文件的 `media_id`、`media_type`、`title`：

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "folder_id": "<folder_id>", "count": 100}' | \
python3 -c "import sys,json; data=json.load(sys.stdin); [print(f\"{f['media_id']}|{f['media_type']}|{f['title']}\") for f in data.get('data',{}).get('list',[])]"
```

### 步骤 2：批量获取链接特性

对每个文件调用 `export_media_for_ima_sandbox`：

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/export_media_for_ima_sandbox" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"media_id": "<media_id>"}'
```

### 步骤 3：生成链接特性表

根据返回结果，建立如下表格：

| media_id | title | media_type | 链接策略 | URL/备注 |
|---------|-------|-----------|---------|---------|
| xxx | 文章A | 2 (网页) | ✅ 可内嵌 | https://... |
| xxx | 文章B | 6 (公众号) | ✅ 可内嵌 | https://... |
| xxx | 文章C | 7 (Markdown) | ⚠️ 不内嵌 | 请在知识库中查看 |
| xxx | 文章D | 11 (笔记) | ⚠️ 不内嵌 | 请在知识库中查看 |

### 步骤 4：按类型分类编译

编译导览笔记时，根据链接特性表选择正确的写法：

| 文件类型 | 编译写法 |
|---------|---------|
| type 2/6 | `[标题](永久URL)` |
| type 7/11 | `标题`（纯文本，不加链接）|
| type 1/3/4/5 | `标题 — 请在知识库中查看` |

## 2. 链接策略表

| media_type | 类型 | 链接策略 |
|-----------|------|---------|
| **2** | 网页链接 | ✅ 获取真实 URL，格式：`[《标题》](URL)` |
| **6** | 公众号文章 | ✅ 获取真实 URL，格式：`[《标题》](URL)` |
| **7** | Markdown | ⚠️ 不内嵌链接，写为纯文本 |
| **11** | 笔记 | ⚠️ 不内嵌链接，写为纯文本 |
| **1** | PDF | ⚠️ 标注"请在知识库中查看" |
| **3** | Word | ⚠️ 标注"请在知识库中查看" |
| **4** | PPT | ⚠️ 标注"请在知识库中查看" |
| **5** | Excel | ⚠️ 标注"请在知识库中查看" |

## 3. 引用格式示例

```markdown
# 可链接的类型（type 2/6）
• 多维度指标体系：A股情绪温度计采集12个维度指标...[《A股情绪温度计》](https://...)详细阐述了...

# 不可直接链接的类型（type 7/11/1/3/4/5）
• 系统化执行：（请在知识库中查看）
```

## 4. 获取公众号/网页的永久 URL

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/export_media_for_ima_sandbox" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"media_id": "<文件media_id>"}'
```

返回的 `data.media_content_url_info.url` 即为永久可跳转链接。

## 5. 特殊字符处理

文章标题中可能含有干扰 Markdown 渲染的字符：
- `|` → 替换为全角 `｜` 或省略
- `[` `]` `_` `*` → 需转义或省略

详见 [guide-template.md](guide-template.md) 第 7 节。

## 6. 反模式教训

### 反模式 1：Markdown 表格中包含 `|` 字符

**问题**：知识库文章标题常含 `|`（如"实务 | 审计抽样实操总结"），在 Markdown 表格中 `|` 是列分隔符，导致表格解析错乱——一个单元格的内容会被拆成多列。

**错误示例**：
```markdown
| # | 文章 | 关键词 |
|---|------|--------|
| 1 | 实务 | 审计抽样实操总结 |  ← "实务"和"审计抽样实操总结"被拆成两列
```

**正确做法**：使用编号列表替代表格：
```markdown
1. **实务｜审计抽样实操总结** — 审计抽样实操、统计抽样方法
```

### 反模式 2：通过 `push_note` + `content_cos_key` 写入短内容

**问题**：COS 上传路径对内容格式敏感，中间环节多（本地文件 → COS 上传 → API 读取），任何一环出错都会导致笔记内容丢失或被系统自动删除（`export_note` 返回 "doc is delete"）。

**正确做法**：对于 < 3KB 的内容，直接使用 `import_doc` + `curl -d @filepath` 写入，跳过 COS 中间环节。

### 反模式 3：创建笔记后不验证

**问题**：笔记创建接口返回成功不代表内容完整。可能出现：标题正确但正文为空、内容被截断、笔记被系统自动清理等情况。

**正确做法**：创建笔记后立即调用 `export_note` 导出内容，与原始内容比对。

### 反模式 4：导览内容基于本地缓存而非知识库实际状态

**问题**：本地 `.md` 文件可能被其他任务覆盖或已过时，基于本地文件生成的导览与知识库实际文章不匹配。

**正确做法**：导览笔记的文章列表必须从 `get_knowledge_list` 返回的实际文件生成。
