# 记忆模板

## 记忆条目格式

```json
{
  "id": "mem_YYYYMMDD_HHMMSS",
  "content": "记忆内容（简洁表述，≤100 字）",
  "category": "preference|fact|decision|task|contact|skill|project|other",
  "importance": 75,
  "source": "对话摘要或来源",
  "timestamp": "2026-03-31T15:30:00+08:00",
  "tags": ["标签 1", "标签 2", "标签 3"],
  "related": ["mem_xxx", "mem_yyy"],
  "reviewAt": "2026-04-07",
  "expiresAt": null,
  "metadata": {
    "sessionId": "xxx",
    "userConfirmed": false,
    "autoEncoded": true
  }
}
```

## 分类说明

| 分类 | 说明 | 示例 |
|------|------|------|
| preference | 用户偏好 | 喜欢蓝色、不喜欢太甜的咖啡 |
| fact | 事实信息 | 住在杭州、GitHub 用户名 |
| decision | 重要决策 | 选择 X 方案、放弃 Y 功能 |
| task | 任务/日程 | 明天开会、下周出差 |
| contact | 联系人信息 | 邮箱、电话、社交账号 |
| skill | 技能/能力 | 会 Python、熟悉 React |
| project | 项目信息 | 项目名称、目标、进度 |
| other | 其他 | 无法归类的重要信息 |

## 重要性评分参考

| 分数 | 含义 | 存储位置 |
|------|------|---------|
| 90-100 | 核心记忆，永不遗忘 | COLD（永久） |
| 70-89 | 重要记忆，长期保存 | COLD |
| 50-69 | 中等重要，定期复习 | WARM |
| 30-49 | 短期记忆，用完即清 | HOT |
| <30 | 不重要，直接遗忘 | 不保存 |

## 标签建议

- 保持 3-5 个标签
- 使用小写，下划线分隔
- 示例：`coffee_preference`, `hangzhou_location`, `github_account`
