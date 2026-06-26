---
name: hope-client
version: 1.0.0
description: "Hope Server Max API 客户端技能。用于发起对 Hope Server Max 服务端的 API 请求。"
author: Linux2010
keywords: [hope, api, client, server-max, openclaw]
metadata:
  hope:
    emoji: "🔌"
    requires:
      env:
        - HOPE_API_KEY
        - HOPE_HOST
---

# hope-client

Hope Server Max API 客户端技能。用于发起对 Hope Server Max 服务端的 API 请求。

## 环境变量配置

OpenClaw 自动加载 `~/.openclaw/.env` 文件中的环境变量：

```bash
# ~/.openclaw/.env
HOPE_API_KEY=hope-openclaw-apikey-2026-0411
HOPE_HOST=hope05
HOPE_PORT=8088
```

**加载优先级（官方文档）：**
1. 进程已存在的环境变量（不会被覆盖）
2. CWD `.env` 文件
3. `~/.openclaw/.env` 文件

技能脚本通过环境变量读取配置：

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `HOPE_API_KEY` | Hope Server Max API Key | - |
| `HOPE_HOST` | 服务器地址 | `hope05` |
| `HOPE_PORT` | 服务端口 | `8088` |

## 认证方式

所有请求必须携带 `X-OpenClaw-Key` 请求头：

```bash
# 使用环境变量
curl -H "X-OpenClaw-Key: $HOPE_API_KEY" \
  http://$HOPE_HOST:$HOPE_PORT/system/channel/list
```

**从本地通过 SSH 调用：**

```bash
sshpass -p 'hope' ssh $HOPE_HOST \
  "curl -s -H 'X-OpenClaw-Key: $HOPE_API_KEY' http://127.0.0.1:$HOPE_PORT/system/channel/list"
```

---

## API 接口文档

### 1. 频道管理 (Channel)

#### 1.1 查询频道列表

```
GET /system/channel/list
```

**查询参数：**
- `channelName` - 频道名称（可选）
- `channelType` - 频道类型：`bili`、`youtube`、`xigua`（可选）
- `channelOffOn` - 启用状态：`on`、`off`（可选）
- `pageNum` - 页码（默认 1）
- `pageSize` - 每页数量（默认 10）

**响应示例：**
```json
{
  "total": 88,
  "rows": [
    {
      "channelId": 267,
      "channelName": "CopyCat-bili",
      "channelType": "bili",
      "channelOffOn": "on",
      "cookieEnable": "true",
      "engineId": 3,
      "engineName": "hope03"
    }
  ],
  "code": 200,
  "msg": "查询成功"
}
```

#### 1.2 获取所有频道名称

```
GET /system/channel/listAllNames
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": ["CopyCat-bili", "CopyCat-youtube", ...]
}
```

#### 1.3 搜索频道名称

```
GET /system/channel/searchNames?channelName=Copy
```

**查询参数：**
- `channelName` - 搜索关键词（可选，最多返回 5 条）

#### 1.4 获取频道详情

```
GET /system/channel/{channelId}
```

#### 1.5 频道统计信息

```
GET /system/channel/statistics
```

#### 1.6 刷新频道 Cookie

```
POST /system/channel/refresh/{channelId}
```

---

### 2. 上传实例 (Upload Instance)

#### 2.1 查询上传实例列表

```
GET /system/instance/list
```

**查询参数：**
- `channelName` - 频道名称（可选）
- `status` - 状态：`0`=成功, `1`=失败, `2`=执行中, `3`=排队（可选）
- `engineName` - 引擎名称（可选）
- `videoName` - 视频名称（可选）
- `pageNum` - 页码
- `pageSize` - 每页数量

**响应示例：**
```json
{
  "total": 150,
  "rows": [
    {
      "instanceId": "abc123",
      "channelName": "CopyCat-bili",
      "videoName": "测试视频",
      "videoPath": "/path/to/video.mp4",
      "status": "0",
      "uploadLog": "上传成功",
      "createTime": "2026-04-16 10:00:00"
    }
  ],
  "code": 200
}
```

#### 2.2 获取上传实例详情

```
GET /system/instance/{instanceId}
```

#### 2.3 查询上传趋势数据

```
GET /system/instance/queryTrend
```

**查询参数：**
- `channelName` - 频道名称（可选）
- `beginTime` - 开始时间（可选）
- `endTime` - 结束时间（可选）

#### 2.4 查询失败排行列表

```
GET /system/instance/failList
```

#### 2.5 查询失败日志

```
POST /system/instance/queryFailLog
```

**请求体：**
```json
{
  "engineName": "hope02",
  "videoPath": "/path/to/video.mp4"
}
```

---

### 3. 下载实例 (Download Instance)

#### 3.1 查询下载实例列表

```
GET /system/downloadInstance/list
```

**查询参数：**
- `downloadId` - 下载 ID（可选）
- `videoName` - 视频名称（可选）
- `cleanFlag` - 清理状态：`0`=已清理, `1`=手动清理, `2`=未清理（可选）
- `pageNum` - 页码
- `pageSize` - 每页数量

#### 3.2 获取下载实例详情

```
GET /system/downloadInstance/{pkInstanceId}
```

#### 3.3 查询待上传视频列表

```
GET /system/downloadInstance/pending
```

**查询参数：**
- `downloadId` - 下载 ID（可选）
- `limit` - 返回数量限制（可选）

**响应示例：**
```json
{
  "total": 500,
  "rows": [
    {
      "pkInstanceId": "md5hash...",
      "videoName": "待上传视频",
      "videoPath": "/path/to/video.mp4",
      "channelName": "CopyCat-bili",
      "cleanFlag": 2
    }
  ],
  "code": 200
}
```

#### 3.4 统计待上传视频数量

```
GET /system/downloadInstance/pending/count
```

**查询参数：**
- `downloadId` - 下载 ID（可选）

**响应示例：**
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": 500
}
```

#### 3.5 查询下载趋势数据

```
GET /system/downloadInstance/trend
```

#### 3.6 更新清理状态

```
PUT /system/downloadInstance/clean/{pkInstanceIds}
```

---

### 4. 账户管理 (Account)

#### 4.1 查询账户列表

```
GET /system/account/list
```

**查询参数：**
- `accName` - 账户名称（可选）
- `accPhone` - 手机号（可选）
- `accDue` - 到期时间（可选）

#### 4.2 获取账户详情

```
GET /system/account/{accId}
```

---

### 5. 引擎管理 (Engine)

#### 5.1 查询引擎列表

```
GET /system/engineInfo/list
```

**响应示例：**
```json
{
  "total": 6,
  "rows": [
    {
      "engineId": 1,
      "engineName": "hope01",
      "engineIp": "192.168.31.54",
      "engineType": "youtube"
    }
  ],
  "code": 200
}
```

#### 5.2 获取所有引擎信息

```
GET /system/engineInfo/listAll
```

#### 5.3 获取引擎详情

```
GET /system/engineInfo/{engineId}
```

---

## 快速调用函数

技能提供以下快捷调用函数（写入 `scripts/api_client.sh`）：

### 基础调用

```bash
# 调用 API 的基础函数
hope_api() {
  local endpoint="$1"
  local params="${2:-}"
  
  sshpass -p 'hope' ssh hope@hope05 \
    "curl -s -H 'X-OpenClaw-Key: hope-openclaw-apikey-2026-0411' \
     'http://127.0.0.1:8088${endpoint}?${params}'"
}
```

### 常用快捷命令

```bash
# 查询频道列表
hope_channel_list() {
  hope_api "/system/channel/list" "pageSize=100"
}

# 查询待上传视频数量
hope_pending_count() {
  hope_api "/system/downloadInstance/pending/count"
}

# 查询待上传视频列表
hope_pending_list() {
  hope_api "/system/downloadInstance/pending" "limit=20"
}

# 查询上传实例列表
hope_upload_list() {
  hope_api "/system/instance/list" "pageSize=50"
}

# 查询引擎列表
hope_engine_list() {
  hope_api "/system/engineInfo/listAll"
}
```

---

## 使用场景

### 场景 1：检查待上传视频数量

```bash
hope_pending_count
# 输出：{"code":200,"data":500}
```

### 场景 2：查询某频道的上传记录

```bash
hope_api "/system/instance/list" "channelName=CopyCat-bili&pageSize=20"
```

### 场景 3：查询失败的上传任务

```bash
hope_api "/system/instance/list" "status=1&pageSize=50"
```

### 场景 4：查询今日下载入库数量

```bash
hope_api "/system/downloadInstance/trend" "beginTime=2026-04-16"
```

---

## 状态码说明

### upload_instance.status

| 值 | 含义 |
|---|------|
| **0** | 成功 |
| **1** | 失败 |
| **2** | 执行中 |
| **3** | 排队/初始化 |

### download_instance.clean_flag

| 值 | 含义 |
|---|------|
| **0** | 已上传清理 |
| **1** | 手动清理 |
| **2** | 未清理（待上传） |

---

## 注意事项

1. **网络访问**：hope05 是内网服务器（192.168.31.167），需通过 SSH 或内网访问
2. **认证必须**：所有请求必须携带 `X-OpenClaw-Key` 请求头
3. **分页参数**：列表接口默认 pageNum=1, pageSize=10
4. **时间格式**：时间参数格式为 `yyyy-MM-dd HH:mm:ss` 或 `yyyy-MM-dd`