---
name: memo-collect
description: This is a simple skill for note-taking, used to quickly record user notes, and provide users with query, delete, and other capabilities.
---

# Memo Collect Skill

这是一个简单的备忘技能，用于快速记录用户的备忘信息，同时提供给用户查询，删除等能力

## 使用方式

运行：

node dist/index.js <action> <content>

## action 类型

add_memo
添加备忘

示例：
node dist/index.js add_memo "买牛奶"

---

list_memo
查看所有备忘

示例：
node dist/index.js list_memo

---

delete_memo
删除备忘

示例：
node dist/index.js delete_memo 3

---


## Agent 调用规则

如果用户说：

- 记录一下这个内容：XXX
- 帮我将如下信息加入到备忘录：XXX
- 我要记录备忘：XXX

调用：

node dist/index.js add_memo "XXX"

---

如果用户说：

- 查询我已有的备忘
- 查询我的备忘记录
- 查询备忘

调用：

node dist/index.js list_memo

---

如果用户说：

第3条备忘完成了

调用：

node dist/index.js delete_memo 3

---