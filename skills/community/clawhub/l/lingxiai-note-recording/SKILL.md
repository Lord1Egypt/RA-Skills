---
name: lingxiai-note-recording
description: |
  灵犀Note录音文件查询 Skill - 查询销售录音和会议录音列表及详情。

  **当以下情况时使用此 Skill**：
  (1) 用户要查询录音列表：「录音列表」「查录音」「销售录音」「会议录音」
  (2) 用户要查看录音详情：「录音详情」「查看录音」
  (3) 用户要配置灵犀 API：「配置灵犀」「连接灵犀」
  (4) 用户要查询会议录音：「会议录音」「会议列表」「查会议」
metadata: {"openclaw": {"requires": {}, "optionalEnv": ["LYK_API_KEY", "LYK_API_URL"], "baseUrl": "https://aiapi.szyldata.com/api", "homepage": ""}}
---

# 灵犀Note录音文件查询 Skill

## 指令路由表

| 指令 | 角色 | 说明 | 详细文档 |
|------|------|------|----------|
| /lyk list 或「录音列表」| 📋 列表官 | 查询录音文件列表（默认销售录音） | [references/list.md](references/list.md) |
| /lyk meeting 或「会议录音」| 📋 会议官 | 查询会议录音列表 | [references/list.md](references/list.md) |
| /lyk detail \<id\> | 🎙️ 详情官 | 查看指定ID录音的完整详情 | [references/list.md](references/list.md) |
| /lyk config 或「配置灵犀」| ⚙️ 配置 | 配置 API Key | [references/config.md](references/config.md) |

---

## 自然语言路由

```
「录音列表」「查录音」「销售录音」        → /lyk list
「会议录音」「会议列表」「查会议」         → /lyk meeting
「录音详情」「查看录音」                  → /lyk detail（需提供ID）
「配置」「连接灵犀」                       → /lyk config
```

**决策原则**：优先区分销售录音和会议录音。有"会议"关键字就是 `/lyk meeting`，其他默认 `/lyk list`。

---

## API 路由表

### 录音文件

| 方法 | 路径 | 说明 | 详细文档 |
|------|------|------|----------|
| GET  | /api/api/apiKeyConfig/innerApi/userRecordingQuery | 销售录音列表查询 | [references/list.md](references/list.md) |
| GET  | /api/api/apiKeyConfig/innerApi/userRecordingMeetingQuery | 会议录音列表查询 | [references/list.md](references/list.md) |

> 完整 URL 格式：LYK_API_URL（默认 `https://aiapi.szyldata.com/api`）+ 路径
>
> ⚠️ 路径为 `/api/api/apiKeyConfig/innerApi/...`（双 `/api`），最终拼接：`https://aiapi.szyldata.com/api/api/apiKeyConfig/innerApi/...`

---

## ⚠️ Agent 必读约束

### 🔑 认证
- **请求头**：`AuthorizationLyk: lyk-xxx`（格式：`lyk-` 开头）
- 每次调用 API 前检查环境变量 `LYK_API_KEY` 是否存在；若不存在，提示用户先完成配置

### 🔢 请求参数规范（严格按文档）
- **文档中未说明的参数，一律不传**
- 销售录音列表接口 `userRecordingQuery` 为**无参 GET 请求**
- 会议录音列表接口 `userRecordingMeetingQuery` 为**无参 GET 请求**
- URL 拼接：`LYK_API_URL` + `/api/api/apiKeyConfig/innerApi/...`（双 `/api`）

### 🚫 反幻觉边界
- 禁止编造录音 ID：所有 id 必须来自 API 响应，不得凭空构造
- 禁止伪造 API 响应：不得在未实际调用 API 的情况下告诉用户查询结果
- 禁止忽略错误码：API 返回非 200 时必须处理，不得静默吞掉

### 🔄 失败重试策略
- **网络/服务错误**（HTTP 5xx 或超时）：等待 5 秒后重试一次，仍失败则报告错误
- **鉴权失败**（401）：检查 API Key 是否正确或已失效
- **服务错误**（500）：稍后重试

### 🔒 安全规则
- 录音数据属于用户隐私，不在群聊中主动展示完整内容
- 调用前验证 API Key 有效性

---

## 通用错误处理

录音文件接口返回格式：
```json
{
  "code": 200,
  "message": "操作成功",
  "msg": "操作成功",
  "data": [],
  "succeed": true
}
```

| code | 说明 | 处理方式 |
|------|------|---------|
| 200 | 成功 | 返回 data 数据 |
| 401 | 鉴权失败 | 检查 API Key |
| 500 | 服务错误 | 稍后重试 |

### 常见错误码（500系列）

| 错误消息 | 说明 | 处理方式 |
|----------|------|---------|
| `AuthorizationLyk不能为空` | 请求头中缺少 AuthorizationLyk 字段 | 检查请求是否正确携带了 `AuthorizationLyk: lyk-xxx` 请求头 |
| `AuthorizationLyk不存在` | 提供的 API Key 无效或已失效 | 确认 API Key 是否正确，或重新配置新的 Key |

---

## 实现说明

### API 请求规范（严格遵循文档）

1. **请求头**：必须携带 `AuthorizationLyk` 字段，格式为 `lyk-xxx`
2. **请求参数**：文档中未明确说明的参数，一律不传。两个列表接口均为**无参请求**
3. **URL 拼接**：完整 URL = `LYK_API_URL` + `/api/apiKeyConfig/innerApi/...`（注意：只有**一个** `/api`）

### 请求示例

**销售录音（无参）：**
```bash
curl -X GET "https://aiapi.szyldata.com/api/api/apiKeyConfig/innerApi/userRecordingQuery" \
  -H "AuthorizationLyk: lyk-xxx" \
  -H "Accept: */*"
```

**会议录音（无参）：**
```bash
curl -X GET "https://aiapi.szyldata.com/api/api/apiKeyConfig/innerApi/userRecordingMeetingQuery" \
  -H "AuthorizationLyk: lyk-xxx" \
  -H "Accept: */*"
```

### Python 实现参考

```python
import requests

def list_recordings(api_key: str, api_url: str = "https://aiapi.szyldata.com"):
    """查询销售录音列表（无参）"""
    url = f"{api_url}/api/api/apiKeyConfig/innerApi/userRecordingQuery"
    headers = {"AuthorizationLyk": api_key, "Accept": "*/*"}
    resp = requests.get(url, headers=headers)
    return resp.json()

def list_meetings(api_key: str, api_url: str = "https://aiapi.szyldata.com"):
    """查询会议录音列表（无参）"""
    url = f"{api_url}/api/api/apiKeyConfig/innerApi/userRecordingMeetingQuery"
    headers = {"AuthorizationLyk": api_key, "Accept": "*/*"}
    resp = requests.get(url, headers=headers)
    return resp.json()
```

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码，200 为成功 |
| message | string | 消息 |
| msg | string | 消息 |
| data | array | 录音数据数组 |
| succeed | boolean | 是否成功 |

### data 数组元素（实际API返回字段）

> ⚠️ 以下字段名称严格来自真实 API 响应，不得删除或修改。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 录音文件ID |
| publicUrl | string | 公网URL（音频文件地址） |
| transcriptionSegmentsJson | string | 带时间戳的录音分析分段（JSON字符串） |
| summaryJson | string | 全文摘要（JSON字符串），解析后含 `title` 和 `summary` |
| keyPointsJson | string | 重点内容（JSON字符串） |
| insightAnalysisJson | string | 洞察分析（JSON字符串） |
| mindMapJson | string | 思维导图（JSON字符串） |
| translationJson | string | 翻译（可能为null） |
| speakerSummaryJson | string | 按说话人总结（JSON字符串） |
| briefSummaryJson | string | 极简总结（JSON字符串） |
| meetingMinutesJson | string | 会议纪要（可能为null） |
| bantRaw | string | BANT销售分析（可能为null） |
| competitorSwotRaw | string | SWOT分析（可能为null） |
| actionItemsRaw | string | 待办事项（JSON字符串） |
| speakerNamesJson | string | 说话人名称映射（可能为null） |
| dialogExcerptsJson | string | 对话节选（JSON字符串） |
| highlightDialogueJson | string | 高光对话（JSON字符串） |
| speechDurationJson | string | 说话人时长占比（JSON字符串） |
| emotionCurveJson | string | 客户情绪曲线（JSON字符串） |
| detailsSupplementJson | string | 详情补充（JSON字符串） |
| analysisDimensionJson | string | 结构化评分数据（JSON字符串） |
| communicationBackgroundJson | string | 沟通背景（JSON字符串） |
| smartBoardJson | string | 智能白板统计数据（JSON字符串） |
| goalAndTopicText | string | 会议目标与主题（纯文本） |
| scenarioAndRequirementsText | string | 场景与需求描述（纯文本） |

- 标题从 `summaryJson.title` 取值，描述从 `summaryJson.summary` 取值