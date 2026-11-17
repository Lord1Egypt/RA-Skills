# 写入与验证（阶段 5 详细）

> 适用于：把编译好的导览内容写入笔记本 + 立即验证。

## 1. 写入笔记

### 1.1 构建请求 JSON

```python
import json
with open('guide_content.md', 'r') as f:
    content = f.read()
with open('note_request.json', 'w') as f:
    json.dump({
        'content_format': 1,
        'content': content,
        'title': '📖 主题导览：[主题名称]'
    }, f, ensure_ascii=False, indent=2)
```

### 1.2 创建笔记

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/import_doc" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d @note_request.json | python3 -m json.tool
# 返回: {"code": 0, "data": {"note_id": "xxx"}}
```

### 1.3 笔记本管理（注意端点命名）

```bash
# 列出笔记本（端点是 list_notebook 单数，不是 list_notebooks）
curl -s -X POST "https://ima.qq.com/openapi/note/v1/list_notebook" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"cursor": "0", "limit": 20}' | python3 -m json.tool

# 创建笔记本（端点是 add_notebook，不是 create_notebook）
curl -s -X POST "https://ima.qq.com/openapi/note/v1/add_notebook" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "知识导览"}' | python3 -m json.tool
```

### 1.4 短内容直接写入

对于 < 3KB 的内容，直接使用 `import_doc` + `curl -d @filepath` 写入，跳过 COS 中间环节：

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/import_doc" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d @short_content.json
```

## 2. 验证

### 2.1 导出笔记内容

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id":"<note_id>","target_content_format":1}' | python3 -c "
import sys,json,urllib.request
d=json.load(sys.stdin)
if d['code']==0:
    url=d['data']['content_url']
    req=urllib.request.Request(url)
    resp=urllib.request.urlopen(req)
    print(resp.read().decode('utf-8'))
else:
    print(d)
"
```

### 2.2 验证清单

- [ ] 标题完整、含 emoji 前缀（📖）
- [ ] 章节结构符合 4 章节模板
- [ ] 关键要素都引用了实际文章链接
- [ ] 链接策略正确（type 2/6 用 URL，type 7/11 用纯文本）
- [ ] 表格中无 `|` 字符冲突
- [ ] 内容长度合理（不要过大或异常截断）

### 2.3 验证失败处理

| 失败类型 | 解决方案 |
|---------|---------|
| 标题正确但正文为空 | 删除重建（参考 [security.md](security.md) 安全删除流程）|
| 内容被截断 | 检查原文是否过长；分批写入或简化 |
| 笔记被系统自动清理 | 用 `export_note` 确认是 "doc is delete"，重新创建 |
| 链接显示为文本 | 检查是否使用了正确的 `[](url)` 格式 |

## 3. 增量更新时的笔记操作

### 3.1 列出笔记

```bash
# 注意：端点是 list_note（单数），不是 list_notes
curl -s -X POST "https://ima.qq.com/openapi/note/v1/list_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"notebook_id": "<notebook_id>", "sort_type": 0, "cursor": "", "limit": 20}' | python3 -c "
import sys, json
d = json.load(sys.stdin)
for note in d.get('data', {}).get('note_book_list', []):
    if '主题导览' in note.get('title', ''):
        print(f\"Found: {note['title']} -> note_id: {note['note_id']}\")
"
```

### 3.2 推荐：创建新笔记而非删除旧笔记

> 💡 详见 [security.md](security.md) 第 3 节推荐替代方案

操作流程：
1. 读取旧版本内容（`export_note`）
2. 基于旧版本生成新内容
3. 创建新笔记（`import_doc`）
4. 在新笔记中标注"替代旧版 v1.X（`note_id=XXX`）"
5. 旧笔记保留作为历史版本
6. 用户在 IMA 客户端手动决定是否删除旧笔记

## 4. 重要提醒

- **预获取链接是编译前的必做步骤**——先建立链接特性表，再基于表编译，避免写完后发现无法链接导致返工
- **每次写入后必须立即验证**——`import_doc` 返回成功不代表内容完整
- **删除是高风险操作**——必须遵循 [security.md](security.md) 的安全删除流程
- **产出是笔记本中的笔记**——使用 `import_doc` 创建笔记，写入笔记本
