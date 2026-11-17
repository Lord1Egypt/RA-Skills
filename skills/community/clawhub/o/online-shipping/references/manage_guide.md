# 寄件管理与工单指南（manage_order.py / ticket.py）

对应官网：

| 页面 | 地址 | 对应脚本 |
|---|---|---|
| 寄件下单 | `https://xdccy.com/send/SellerDelivery.aspx` | `place_order.py` |
| 地址识别 | `https://xdccy.com/send/AddrRecognition.html` | `addr_parse.py` |
| **寄件管理** | `https://xdccy.com/send/DeliveryManage.aspx` | `manage_order.py` |
| **提交工单** | `https://xdccy.com/AddWorkOrder.html`（**根目录**，不是 `/send/`） | `ticket.py new` |
| **工单列表** | `https://xdccy.com/WorkOrderManage.html`（**根目录**） | `ticket.py list` |

> 逆网页面时注意：`/send/AddWorkOrder.html` 与 `/send/WorkOrderManage.html` 会返回站点首页
> 外壳（抓下来两个文件字节完全相同），真正的页面在根目录。

> 📌 **本文档示例已全部脱敏**：命令里的订单号（`260926000005`）、手机号（`138****1234`）、
> 姓名、地址都只是占位值，请替换成你自己的真实信息后运行。

---

## 一、我的寄件（manage_order.py）

### 命令

```bash
python manage_order.py list                      # 最近寄件（默认 15 条）
python manage_order.py list --cancelable         # 只看还能取消的
python manage_order.py list --keyword 260926000005   # 订单号 / 运单号
python manage_order.py list --shipper 极兔       # 按快递公司
python manage_order.py list --order-status 8     # 只看已签收
python manage_order.py list --phone 138****1234  # 按收件人手机
python manage_order.py list --json               # 给程序读

python manage_order.py show 260926000005         # 订单详情

python manage_order.py cancel 260926000005       # 预演（不生效）
python manage_order.py cancel 260926000005 --confirm   # 真取消
```

### 状态字典（接口只返回数字）

| OrderStatus | 含义 | 可取消？ |
|---|---|---|
| 1 | 下单成功 | ✅ |
| 2 | 分配网点 | ✅ |
| 3 | 分配快递员 | ✅ |
| 4 | 已取件 | ❌ |
| 5 | 已揽件 | ❌ |
| 6 | 已取消 | — |
| 7 | 在途中 | ❌ |
| 8 | 已签收 | ❌ |
| 9 | 已赔付 | ❌ |
| 10 | 下单失败 | ❌ |

- `LogisticsStatus`：1 待揽件 / 2 已揽件 / 3 在途中 / 4 派件中 / 5 已签收。
  页面只在 `OrderStatus >= 4`（且不是 6/10）时才用这张表映射，否则一律显示 `-`。
- `PayStatus`：1 已冻结 / 2 已解冻 / 3 已扣款 / 4 已退款。
- 脚本里的「可取消 ✅」就是照抄页面操作栏 `barDemo` 的条件 `OrderStatus == 1||2||3`。

### 取消的安全闸门

`CancelOrder` 没有预览态，调了就是真的取消。所以：

1. 先 `GetOrderDetail` 把那笔订单拉出来，判断状态是否属于 1/2/3；
2. 不属于 → 直接打印原因跳过，不发请求；
3. 属于 → 完整打印这笔订单，提示加 `--confirm`；
4. 只有 `--confirm` 时才调 `CancelOrder`。

### 已知接口限制（都是实测）

- **列表接口不认分页**：`PageIndex` / `PageSize` 传什么都一样，固定返回**最近 15 条**
  （`TotalCount` 仍是全量）。想看更早的单子只能用 `--keyword` / `--order-status` 收窄。
- **列表里的手机号是脱敏的**（形如 `138****1234`）。要看完整号码必须再调 `show` / `GetOrderDetail`
  —— 详情接口里才有 `ProvinceName / CityName / AreaName / Mobile` 全量字段。
- **重复取消会报错**：「订单已取消，无需重复提交」，脚本在可取消判断里已经拦住，不会有这个分支。
- 列表结果的 `PredictCost` 是**预估**运费，实际扣款以 `Cost` 为准。

---

## 二、工单（ticket.py）

### 工单类型与附加必填项

`GetWorkOrderCategoryList` 返回的是分组树（`CategoryCode` + `Children`），
前端 `workOrderTypeMap` 才决定「这一档还要填什么」。分类树里**没有**「更改收件信息」，
页面手工补了 `categoryCode=18`。技能包里内置了同样的规则表 `WORK_ORDER_RULES`：

| categoryCode | 类型 | 反馈重量 | 商品价值 | 新收件信息 | 截图 |
|---|---|---|---|---|---|
| 3 | 重量/运费异常 | ✅ | | | 要 |
| 6 | 包裹破损 | | ✅ | | 要 |
| 8 | 丢件 | | ✅ | | 要 |
| 585698 | 收到后少件 | | ✅ | | 要 |
| 585696 | 包裹收到错件 | | ✅ | | 要 |
| 18 | 更改收件信息 | | | ✅（三段齐全） | 要 |
| 1 / 2 / 5 / 10 / 11 / 13 / 401 / 678679 | 虚假揽件 / 服务态度差 / 超时揽件 / 物流长时间未更新 / 轨迹签收实际未收到货 / 快递员私下收费 / 拦截 / 核实退回 | | | | 要 |

所以：

```bash
# 丢件：必须给 --goods-value，否则本地就拒（接口多半也会拒）
python ticket.py new --order-code 260926000005 --type 丢件 \
    --content "包裹三天没更新" --goods-value 199.00 --confirm

# 重量异常：必须给 --tel-weight
python ticket.py new --order-code ... --type "重量/运费异常" --tel-weight 2.5kg --confirm

# 更改收件信息：三段都要
python ticket.py new --order-code ... --type 更改收件信息 --content "客户要改地址" \
    --new-name 张三 --new-phone 138****1234 \
    --new-address "省/市/区 + 详细地址" --confirm
```

`--type` 三种写法都行：`8`（编码）、`丢件`（中文名）、`投诉/包裹破损`（分组/类型）。

### 提交体字段（照抄页面 getData()）

```
OrderCode=…            Type=3（3-工单反馈；1-拦截转寄 2-拦截退回）
WorkOrderType=8        WorkOrderContent=问题描述
LinkMan=…   MobilePhone=…
Reason=我是张三,电话：138****1234,如有疑问请联系我。   ← 前端自动拼
Role=1（1寄方 2收方 3第三方）  PayMode=4（4=寄付月结）  SourcePage=1
ImageNameList=[]       ← 本技能无图片上传能力，留空
TelWeight / ModityValue / NewReceiverName / NewReceiverPhone / NewReceiverAddress
```

- 选「更改收件信息」时，页面会把新收件人三段拼进 `WorkOrderContent`
  （`【更改后收件信息】姓名：…，电话：…，地址：…`），技能包保留了同样的行为。
- 联系人（`LinkMan` / `MobilePhone`）不给时自动取地址簿默认寄件人
  （`GetDefaultAddr` 的 `FullName` / `MobilePhone`），只是读，不写。

### 拦截转寄 / 拦截退回

走的是另一条接口 `WaybillIntercept`，**必须带月结号**，type=1 还要新收件地址：

```bash
python ticket.py intercept --order-code 260926000005 --type 2 \
    --month-code 7890123 --confirm          # 拦截退回
python ticket.py intercept --order-code ... --type 1 \
    --month-code 7890123 --new-province 广东省 --new-city 深圳市 \
    --new-area 南山区 --new-address 科技园 --confirm   # 拦截转寄
```

### 查看进度

```bash
python ticket.py list                 # 全部工单
python ticket.py list --status 0      # 只看待处理（1 已处理 / 2 已关闭）
python ticket.py detail 260918000015  # 工单号或内部 ID
python ticket.py detail 819
```

工单状态：0 待处理 / 1 已处理 / 2 已关闭。

> ⚠️ **真实的坑**：`GetWorkOrderDetail` 校验的是**内部自增 ID**（列表行里的 `ID` 字段），
> 传 `WorkOrderCode`（如 `260918000015`）会返回「工单ID不能为空」。
> `ticket.py detail` 已经自动处理——先按工单号在列表里把 ID 捞出来再拉详情，
> 所以两种值都能直接输；如果工单号不在最近若干条里，脚本会提示改用列表里的 ID。

---

## 三、安全闸门（三道，别绕过）

| 操作 | 默认 | 生效条件 |
|---|---|---|
| 下单 `place_order.py` | 预览 | `--confirm` |
| 取消寄件 `manage_order.py cancel` | 预演 | `--confirm` |
| 提交工单 / 拦截 `ticket.py new\|intercept` | 预览 | `--confirm` |

三道闸门都有自检守着（把真正的提交函数替换成会抛异常的桩，
断言预演路径一次都没被调用）：`selftest.py` 的 `[12]` / `[14]` / `[15]`。

## 四、常见失败原因

| 现象 | 原因与处理 |
|---|---|
| 「没有符合条件的寄件记录」 | 列表只回最近 15 条，加 `--keyword` / `--order-status` 收窄 |
| 「不属于可取消范围」 | 只有下单成功/分配网点/分配快递员能取消，已取件及之后不行 |
| 「该工单类型需填写商品价值」 | 丢件/破损/少件/错件必须给 `--goods-value` |
| 「该工单类型需填写反馈重量」 | 重量/运费异常必须给 `--tel-weight` |
| 「工单ID不能为空」 | 用了工单号查详情——脚本已自动转内部 ID，仍报就是该工单不在最近列表里 |
| 「订单不存在」 | 单号写错，或该订单不属于当前登录账号 |
| 401 / 「身份验证失败」 | token 过期，跑 `web_login.py --force` 重登 |
