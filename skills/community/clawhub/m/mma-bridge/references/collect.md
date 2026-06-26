# collect API

## 描述

收藏单条或多条流星检测数据。支持单条收藏和批量收藏两种方式。

## 命令

```bash
mma post --method collect --data-file <filePath>
```

## 请求参数

### 单条收藏

```json
{
  "id": "12345"
}
```

### 批量收藏

```json
{
  "ids": ["12345", "12346", "12347"]
}
```

## 参数说明

- `id` (字符串, 可选): 数据的唯一标识符，通过getDataList接口获取。用于单条收藏。
- `ids` (数组, 可选): 数据的唯一标识符数组，用于批量收藏。数组中的每个元素必须是字符串。
- `id` 和 `ids` 参数互斥，不能同时使用，必须提供其中之一。

## 示例

```bash
# 收藏单条数据
echo '{"id": "12345"}' > data.json
mma post --method collect --data-file data.json

# 批量收藏多条数据
echo '{"ids": ["12345", "12346", "12347"]}' > data.json
mma post --method collect --data-file data.json

# 指定端口收藏数据
echo '{"id": "12345"}' > data.json
mma post --method collect --port 9000 --data-file data.json
```

## 响应格式

### 单条收藏响应

```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "id": "12345",
    "data": "success",
    "msg": "收藏成功",
    "summary": "",
    "suggested_actions": []
  }
}
```

### 批量收藏响应

```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "ids": ["12345", "12346", "12347"],
    "collectedCount": 3,
    "failedCount": 0,
    "data": "success",
    "msg": "批量收藏完成，成功收藏3项，失败0项",
    "summary": "",
    "suggested_actions": []
  }
}
```

### 批量收藏（部分失败）响应

```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "ids": ["12345", "12346", "12347"],
    "collectedCount": 2,
    "failedCount": 1,
    "data": "success",
    "msg": "批量收藏完成，成功收藏2项，失败1项",
    "summary": "",
    "suggested_actions": [],
    "errors": [
      {
        "id": "12347",
        "error": "错误信息"
      }
    ]
  }
}
```

## 响应字段说明

### 单条收藏响应字段

- `success` (布尔值): 表示请求是否成功
- `message` (字符串): 状态消息
- `data` (对象): 包含实际信息
  - `id` (字符串): 被收藏的数据ID
  - `data` (字符串): 操作结果，"success"表示成功
  - `msg` (字符串): 状态消息，"收藏成功"
  - `summary` (字符串): 接口摘要
  - `suggested_actions` (数组): 建议的后续操作

### 批量收藏响应字段

- `success` (布尔值): 表示请求是否成功
- `message` (字符串): 状态消息
- `data` (对象): 包含实际信息
  - `ids` (数组): 请求收藏的数据ID数组
  - `collectedCount` (整数): 成功收藏的数量
  - `failedCount` (整数): 收藏失败的数量
  - `data` (字符串): 操作结果，"success"表示成功
  - `msg` (字符串): 状态消息，描述批量收藏的结果
  - `summary` (字符串): 接口摘要
  - `suggested_actions` (数组): 建议的后续操作
  - `errors` (数组, 可选): 失败的详细信息，仅在有失败项时存在
    - 每个元素包含:
      - `id` (字符串): 收藏失败的数据ID
      - `error` (字符串): 失败原因

## 注意事项

1. `id` 或 `ids` 参数必须通过 `getDataList` 接口获取
2. 如果提供的 `id` 或 `ids` 不存在，将返回错误信息
3. 如果软件处于首页（mode=0），将返回错误信息"当前软件只停留在首页，没有数据可供查询"
4. 批量收藏时，即使部分数据收藏失败，也会继续收藏其他数据，并在响应中返回失败信息
5. 已收藏的数据再次调用收藏接口不会产生错误
