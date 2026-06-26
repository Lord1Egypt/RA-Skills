# 例子：用户粘贴文字存入知识库（文本导入）

> 用户在对话中粘贴了一段会议纪要，想存到知识库里。后端没有独立的文本创建接口，Agent 需要自行创建 md 文件后上传。

## 用户输入

```
帮我把下面这段内容存到「项目文档」知识库里：

## Q1 产品规划会议纪要
日期：2026-03-15
参会人：张三、李四、王五

### 决议事项
1. 4月底完成 v2.0 核心功能开发
2. 5月中旬启动内测
3. 用户增长目标：月活 50 万
```

## 调用链路

```
步骤 1 — 找到目标知识库
GET /api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=50
→ 找到「项目文档」collectionId: "xxx"
（如果找不到，问用户是否要创建新的）

步骤 2 — Agent 创建临时 md 文件
在本地创建临时文件，将用户粘贴的文本写入：
  TMP_FILE=$(mktemp /tmp/iflow_text_XXXXXX.md)
  cat > "$TMP_FILE" << 'CONTENT_EOF'
  ## Q1 产品规划会议纪要
  日期：2026-03-15
  ...（用户的全部内容）
  CONTENT_EOF

步骤 3 — 通过 upload 接口上传临时文件
POST /api/v1/knowledge/upload
[multipart: file=@/tmp/iflow_text_XXXXXX.md, collectionId=xxx, type=MARKDOWN]
→ data.contentId: "content_text"

步骤 4 — 清理临时文件
  rm "$TMP_FILE"

步骤 5 — 等待文件解析完成
POST /api/v1/knowledge/pageQueryContents?collectionId=xxx&pageNum=1&pageSize=50
→ 找到 contentId="content_text" 的文件，检查 status
→ status: "processing" → 等待
→ status: "success" ✓

（可选）步骤 6 — 重命名文件（临时文件名不友好，给它起个好名字）
先从步骤 5 的返回中获取 contentType（如 "UPLOADV2"）
POST /api/v1/knowledge/updateContent2Collection
Body(JSON): {
  "collectionId": "xxx",
  "contentType": "UPLOADV2",
  "contentId": "content_text",
  "removeFlag": false,
  "extra": {"fileName": "Q1产品规划会议纪要.md"}
}
```

## 展示给用户

```
已将内容保存到知识库「项目文档」

文件「Q1产品规划会议纪要.md」已创建并解析完成。
```

## 关键规则

- **后端没有文本创建接口**，Agent 必须自行创建 `.md` 临时文件后通过 upload 上传
- 文件 type 固定为 `MARKDOWN`
- 上传后记得清理临时文件（`rm $TMP_FILE`）
- 建议上传后重命名，让文件名对用户更友好
- 如果用户没指定标题，Agent 应从文本内容中提取一个合适的标题作为文件名
