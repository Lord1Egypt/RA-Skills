# Hope Server Max API 响应格式参考

## 标准响应格式

### 列表响应 (TableDataInfo)

```json
{
  "total": 100,
  "rows": [
    { ... }
  ],
  "code": 200,
  "msg": "查询成功"
}
```

### 单条响应 (AjaxResult)

```json
{
  "code": 200,
  "msg": "操作成功",
  "data": { ... }
}
```

### 操作响应

```json
{
  "code": 200,
  "msg": "操作成功"
}
```

---

## 状态码说明

| code | 说明 |
|------|------|
| **200** | 成功 |
| **401** | 未授权（缺少或错误的 API Key） |
| **403** | 无权限 |
| **500** | 服务器错误 |

---

## 实体字段说明

### ChannelInfo

| 字段 | 类型 | 说明 |
|------|------|------|
| channelId | Long | 频道 ID |
| channelName | String | 频道名称 |
| channelType | String | 频道类型：`bili`、`youtube`、`xigua` |
| channelOffOn | String | 启用状态：`on`、`off` |
| cookieEnable | String | Cookie 是否有效：`true`、`false` |
| cookieJson | String | Cookie JSON |
| engineId | Long | 引擎 ID |
| engineName | String | 引擎名称 |
| username | String | 登录用户名 |
| password | String | 登录密码 |
| accDue | Date | 账号到期时间 |

### UploadInstance

| 字段 | 类型 | 说明 |
|------|------|------|
| instanceId | String | 实例 ID（UUID） |
| channelName | String | 频道名称 |
| videoName | String | 视频名称 |
| videoPath | String | 视频路径 |
| status | String | 状态：`0`=成功, `1`=失败, `2`=执行中, `3`=排队 |
| uploadLog | String | 上传日志 |
| engineName | String | 引擎名称 |
| createTime | Date | 创建时间 |
| modifyTime | Date | 更新时间 |

### DownloadInstance

| 字段 | 类型 | 说明 |
|------|------|------|
| pkInstanceId | String | 主键 ID（MD5） |
| downloadId | Long | 下载 ID |
| videoName | String | 视频名称 |
| videoPath | String | 视频路径 |
| videoSize | Long | 视频大小（字节） |
| channelName | String | 频道名称 |
| cleanFlag | Integer | 清理状态：`0`=已清理, `1`=手动, `2`=未清理 |
| uploadInstanceId | String | 关联的上传实例 ID |
| createTime | Date | 创建时间 |

### EngineInfo

| 字段 | 类型 | 说明 |
|------|------|------|
| engineId | Long | 引擎 ID |
| engineName | String | 引擎名称 |
| engineIp | String | 引擎 IP |
| engineType | String | 引擎类型 |
| engineStatus | String | 引擎状态 |

### AccountInfo

| 字段 | 类型 | 说明 |
|------|------|------|
| accId | Long | 账户 ID |
| accName | String | 账户名称 |
| accPhone | String | 手机号 |
| accDue | Date | 到期时间 |
| accStatus | String | 账户状态 |

---

## 分页参数

列表接口支持分页：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| pageNum | 1 | 页码 |
| pageSize | 10 | 每页数量 |

**示例：**
```
GET /system/channel/list?pageNum=1&pageSize=20
```