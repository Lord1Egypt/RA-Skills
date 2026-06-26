# 录音文件列表查询

## 接口信息

| 类型 | 方法 | 路径 |
|------|------|------|
| 销售录音 | GET | /api/api/apiKeyConfig/innerApi/userRecordingQuery |
| 会议录音 | GET | /api/api/apiKeyConfig/innerApi/userRecordingMeetingQuery |

> 完整 URL：LYK_API_URL（默认 `https://aiapi.szyldata.com`）+ 路径
>
> ⚠️ 路径为 `/api/api/apiKeyConfig/innerApi/...`（双 `/api`），最终拼接：`https://aiapi.szyldata.com/api/api/apiKeyConfig/innerApi/...`

---

## 请求规范（严格按文档）

- **请求头**：`AuthorizationLyk: lyk-xxx`
- **查询参数**：文档中未说明的参数一律不传，两个列表接口均为**无参 GET 请求**

---

## 请求示例

**销售录音：**
```bash
curl -X GET "https://aiapi.szyldata.com/api/api/apiKeyConfig/innerApi/userRecordingQuery" \
  -H "AuthorizationLyk: lyk-xxx" \
  -H "Accept: */*"
```

**会议录音：**
```bash
curl -X GET "https://aiapi.szyldata.com/api/api/apiKeyConfig/innerApi/userRecordingMeetingQuery" \
  -H "AuthorizationLyk: lyk-xxx" \
  -H "Accept: */*"
```

---

## 响应格式

```json
{
  "code": 200,
  "message": "操作成功",
  "msg": "操作成功",
  "data": [],
  "succeed": true
}
```

### data 数组元素字段（实际API返回）

> ⚠️ 以下字段名称严格来自真实 API 响应，不得删除或修改。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 录音文件ID |
| publicUrl | string | 公网URL（音频文件地址） |
| transcriptionSegmentsJson | string | 带时间戳的录音分析分段 |
| summaryJson | string | 全文摘要（解析后含 `title` 和 `summary`） |
| keyPointsJson | string | 重点内容 |
| insightAnalysisJson | string | 洞察分析 |
| mindMapJson | string | 思维导图 |
| translationJson | string | 翻译（可能为null） |
| speakerSummaryJson | string | 按说话人总结 |
| briefSummaryJson | string | 极简总结 |
| meetingMinutesJson | string | 会议纪要（可能为null） |
| bantRaw | string | BANT销售分析（可能为null） |
| competitorSwotRaw | string | SWOT分析（可能为null） |
| actionItemsRaw | string | 待办事项 |
| speakerNamesJson | string | 说话人名称映射（可能为null） |
| dialogExcerptsJson | string | 对话节选 |
| highlightDialogueJson | string | 高光对话 |
| speechDurationJson | string | 说话人时长占比 |
| emotionCurveJson | string | 客户情绪曲线 |
| detailsSupplementJson | string | 详情补充 |
| analysisDimensionJson | string | 结构化评分数据 |
| communicationBackgroundJson | string | 沟通背景 |
| smartBoardJson | string | 智能白板统计数据 |
| goalAndTopicText | string | 会议目标与主题（纯文本） |
| scenarioAndRequirementsText | string | 场景与需求描述（纯文本） |

## 注意事项

- **无单独详情接口**——列表返回的对象已包含完整分析数据
- 所有 `*Json` 字段均为 JSON 字符串，需 `JSON.parse` 后使用