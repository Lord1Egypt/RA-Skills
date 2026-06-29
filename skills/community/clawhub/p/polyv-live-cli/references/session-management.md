# 场次管理

场次（Session）是直播频道的一次直播活动记录。每个频道可以有多个场次，用于记录不同的直播活动。

## 重要：新版场次 vs 历史场次

PolyV 直播存在两套场次数据，查询命令和 `session get` 的适用范围不同，混用会查不到数据：

| 数据集 | 查询命令 | `session get` 是否支持 |
|--------|----------|------------------------|
| **新版场次**（通过新版场次系统创建/管理的场次） | `session list` | ✅ 支持 |
| **历史场次**（早期直播产生的场次，新版列表查不到） | `session legacy-list` 或 `session data-list` | ❌ 不支持（`session get` 仅支持新版场次 ID） |

典型坑：`session list` 返回空，但 `session legacy-list`/`session data-list` 能查到场次；此时拿到的历史 `sessionId` 不能再用 `session get` 查询（会返回"场次不存在"）。历史场次的详情请直接使用 `session legacy-list`/`session data-list` 的返回结果。

## 命令概览

| 命令 | 说明 |
|------|------|
| `session list` | 获取**新版**场次列表（仅新版场次系统） |
| `session legacy-list` | 查询频道**历史**场次信息 |
| `session data-list` | 查询频道**历史**场次数据列表 |
| `session get` | 获取**单个新版场次**详情（仅支持 `session list` 返回的 sessionId） |
| `session create` | 创建新版场次 |
| `session update` | 更新新版场次 |
| `session delete` | 删除新版场次 |
| `session external` | 管理外部场次 ID 关联 |

## 场次列表

获取频道或账号下的场次列表。

### 语法

```bash
<CLI> session list [-c <频道ID>] [--page <页码>] [--page-size <数量>] [-o <格式>]
```

### 参数

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--channel-id` | `-c` | 否 | 频道ID，不传则获取整个账号下的所有场次 |
| `--page` | | 否 | 页码，默认 1 |
| `--page-size` | | 否 | 每页数量，默认 10 |
| `--output` | `-o` | 否 | 输出格式：`table`（默认）或 `json` |

### 示例

```bash
# 获取频道场次列表
<CLI> session list -c 2588188

# 获取整个账号下的场次
<CLI> session list

# 分页查询
<CLI> session list -c 2588188 --page 2 --page-size 20

# JSON 格式输出
<CLI> session list -c 2588188 -o json
```

### 表格输出示例

```
场次列表 - 频道: 2588188
共 2 个场次

场次ID          名称          状态      开始时间              结束时间
e9s2h3jd8f     测试场次1     已结束    2024-01-15 10:30     2024-01-15 11:00
k7d9f2h1l5     测试场次2     直播中    2024-01-15 14:00     -
```

## 场次详情

获取指定场次的详细信息。

> ⚠️ `session get` 仅支持**新版场次**的 `sessionId`（即 `session list` 返回的 ID）。历史场次的 `sessionId`（来自 `session legacy-list` / `session data-list`）不支持，会返回"场次不存在"，请直接使用历史列表命令的返回结果。

### 语法

```bash
<CLI> session get -c <频道ID> --session-id <场次ID> [-o <格式>]
```

### 参数

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--channel-id` | `-c` | 是 | 频道ID |
| `--session-id` | | 是 | 场次ID |
| `--output` | `-o` | 否 | 输出格式：`table`（默认）或 `json` |

### 示例

```bash
# 获取场次详情
<CLI> session get -c 2588188 --session-id e9s2h3jd8f

# JSON 格式输出
<CLI> session get -c 2588188 --session-id e9s2h3jd8f -o json
```

### 表格输出示例

```
场次详情 - 频道: 2588188

场次ID: e9s2h3jd8f
名称: 测试场次1
状态: 已结束
开始时间: 2024-01-15 10:30
结束时间: 2024-01-15 11:00
计划开始: 2024-01-15 10:00
计划结束: 2024-01-15 12:00
推流类型: client
推流客户端: web
观看地址: https://live.polyv.net/2588188/e9s2h3jd8f
```

## 场次状态

| 状态值 | 中文名称 | 说明 |
|--------|----------|------|
| `unStart` | 未开始 | 场次已创建但尚未开始 |
| `live` | 直播中 | 正在直播 |
| `end` | 已结束 | 直播已结束 |
| `playback` | 回放中 | 正在播放回放 |
| `expired` | 已过期 | 场次已过期 |

## JSON 输出字段

### 场次列表响应

```json
{
  "contents": [
    {
      "sessionId": "e9s2h3jd8f",
      "channelId": "2588188",
      "name": "测试场次1",
      "status": "end",
      "startTime": "2024-01-15 10:30",
      "endTime": 1705287600000,
      "createdTime": 1705285800000,
      "planStartTime": 1705284000000,
      "planEndTime": 1705291200000,
      "streamType": "client",
      "pushClient": "web",
      "watchUrl": "https://live.polyv.net/2588188/e9s2h3jd8f",
      "userId": "user123"
    }
  ],
  "pageNumber": 1,
  "pageSize": 10,
  "totalItems": 2,
  "totalPages": 1
}
```

### 场次详情字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `sessionId` | String | 场次ID |
| `channelId` | String | 频道ID |
| `name` | String | 场次名称 |
| `status` | String | 场次状态 |
| `startTime` | String | 开始时间 |
| `endTime` | Number | 结束时间（毫秒时间戳） |
| `createdTime` | Number | 创建时间（毫秒时间戳） |
| `planStartTime` | Number | 计划开始时间（毫秒时间戳） |
| `planEndTime` | Number | 计划结束时间（毫秒时间戳） |
| `streamType` | String | 流类型 |
| `pushClient` | String | 推流客户端类型 |
| `watchUrl` | String | 观看地址 |
| `userId` | String | 用户ID |
| `splashImg` | String | 封面图 |
| `splashLargeImg` | String | 竖屏大图封面 |

## 相关 API 文档

- [获取场次列表](../../docs/api/v4/channel/session/new/list.md)
- [获取场次详情](../../docs/api/v4/channel/session/new/get.md)

## 相关命令

- [频道管理](channel-management.md) - 管理直播频道
- [回放管理](playback.md) - 管理直播回放
- [推流操作](streaming.md) - 开始/结束直播
