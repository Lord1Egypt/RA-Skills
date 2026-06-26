# 飞书日历 API 详细参考

## 认证

### 获取 tenant_access_token

```
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
Content-Type: application/json

{
  "app_id": "<FEISHU_APP_ID>",
  "app_secret": "<FEISHU_APP_SECRET>"
}

Response:
{
  "code": 0,
  "tenant_access_token": "t-xxx",
  "expire": 7200
}
```

token 有效期 2 小时，建议缓存（脚本已内置）。

---

## 空闲忙查询

### 批量查询（推荐，最多 50 人）

```
POST https://open.feishu.cn/open-apis/calendar/v4/freebusy/batch?user_id_type=open_id
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_ids": ["ou_xxx1", "ou_xxx2"],
  "time_min": "2026-03-26T00:00:00+08:00",
  "time_max": "2026-03-26T23:59:59+08:00",
  "only_busy": false
}

Response (code=0):
{
  "data": {
    "freebusy_list": {
      "freebusy_items": [
        {
          "start_time": {"timestamp": "1711497600"},
          "end_time": {"timestamp": "1711501200"},
          "free_busy_status": "busy"
        }
      ]
    }
  }
}
```

`free_busy_status` 取值：`free` | `busy` | `tentative` | `out_of_office`

---

## 日程管理

### 获取主日历 ID

```
GET https://open.feishu.cn/open-apis/calendar/v4/calendars
Authorization: Bearer <token>
```

返回的日历列表中，`type` 为 `primary` 的即为主日历。

### 创建日程（含飞书视频会议）

```
POST https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events
Authorization: Bearer <token>
Content-Type: application/json

{
  "summary": "面试 — 前端工程师 — 张三",
  "description": "岗位：前端工程师\n候选人：张三\n面试官：李四、王五",
  "need_notification": true,
  "start_time": {"timestamp": "1711497600"},
  "end_time": {"timestamp": "1711501200"},
  "color": -1,
  "visibility": 0,
  "reminders": [{"minutes": 15}],
  "meeting_settings": {
    "is_meeting": true,
    "meeting_type": 0,
    "require_attendee_info": false
  }
}
```

**关键**：
- `timestamp` 必须是**秒级时间戳字符串**，如 `"1711497600"`
- `meeting_type`: 0 = 飞书视频会议
- `need_notification`: true = 向参会者发飞书通知
- 响应中包含 `meeting_url` 字段（视频会议链接）

### 获取日程详情（提取会议链接）

```
GET https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}
Authorization: Bearer <token>
```

响应中的 `data.event.meeting_url` 即为飞书视频会议链接。

### 添加参会者

创建日程后单独调用：

```
POST https://open.feishu.cn/open-apis/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees?user_id_type=open_id
Authorization: Bearer <token>
Content-Type: application/json

{
  "attendees": [
    {"type": "user", "user_id": "ou_xxx1"}
  ],
  "need_notification": true
}
```

### 查询 / 更新 / 删除日程

| 操作 | 方法 | 端点 |
|------|------|------|
| 查询日程 | GET | `/calendar/v4/calendars/{cal_id}/events?time_min=<RFC3339>&time_max=<RFC3339>` |
| 更新日程 | PATCH | `/calendar/v4/calendars/{cal_id}/events/{event_id}` |
| 删除日程 | DELETE | `/calendar/v4/calendars/{cal_id}/events/{event_id}` |

---

## 按姓名查询用户 open_id

使用飞书通讯录搜索 API：

```
POST https://open.feishu.cn/open-apis/usable_contact/v1/user/search
Authorization: Bearer <token>
Content-Type: application/json

{
  "query": "李四",
  "page_size": 5
}
```

从响应 `data.items` 中提取 `user_id.open_id`。找不到时向用户确认姓名或直接要求提供 open_id。

---

## 时间格式

- **RFC 3339**（freebusy 查询）：`2026-03-26T14:00:00+08:00`
- **秒级时间戳字符串**（event 创建/更新）：`"1711497600"`
- 不要用毫秒时间戳，不要用数字类型

## 错误处理

常见错误码：
- `99991663`：无权限，检查应用权限配置
- `99991668`：参数错误，通常 timestamp 格式不对
- `99991672`：日程不存在
- `99991400`：频率超限，降频重试

## 计算共同空闲时间算法

1. 对每个参与者，从 freebusy 响应中提取所有 busy 时段
2. 将所有 busy 时段合并为一个时间段列表（取并集）
3. 在查询时间范围内，busy 之间的间隔即为共同空闲时间
4. 按所需面试时长过滤，保留足够长的空闲段
5. 按偏好排序：工作日 > 周末，上午(9:00-12:00) > 下午(14:00-18:00)
