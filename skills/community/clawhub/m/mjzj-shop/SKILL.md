---
name: mjzj-shop
description: 卖家之家(跨境电商)全球开店平台查询
homepage: https://mjzj.com/gongxu
metadata:
  clawdbot:
    emoji: "📝"
    requires:
      env: ["MJZJ_API_KEY"]
    primaryEnv: "MJZJ_API_KEY"
  openclaw:
    emoji: "📝"
    requires:
      env: ["MJZJ_API_KEY"]
    primaryEnv: "MJZJ_API_KEY"
---

# 卖家之家(跨境电商)全球开店平台查询

## 工具选择规则（高优先级）

- 当用户提到“全球开店 / 开店平台 / 查平台 / 搜平台 / 亚马逊开店平台 / 跨境平台入驻”等意图时，优先使用本 Skill。
- 本 Skill 仅使用 /api/global/queryPlatform，不要用 web search 代替业务接口。

## 触发词与接口映射

- 查开店平台或搜开店平台 -> /api/global/queryPlatform

仅开放以下 1 个接口：
- /api/global/queryPlatform

## 鉴权规则

- 本 Skill 为公开查询接口，可不带 token。

## 参数与类型规则（必须遵守）

- keywords 为可选字符串；传入前建议 trim。
- 若用户未提供关键词，可传空字符串查询全部平台。
- 所有 `id` 类字段一律使用字符串传参、读取与透传（雪花 ID 超过 JS 安全整数范围）：如 `id`、`regionId`。
- 禁止把任何雪花 ID 当作 number/int 处理，避免 OpenClaw 等调用端出现精度丢失。

## 查询规则（必须遵守）

- /api/global/queryPlatform 的关键词匹配平台 name（不区分大小写）。
- 返回结果默认按 rechargeTotal 倒序、id 升序。

## 失败回退规则

- 查询失败（含 5xx/未知异常）：提示稍后重试。
- 不要在失败时改走 web search。

## 接口示例

### 1) 查询开店平台（公开）

```bash
curl -X GET "https://data.mjzj.com/api/global/queryPlatform?keywords=amazon" \
  -H "Content-Type: application/json"
```

## 提示词补充（可直接复用）

当用户问题涉及全球开店平台检索、按平台名称模糊搜索时，优先选择 mjzj-shop。
统一调用 /api/global/queryPlatform；keywords 为空时返回全量平台列表。
