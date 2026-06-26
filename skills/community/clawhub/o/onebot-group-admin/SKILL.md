---
name: onebot-group-admin
description: QQ 群管理操作，通过 OneBot 11 API 实现群名修改、群公告、禁言、踢人、设置管理员、全员禁言等功能。当用户需要在 QQ 群中执行管理操作时使用，如修改群名、发公告、禁言某人、踢人、设置管理员等。
read_when:
  - 修改群名
  - 设置群公告
  - 禁言
  - 踢人
  - 设置管理员
  - 全员禁言
  - 群管理
  - QQ群管理
---

# OneBot 群管理

通过 `scripts/onebot-action.js` 调用 napcat 的 OneBot 11 API 执行群管理操作。

## 脚本路径

```
~/.openclaw/workspace/skills/onebot-group-admin/scripts/onebot-action.js
```

## 用法

```bash
node <脚本路径> <action> [key=value ...]
```

参数中的数字会自动转为整数，字符串不需要引号。含空格的值用双引号包裹。

## 常用操作

### 修改群名
```bash
node onebot-action.js set_group_name group_id=<群号> group_name="新群名"
```

### 发送群公告
```bash
node onebot-action.js _send_group_notice group_id=<群号> content="公告内容"
```
⚠️ 注意是 `_send_group_notice`（带下划线前缀），这是 napcat 扩展 API，标准 `send_group_notice` 不可用。

### 禁言成员（单位：秒，0为解除）
```bash
node onebot-action.js set_group_ban group_id=<群号> user_id=<QQ号> duration=600
```
- `duration=0` 解除禁言
- `duration=3600` 禁言1小时
- `duration=86400` 禁言1天
- `duration=2592000` 禁言30天

### 全员禁言
```bash
# 开启全员禁言
node onebot-action.js set_group_whole_ban group_id=<群号> enable=1
# 关闭全员禁言
node onebot-action.js set_group_whole_ban group_id=<群号> enable=0
```

### 踢出成员
```bash
node onebot-action.js set_group_kick group_id=<群号> user_id=<QQ号> reject_add_request=0
```
- `reject_add_request=1` 拒绝再次加群

### 设置/取消群管理员
```bash
# 设置管理员
node onebot-action.js set_group_admin group_id=<群号> user_id=<QQ号> enable=1
# 取消管理员
node onebot-action.js set_group_admin group_id=<群号> user_id=<QQ号> enable=0
```

### 设置群成员名片
```bash
node onebot-action.js set_group_card group_id=<群号> user_id=<QQ号> card="新名片"
```

### 设置群成员头衔
```bash
node onebot-action.js set_group_special_title group_id=<群号> user_id=<QQ号> title="头衔" duration=-1
```

### 设置群头像
```bash
node onebot-action.js set_group_portrait group_id=<群号> file="<图片路径>"
```
⚠️ API 名称是 `set_group_portrait`（go-cqhttp 扩展 API），不是 OneBot 11 标准的 `set_group_avatar`。Bot 需要管理员权限。
- `file` 支持本地路径（如 `/tmp/openclaw-onebot/xxx.png`）、`file://` 协议、`base64://` 协议、HTTP URL

### 撤回消息
```bash
node onebot-action.js delete_msg message_id=<消息ID>
```

### 获取群信息
```bash
node onebot-action.js get_group_info group_id=<群号>
```

### 获取群成员列表
```bash
node onebot-action.js get_group_member_list group_id=<群号>
```

### 获取群成员信息
```bash
node onebot-action.js get_group_member_info group_id=<群号> user_id=<QQ号>
```

## 注意事项

- 群号 > 100000000 时 OneBot 插件可能误判为用户 ID，脚本直接传数字即可
- Bot 需要对应的管理员权限才能执行这些操作
- 敏感操作（踢人、禁言）执行前应先确认
- 默认连接 `ws://127.0.0.1:13001`，可通过环境变量 `ONEBOT_WS_URL` 和 `ONEBOT_WS_TOKEN` 覆盖
