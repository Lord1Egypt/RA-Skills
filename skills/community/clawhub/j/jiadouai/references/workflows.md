# 公共接口与常见工作流

## account_page

> 调用方式见 SKILL.md「调用方式」

获取已授权的社媒平台账号列表。发布视频/图文前必须调用此接口获取 `account_id`。

```json
{}
```

用 `{}` 获取全部账号。返回 `data` 数组，每个元素含：

| 字段 | 说明 |
|------|------|
| `_id` | 账号唯一标识，作为发布时的 `account_id` |
| `platform` | 平台类型：1=抖音, 5=B站, 6=快手, 11=小红书 |
| `account_name` | 平台账号名称 |
| `status` | `normal` 表示正常 |

## video_publish_status

> 调用方式见 SKILL.md「调用方式」

查询视频/图文发布任务的执行状态。

```json
{
  "task_id": "<发布任务 _id>"  // 必填：video_publish 或 image_publish 返回的 _id
}
```

> ⚠️ 名称暗示视频，但**图文发布也用它**。

## signature

> 调用方式见 SKILL.md「调用方式」

获取 OSS 预签名上传 URL。通常不直接调用，由 `upload.mjs` 内部使用。

```json
{
  "filename": "example.jpg",        // 必填：文件名
  "content_type": "image/jpeg"      // 必填：MIME 类型
}
```

---

## 常见工作流

### 生成 → 轮询

```
echo '<JSON>' | mcporter call ClawAgent.<生成工具> --args -  → 拿到 data._id
  ↓
echo '{"id":"<值>"}' | mcporter call ClawAgent.get_job_status --args -
  → status=processing → 等 5-10s 重试（最多 60 次）
  → status=complete → 提取 urls/videos
```

### 发布

```
account_page → 拿到目标平台账号 _id
  ↓
video_publish / image_publish → 拿到 task_id
  ↓
video_publish_status → 查询发布结果
```
