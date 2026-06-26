# Memo Collect Skill

简单的备忘录 OpenClaw Skill。用于快速记录、查询、删除备忘信息。

## 功能特性

- 添加备忘（自动记录时间戳）
- 查看所有备忘列表
- 按编号删除备忘

## 使用

```bash
# 添加备忘
pnpm start add_memo "买牛奶"

# 查看备忘列表
pnpm start list_memo

# 删除第 N 条备忘
pnpm start delete_memo 3
```

## 数据存储

备忘记录保存在 `~/memo-knowledge/db.json`。

## 依赖

无第三方依赖，仅使用 Node.js 内置模块。
