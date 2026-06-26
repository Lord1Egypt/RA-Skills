---
name: contacts
version: "1.0.3"
description: 通讯录查询与维护技能。用于查找联系人信息（open_id、chat_id、account_id 等）、记录新联系人、或查询历史沟通偏好。触发时机：(1) 需要 @某人或向某渠道发消息时 (2) 认识新联系人后需要录入通讯录时 (3) 查询某人的联系方式或交流偏好时 (4) 询问"谁知道xxx的飞书ID"或"怎么联系xxx"时。
---

# Contacts Skill — 通讯录技能

> 记录联系人沟通方式与交流规范，让 Agent 每次联系人都能查表办事，不用靠猜。

## 核心原则

- **每个 Agent 自行维护**自己的通讯录，不共享
- **脱敏信息**：只记录沟通相关字段，不记录敏感个人信息
- **YAML 格式**：方便程序读取查询，不用正则匹配 Markdown
- **自动维护**：认识新联系人后自然录入，不需要人工干预
- **Skill 不含数据**：实际联系人数据放在 Agent 的 `memory/contacts/` 下，Skill 仅描述格式与规范

## 通讯录位置

```
memory/contacts/
├── contacts.d/              # 联系人卡片目录
│   └── <contact_id>.yaml   # 每个联系人一个 YAML 文件
├── channels/                # 渠道最佳实践
│   └── feishu.md           # 飞书交流规范
└── schema.md               # 联系人数据 Schema 说明
```

## 联系人卡片格式

每个联系人在 `contacts.d/` 下有一个 YAML 文件，文件名即 `contact_id`（内部唯一标识）。

### 必需字段

```yaml
contact_id: "unique_id"      # 内部唯一标识（如 mala, zero-producer）
name: "通用名称"              # 内部通用名字

channels:
  feishu:
    open_id: "ou_xxx"       # 飞书 open_id（用于 @ 路由）
    nickname: "群名片"        # 飞书群里的显示名
    chat_id: "oc_xxx"       # 所在群 chat_id
    account_id: "账号名"      # message 工具发送时用的 accountId
```

### 可选字段

```yaml
internal:
  agent_id: "agent_name"     # OpenClaw agent ID（如与 contact_id 不同）
  role: "职责"               # 角色
  project: "项目"             # 所属项目

preferences:
  preferred: "feishu"        # 首选渠道
  language: "中文"
  formality: "随意"          # 沟通风格

context:
  met_via: "认识途径"
  collaboration: "合作项目"
  history: "历史记录"

notes:
  - "踩过的坑"
```

### 字段说明

| 字段 | 必须 | 说明 |
|------|------|------|
| `contact_id` | ✅ | 内部唯一标识 |
| `name` | ✅ | 内部通用名称 |
| `channels.feishu.open_id` | ✅ | 飞书 open_id，@ 时用 |
| `channels.feishu.nickname` | ✅ | 飞书群里的显示名，@ 时填这个 |
| `channels.feishu.chat_id` | ✅ | 所在群 chat_id |
| `channels.feishu.account_id` | ✅ | message 工具的 accountId 参数 |
| `internal` | ❌ | 内部身份信息 |
| `preferences` | ❌ | 沟通偏好 |

## 查询方法

```bash
# 查单个联系人
cat memory/contacts/contacts.d/mala.yaml

# 按名字搜索
grep -rl "name:" memory/contacts/contacts.d/ | xargs grep -l "小龙虾"

# 或使用脚本（需要先将 skills/contacts/scripts/ 加入 PATH）
list.sh              # 列出所有联系人
search.sh <名字>      # 按名字搜索
get.sh <contact_id>   # 查看单个联系人详情
```

## 新增联系人流程

1. 认识新联系人（通过对话、任务协作等）
2. 在 `memory/contacts/contacts.d/` 下创建 `<contact_id>.yaml`
3. 填写沟通相关字段（类型、渠道地址、交流偏好）
4. 如果是 Agent，记录其 Agent ID 和职责

## 维护规则

- 每次成功联系某人后，如发现新的沟通偏好，更新卡片
- 踩过的坑（如"此人不喜欢直接打电话"）及时补充到 `notes`
- 至少每月检查一次卡片，过时信息清理

## 已有联系人（示例）

| contact_id | 名字 | 飞书昵称 | 类型 |
|------------|------|---------|------|
| mala | 麻辣小龙虾 | 麻辣小龙虾 | Agent |
| main | 小爪子 | 龙虾养殖厂代表 | Agent |
| ... | | | |
