---
name: linkfox-ehunt-shopify-store-query
version: 1.0.0
category: product-sourcing
description: 通过 EHunt Shopify 店铺查询（网关路由 `ehunt/shopify/storeQuery`）按多维度筛选独立站 Shopify 店铺（店名/域名、国家、创建年限、产品数、广告数、月访问量、月订单量、社媒粉丝等）。当用户提到 EHunt Shopify 店铺、Shopify 店铺分析、独立站店铺、Shopify seller、独立站竞品店铺、Shopify 月访问量、独立站广告库、shopify stores、Shopify store query 时触发。即使用户未写 EHunt，只要在 Shopify 独立站上找店铺、筛店铺数据或分析店铺表现，也应触发此技能。
---

# EHunt Shopify 店铺查询（`ehunt/shopify/storeQuery`）

在具备 LinkFox「第三方数据服务」MCP 时，对应网关路由 **`ehunt/shopify/storeQuery`** 调用（MCP 展示名：**Shopify 店铺查询**，确切工具名以当前环境下发的工具元数据为准）。鉴权与上游路由由网关处理；若响应含根级 `code` 字段，是否成功以实网为准。

## 要点

- **分页**：`page` 从 1 起；`pageSize` 默认 20、最大 100。
- **区间入参**：`*Min` / `*Max` 成对出现（产品数、广告数、月访问量、月订单量），组成上游区间。
- **店铺年限** `year`：1=最近 1 年、2=1~2 年、3=2~3 年、4=3 年以上。
- **排序**：`sortBy` 整数枚举（0=产品数,1=类目数,2=月访问量,3=FB 粉丝,4=Ins 粉丝,5=广告数,6=相关度,7=月订单数默认）；`orderBy` 为 `desc`（默认）/`asc`。
- **国家**：`country` 传国家代码（如 `US`、`CN`）。

## 脚本（可选）

命令行调试：`python scripts/ehunt_shopify_store_query.py '<JSON>'`（需 `LINKFOXAGENT_API_KEY`）。详见 [references/api.md](references/api.md) 末尾。

## 参考

入参/出参表见 [references/api.md](references/api.md)。

<!-- LF_LARGE_RESPONSE_BLOCK -->
## Handling Large Responses

To avoid overflowing the agent context, persist the response to disk and extract only the fields you need:

```
python scripts/response_io.py run --script scripts/ehunt_shopify_store_query.py --out-dir <DIR> '<params>'
python scripts/response_io.py read <file> --fields "<paths>"   # or --path "<JMESPath>"
```

> Pick `--out-dir` outside any git working tree (e.g. `/tmp/...` on Unix, `%TEMP%/...` on Windows). Persisted responses may contain PII, pricing, or auth-sensitive data — do not commit them. Files are not auto-deleted; clean up when the task is done.

`run` writes the full response to a file and emits only a schema preview + file path. `read` projects specific fields, with `--limit/--offset` for slicing and `--format json|jsonl|csv|table` for output.

**When to prefer this pattern** — apply your judgment based on the response characteristics, e.g.:
- High field count per record, or fields you don't need
- Batch/paginated results (multiple items per call)
- Long-text fields (descriptions, reviews, HTML, time series)
- Output reused across later steps rather than consumed immediately

For small, single-use responses, calling the main script directly is fine.

⚠️ The preview is a truncated schema + sample, not the full data. Any field-level decision must read from the persisted file via `read`.
<!-- /LF_LARGE_RESPONSE_BLOCK -->
