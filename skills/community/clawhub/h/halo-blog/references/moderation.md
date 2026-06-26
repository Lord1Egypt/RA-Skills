# Halo CLI 评论审核与通知管理

## 评论（Comment）

### 列表与查看

```bash
halo comment list
halo comment list --approved=false
halo comment list --owner-kind Post --owner-name my-post
halo comment get comment-abc123
```

可用过滤参数：
- `--page` / `--size`：分页
- `--keyword`：关键词过滤
- `--owner-name` / `--owner-kind`：按所属资源过滤
- `--approved`：`true` 或 `false`
- `--sort`：排序方式

### 审核与删除

```bash
halo comment approve comment-abc123
halo comment delete comment-abc123 --force
```

## 回复（Reply）

```bash
halo comment reply list
halo comment reply list --comment comment-abc123
halo comment reply get reply-abc123
halo comment reply approve reply-abc123
halo comment reply delete reply-abc123 --force
```

### 创建官方回复

```bash
halo comment create-reply comment-abc123 --content "Thanks for your feedback"
halo comment create-reply comment-abc123 --content "Following up" --quote-reply reply-abc123
halo comment create-reply comment-abc123 --content "Internal note" --hidden
```

注意：`create-reply` 在控制台上下文中创建的回复默认已审核通过。非交互模式下必须提供 `--content`。

## 通知（Notification）

```bash
halo notification list
halo notification list --unread=false
halo notification get notification-abc123
halo notification mark-as-read notification-abc123
halo notification mark-as-read --all
halo notification delete notification-abc123 --force
```

可用过滤参数：
- `--page` / `--size`
- `--unread`：`true` 或 `false`
- `--sort`
