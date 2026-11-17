---
name: linkfox-1688-sourcing
display_name: Linkfox 1688货源
display_name_en: LinkFox 1688 Sourcing
description: 1688 货源一站式 AI 工具集，整合商品搜索、热销榜单、以图搜图与已授权采购履约，覆盖找货、选品、比价、图搜同款与下单全流程。
description_zh: 1688 货源一站式工具集：店雷达商品搜索与热销榜单（关键词/链接/ID 检索、周榜月榜、多维筛选排序、批发价/代发价/销量与供应商资质）、1688 以图搜图（图片 URL/Base64/imageId 视觉检索同款货源，含本地图片上传）、1688 已授权采购全流程（OAuth 授权检查、SKU/收货地址、下单预览、创建订单、支付链接、订单状态、物流轨迹、取消订单、确认收货）。当用户需要 1688 找货源、找供应商、批发选品、热销榜单、以图找同款、跨境找工厂或已授权采购下单与物流跟踪时触发。各子能力完整参数见 references/ 对应文件，脚本见 scripts/。
description_en: One-stop 1688 sourcing AI toolkit: store-radar product search and bestseller billboards (keyword/URL/ID retrieval, weekly/monthly rankings, multi-dimensional filters and sorting, wholesale/dropship price, sales and supplier qualifications), 1688 image search (visual retrieval of same-style sourcing by image URL/Base64/imageId, with local image upload), and end-to-end authorized 1688 procurement (OAuth checks, SKU/address, order preview, order creation, payment URL, order status, logistics tracking, cancellation, receipt confirmation). Triggered when the user needs 1688 sourcing, supplier discovery, wholesale product selection, bestseller rankings, image-based same-product search, cross-border factory sourcing, or authorized 1688 procurement ordering and logistics tracking. Full params per sub-capability are in references/, executable scripts in scripts/.
category: e-commerce
version: 1.0.0
author: LinkFox
---

# Linkfox 1688货源（1688 Sourcing）

1688 货源一站式 AI 工具集，整合 **3 类底层工具、4 项子能力**，覆盖货源搜索与热销榜单、以图搜图、已授权采购履约。各子能力完整参数、响应字段与错误码见 `references/` 下对应文件，可执行脚本见 `scripts/`。

## 能力边界

### ✅ 能力范围
- **货源搜索与榜单（`1688_sourcing`）**：商品搜索（`linkfox-dld-product-search`，按关键词/商品链接/商品 ID 检索 1688 批发商品，近 7 天/30 天销量周期，按价格/销量/销售额/上架时间排序，按公司类型/卖家会员/发货时间/代发权益/面单支持等筛选）、商品热销榜单（`linkfox-dld-product-billboard`，周榜/月榜，按销售笔数/销售额/销量排序，发现爆款与趋势货源）。返回批发价、代发价、销售笔数/件数、预估销售额、起批量、供应商资质、店铺与商品链接等。
- **以图搜图（`1688_search_by_image`）**：1688 以图搜图（`linkfox-1688-search-by-image`，通过图片 URL/Base64/imageId 视觉检索外观相似或同款货源），返回标题、批发价、代发价、月销量、起批量、复购率、交易评分、商家身份（超级工厂/实力商家/诚信通）等；支持价格/筛选（1688 严选/认证工厂/发货时效/品质退款率等）/排序/分页；本地图片先用 `upload_image.py` 上传获取公网 URL（有效期 24h）。
- **采购履约（`1688_procurement`）**：1688 采购全流程（`linkfox-1688-procurement`），覆盖 OAuth 授权检查与发起授权、SKU/规格与收货地址查询、下单预览、创建订单、获取支付链接、订单状态、物流概览与物流轨迹、取消订单、确认收货。除授权类操作外每个 endpoint 前自动校验当前用户 ACTIVE 且未过期的 1688 授权；高风险写操作（创建订单/支付链接/取消订单/确认收货）需用户单独中文确认后由 Agent 注入对应 boolean 安全字段。
- 数据平台均为中国大陆 1688 批发平台（阿里巴巴国内 B2B 市场），无多站点概念。

### ❌ 边界与限制
- **API Key 必需**：所有工具均需环境变量 `LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`）；各工具独立计费、独立限频。
- **计费约束**：商品搜索/热销榜单固定计费（成功约 9 积分/18000 token），以图搜图固定计费（约 4.5 积分/9000 token），采购履约各操作消耗积分；同一会话同一参数组合默认只调用一次（搜索/榜单/图搜脚本带 24h 本地缓存）；失败、空结果、参数不全或授权不足不得自动换关键词、翻页或连续试探；需继续检索时先向用户说明会产生额外消耗（各工具计费规则见 `skills-version.json` 对应条目与 references 内 api.md）。
- **采购授权前置**：采购类操作依赖当前用户已授权的 1688 OAuth；无 ACTIVE 授权时不调用目标 endpoint；高风险写操作失败不自动重试；不向用户索要 1688 token/refresh token/callback code/app secret。
- **不在范围内**：Amazon/TikTok/沃尔玛等其他平台选品（用对应平台技能）；Alibaba.com 国际站数据；1688 店铺级分析（店铺流量/排名/评分）；商品评论分析；价格历史与趋势分析；图片生成或编辑；物流成本计算与货代；实时库存与订单系统对接；与供应商或平台的直接沟通。
- **数据时效**：商品搜索/榜单为店雷达分析数据（7 天/30 天/周榜近 90 天/月榜近 12 个月）；以图搜图为实时搜索、不入库、无法二次 SQL 处理；采购履约为依赖 OAuth 的实时接口。

## 工具选择指南

按需求在下表定到子能力，再跳到【业务需求路由速查】查端点/脚本/references 取参执行。

| 需求 / 用户说 | 默认推荐（子能力） | 何时换用其他 |
|---|---|---|
| 关键词找 1688 货源 / 找供应商（"1688 上找 XX 货源"） | `linkfox-dld-product-search`（关键词搜索，7/30 天销量） | 要看周/月排行榜用 `linkfox-dld-product-billboard`；有图片找同款用 `linkfox-1688-search-by-image` |
| 1688 什么好卖 / 趋势 / 热销榜（"1688 热销榜""什么火"） | `linkfox-dld-product-billboard`（周榜/月榜排名） | 要按关键词实时搜 + 销量筛选用 `linkfox-dld-product-search` |
| 用图片找 1688 同款 / 以图搜图（"用图找货源""找同款"） | `linkfox-1688-search-by-image`（唯一图搜，需图片 URL） | 本地图片先 `upload_image.py` 上传换公网 URL；要按关键词文本搜索用 `linkfox-dld-product-search` |
| 按商品 ID / 商品链接查 1688 商品 | `linkfox-dld-product-search`（支持 `goodsUrl`/`productIds`） | 仅按 ID 查榜单商品也可用 `linkfox-dld-product-billboard` |
| 工厂直供 / 超级工厂 / OEM 供应商（"找工厂""顶级工厂"） | `linkfox-dld-product-search`（`companyType=2`/`shiLiType=superFactory`） | 要榜单里的工厂货用 `linkfox-dld-product-billboard` |
| 1688 一件代发货源（"一件代发""支持代发"） | `linkfox-dld-product-search`（`proxyRights=4360897`） | 要榜单代发货用 `linkfox-dld-product-billboard` |
| 跨境货源 / 出口商品（"跨境商品""1688 严选"） | `linkfox-dld-product-search`（`offerType=4`） | 要图搜跨境同款用 `linkfox-1688-search-by-image`（`filter=1688Selection`） |
| 1688 新品 / 最近上架（"新品""最近上的"） | `linkfox-dld-product-search`（`sortField=offerCreateTime`） | 要榜单新品用 `linkfox-dld-product-billboard`（`offerType=2`） |
| 对比供应商 / 跨供应商比价 | `linkfox-dld-product-search`（多维排序） | — |
| 查我的 1688 授权店铺（"我的 1688 授权"） | `linkfox-1688-procurement`（`authorized_stores.py`） | — |
| 生成 1688 授权链接（"授权 1688"） | `linkfox-1688-procurement`（`authorize_url.py`） | — |
| 查 offerId 的 SKU / 规格 / 起订量 / 库存 | `linkfox-1688-procurement`（`sku.py`） | 找 offerId 先用图搜或商品搜索 |
| 查 1688 收货地址 | `linkfox-1688-procurement`（`receive_address_list.py`） | — |
| 预览 1688 订单（"帮我预览订单"） | `linkfox-1688-procurement`（`order_preview.py`） | — |
| 1688 下单 / 获取支付链接（"确认下单""获取支付链接"） | `linkfox-1688-procurement`（`create_order.py`/`payment_url.py`，高风险需确认） | — |
| 查 1688 订单状态 / 物流 / 物流轨迹 | `linkfox-1688-procurement`（`order_status.py`/`logistics.py`/`logistics_trace.py`） | — |
| 取消 1688 订单 / 确认收货（"取消订单""确认收货"） | `linkfox-1688-procurement`（`cancel_order.py`/`confirm_receive.py`，高风险需确认） | — |

### 工具选择思路
- **重要**：多个子能力满足需求时，要依据需求深入分析子能力的功能、用途、出入参、从中调研出最合适的子能力，并推荐用户，让用户自己决定。
- 满足程度同等的前提下，向用户推荐"默认推荐子能力"。注意：找货/选品用搜索或榜单（`1688_sourcing`）或图搜（`1688_search_by_image`），已授权采购履约用 `1688_procurement`——前者只查货不交易，后者才可下单。

## 业务需求路由速查

按【工具选择指南】定到子能力后，下表查端点、脚本与 references 文件取参执行：

### 子能力 ↔ references 文件 ↔ 端点 ↔ 脚本（4 项）

**1688_sourcing**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-dld-product-billboard | references/linkfox-dld-product-billboard.md | POST /dld/productBillboard | dld_product_billboard.py |
| linkfox-dld-product-search | references/linkfox-dld-product-search.md | POST /dld/productSearch | dld_product_search.py |

**1688_search_by_image**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-1688-search-by-image | references/linkfox-1688-search-by-image.md | POST /alibaba1688/imageSearch | alibaba1688_image_search.py、upload_image.py（本地图片上传） |

**1688_procurement**
| 子能力 | references 文件 | 端点 | 脚本 |
|---|---|---|---|
| linkfox-1688-procurement | references/linkfox-1688-procurement.md | POST /alibaba1688/{operation} | 见下表（12 个操作脚本 + `_alibaba1688_common.py` 共享模块） |

**1688 采购操作明细（operation ↔ 脚本 ↔ 风险）**

| operation | 端点 | 脚本 | 风险 | 高风险确认字段 |
|---|---|---|---|---|
| authorizeUrl | POST /alibaba1688/authorizeUrl | authorize_url.py | 低（不需 ACTIVE 前置） | — |
| authorizedStores | POST /alibaba1688/authorizedStores | authorized_stores.py | 低（不需 ACTIVE 前置） | — |
| receiveAddressList | POST /alibaba1688/receiveAddressList | receive_address_list.py | 低（需 ACTIVE） | — |
| sku | POST /alibaba1688/sku | sku.py | 低（需 ACTIVE） | — |
| orderPreview | POST /alibaba1688/orderPreview | order_preview.py | 中（需 ACTIVE） | — |
| createOrder | POST /alibaba1688/createOrder | create_order.py | 高（需 ACTIVE） | `confirmCreateOrder=true` |
| paymentUrl | POST /alibaba1688/paymentUrl | payment_url.py | 高（需 ACTIVE） | `confirmGetPaymentUrl=true` |
| orderStatus | POST /alibaba1688/orderStatus | order_status.py | 低（需 ACTIVE） | — |
| logistics | POST /alibaba1688/logistics | logistics.py | 低（需 ACTIVE） | — |
| logisticsTrace | POST /alibaba1688/logisticsTrace | logistics_trace.py | 低（需 ACTIVE） | — |
| confirmReceive | POST /alibaba1688/confirmReceive | confirm_receive.py | 高（需 ACTIVE） | `confirmReceive=true` |
| cancelOrder | POST /alibaba1688/cancelOrder | cancel_order.py | 高（需 ACTIVE） | `confirmCancel=true` |

## 调用方式

- **网关**：`${LINKFOX_TOOL_GATEWAY}/<端点>`，请求方式 POST、Content-Type `application/json`，认证 Header `Authorization: <api_key>`（api_key 从环境变量 `LINKFOX_AGENT_API_KEY` 或 `LINKFOXAGENT_API_KEY` 读取；未配置按下方【解决认证和积分问题】处理）。各端点路径见上方【业务需求路由速查】与对应 references 文件（注意：商品搜索/榜单走 `/dld/` 前缀，图搜与采购走 `/alibaba1688/` 前缀）。
- **Python 脚本**：每项子能力对应 `scripts/<脚本名>.py '<JSON 参数>' [--inline]`（脚本名与端点见路由速查表）。采购类脚本另支持 `--payload-env PAYLOAD` / `--payload-file payload.json` / `--save` / `--no-save`（Windows 推荐用 `$env:PAYLOAD` 传参，见 references/linkfox-1688-procurement.md）；`upload_image.py` 用法为 `python scripts/upload_image.py /path/to/local/image.png`，返回公网图片 URL（`{"url": "..."}`，有效期 24h）。
- **输出策略**：商品搜索/榜单/图搜脚本**始终**将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/<skill>-<timestamp>.json`（`<cwd>` 为脚本执行时工作目录；`<session>` 取自 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）；响应体 ≤ 8 KB 落盘后完整打印到 stdout，> 8 KB 仅打印摘要（顶层字段、常见计数、最大列表长度 + 前 3 条样本）；加 `--inline` 强制全量打印（同样落盘）。采购类脚本略有不同：响应体 ≤ 8 KB 默认**不落盘**、直接把完整脱敏 JSON 打印到 stdout，> 8 KB 默认写入 `<writable-root>/linkfox/.../data/linkfox-1688-procurement-<operation>-<timestamp>.json` 并仅输出摘要；加 `--save`/`LINKFOX_SKILL_SAVE_RESPONSE=1` 强制保存，`--no-save`/`LINKFOX_SKILL_NO_SAVE=1` 禁止保存。
- **读数据建议**：先看 stdout 摘要判断是否足够；需要具体字段时优先用 `jq` 或 PowerShell `ConvertFrom-Json` 从保存的 json 文件按需抽取，避免整份 JSON 进入上下文。
- **完整参数**：每个子能力的请求参数、响应字段、错误码、curl 示例见 `references/<源skill>.md`（文件内含该子能力 SKILL.md 正文与 api.md 全文；采购另含 workflow.md 流程地图）。

## 使用示例

以下按数据层给出代表性子能力的出入参示例；其余子能力参数见对应 references 文件。1688 为中国大陆平台，价格币种为人民币（¥/CNY）。

### 货源搜索与榜单层

**1. 关键词商品搜索（1688_sourcing → dld_product_search.py）**
```json
{"keyWord": "瑜伽垫", "cycle": "30", "sortField": "saleCount30d", "sortType": "desc", "pageSize": 20}
```
出参：`products[]`（offerId/title/price/consignPrice/quantityBegin/salesOrderCount/salesQuantity/estimatedSalesAmount/company/shopId/shopUrl/asinUrl/imageUrl/deliveryTime/availableDate）、`total`、`costToken`。`keyWord`/`goodsUrl`/`productIds` 三选一；`cycle` 为 `7`/`30`。

**2. 商品热销榜单（1688_sourcing → dld_product_billboard.py）**
```json
{"keyWord": "手机壳", "pageType": 3, "date": "2026-03-01", "sortField": "orderCount", "sortType": "desc", "pageSize": 20}
```
出参：`products[]`（字段同上）、`total`、`dataType`（`monthlyData`=月榜/`weeklyData`=周榜）、`costToken`。`pageType=2` 周榜（`date` 传该周周日，近 90 天），`pageType=3` 月榜（`date` 传该月第一天，近 12 个月）。

### 以图搜图层

**3. 以图搜图（1688_search_by_image → alibaba1688_image_search.py）**
```json
{"imageUrl": "https://m.media-amazon.com/images/I/719mRAn2VrL._AC_SL1500_.jpg", "page": 1, "pageSize": 20, "filter": "1688Selection,totalEpScoreLv1", "sort": "{\"monthSold\":\"desc\"}"}
```
出参：`products[]`（offerId/title/price/consignPrice/salesQuantity/estimatedSalesAmount/quantityBegin/repurchaseRate/tradeScore/sellerIdentities/offerIdentities/sendGoodsAddressText/deliveryTime/isOnePsale/asinUrl/imageUrl）、`imageId`（分页回传加速）、`total`、`totalPage`、`costToken`。`imageUrl`/`imageBase64`/`imageId` 三选一；本地图片先 `upload_image.py` 上传换公网 URL。仅支持 png/jpg/jpeg。

### 采购履约层

**4. 授权检查（1688_procurement → authorized_stores.py）**
```json
{}
```
出参：当前 LinkFox 用户的 1688 授权店铺列表，每条含 `status`（需 `ACTIVE`）、`expired`（需 `false`）。有 ACTIVE 授权可继续采购，无则先 `authorize_url.py` 发起授权。

**5. SKU 查询（1688_procurement → sku.py）**
```json
{"offerId": "123456789"}
```
出参：SKU/规格、价格、起订量（MOQ）、库存。`offerId` 可由图搜或商品搜索结果获得。

**6. 下单预览（1688_procurement → order_preview.py）**
```json
{"offerId": "123456789", "quantity": 10, "addressId": "..."}
```
出参：商品/offerId、SKU/规格、数量、单价与商品总价、运费、收货地址、订单总额、买家留言、异常/库存/价格变化提示。预览失败则停止，不进入创建订单。具体入参以网关 schema 为准。

**7. 创建订单[高风险]（1688_procurement → create_order.py）**
```json
{"offerId": "123456789", "quantity": 10, "addressId": "...", "confirmCreateOrder": true}
```
出参：订单号与下单结果。用户单独中文确认后（如"确认创建这个订单"），Agent 在 payload 注入 boolean `confirmCreateOrder=true` 再调用；脚本本地拒绝缺少该字段的请求，失败不自动重试。支付链接（`payment_url.py`，需 `confirmGetPaymentUrl=true`）、取消订单（`cancel_order.py`，需 `confirmCancel=true`）、确认收货（`confirm_receive.py`，需 `confirmReceive=true`）同理各自独立确认。

## 展示规则

1. **客观呈现数据**：以清晰表格展示商品标题、批发价、代发价、销售笔数/件数、预估销售额、起批量、供应商资质等，不做主观商业建议（除非用户主动要求）。
2. **来源标注**：展示数据时说明来自店雷达商品搜索/热销榜单、1688 以图搜图还是 1688 采购履约。
3. **价格与销量口径**：价格须带币种（¥/CNY），并注明是批发价还是代发价；销量按 `dataType`/`cycle` 标明是周数据/月数据/7 天/30 天。
4. **采购展示**：依赖 OAuth 时先展示授权状态，不单凭浏览器跳转判断；下单预览清晰展示商品/SKU/数量/单价/运费/收货地址/订单总额/异常提示；`authorizedStores` 输出是当前用户授权状态，不要描述成数据库全库账号列表。
5. **高风险确认**：创建订单、获取支付链接、取消订单、确认收货前复述精确操作、关键 ID、金额/状态（如可得），请用户中文自然语言确认；不要求用户输入内部 boolean 字段（`=true` 由 Agent 注入）。
6. **不可用数据**：值为 `0` 或 `-1` 的字段表示数据不可用，标注"N/A"或省略，不作实际值展示。
7. **敏感信息**：永不展示完整 API key、JWT、access token、refresh token、callback code、app secret、session key、Authorization header；收货地址展示到足以安全选择即可，避免不必要重复完整手机号或敏感细节。
8. **错误处理与协同**：查询失败时根据响应 `errcode`/`errmsg` 说明原因并建议修正（关键词需中文、日期格式、ASIN/offerId 格式、授权不足等）；连续使用多工具时（如先图搜找 offerId 再采购下单）将各工具发现汇总为连贯分析，标注数据来源与时间窗；返回 `costToken` 等成本字段时如实展示。

## 解决认证和积分问题
发生以下异常情况时，采用 references/onboarding.md 引导解决问题：

**注意**：你是workbuddy，并且渠道是workbuddy，使用 onboarding 引导登录注册时 channel **必须**为 workbuddy。这非常重要！

### 异常情况
- **未配置API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应401或402状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。
