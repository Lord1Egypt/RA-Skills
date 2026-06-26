---
name: loss-items-query
description: 查询 待复购商品/ 待购买商品 /资损品物品列表/商品补货，支持分页、状态、排序等参数。直接调用你的业务 HTTPS 接口。
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - LOSS_API_TOKEN
    primaryEnv: LOSS_API_TOKEN
---

# Loss Items 查询技能

## 能力
当用户说以下任意关键词时触发：
- “待复购商品/需要购买的复购商品 / 复购商品 / 待购买物品 / pending”
- “查询第几页的 loss items”
- “due remind 的物品”、“status=pending 的列表”等

## 执行逻辑（必须严格遵守）
1. 从用户消息中提取参数（默认值见下）：
   - page（默认 1）
   - size（默认 20）
   - status（默认 pending）
   - sort（默认 due_remind_at）
   - include_deleted（默认 false）

2. 执行本目录下的 `query_loss_items.py` 脚本，传入以上参数。

3. 把脚本返回的 JSON 转为自然语言总结回复用户（例如“共找到 12 条 pending 记录，第 1 页显示前 20 条...”）

## 示例对话
用户：查一下 哪些需要复购的商品
→ 调用 query_loss_items.py --status pending --page 1 --size 20
→ 回复：当前有 8 条待复购的商品，最新 due remind 时间是...

用户：看第 2 页的物品
→ 调用 query_loss_items.py --page 2
