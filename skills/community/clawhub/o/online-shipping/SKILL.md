---
name: xdcc-price-query
version: 6.0.1
display_name: 小递查查寄件比价、在线下单与寄件管理
display_name_en: Xdcc Shipping Quote, Order & Management
description: 寄件一条龙技能——登录 xdccy.com 后按发件/收件的省市区与重量，一次性列出多家快递公司的预估运费并比价；确认后可直接在线下单取件。支持把一整段「姓名+电话+地址」文本智能识别成省市区、详细地址与联系电话（对应官网 AddrRecognition 页）。还能查看「我的寄件」列表、查订单详情、取消未取件的寄件，以及提交与查看工单（含拦截转寄/退回），对应官网 DeliveryManage.aspx 与根目录 AddWorkPage/WorkOrderManage 页。支持单条与批量（CSV 输入输出），报价按价格升序展示并导出 JSON/CSV。地址支持口语化输入（"广东 深圳 南山"、"深圳南山"、"北京朝阳"），快递渠道支持中文名（"顺丰"）、通用缩写（SF）与接口编码（shunfeng）三种写法；省市区数据随包分发、运行时零网络依赖。下单默认仅预览，必须显式确认才提交；取消寄件与提交工单同样默认预演。
description_zh: 登录小递查查后按省市区+重量查多家快递报价并比价，确认后在线下单取件；还可查我的寄件、取消未取件订单、提交与查看工单。支持单条/批量、按价格升序、导出 JSON/CSV、中文渠道名与取件时段选择。
description_en: After logging into xdccy.com, quote and compare shipping prices across couriers by route and weight, place a pickup order online, list your shipments, cancel not-yet-picked-up ones, and file/track support work orders. Single/batch, sorted by price, JSON/CSV export, Chinese courier names, pickup-slot selection.
agent_created: true
---

# 小递查查 · 寄件比价、下单与管理

> 📌 **全文示例已脱敏**：示例里的姓名（张三 / 李四）、手机号（`13800138000`
> 这类公认占位号码，或 `138****1234` 这类脱敏写法）、订单号、详细地址都只是占位值，
> 运行前请替换成你自己的真实信息。技能包**不内置任何真实联系号码**。

## 这个技能解决什么

把官网 **SellerDelivery.aspx**（寄件下单）、**AddrRecognition.html**（地址智能识别）、
**DeliveryManage.aspx**（寄件管理/工单入口）三个页面的能力搬到对话里，**四条主线，一条龙走完**：

```
【主线一 · 比价】客户说出「发件地 / 收件地 / 重量」→ 列出各家报价 → 按价格排序 → 导出
【主线二 · 下单】比价后加一句「就下这家」→ 校验余额 → 选取件时段 → 提交 → 返回订单号
【主线三 · 寄件管理】「我昨天那票到哪了」→ 查列表/详情 → 未取件可取消 → 走退款解冻
【主线四 · 工单】「快递员态度差 / 包裹丢了」→ 选类型 → 预览 → 提交 → 看处理结果

【地址识别】客户粘贴一整段「李四，13800138000，湖南怀化鹤城迎丰中路189号」
          → 拆出姓名 / 电话 / 省 / 市 / 区 / 街道 / 详细地址 → 直接喂给下单
```

> 客户说「从深圳南山寄到杭州西湖，1 公斤多少钱」→ 给出排好序的报价单；
> 再说「用圆通下单，收件人张三 138****1234」→ 走完下单并回订单号；
> 或者直接甩一段快递面单文字「李四，13800138000，湖南怀化鹤城…」→ 自动拆字段后下单；
> 事后问「260926000005 这笔能不能取消」「丢了件怎么投诉」→ 走管理/工单主线。

**不适用于**：批量查物流轨迹、查第三方运单的配送进度（属其他能力）。

## 何时使用（触发词）

- "从深圳寄到北京多少钱" / "寄 2 公斤到杭州哪个快递便宜"（→ 比价）
- "查一下运费" / "快递报价" / "寄件价格" / "比价" / "试算运费"
- "帮我下单" / "用顺丰寄" / "安排上门取件" / "就下这家"（→ 在线下单）
- "这批订单走哪家快递最便宜"（→ 批量比价）
- **"我寄过的件" / "我的寄件" / "查一下那笔订单" / "这笔能取消吗" / "帮我取消寄件"**
  （→ 寄件管理：`manage_order.py`）
- **"我要投诉快递员" / "包裹丢了怎么办" / "提交工单" / "工单进度"**
  （→ 工单：`ticket.py`）
- 客户同时提供了**发件地、收件地、重量**这三项信息时

## 工作流

```
【地址识别】（可有可无，客户甩一段面单文字时走这条）
  客户粘贴整段文本
        ↓
  AddressAnalysis（/ToDoorOrder/AddressAnalysis）
        ↓
  本地校验：姓名 / 电话 / 省市区必须齐且能查到 → 拆成 姓名·电话·省·市·区·街道·详细地址
        ↓
  直接喂给下面的下单流程（省掉手工拆「李四 138****1234 湖南…」）

【比价】
客户说出「发件地 / 收件地 / 重量」
        ↓
  region.py 把口语地址规范化："广东 深圳 南山" → 广东省 / 深圳市 / 南山区
        ↓
  确保网页登录 token（有则复用；没有则 web_login.py 拉浏览器登录）
        ↓
  GetFreightPredictList → 按价格升序渲染报价单 → 导出 JSON/CSV → present_files

【下单】（在比价基础上继续）
  选定渠道（客户指定 或 自动取最便宜的可用渠道）
        ↓
  GetAccountBalanceInfo 校验余额是否够（不够直接拦下，不白跑一趟）
        ↓
  GetAccessibleList 拉可取件时间段（顺丰是小时级，其他多为整天）
        ↓
  组装订单 → **打印预览并停下**
        ↓
  客户确认 → 加 --confirm 真正调用 PlaceOrder → 回订单号 + 写订单日志

【寄件管理】（售后）
  SearchOrderList → 列表 / 详情（GetOrderDetail 才有完整号码）
        ↓
  状态属于「下单成功/分配网点/分配快递员」才可取消
        ↓
  取消默认预演 → 客户确认 → --confirm 才调 CancelOrder

【工单】
  GetWorkOrderCategoryList → 选类型（决定要不要附反馈重量/商品价值/新收件信息）
        ↓
  组装提交体 → 本地校验 → **预览并停下** → --confirm → AddWorkOrder
        ↓
  GetWorkOrderList / GetWorkOrderDetail 看处理进度
```

## 操作要点（对 Agent）

### 地址识别
0. **客户扔来一整段面单文字，用 --from-text / --to-text 直接吃**：
   ```bash
   python place_order.py \
     --from-text "张三13800138000广东省深圳市南山区科技园科苑路8号" \
     --to-text   "李四，13800138000，湖南省怀化市鹤城区迎丰中路189号城市中央华盛堂A座" \
     -w 1 --goods 服装
   ```
   也支持单独调用识别模块：`python addr_parse.py "<整段文本>" [--json]`。
   **识别结果一定会先过本地校验**（缺姓名/电话、省市区查不到 → 直接拒绝），
   因为实测喂乱码它也会返回 200 并「脑补」出一个湖北随州的地址。详见
   `references/addr_recognition.md`。

### 比价
1. **一句话就能查**：
   ```bash
   python price_query.py --from "广东 深圳 南山" --to "浙江 杭州 西湖" --weight 1.5
   ```
2. **地址怎么写都行**：`广东省深圳市南山区`、`广东,深圳,南山`、`深圳南山`（省略省份自动反查）、
   `北京朝阳`（直辖市）、`东莞南城`（直筒子市）都能解析。尾部多余内容自动识别为详细地址。
3. **缺区县会兜底并告警**，不会静默猜错——看到告警就引导客户补全区县。
4. **批量比价**（CSV `寄件,收件,重量`）：
   ```bash
   python price_query.py --batch routes.csv --output 报价结果
   ```

### 下单
5. **默认只预览，不扣款**。必须显式加 `--confirm` 才提交：
   ```bash
   # 预览（安全，可反复跑）
   python place_order.py -f "广东 深圳 龙华" -t "湖南 长沙 岳麓" -w 1 \
       --to-name 张三 --to-phone 13800138000 --goods 服装

   # 客户明确确认后才加 --confirm
   python place_order.py ... --confirm
   ```
6. **快递渠道三种写法都认**：`--shipper 顺丰`、`--shipper SF`、`--shipper shunfeng`
   （接口编码不按通用缩写来：顺丰=shunfeng、申通=shentong、极兔=jtexpress）。
7. **寄件人默认取自地址簿**（官网也是这么做的），不用客户重复填；
   要强制手工指定用 `--no-default-sender --from-name X --from-phone Y`。
8. **取件时段**：`--list-slots` 查看全部，`--pickup N` 指定；默认自动选最早的可用时段。
9. **批量下单**（CSV 列：`寄件,收件,重量,收件人,收件电话,物品`）：
   ```bash
   python place_order.py --batch orders.csv --confirm
   ```
10. **订单留痕**：提交成功后追加一行 JSON 到 `~/.workbuddy/xdcc-orders.jsonl`，便于对账；
    `--no-log` 可关闭。

> ⚠️ 下单会真实扣款且不可撤销。**务必先把预览结果给客户看，得到明确确认后再加 `--confirm`**，
> 不要在客户只说「帮我寄一下」时就直接提交。

### 寄件管理（manage_order.py）
11. **先看列表，再定位单号**：
   ```bash
   python manage_order.py list                 # 最近寄件
   python manage_order.py list --cancelable    # 只看还能取消的
   python manage_order.py list --keyword 260926000005
   python manage_order.py list --order-status 8   # 只看已签收
   python manage_order.py show 260926000005       # 详情（含完整寄收件人号码）
   ```
12. **取消默认预演**，把要取消的那一笔完整列出来，确认后才 `--confirm`：
   ```bash
   python manage_order.py cancel 260926000005          # 预演
   python manage_order.py cancel 260926000005 --confirm # 真取消
   ```
   **只有「下单成功 / 分配网点 / 分配快递员」这三档能取消**（已取件、在途中、已签收一律跳过，
   脚本会说明原因，不会白试一次）。
13. **列表接口一次只回最近 15 条，且不认翻页参数**（`PageIndex`/`PageSize` 传了也无效）。
   要看更早的单子，用 `--keyword` / `--order-status` 等筛选条件收窄。

### 工单（ticket.py）
14. **提交前先看有哪些类型**（接口分类树不返回「更改收件信息」，脚本手工补了一档）：
   ```bash
   python ticket.py categories
   ```
   | 类型 | 额外必填项 |
   |---|---|
   | 重量/运费异常 | `--tel-weight`（如 2.5kg） |
   | 丢件 / 包裹破损 / 收到后少件 / 包裹收到错件 | `--goods-value`（如 199.00） |
   | 更改收件信息 | `--new-name` `--new-phone` `--new-address` |
   | 以上全部 | 截图凭证由本技能跳过（无图片上传能力） |
15. **提交工单默认预演**：
   ```bash
   python ticket.py new --order-code 260926000005 --type 丢件 \
       --content "包裹三天没更新" --goods-value 199.00 --confirm
   python ticket.py new --order-code ... --type "投诉/快递员服务态度差" --content "态度很差"
   ```
   `--type` 支持编码（8）、中文名（丢件）、`分组/类型`（投诉/快递员服务态度差）三种写法；
   联系人不给则自动取地址簿默认寄件人。
16. **拦截转寄/退回**走另一条接口，必须带月结号：
   ```bash
   python ticket.py intercept --order-code 260926000005 --type 2 \
       --month-code 7890123 --confirm
   ```
17. **看工单进度**：
   ```bash
   python ticket.py list --status 0        # 只看待处理
   python ticket.py detail 260918000015   # 工单号或内部 ID
   ```
   > ⚠️ 工单详情接口只认**内部自增 ID**，传工单号会报「工单ID不能为空」。
   > 脚本已自动处理：先按工单号在列表里把 ID 捞出来再拉详情，所以两种都能直接输。

> ⚠️ 取消寄件与提交工单都是**真实生效、不可回退**的写操作。默认一律预演，
> 必须客户明确确认后才加 `--confirm`。

## 凭据说明

报价与下单都走**网页侧鉴权**：请求头带 `auth: <userToken>`，这个 token 只存在于浏览器
localStorage，必须通过真实登录一次拿到。

- 存放位置：`~/.workbuddy/xdcc-credentials.env` 的 `XDCC_USER_TOKEN`
- 获取方式：`python web_login.py --username <账号> --password <密码>`
  —— **全自动**：填表 → 点登录 → 取 token。登录页只有「用户名或邮箱 + 密码」两个字段，
  **没有**短信验证码和滑块（那是注册页的），所以无需人工介入。
- 没给账号时：`python web_login.py` 退化成人工填写，脚本继续等待。
- 检查/重登：`python web_login.py --check` / `--force`
- 会过期；接口返回 401 时会自动引导重新登录并重试一次

> 账号通常是手机号。`--username` 与 `--phone` 等价。

## 接口速查

页面 JS 逆向所得，全部 `POST` + `application/x-www-form-urlencoded` + 请求头 `auth`，
嵌套对象按 jQuery `$.param` 规则序列化（`Sender[ProvinceName]=广东省`）。

| 接口 | 路径 | 用途 |
|---|---|---|
| GetFreightPredictList | `/ToDoorOrder/GetFreightPredictList` | 报价列表（比价） |
| AddressAnalysis | `/ToDoorOrder/AddressAnalysis` | 地址智能识别（AddrRecognition 页） |
| GetAccessibleList | `/ToDoorOrder/GetAccessibleList` | 可取件时间段 + 超区校验 |
| PlaceOrder | `/ToDoorOrder/PlaceOrder` | **提交订单（扣款）** |
| GetAccountBalanceInfo | `/UserInfo/GetAccountBalanceInfo` | 可用余额 |
| GetDefaultAddr | `/AddressLib/GetDefaultAddr` | 默认寄件人地址簿 |
| SearchOrderList | `/ToDoorOrder/SearchOrderList` | 我的寄件列表 |
| GetOrderDetail | `/ToDoorOrder/GetOrderDetail` | 订单详情（完整寄收件人号码、取消原因） |
| CancelOrder | `/ToDoorOrder/CancelOrder` | **取消寄件（不可撤销）** |
| GetWorkOrderCategoryList | `/ToDoorOrder/GetWorkOrderCategoryList` | 工单类型树 |
| GetWorkOrderList | `/ToDoorOrder/GetWorkOrderList` | 工单列表 |
| GetWorkOrderDetail | `/ToDoorOrder/GetWorkOrderDetail` | 工单详情（参数是内部 ID） |
| AddWorkOrder | `/ToDoorOrder/AddWorkOrder` | **提交工单（type=3）** |
| WaybillIntercept | `/ToDoorOrder/WaybillIntercept` | **运单拦截（type=1 转寄 / 2 退回）** |

### 订单状态字典（接口只返回数字，来自 DeliveryManage.aspx）
| OrderStatus | 含义 | OrderStatus | 含义 |
|---|---|---|---|
| 1 | 下单成功 | 7 | 在途中 |
| 2 | 分配网点 | 8 | 已签收 |
| 3 | 分配快递员 | 9 | 已赔付 |
| 4 | 已取件 | 10 | 下单失败 |
| 5 | 已揽件 | 6 | 已取消 |
| LogisticsStatus | 1待揽件 2已揽件 3在途中 4派件中 5已签收（仅 OrderStatus≥4 时映射） | | |
| PayStatus | 1已冻结 2已解冻 3已扣款 4已退款 | | |
| 可取消范围 | **仅 1 / 2 / 3** | | |

### 工单提交体（对应页面 AddWorkOrder.html 的 getData()）
```
OrderCode=260926000005        Type=3（3-工单反馈；1-拦截转寄 2-拦截退回）
WorkOrderType=8（接口 categoryCode）  WorkOrderContent=包裹三天没更新
LinkMan=张三   MobilePhone=13800138000
Reason=我是张三,电话：13800138000,如有疑问请联系我。（前端自动拼）
Role=1（发起方：1寄方 2收方 3第三方）   PayMode=4（4=寄付月结）  SourcePage=1
ImageNameList=[]（无图片上传能力，留空）
TelWeight=…（重量异常）  ModityValue=…（破损/丢件/少件/错件）
NewReceiverName/Phone/Address（更改收件信息，且会把三段拼进 WorkOrderContent）
```

### 地址识别请求体
```
Content=李四，13800138000，湖南省怀化市鹤城区迎丰中路189号城市中央华盛堂A座
```
只有一个参数 `Content`（用户粘贴的原始整段文本）。返回 `Data`：

| 字段 | 含义 | 落地到下单参数 |
|---|---|---|
| `Name` | 客户姓名 | `Sender/Receiver.Name` |
| `Mobile` | 电话（手机或座机） | `Sender/Receiver.Mobile` 或 `.Tel` |
| `ProvinceName` | 省（直辖市可能返回裸名「北京」） | `Sender/Receiver.ProvinceName` |
| `CityName` | 市 | `Sender/Receiver.CityName` |
| `ExpAreaName` | 区（直筒子市会回落成市名） | `Sender/Receiver.ExpAreaName` |
| `StreetName` | 街道 | 拼进 `Address` |
| `Address` | 详细地址 | 拼进 `Address` |

### 报价请求体
```
Weight=1.5
Receiver[ProvinceName]=浙江省   Receiver[CityName]=杭州市
Receiver[ExpAreaName]=西湖区    Receiver[Address]=文三路
Sender[ProvinceName]=广东省     Sender[CityName]=深圳市
Sender[ExpAreaName]=南山区      Sender[Address]=科技园
IsRequestKdn=true
```
响应 `Data[]`：`ShipperCode`/`ShipperName`、`cost`（预估运费）、`MarketCost`（市场价）、
`IsAvailable`（1 可达 / 0 不可达）、`ShipperComment`（渠道说明或不可达原因）。

### 下单请求体（对应页面 GoBuy()）
```
PlatFormOrderCode=KDN<毫秒时间戳><6位随机>   ShipperCode=STO
Quantity=1        PayType=1（1现付 2到付 3月结 4第三方付）
PayAmount=6.19    Weight=1
Sender[ProvinceName|CityName|ExpAreaName|Address|Name|Mobile|Tel]=…
Receiver[…]=…     StartDate=2026-10-05 09:00:00    EndDate=2026-10-05 20:00:00
GoodsName=服装    Remark=…      SaveSender=false    SaveReceiver=false
```
- 手机号判定与页面一致：**11 位且不含 `-`** 走 `Mobile`，否则走 `Tel`（座机/分机）。
- 取件时间必填；`GetAccessibleList` 返回 `Data.BookableTime[]`，每项含
  `StartTime`/`EndTime`/`EndFetchTime`。

## 兜底与自助排查（会话内完成）

技能包**不内置任何外部联系渠道**——不写第三方即时通讯账号、电子邮箱、电话、
外部站点地址，也不夹带推广。失败统一收敛为 `common.price_hint()` 的会话内排查步骤：

1. 执行 `web_login.py --check` 确认登录 token 是否存在
2. 若已过期，执行 `web_login.py --force` 重新登录
3. 确认发件/收件的省市区填写完整
4. 下单失败时先看报错：余额不足 / 渠道超区 / 取件时段已过，脚本都会直接说明原因
5. 把报错原文发回会话，助手带着上下文继续协助

> 部署方如需接入自有支持入口，请自行扩展 `common.py` 的 `price_hint()`，不要写回本技能包。

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 成功（含「预览模式未提交」这一正常结果） |
| 1 | 查询/下单失败、无可用渠道、部分路线/订单失败 |
| 2 | 参数错误（地址解析失败、重量非法、缺少收寄件人、工单缺必填项、批量文件无有效记录） |

## 资源

### scripts/
- `price_query.py` — **比价主脚本**：单条/批量试算、按价格升序渲染、JSON/CSV 导出、`--headed` 浏览器兜底。
- `place_order.py` — **下单主脚本**：报价→选渠道→查余额→选取件时段→预览→`--confirm` 提交，
  支持 `--from-text`/`--to-text` 整段文本识别、批量与订单日志。
- `manage_order.py` — **寄件管理**：`list` / `show` / `cancel`，取消默认预演、`--confirm` 生效。
- `ticket.py` — **工单**：`categories` / `list` / `detail` / `new` / `intercept`，提交默认预演、`--confirm` 生效。
- `order_api.py` — 接口层：报价与下单（余额/地址簿/取件时段/提交订单/地址识别），
  以及寄件与工单（列表/详情/取消/工单类型/工单详情/提交工单），含表单扁平化、订单号生成、
  渠道名归一化、状态字典与工单必填项规则。
- `addr_parse.py` — **地址识别模块与 CLI**：调 AddressAnalysis，拆出姓名/电话/省市区/街道/详细地址，
  并做「必须能查到」的本地校验（独立可跑：`python addr_parse.py "<文本>"`）。
- `region.py` — 省市区解析与规范化（可单独调试：`python region.py "广东深圳南山"`）。
- `regions.json` — 随包分发的省市区数据（31 省 / 342 市 / 3344 区，源自官方城市库）。
- `web_login.py` — 网页登录取 token（浏览器探测 + 引导横幅 + 自动填表），支持 `--check` / `--force`。
- `common.py` — 共用：兜底提示 `price_hint()`、凭据读写与增量更新。
- `selftest.py` — 纯静态自检（零网络，241 项）：含上架发布合规扫描、下单/取消/工单三道安全闸门、地址识别校验回归。
- `package.py` — 打包器，输出 `dist/xdcc-price-query-<version>.zip`。

### references/
- `price_guide.md` — 比价上手指南 + FAQ + 排查清单。
- `addr_recognition.md` — 地址智能识别：接口字段、实测准确率、必须做的本地校验。
- `order_guide.md` — 在线下单指南：字段说明、取件时段、安全确认流程、常见失败原因。
- `manage_guide.md` — 寄件管理与工单：状态字典、可取消范围、工单类型与必填项、两个真实接口坑。
- `SECURITY_AUDIT.md` — 安全审计与发布合规自查记录（项目根目录）。

### 打包与验收

```bash
python scripts/selftest.py     # 先过自检（241 项，含上架合规扫描与三道安全闸门）
python scripts/package.py      # 产出 dist/xdcc-price-query-6.0.1.zip
```

zip 内顶层为一层目录 `xdcc-price-query/`，解压即为完整技能包。

---

**安全与合规提醒**
- 登录 token 写入 `~/.workbuddy/xdcc-credentials.env`，**勿硬编码进代码或公开文档**。
- 账号密码由客户提供，技能只做自动填入与提交；不代客户设定密码，也不存储密码。
- 报价必须传省市区，这是功能必需输入；可选的**详细地址**只有客户主动写在输入里才会发出。
- **下单会真实扣款**：脚本默认只预览，`--confirm` 才提交；Agent 必须取得客户明确确认后再加该参数。
- **取消寄件与提交工单同样不可回退**：`manage_order.py cancel` 与 `ticket.py new/intercept`
  默认只做预演，Agent 必须先把预演结果给客户看，客户明确确认后才加 `--confirm`。
- 工单的姓名、电话、问题描述由客户提供；联系人不给时脚本自动填地址簿默认寄件人，
  这一步只读取已存的地址簿，不会新增任何联系方式。
- 收寄件人姓名与电话是承运必需信息，由客户提供；订单日志落在 `~/.workbuddy/xdcc-orders.jsonl`（本机，不随包分发）。
- 发布合规：包内不含第三方推广，也不内置外部联系渠道；页面注入的提示条为中性无品牌样式。
