# Likes Open API Documentation

Complete API reference for My Likes platform integration.

## Base URL

```
https://my.likes.com.cn/api/open
```

## Authentication

All requests require `X-API-Key` header:
```
X-API-Key: your-api-key
```

Get your API key: https://my.likes.com.cn → 设置 → API 文档

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| GET /activity | 1 request per minute |
| Other endpoints | Standard rate limiting |

## Endpoints

### 1. Data List (Activities)

**GET /api/open/activity**

Fetch user activity data. **Rate limit: 1 request per minute.** Date range max 30 days.

**Headers:**
- `X-API-Key`: Your API key

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | integer | No | User ID (for coaches to query trainees) |
| start_date | string | No | Start date (YYYY-MM-DD) |
| end_date | string | No | End date (YYYY-MM-DD, max 30 days from start) |
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Items per page (default: 20, max: 2000) |
| order_by | string | No | Sort field: sign_date, run_km, run_time, tss (default: sign_date) |
| order | string | No | Sort order: asc or desc (default: desc) |

**Response:**
```json
{
  "list": [
    {
      "id": 1,
      "user_id": 1,
      "sign_date": 1704067200,
      "run_km": 10.5,
      "run_time": 3600,
      ...
    }
  ],
  "total": 100,
  "page": 1,
  "limit": 20,
  "has_more": true
}
```

### 2. Plans List (Calendar Plans)

**GET /api/open/plans**

Fetch calendar plans for next 42 days from start date.

**Headers:**
- `X-API-Key`: Your API key

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start | string | No | Start date (YYYY-MM-DD), defaults to today |
| game_id | integer | No | Filter by training camp ID |

**Response:**
```json
{
  "total": 10,
  "rows": [
    {
      "id": 1,
      "title": "有氧训练",
      "name": "40min@(HRR+1.0~2.0)",
      "start": "2024-01-15",
      "weight": "q2",
      "type": "e",
      ...
    }
  ]
}
```

### 3. Training Feedback

**GET /api/open/feedback**

Fetch user training feedback. Date range max 7 days.

**Headers:**
- `X-API-Key`: Your API key

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start | string | Yes | Start date (YYYY-MM-DD) |
| end | string | Yes | End date (YYYY-MM-DD, max 7 days from start) |
| user_ids | string | No | Comma-separated user IDs (e.g., "4,5,6") for coach to query multiple trainees |

**Response:**
```json
{
  "total": 2,
  "rows": [
    {
      "id": 227639,
      "user_id": 4,
      "content": "训练感觉不错",
      "plan_title": "有氧训练",
      "plan_content": "10min@(HRR+1.0~2.0);40min@(HRR+2.0~3.0);10min@(HRR+1.0~2.0)",
      "activity": {
        "run_km": 8.5,
        "run_time": 3600,
        "score": 85
      },
      "coach_comment": false,
      "created_time": 1757249735
    }
  ]
}
```

**Response Fields:**
| Field | Description |
|-------|-------------|
| `id` | Feedback ID |
| `user_id` | Trainee user ID |
| `content` | Trainee's feedback text |
| `plan_title` | Title of the planned workout |
| `plan_content` | Course code/segments for coach reference |
| `activity` | Linked workout overview with system `score` |
| `coach_comment` | Whether coach has commented (true/false) |
| `created_time` | Timestamp when feedback was created |

### 4. Push Training Plans (Batch Write)

**POST /api/open/plans/push**

Push training plans to calendar. Max 200 plans per request.

**Headers:**
- `X-API-Key`: Your API key
- `Content-Type: application/json`

**Request Body:**
```json
{
  "plans": [
    {
      "name": "10min@(HRR+1.0~2.0);{5min@(HRR+3.0~4.0);1min@(rest)}x3;5min@(HRR+1.0~2.0)",
      "title": "有氧间歇训练",
      "start": "2025-06-10",
      "weight": "q2",
      "type": "i",
      "description": "周二有氧间歇",
      "sports": 1,
      "game_id": 0
    }
  ],
  "game_id": 0,
  "user_ids": []
}
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| plans | array | Yes | Array of plan objects (max 200) |
| plans[].name | string | Yes | Training code in Likes format |
| plans[].title | string | Yes | Display title (max 20 chars) |
| plans[].start | string | Yes | Date (YYYY-MM-DD) |
| plans[].weight | string | No | Intensity: q1/q2/q3/xuanxiu |
| plans[].type | string | No | Training type (see below) |
| plans[].description | string | No | Notes |
| plans[].sports | integer | No | Sport type: 1=run, 2=cycle, 3=strength, 5=swim, 254=other |
| plans[].game_id | integer | No | Training camp ID |
| game_id | integer | No | Global camp ID (overrides plans[].game_id when user_ids set) |
| user_ids | array | No | Array of user IDs for bulk push (e.g., [4,5,6]) |

**Bulk Push:**
When `user_ids` is provided, you must also provide `game_id`. Requirements:
- Current user must be creator or coach of the camp
- All user_ids must be members of the camp
- Plans use outer `game_id` (ignores individual plan game_id)

**Response:**
```json
{
  "total": 2,
  "parse_ok": 1,
  "parse_failed": 1,
  "inserted": 2,
  "insert_failed": 0,
  "results": [
    {
      "index": 0,
      "title": "有氧间歇训练",
      "start": "2025-06-10",
      "status": "ok",
      "message": ""
    }
  ]
}
```

**Status Values:**
- `ok`: Success
- `parse_error`: Code parsing failed (still written, content=[])
- `validate_error`: Field validation failed (not written)
- `insert_error`: Database error (not written)

### 5. Add Coach Comment to Feedback

**POST /api/open/feedback/comment**

Coach adds a comment to a trainee's training feedback. Current user must be a coach; identity is determined by the server.

**Headers:**
- `X-API-Key`: Your API key
- `Content-Type: application/json`

**Request Body:**
```json
{
  "content": "跑得很好，注意拉伸放松",
  "feedback_id": 227639
}
```

**Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content | string | Yes | Comment content / training advice |
| feedback_id | integer | Yes | The training feedback id (from list_feedback rows) |

**Note:** Coach identity is automatically determined by the server based on your API key.

**Response:**
```json
{
  "id": 12345,
  "feedback_id": 227639,
  "user_id": 4,
  "content": "跑得很好，注意拉伸放松",
  "created_time": 1757249735
}
```

### 6. Training Camp Details

**GET /api/open/game**

Fetch camp details and member list. Requires creator or coach role.

**Headers:**
- `X-API-Key`: Your API key

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| game_id | integer | Yes | Training camp ID |

**Response:**
```json
{
  "game": {
    "id": 973,
    "name": "马拉松训练营",
    "description": "...",
    "status": 1,
    ...
  },
  "total": 20,
  "rows": [
    {
      "user_id": 103260,
      "user_name": "张三",
      "head_img_url": "...",
      "sex": "M",
      "weight": 65,
      "max_rate": 185,
      "run_force": 45.2,
      ...
    }
  ]
}
```

### 7. My Training Camps List

**GET /api/open/games**

Fetch camps where you are creator or coach.

**Headers:**
- `X-API-Key`: Your API key

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Items per page (default: 10, max: 10) |

**Response:**
```json
{
  "total": 5,
  "page": 1,
  "limit": 10,
  "rows": [
    {
      "id": 973,
      "name": "马拉松训练营",
      "description": "...",
      "status": 1,
      ...
    }
  ]
}
```

## Training Code Format (name field)

Format: `task1;task2;...`

**Basic task:** `duration@(type+range)`
- `30min@(HRR+1.0~2.0)` - 30 min easy run
- `5km@(PACE+5'00~4'30)` - 5km with pace target

**Interval group:** `{task1;task2}xN`
- `{5min@(HRR+3.0~4.0);1min@(rest)}x3` - 3 sets

**Rest:** `2min@(rest)` - Rest period

### Intensity Types

| Type | Description | Example |
|------|-------------|---------|
| HRR | Heart rate reserve % | `HRR+1.0~2.0` |
| VDOT | VDOT pace zone | `VDOT+4.0~5.0` |
| PACE | Absolute pace (min'sec) | `PACE+5'30~4'50` |
| t/ | Threshold pace % | `t/0.88~0.99` |
| MHR | Max heart rate % | `MHR+0.85~0.95` |
| LTHR | Lactate threshold HR % | `LTHR+1.0~1.05` |
| EFFORT | Perceived effort | `EFFORT+0.8~1.0` |
| FTP | Power % (cycling) | `FTP+0.75~0.85` |
| CP | Absolute power W | `CP+200~240` |
| CSS | Critical swim speed % | `CSS+0.95~1.05` |
| TSP | Threshold swim pace % | `TSP+0.95~1.05` |
| OPEN | Open-ended | `OPEN+1` |

### Duration Units
- `min` = minutes
- `s` = seconds
- `m` = meters
- `km` = kilometers
- `c` = count/reps

## Training Type Mapping

| Type Code | Description |
|-----------|-------------|
| qingsong | Easy run |
| xiuxi | Rest day |
| e | Aerobic training |
| lsd | Long slow distance |
| m | Marathon pace |
| t | Threshold/lactate training |
| i | Interval training |
| r | Speed/repetition |
| ft | Fartlek |
| com | Combined workout |
| ch | Variable pace |
| jili | Strength training |
| max | Max HR test |
| drift | Aerobic stability test |
| other | Other |
| 1/7/2/3/4/5/6 | 1.6km/2km/3km/5km/10km/HM/FM test |

## Intensity Weights

| Weight | Color | Description |
|--------|-------|-------------|
| q1 | Red | High intensity |
| q2 | Orange | Medium intensity |
| q3 | Green | Low intensity |
| xuanxiu | Blue | Optional/recovery |

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad request (invalid parameters, date range > 30 days, missing game_id for bulk push) |
| 401 | Unauthorized (invalid API key) |
| 403 | Forbidden (not authorized to query user, not camp creator/coach for bulk push) |
| 404 | Not found (camp does not exist) |
| 429 | Rate limit exceeded |
| 500 | Server error |
