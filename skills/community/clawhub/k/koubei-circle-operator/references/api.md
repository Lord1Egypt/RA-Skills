# OpenClaw CLI 命令参考

**配置**: 首次使用运行 `node scripts/openclaw.js init --key <your_key>` 完成验证和绑定。
所有命令自动从 `scripts/config.json` 读取配置，无需手动传入 Key。

---

## 1. 数据查询

### 获取开放表列表

```bash
node scripts/openclaw.js tables
```

返回当前圈子下开放的数据表名和字段，用于生成 SQL 查询。

**使用规则**:
- 只能查询返回结果中列出的表和字段
- `searchable: true` 的字段可作为 WHERE 搜索条件，`searchable: false` 的禁止作为 WHERE 条件
- 禁止使用 `SELECT *`，必须明确指定字段名

### 执行 SQL 查询

```bash
node scripts/openclaw.js query "SELECT user_id, nickname FROM wb_users_attribute WHERE is_admin = 1 ORDER BY created_at DESC LIMIT 20"
```

返回 JSON 格式的查询结果。

**使用规则**:
- LIMIT 最大 500
- 严格按用户要求的时间范围添加 WHERE 条件
- 默认只查询审核通过的帖子（audit_status=1）

---

## 2. 发帖

**发帖前必须先向用户确认**：这是普通贴还是活动贴？禁止跳过此步骤。

### 普通帖发帖

```bash
node scripts/openclaw.js publish '{"user_id":12,"type":1,"topic_id":3,"title":"标题","message":"内容"}'
```

**必填参数**:
- `user_id`: 马甲/作者 ID（先查询可用马甲列表）
- `topic_id`: 话题 ID（先查询可用话题列表）
- `title`: 帖子标题
- `message`: 帖子内容
- `type`: 帖子类型（查询帖子表获取，文字贴通常为 `1`）

**注意**: 发帖成功后禁止再次查询验证，避免重复发帖。

### 帖子优化（图片透传）

优化含图片的帖子时：
- 先用 vision 工具查看图片内容，理解图片传达的信息
- 结合图片优化文案
- 将优化后的文案和原始图片链接一起传给接口
- **禁止修改图片链接**，原样透传

### 热议话题发帖

```bash
node scripts/openclaw.js publish-hot '{"user_id":12,"type":1,"hot_say_id":8,"title":"标题","message":"内容"}'
```

**必填参数**:
- `user_id`: 马甲 ID
- `hot_say_id`: 热议话题 ID（先查询热议话题列表）
- `title`: 帖子标题
- `message`: 帖子内容
- `type`: 帖子类型（查询帖子表获取，通常为 `1`）

---

## 3. 帖子编辑

**编辑前必须先向用户确认帖子类型**（普通贴还是活动贴）。

### 编辑帖子标题和内容

```bash
node scripts/openclaw.js update-thread --thread-id=1002 --title="新标题" --message="新内容"
```

**参数**:
- `--thread-id`: 帖子 ID（必填）
- `--title`: 新标题（可选）
- `--message`: 新内容（可选）
- 至少提供 `--title` 或 `--message` 之一

---

## 4. 马甲管理

### 新增马甲

```bash
node scripts/openclaw.js add-mark --names=["马甲A","马甲B"]
```

马甲头像由服务端从公共头像库随机分配。

### 编辑马甲昵称

```bash
node scripts/openclaw.js edit-mark --user=15 --nickname="新昵称"
```

---

## 5. 积分管理

### 批量增加积分

```bash
node scripts/openclaw.js add-integral --users=[12,13] --integral=5 --reason="活动奖励"
```

**参数**:
- `--users`: 用户 ID 数组（必填）
- `--integral`: 增加积分数（必填）
- `--reason`: 增加原因/备注（可选）

---

## 6. 用户互动

### 批量发送站内信

```bash
node scripts/openclaw.js station-mail --users=[12,34,56] --message="这是一条社区通知"
```

- `--users` 必须是 JSON 数组格式，单用户写成 `[12]`
- `--message` 必须使用 UTF-8 字符集

### 获取帖子点赞列表

```bash
node scripts/openclaw.js thread-likes <thread_id> [page] [page_size]
```

---

## 7. 标签管理

### 获取标签列表

```bash
node scripts/openclaw.js label-list
```

返回当前圈子所有标签，包含系统标签和口碑圈标签。

### 查看用户标签

```bash
node scripts/openclaw.js user-labels <user_id>
```

### 查看标签下的用户

```bash
node scripts/openclaw.js label-users <label_id> [page] [page_size]
```

### 给用户打标签

按已有标签 ID 打标（仅口碑圈标签可手动打标）:
```bash
node scripts/openclaw.js set-label --user=12 --label-id=8
```

按标签名称打标（标签不存在则自动创建口碑圈标签）:
```bash
node scripts/openclaw.js set-label --user=12 --label-name="高价值用户"
```

---

## 8. 资源上传

### 生成图床上传链接

```bash
node scripts/openclaw.js upload-page
```

在浏览器中打开返回的链接上传图片/视频，上传完成后回复 AI 获取资源地址。

### 获取已上传的资源

```bash
node scripts/openclaw.js upload-resource <upload_id>
```

### 直接上传文件

```bash
node scripts/openclaw.js upload-image ./image.jpg
node scripts/openclaw.js upload-video ./video.mp4
```

---

## 错误处理

命令执行失败时，向用户说明"操作出错了，请稍后重试"，禁止暴露服务端接口信息或原始错误详情。
