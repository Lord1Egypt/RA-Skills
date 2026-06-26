---
name: onebound-api
description: Search Taobao and 1688 products, and fetch product details, through the Onebound platform gateway.
license: MIT-0
user-invocable: true
metadata:
  openclaw:
    emoji: "\U0001F6D2"
    primaryEnv: ONEBOUND_API_KEY
    requires:
      env:
        - ONEBOUND_API_KEY
      bins:
        - curl
        - jq
---

# Onebound API

Provides four e-commerce data capabilities through the Onebound platform gateway:

1. **Taobao Keyword Search** - Search Taobao and Tmall products by keyword
2. **Taobao Item Detail** - Fetch detailed Taobao product data by item ID
3. **1688 Keyword Search** - Search 1688 products by keyword
4. **1688 Item Detail** - Fetch detailed 1688 product data by item ID

## Setup

Users should register on your Onebound platform, create a platform API key, and use that key with this skill.

Set these environment variables:

| Variable | Description | Example |
|---|---|---|
| `ONEBOUND_API_KEY` | Your platform API key | `ak_xxxxxxxxxxxx` |
| `ONEBOUND_BASE_URL` | Platform gateway base URL, optional | `https://onebound.vercel.app` |

## Workflow

### Taobao Keyword Search

Use when the user asks to search Taobao or Tmall products by keyword.

Run:

```bash
bash {baseDir}/scripts/taobao-item-search.sh "<keyword>" "<page>" "<page_size>" "<sort>" "<cat>"
```

- `keyword` - Search keyword, required
- `page` - Page number, optional, defaults to `1`
- `page_size` - Page size, optional, defaults to `10`
- `sort` - Sort mode, optional
- `cat` - Category ID, optional, defaults to `0`

Example:

```bash
bash {baseDir}/scripts/taobao-item-search.sh "女装"
bash {baseDir}/scripts/taobao-item-search.sh "蓝牙耳机" "1" "20"
```

### Taobao Item Detail

Use when the user asks to fetch Taobao product details by item ID.

Run:

```bash
bash {baseDir}/scripts/taobao-item-detail.sh "<num_iid>" "<is_promotion>"
```

- `num_iid` - Taobao item ID, required
- `is_promotion` - Whether to request promotion info, optional, defaults to `1`

Example:

```bash
bash {baseDir}/scripts/taobao-item-detail.sh "652874751412"
```

### 1688 Keyword Search

Use when the user asks to search 1688 products by keyword.

Run:

```bash
bash {baseDir}/scripts/alibaba-1688-item-search.sh "<keyword>" "<page>" "<page_size>" "<sort>" "<cat>"
```

- `keyword` - Search keyword, required
- `page` - Page number, optional, defaults to `1`
- `page_size` - Page size, optional, defaults to `40`
- `sort` - Sort mode, optional
- `cat` - Category ID, optional, defaults to `0`

Example:

```bash
bash {baseDir}/scripts/alibaba-1688-item-search.sh "女装"
bash {baseDir}/scripts/alibaba-1688-item-search.sh "围巾" "1" "40"
```

### 1688 Item Detail

Use when the user asks to fetch 1688 product details by item ID.

Run:

```bash
bash {baseDir}/scripts/alibaba-1688-item-detail.sh "<num_iid>" "<sales_data>" "<agent>"
```

- `num_iid` - 1688 item ID, required
- `sales_data` - Whether to include recent sales data, optional, defaults to `0`
- `agent` - Whether to include distribution pricing data, optional, defaults to `0`

Example:

```bash
bash {baseDir}/scripts/alibaba-1688-item-detail.sh "610947572360"
```

## Output Format

Scripts output results in Markdown format. Present the output directly to the user.

## OpenAPI Specification

For integration with OpenClaw, the gateway exposes the following OpenAPI Specification:

```yaml
openapi: 3.0.3
info:
  title: OneBound AI Skills API
  description: 提供淘宝(Taobao)和1688电商平台的商品数据检索与详情获取能力，专为AI Agent与OpenClaw技能设计。
  version: 1.0.0
  contact:
    name: API Support
    url: https://onebound.vercel.app

servers:
  - url: https://onebound.vercel.app/api/v1/proxy
    description: 生产环境网关

# 安全认证方式配置：要求用户提供 API Key (Bearer Token 格式)
security:
  - bearerAuth: []

paths:
  /taobao/item-search:
    get:
      summary: 淘宝商品关键词搜索
      description: 通过关键词搜索淘宝平台上的商品，支持分页。返回商品列表、价格、销量、主图等基础信息。
      operationId: searchTaobaoItems
      tags:
        - Taobao
      parameters:
        - name: q
          in: query
          description: 搜索关键词 (例如："女装", "iPhone 15")
          required: true
          schema:
            type: string
            maxLength: 100
        - name: page
          in: query
          description: 页码 (默认第1页)
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 1
      responses:
        '200':
          description: 搜索成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SearchResponse'
        '400':
          description: 请求参数错误 (例如缺少关键词)
        '401':
          description: API Key 缺失或无效
        '402':
          description: 账户余额不足
        '429':
          description: 请求过于频繁 (触发限流)

  /taobao/item-detail:
    get:
      summary: 淘宝商品详情获取
      description: 通过商品ID(num_iid)获取淘宝商品的详细信息，包括SKU属性、图文详情、库存状态等。
      operationId: getTaobaoItemDetail
      tags:
        - Taobao
      parameters:
        - name: num_iid
          in: query
          description: 淘宝商品唯一数字ID (例如："652874751412")
          required: true
          schema:
            type: string
            pattern: '^\d+$'
      responses:
        '200':
          description: 获取详情成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DetailResponse'
        '400':
          description: 请求参数错误 (例如ID不是纯数字)
        '401':
          description: API Key 缺失或无效
        '402':
          description: 账户余额不足

  /1688/item-search:
    get:
      summary: 1688商品关键词搜索
      description: 通过关键词搜索阿里巴巴1688平台上的商品，适用于B2B采购比价场景。
      operationId: search1688Items
      tags:
        - 1688
      parameters:
        - name: q
          in: query
          description: 搜索关键词 (例如："批发水杯", "定制包装盒")
          required: true
          schema:
            type: string
            maxLength: 100
        - name: page
          in: query
          description: 页码 (默认第1页)
          required: false
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 1
      responses:
        '200':
          description: 搜索成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SearchResponse'

  /1688/item-detail:
    get:
      summary: 1688商品详情获取
      description: 通过商品ID(num_iid)获取1688商品的详细信息，包括起批量、阶梯价格、供应商信息等。
      operationId: get1688ItemDetail
      tags:
        - 1688
      parameters:
        - name: num_iid
          in: query
          description: 1688商品唯一数字ID (例如："610947572360")
          required: true
          schema:
            type: string
            pattern: '^\d+$'
      responses:
        '200':
          description: 获取详情成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DetailResponse'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: API_KEY

  schemas:
    SearchResponse:
      type: object
      properties:
        items:
          type: array
          description: 搜索到的商品列表
          items:
            type: object
            properties:
              title:
                type: string
                description: 商品标题
              price:
                type: number
                description: 商品价格
              pic_url:
                type: string
                description: 商品主图链接
              sales:
                type: integer
                description: 销量
              num_iid:
                type: string
                description: 商品ID (用于查询详情)
        gateway_request_id:
          type: string
          description: 网关请求流水号
        cost:
          type: number
          description: 本次调用扣费金额
        balance:
          type: number
          description: 账户剩余余额
          
    DetailResponse:
      type: object
      properties:
        item:
          type: object
          description: 商品详细信息
          properties:
            title:
              type: string
            price:
              type: number
            desc:
              type: string
              description: 图文详情 (HTML格式)
            skus:
              type: object
              description: 商品SKU信息与价格
        gateway_request_id:
          type: string
        cost:
          type: number
        balance:
          type: number
```

## Guardrails

- Always check that `ONEBOUND_API_KEY` is set before calling any script. If missing, tell the user to set it.
- Default to `https://onebound.vercel.app` when `ONEBOUND_BASE_URL` is not set.
- Never ask the user for upstream credentials when using this skill.
- Never fabricate product search or detail results. Always call the platform gateway.
- If a script returns an error, show the error message to the user.
- Do not expose the API key in output.
- For keyword search, make sure the keyword is meaningful and not empty.
- For detail queries, require a valid item ID before making the call.

## Failure Handling

- If the API returns a 401 error, the platform API key is invalid or expired. Ask the user to verify their credentials.
- If the API returns a 400 error, check the required parameters.
- If the API returns a 402 or a balance-related error, ask the user to recharge the platform balance.
- If the API returns a 500 error, it is a server-side issue. Suggest the user try again later.
- If the script exits with code 1, read the error message from stderr.
