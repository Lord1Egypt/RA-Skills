---
name: huo15-mem / 火一五记忆
version: 1.0.0
description: 【版权：青岛火一五信息科技有限公司 账号：huo15】火一五记忆管理系统，按企微用户分类存储个人和公有记忆
author: Xun
tags: [记忆, 用户, 分类, 火一五]
---

# huo15-mem - 火一五记忆管理系统

按企微用户（chat_id）自动分类存储记忆。

## 解决的问题

- 个人记忆 vs 公有记忆混在一起
- 多用户记忆无法隔离
- 管理员无法按用户清理记忆

## 目录结构

```
memory/
├── shared/           # 公有记忆（所有用户共享）
│   └── MEMORY.md
├── default/          # 默认用户
│   └── MEMORY.md
├── xun/              # Xun 个人记忆
│   └── MEMORY.md
├── ZhaoBo/           # 赵博个人记忆
│   └── MEMORY.md
└── {其他用户}/
    └── MEMORY.md
```

## 激活条件

对话结束或用户说"记住xxx"时触发。

## 判断逻辑

| 内容类型 | 存储位置 |
|----------|----------|
| 个人偏好/习惯 | `memory/{user}/MEMORY.md` |
| 个人决策/总结 | `memory/{user}/MEMORY.md` |
| 公司/项目知识 | `memory/shared/MEMORY.md` |
| 多人经验总结 | `memory/shared/MEMORY.md` |
| 技能使用经验 | `memory/shared/MEMORY.md` |

## 存入格式

### 个人记忆
```markdown
# Xun 的记忆

- 偏好简洁回复风格
- 喜欢用语音讲故事
```

### 公有记忆（必须标注来源）
```markdown
# 公有记忆

## Xun存入
- 技能 file-organizer-zh 已安装

## 赵博存入
- 常用数字人 Avatar ID: b2f84d86855349b6af0d0920f6597ec8
```

## 管理员清理

按用户清理公有记忆：
```bash
# 搜索某用户的公有记忆
grep -n "## Xun存入" memory/shared/MEMORY.md

# 删除某用户的公有记忆（需要保留其他用户内容）
# 手动编辑或写脚本按章节删除
```

## 启动时加载

根据 `chat_id` 加载对应用户的记忆：
- chat_id = "Xun" → 加载 `memory/xun/MEMORY.md`
- chat_id 不存在 → 加载 `memory/default/MEMORY.md`
- 同时加载 `memory/shared/MEMORY.md`（公有）

## 使用示例

- "记住我喜欢语音回复" → 存入个人记忆
- "这是所有人的经验" → 存入公有记忆，标注来源
- "整理工作区" → 不存记忆
