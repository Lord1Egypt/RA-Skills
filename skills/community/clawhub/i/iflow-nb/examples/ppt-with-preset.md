# 例子：生成 PPT 并选择风格

> 用户想用知识库里的内容做一份演示文稿，可以选择商务或卡通风格。

## 用户输入

```
用「竞品分析」知识库做个卡通风格的PPT
```

## 调用链路

```
步骤 1 — 找到目标知识库
GET /api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=50
→ 找到「竞品分析」collectionId: "xxx"

步骤 2 — 确认文件状态
POST /api/v1/knowledge/pageQueryContents?collectionId=xxx&pageNum=1&pageSize=50
→ 5 个文件，全部 status: "success" ✓

步骤 3 — 提交创作任务（PPT + 卡通风格）
POST /api/v1/knowledge/creationTask
Body(JSON): {
  "collectionId": "xxx",
  "type": "PPT",
  "preset": "卡通",
  "query": "生成一份竞品分析演示文稿"
}
→ data: "creation_ppt"

⚠️ PPT 专属参数说明：
  - type 固定为 "PPT"（大写）
  - preset 为 "商务" 或 "卡通"（中文）
  - 用户没指定风格时，默认 preset 为 "商务"

步骤 4 — 异步等待（PPT 预计 15-30 分钟）
提交后不阻塞，告知用户预计耗时，后续用户询问时再查询状态：
GET /api/v1/knowledge/creationList?collectionId=xxx&pageNum=1&pageSize=10
→ 找到 contentId == "creation_ppt" 的记录
→ extra.fileType: "PPT", extra.status: "processing" / "success"
```

## 意图识别参考

| 用户说的 | type | preset |
|---------|------|--------|
| "做个PPT" / "生成演示文稿" | `PPT` | `"商务"`（默认） |
| "做个卡通风格的PPT" / "活泼一点的PPT" | `PPT` | `"卡通"` |
| "做个商务风的PPT" / "正式一点的PPT" | `PPT` | `"商务"` |

## 展示给用户

```
已提交卡通风格的 PPT 生成任务，预计需要 15-30 分钟，完成后我会告诉你。
```

## 关键规则

- PPT 的 `type` 是大写 `"PPT"`，与其他类型一致
- PPT 的 `preset` 是中文：`"商务"` 或 `"卡通"`
- 用户没明确说风格时，默认使用 `"商务"`
- PPT 是长任务（预计 15-30 分钟），提交后不阻塞等待，告知用户预计耗时
