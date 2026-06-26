---
name: ideas
description: 记录日常奇思妙想、灵感片段、技术创意。支持按主题分类、状态追踪、关键词搜索。
triggers: 想了个主意, 灵感, 创意, 记一下, 这个想法, 有个念头, 发现, 想法
version: 1.0.0
author: Akira
license: MIT
---
# ideas v1.0 - 奇思妙想记录

## 数据文件（存放于 `~/.openclaw/workspace/ideas-data/`）
- `~/.openclaw/workspace/ideas-data/ideas.json` — 创意记录列表

## 数据格式
```json
{
  "ideas": [
    {
      "id": "uuid",
      "content": "想法内容",
      "tags": ["标签1", "标签2"],
      "status": "pending | in_progress | done | dropped",
      "created_at": "YYYY-MM-DDTHH:mm:ss",
      "updated_at": "YYYY-MM-DDTHH:mm:ss"
    }
  ]
}
```

## 操作
1. **记录想法**：解析内容 → 提取标签 → 生成 ID → 追加到 ideas.json → 反馈已记录
2. **查看列表**：读取 ideas.json → 按时间倒序展示 → 支持筛选 pending/in_progress/done
3. **搜索想法**：按关键词搜索 content 和 tags
4. **更新状态**：找到对应想法 → 更新 status 和 updated_at
5. **删除想法**：软删除（标记 status 为 dropped）或彻底删除

## 状态说明
- `pending` — 待处理（默认）
- `in_progress` — 进行中
- `done` — 已完成
- `dropped` — 已放弃

## 标签建议
技术、生活、产品、学习、投资、健康等

## 注意事项
- 每个想法单独一条，content 尽量完整记录原始念头
- tags 自动提取或用户补充
- 按时间倒序展示，最新的在最前面
