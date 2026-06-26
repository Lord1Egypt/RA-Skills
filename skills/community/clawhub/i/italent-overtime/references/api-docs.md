# 北森 iTalent 加班 API 接口文档

## 基础信息

**基础 URL:** `https://openapi.italent.cn`

**认证方式:** Bearer Token

**Content-Type:** `application/json`

---

## 1. 获取 Access Token

所有 API 调用的前提是先获取 `access_token`。

### 请求

```http
POST /token
Content-Type: application/json

{
  "grant_type": "client_credentials",
  "app_key": "你的 AppKey",
  "app_secret": "你的 AppSecret"
}
```

### 响应

```json
{
  "access_token": "X4eTEiMr-r_64sjPaOQ6...",
  "token_type": "bearer",
  "expires_in": 7200,
  "refresh_token": "Z0HaROZY-kJFasI6_u9jKRwXXxkq7Tn68M6O9HfPhpti4ap_-7l6wZDziZj7E-Eq7eL8ZAAQ5"
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `access_token` | string | 访问令牌，有效期 2 小时 |
| `token_type` | string | 令牌类型，固定为 `bearer` |
| `expires_in` | int | 过期时间（秒），默认 7200 |
| `refresh_token` | string | 刷新令牌 |

---

## 2. 推送加班并发起审批

### 请求

```http
POST /AttendanceOpen/api/v1/AttendanceOvertime/PostOverTimeWithApproval
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "attendanceOverTime": {
    "staffId": "11xxxxx80",
    "startDate": "2024-01-01 18:00:00",
    "stopDate": "2024-01-01 20:00:00",
    "compensationType": 1,
    "reason": "项目上线",
    "properties": {}
  },
  "identityType": 0
}
```

### 请求参数

**根对象：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `attendanceOverTime` | object | 是 | 加班数据对象 |
| `identityType` | int | 否 | 主键类型：0=员工邮箱，1=北森 UserId |

**attendanceOverTime 对象：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `staffId` | string | 条件 | 北森 StaffId（identityType=1 时必填） |
| `email` | string | 条件 | 员工邮箱（identityType=0 时必填） |
| `startDate` | string | 是 | 开始时间，格式：`2024-01-01 18:00:00` |
| `stopDate` | string | 是 | 结束时间，格式：`2024-01-01 20:00:00` |
| `compensationType` | int | 是 | 加班补偿方式 |
| `reason` | string | 否 | 加班原因 |
| `overtimeCategory` | string | 否 | 加班类别 (UUID) |
| `transferOrganization` | string | 否 | 支援组织 |
| `transferPosition` | string | 否 | 支援职位 (UUID) |
| `transferTask` | string | 否 | 支援任务 (UUID) |
| `properties` | object | 否 | 自定义字段 |

### 响应

```json
{
  "code": "200",
  "data": "ccd2ca1e-xxxx-xxxx-xxxx-b2ca3b580bbc",
  "message": null
}
```

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | string | 状态码：200=成功，417=失败，401=无权限 |
| `data` | string | 推送成功后的加班 ID |
| `message` | string | 错误信息（成功时为 null） |

---

## 3. 查询加班数据

### 请求

```http
POST /AttendanceOpen/api/v1/AttendanceOvertime/GetScheduledOverTimeRangeList
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "staffIds": [11xxxxx80, 11xxxxx81],
  "startDate": "2024-01-01",
  "stopDate": "2024-01-07"
}
```

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `staffIds` | array[int] | 是 | 员工 ID 列表 |
| `startDate` | string | 是 | 开始日期，格式：`2024-01-01` |
| `stopDate` | string | 是 | 结束日期，格式：`2024-01-07` |

**限制：** 员工数 × 天数 ≤ 100

### 响应

```json
{
  "code": "200",
  "message": "Succeed",
  "data": [
    {
      "staffId": 11xxxxx80,
      "scheduledDate": "2024-01-01",
      "overTimeStartTime": "2024-01-01 18:00",
      "overTimeEndTime": "2024-01-01 20:00"
    }
  ]
}
```

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `staffId` | int | 员工 ID |
| `scheduledDate` | string | 排班日期 |
| `overTimeStartTime` | string | 加班开始时间 |
| `overTimeEndTime` | string | 加班结束时间 |

---

## 4. 撤销加班

### 请求

```http
POST /AttendanceOpen/api/v1/AttendanceOvertime/PostRevokeOverTimeWithApproval
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "overTimeRevokeId": "0073xxxx-xxxx-xxxx-xxxx-xxxxxxxx3d31"
}
```

### 请求参数

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `overTimeRevokeId` | string | 是 | 要撤销的加班 ID |

### 响应

```json
{
  "code": "200",
  "message": null
}
```

---

## 错误码说明

| 错误码 | 说明 | 解决方案 |
|--------|------|---------|
| 200 | 成功 | - |
| 206 | 部分成功 | - |
| 401 | 无权限 | 检查 access_token 是否有效 |
| 417 | 业务失败 | 根据 message 调整参数 |
| 500 | 服务器错误 | 联系北森技术支持 |

### 常见 417 错误

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `不能提交历史考勤期间的单据` | 日期是过去 | 使用未来日期 |
| `您的企业没有 [工作日加班项目]` | 企业未配置 | 联系管理员配置 |
| `参数不可为空` | 缺少必填参数 | 检查请求参数 |

---

## 频率限制

| 限制类型 | 值 |
|---------|-----|
| QPS | 50 次/秒/企业 |
| QPM | 1500 次/分钟/企业 |

---

## 最佳实践

1. **Token 管理**
   - 缓存 access_token，避免频繁请求
   - Token 过期前主动刷新
   - 使用 `--save` 参数自动保存

2. **错误处理**
   - 检查响应 code 字段
   - 401 错误时重新认证
   - 417 错误时提示具体原因

3. **批量操作**
   - 查询时注意 100 条限制
   - 推送时单次一条
   - 必要时分批处理

---

**最后更新：** 2026-03-31
