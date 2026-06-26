# Contact Schema

## 目录结构
```
memory/contacts/
├── contacts.d/          # 联系人卡片目录
│   └── <contact_id>.yaml
├── channels/           # 渠道最佳实践
│   └── feishu.md
└── schema.md           # 本文件
```

## 字段定义

| 字段 | 类型 | 必须 | 说明 |
|------|------|------|------|
| contact_id | string | ✅ | 唯一标识 |
| name | string | ✅ | 通用名称 |
| channels.feishu.open_id | string | ✅ | 飞书 open_id |
| channels.feishu.nickname | string | ✅ | 群名片 |
| channels.feishu.chat_id | string | ✅ | 群 ID |
| channels.feishu.account_id | string | ✅ | message 工具用 |
| internal.agent_id | string | ❌ | agent ID |
| internal.role | string | ❌ | 角色 |
| preferences.preferred | string | ❌ | 首选渠道 |
| preferences.language | string | ❌ | 语言 |
| preferences.formality | string | ❌ | 沟通风格 |
