# 告警与事件 API 详细说明

## 告警管理

### 获取告警列表
**接口：** `POST /alert/problem-list`

**参数：**
- `page` (int, 必填): 页码
- `pageSize` (int, 必填): 每页数量
- `status` (int, 可选): 问题状态
- `severity` (int, 可选): 严重程度
- `clock_begin` (int, 可选): 开始时间（Unix时间戳，北京时间 UTC+8）
- `clock_end` (int, 可选): 结束时间（Unix时间戳，北京时间 UTC+8）

### 获取告警数量统计
**接口：** `POST /alert/problem-report`

**参数：**
- `searchtype` (string, 必填): 搜索类型（history-历史）
- `page` (int, 必填): 页码
- `pageSize` (int, 必填): 每页数量
- `clock_begin` (string, 可选): 开始时间（格式: 2022-04-16 10:48:38，北京时间）
- `clock_end` (string, 可选): 结束时间（格式: 2022-05-16 10:48:38，北京时间）
- `ip` (string, 可选): IP模糊查询
- `is_ip` (bool, 可选): 是否精确IP查询
- `keyword` (string, 可选): 关键字
- `isMaintenanced` (bool, 可选): 是否维护
- `isAcked` (bool, 可选): 是否已确认
- `status` (int, 可选): 告警恢复 (1-未恢复, 2-已恢复)
- `classification` (int, 可选): 大类ID（如: 操作系统=101）
- `subtype` (int, 可选): 子类ID（如: LINUX=101001）
- `groupid` (int, 可选): 对象分组ID

**返回字段说明：**
- `label`: 级别标签
- `value`: 级别数值 (1-信息, 2-警告, 3-次要, 4-严重, 5-紧急)
- `count`: 级别数量

### 确认问题
**接口：** `POST /alert/problem-ack`

**参数：**
- `eventid` (int, 必填): 事件ID
- `message` (string, 可选): 确认消息

### 获取问题列表 (v6)
**接口：** `POST /alert/problem-list`

**说明：** 获取问题列表（v6 版本，支持更详细的筛选）

**参数：**
- `searchtype` (string, 可选): 搜索类型（history-历史）
- `page` (int, 可选): 页码（默认 1）
- `pageSize` (int, 可选): 每页数量（默认 20）
- `clock_begin` (string, 可选): 开始时间（格式: 2022-04-16 10:48:38，北京时间）
- `clock_end` (string, 可选): 结束时间（格式: 2022-05-16 10:48:38，北京时间）
- `ip` (string, 可选): IP 模糊查询
- `is_ip` (bool, 可选): 是否精确 IP 查询
- `keyword` (string, 可选): 关键字
- `isMaintenanced` (bool, 可选): 是否维护
- `isAcked` (bool, 可选): 是否已确认
- `status` (int, 可选): 告警恢复 (1-未恢复, 2-已恢复)
- `classification` (int, 可选): 大类 ID
- `subtype` (int, 可选): 子类 ID
- `groupid` (int, 可选): 对象分组 ID
- `priority` (int, 可选): 告警级别（1-信息, 2-警告, 3-次要, 4-严重, 5-紧急）
- `sortOrder` (string, 可选): 排序方式（asc/desc）
- `sortName` (string, 可选): 排序字段

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": {
        "total": 100,
        "list": [
            {
                "eventid": "55386_1680745801",
                "clock": "2023-04-06 09:50:01",
                "host": "HUAWEI-Quidway",
                "ip": "192.168.1.98",
                "priority": 4,
                "description": "SNMP采集中断",
                "is_unrecovery": 1,
                "is_unack": 1
            }
        ]
    }
}
```

## 事件平台

### 获取事件列表
**接口：** `POST /aialert/list`

**参数：**
- `page` (int, 必填): 页码
- `pageSize` (int, 必填): 每页数量
- `clock_begin` (int, 可选): 开始时间（Unix时间戳，北京时间 UTC+8）
- `clock_end` (int, 可选): 结束时间（Unix时间戳，北京时间 UTC+8）
- `level` (int, 可选): 事件级别
- `source` (string, 可选): 事件来源

### 获取事件详情
**接口：** `POST /aialert/info`

**参数：**
- `eventid` (int, 必填): 事件ID

### 关闭事件
**接口：** `POST /aialert/close`

**参数：**
- `eventids` (int[], 必填): 事件ID数组

### 接收事件数据
**接口：** `POST /aialert/receive`

**说明：** 用于外部系统推送事件数据到平台

**参数：**
- `title` (string, 必填): 事件标题
- `level` (int, 必填): 事件级别
- `object` (string, 可选): 告警对象
- `ip` (string, 可选): IP地址
- `description` (string, 可选): 描述
- `event_time` (int, 可选): 事件时间（Unix 时间戳，北京时间 UTC+8）

## 事件平台告警管理

### 获取事件平台告警列表
**接口：** `POST /aialert/list`

**特殊说明：** 此接口使用 JSON 序列化的 `data` 字段传递参数

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒，北京时间 UTC+8）
- `sign` (string, 必填): 请求签名

**data 参数内容：**
- `page` (int, 必填): 页码
- `pageSize` (int, 必填): 每页数量
- `clock_begin` (int, 可选): 开始时间（Unix 时间戳，北京时间 UTC+8）
- `clock_end` (int, 可选): 结束时间（Unix 时间戳，北京时间 UTC+8）
- `status` (int, 可选): 告警状态 (0-待处理, 1-处理中, 2-已处理)
- `title` (string, 可选): 告警标题
- `user_id` (string, 可选): 参与人ID
- `platform_id` (string, 可选): 平台AppId
- `true_ip` (int, 可选): 是否精确匹配IP (1-是, 0-否)
- `ip` (string, 可选): 告警IP
- `object` (string, 可选): 告警对象
- `object_type` (string, 可选): 对象类型
- `object_group` (string, 可选): 对象分组
- `object_group_cluster` (string, 可选): 对象分组集群
- `object_tag` (string, 可选): 对象标签

**返回字段说明：**
- `id`: 告警ID
- `platform_id`: 平台ID
- `problem_raw_id`: 原始告警ID
- `title`: 告警标题
- `level`: 告警等级 (1-5)
- `object`: 告警对象
- `object_type`: 告警对象类型
- `description`: 告警描述
- `ip`: 告警对象IP
- `status`: 告警状态 (0-待处理, 1-处理中, 2-已处理)
- `event_time`: 告警时间（北京时间）
- `created_at`: 告警创建时间
- `current_process_users`: 当前处理用户
- `closed_user_name`: 告警关闭用户名称

### 更新告警处理状态
**接口：** `POST /aialert/update-status`

**参数：**
- `id` (int, 必填): 告警ID
- `status` (int, 必填): 状态 (1-处理中, 2-已处理)

### 第三方推送告警恢复
**接口：** `POST /aialert/recovery`

**说明：** 第三方系统推送告警恢复通知

**特殊说明：** 此接口使用 JSON 序列化的 `data` 字段传递参数

**参数：**
- `data` (string, 必填): 参数的 JSON 序列化字符串
- `timestamp` (long, 必填): Unix 时间戳（秒），北京时间 UTC+8
- `sign` (string, 必填): 请求签名

**data 参数内容：**
- `appid` (string, 必填): 应用 ID
- `token` (string, 必填): 应用 token
- `event_id` (string, 可选): 事件 ID（当 trigger_id 存在时可不传）
- `trigger_id` (string, 可选): 触发 ID（当存在且 event_id 不传时，会把所有同一个 trigger_id 的未恢复事件全部恢复）
- `recovery_time` (int, 必填): 事件恢复时间，Unix 时间戳（北京时间 UTC+8）

**请求示例：**
```json
{
    "data": "{\"appid\":\"4133289624\",\"token\":\"1989b431c60ecc7fc0b957f7afe9c5f602f8c66f\",\"event_id\":123344,\"trigger_id\":5538,\"recovery_time\":1680745901}",
    "timestamp": 1680745901,
    "sign": "1989b431c60ecc7fc0b957f7afe9c5f602f8c6321"
}
```

**返回示例：**
```json
{
    "code": 0,
    "message": "",
    "data": {
        "success": [
            {
                "recovery_time": "2022-04-06 09:51:41",
                "event_id": "553834",
                "problem_raw_id": 304345,
                "msg": ""
            }
        ],
        "fail": []
    }
}
```

**返回字段说明：**
- `success`: 成功恢复的告警列表
- `fail`: 恢复失败的告警列表
  - `recovery_time`: 恢复时间（北京时间）
  - `event_id`: 事件 ID
  - `problem_raw_id`: 原始告警 ID
  - `msg`: 提示信息

### 关闭事件平台告警
**接口：** `POST /aialert/close`

**参数：**
- `id` (int, 必填): 告警ID
