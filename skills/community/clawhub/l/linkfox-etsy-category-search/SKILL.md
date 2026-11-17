---
name: linkfox-etsy-category-search
description: Etsy 类目数据。可检索类目名称、id 与 parentIds，用于商品/店铺筛选的类目 id。当用户提到 Etsy 类目、Etsy category id、Etsy 类目树、Etsy品类查询、syncEtsyCategory、查询类目时触发。即使用户未提及工具名，只要在本地已同步的 Etsy 类目库里按关键词找类目 id，也应触发此技能。
---

# Etsy 类目检索

## 要点

- **必填**：`keyword`（子串匹配类目名称、类目 id、`parentIds`）。
- **分页**：`page` 从 1 起；`pageSize` 默认 50、最大 200。
- 返回的 **`id`** 可作为 Etsy商品搜索 / 店铺侧 `category` 等入参的类目标识（与具体工具 schema 一致即可）。

## 脚本（可选）

命令行调试：`python scripts/etsy_category_search.py '<JSON>'`（需 `LINKFOXAGENT_API_KEY`）。详见 [references/api.md](references/api.md) 末尾。

## 参考

入参/出参表见 [references/api.md](references/api.md)。

## 解决认证和算力问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示算力或余额不足**：消息含"算力余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

## 算力消耗规则

不消耗算力。
