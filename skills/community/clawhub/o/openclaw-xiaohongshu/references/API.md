# 小红书 API 参考文档

本文件整理了可用的 API 操作及其参数描述。

## 认证与状态

### get_session
获取用户会话信息

**示例响应**：
```
{
  "user_id": "123456789",
  "nickname": "用户名",
  "avatar_url": "头像链接",
  "followers": 1000,
  "following": 100,
  "total_likes": 5000,
  "session_status": "active"
}
```

### check_auth_status
检查认证状态

## 笔记操作

### get_all_notes
获取所有笔记列表

**参数**：
- `status`: 笔记状态（"published"/"draft"/"deleted"）
- `page`: 页码（默认 1）
- `pageSize`: 每页数量（默认 10，最多 20）

**示例响应**：
```
{
  "total": 50,
  "notes": [
    {
      "note_id": "63a1234567890",
      "title": "笔记标题",
      "status": "published",
      "created_at": "2024-01-15 10:30:00",
      "type": "video"
    }
  ]
}
```

### get_note_by_id
获取单篇笔记详情

**参数**：
- `note_id`: 笔记 ID（必需）

### get_note_data
获取单篇笔记的阅读和互动数据

**参数**：
- `note_id`: 笔记 ID（必需）

**示例响应**：
```
{
  "note_id": "63a1234567890",
  "views": 1234,
  "likes": 56,
  "collections": 23,
  "comments": 12,
  "share_count": 8,
  "last_updated": "2024-01-15 14:30:00"
}
```

### create_note
发布新笔记

**参数**：
- `note_type`: 笔记类型（"image"/"video"）
- `title`: 标题（10-20 个字符）
- `content`: 正文内容（最多 2000 字符）
- `images`: 图片 URL 列表（发布图片笔记时）
- `video_url`: 视频 URL（发布视频笔记时）
- `tags`: 标签列表
- `category`: 分类 ID
- `is_draft`: 是否存为草稿（bool）

**示例响应**：
```
{
  "note_id": "63a1234567890",
  "status": "published",
  "created_at": "2024-01-15 10:30:00"
}
```

### edit_note
编辑已发布笔记

**参数**：
- `note_id`: 笔记 ID
- `content_change`: 内容变更信息（包括 title, content, images 等）

### publish_note
发布已发布的笔记

**参数**：
- `note_id`: 笔记 ID

### delete_note
删除笔记

**参数**：
- `mode`: 删除模式（"delete"/"archive"）

### set_note_recommended
设置笔记为推荐内容

**参数**：
- `note_id`: 笔记 ID
- `is_rec`: bool 值

## 互动管理

### get_note_comments
获取笔记评论

**参数**：
- `note_id`: 笔记 ID
- `page`: 页码
- `limit`: 返回数量

### publish_comment
发表评论

**参数**：
- `note_id`: 笔记 ID
- `comment_text`: 评论内容

### delete_comment
删除评论

**参数**：
- `comment_id`: 评论 ID
- `parent_comment_id`: 父评论 ID（可选）

### fetch_pager_comments
获取笔记的所有评论

### get_comment_by_id
获取指定评论详情

### block_user
拉黑用户

**参数**：
- `user_id`: 用户 ID

### unblock_user
解除拉黑

### unpub_comment
取消置顶评论

## 用户与账号

### get_user_info
获取用户信息

### get_follower_list
获取粉丝列表

**参数**：
- `page`: 页码
- `limit`: 每页数量

### get_following_list
获取关注列表

### set_user_tag
设置用户标签

**参数**：
- `tag_list`: 标签 ID 列表

### add_account
绑定关联账号

### delete_account
解除绑定

### set_user_profile
修改个人主页

## 分类与标签

### get_all_categories
获取所有分类列表

### get_recommend_tags
获取推荐标签

### search_tags
搜索标签

## 内容审核

### check_publish_ability
检测发布能力

### check_audit_status
审核状态检测

### fetch_draft_list
获取草稿列表

### upload_image
上传图片

### upload_video
上传视频

---

**提示**：具体参数类型和限制请参考官方文档。本文件仅包含 API 操作的基本参数说明。
