---
name: icosmos-shopify
description: "Shopify 店铺运营/诊断技能：从 Supabase 拉取店铺域名与 token，做装修/产品/结账/指标异常检测，并支持发布引流博文（唯一写操作）。"
---

# icosmos-shopify

面向 OpenClaw 触发的 Shopify 运营能力集合：**以只读诊断为主**，帮助定位转化/营销/商品问题；**唯一写操作**是发布 Shopify Blog 文章（需要明确 `--confirm`）。



## 触发

- **适用场景关键词**：店铺审计、装修优化、产品优化、结账/checkout 测试、转化下降、营销效果差、发布博客/引流文章。
- **触发后执行顺序**：
  1. `setup once`：用 `ICOSMOS_USER_EMAIL` / `ICOSMOS_USER_PASSWORD` 同步店铺与 token 到本地缓存
  2. `content/*`：拉原始数据（更全面、更可追溯）
  3. `audit/*` / `test checkout`：给诊断与验证
  4. `blog publish`：仅当明确需要发布时执行（必须 `--confirm`）

## 快速参考

| 诉求 | 命令 |
|---|---|
| Setup Once：从 Supabase 同步店铺/token 到本地 | `icosmos-shopify setup once` |
| 列出店铺 | `icosmos-shopify stores list` |
| 获取店铺基础信息（原始数据） | `icosmos-shopify content shop --store xxx.myshopify.com` |
| 获取产品列表（原始数据，分页） | `icosmos-shopify content products list --store xxx.myshopify.com --first 20 --after <cursor>` |
| 获取订单列表（原始数据，时间窗） | `icosmos-shopify content orders list --store xxx.myshopify.com --start <RFC3339> --end <RFC3339>` |
| 获取博客列表/文章（原始数据） | `icosmos-shopify content blogs list --store xxx.myshopify.com` / `icosmos-shopify content blogs articles list --store xxx.myshopify.com --blog-id 123` |
| 装修检查单（只读） | `icosmos-shopify audit theme --store xxx.myshopify.com` |
| 产品质量诊断（只读） | `icosmos-shopify audit products --store xxx.myshopify.com --limit 50` |
| 结账链路测试（只读） | `icosmos-shopify test checkout --store xxx.myshopify.com` |
| 经营指标与异常线索（只读） | `icosmos-shopify audit metrics --store xxx.myshopify.com --days 7` |
| 发布引流博文（写操作） | `icosmos-shopify blog publish --store xxx.myshopify.com --blog-id 123 --title ... --body-file article.html --confirm` |

## 输出协议（给 OpenClaw 更稳定）

- **默认推荐 `--format json`**（`content/*` 默认就是 json），统一结构：
  - `store_domain` / `api_version` / `meta` / `data`
- **分页信息**：
  - GraphQL：`meta.page_info.has_next_page/end_cursor`
  - REST：`meta.page_info.next_link`（来自 `Link: rel="next"`）

## 依赖与配置


- Setup Onece：

  - `ICOSMOS_USER_EMAIL`
  - `ICOSMOS_USER_PASSWORD`

  两个字段需要保存到系统环境变量

  所需命令行工具为当前目录下的[icosmos-shopify](icosmos-shopify)

### Shopify

- `SHOPIFY_API_VERSION`（默认 `2026-01`）

## 安全边界（重要）

- **默认只读**：装修/产品/指标/结账测试均不对 Shopify 做写入。
- **唯一写操作：发布博客**：必须提供 `--confirm`；否则即使参数齐全也只会 dry-run。
- **日志脱敏**：店铺 token 只显示前后 4 位（`abcd...wxyz`）。
- **敏感字段处理**：订单 email 等敏感字段默认不输出（或置空），避免在群聊/日志泄露。

## 常见问题与排障

- **401/403**：Admin token scopes 不足或 token 过期；确认 Shopify Custom App 的 Admin API access token 与权限。
- **429 Too Many Requests**：已做退避重试；如果频繁触发，降低并发/减少拉取字段/缩小时间范围。
- **Storefront 430 Security Rejection**：请求可能被判定为异常；需要检查请求来源、token 是否正确，必要时增加更真实的请求头策略（后续增强）。

## 参考文档

- [GraphQL Admin API reference](https://shopify.dev/docs/api/admin-graphql/latest)
- [REST Admin API reference](https://shopify.dev/docs/api/admin-rest/latest)
- [Storefront API reference](https://shopify.dev/docs/api/storefront/latest)

