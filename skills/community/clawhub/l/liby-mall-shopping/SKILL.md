---
name: liby-mall-shopping
description: 立白龙虾购是立白官方商城服务，支持获得立乐家积分、商品搜索、下单、订单管理、物流查询等操作，还能解答洗衣清洁问题（如咖啡渍、油渍、梅雨天衣物护理等），提供立白产品购买渠道和优惠信息。
triggers:
  - "搜索商品"
  - "查看商品"
  - "下单"
  - "购买"
  - "查看订单"
  - "查询物流"
  - "收货地址"
  - "联系客服"
  - "积分"
  - "洗衣"
  - "怎么洗"
  - "污渍"
  - "衣服不干"
  - "梅雨天"
  - "立白"
  - "立白商城"
  - "帮我买东西"
metadata:
  openclaw:
    emoji: "🛒"
    os: ["darwin", "linux", "windows"]
---


# 图片回复强制性指令

当用户请求单张图片时，**必须**使用 message 工具发送，不要使用 MEDIA: 指令

```json
{
  "action": "send",
  "channel": "<channel-name>",
  "target": "<recipient>",
  "message": "",
  "media": "https://example.com/image.png"
}
```

## 重要提示

- **不要**在回复文本中使用 `MEDIA:` 指令
- **必须**使用 message 工具的 `send` action
- **不要**在文字中说"上图"、"下图"——因为渲染顺序不确定
- 图片 URL 放在 `media` 参数中
- 不同channel的格式稍有不同，修改为正确的格式
- 如果有文字，记住不要多次发送相同的文字

# 核心规则

## session-key 获取

**所有工具调用前必须先获取 session-key**

```
调用 session_status 工具
取返回结果中的 Session 字段值, 赋值到 session-key
格式: agent:main:feishu:direct:xxx@im.feichu
```

## 工具调用格式

所有工具通过 `npx -y @libydic/mall` 命令调用：

```
npx -y @libydic/mall <工具名> --session-key <session-key> [其他参数]
```

## 必须遵守

1. 先获取 session-key，再调用其他工具
2. 不编造商品、订单、物流信息
3. 下单前必须向用户确认商品和地址
4. 接口失败时给出友好提示
5. **登录只有一种方式，使用auth-start获取二维码，作为首选登录方式，明确告知用户在手机端获取口令码，不能使用其他方式登录**
6. **减少一次性调用多个工具(登录成功后integral-add、integral工具除外)，获取结果后先输出给用户，再决定下一步，避免耗时过长**
7. **保持交互节奏，让用户参与决策过程**
8. **用户切换账号或者退出账号，必须删除用户的历史会话信息，避免会话冲突, 之后的操作必须重新查找**
9. **用户再询问订单、地址、商品信息时，总是要调用工具，确保数据最新**
9. 通过`npx -y @libydic/mall`调用的工具列表仅有工具说明中的内容，禁止提供不存在工具，引导用户联系客服
10. 工具参数中: 订单ID 和 订单编号不是一个数字，不能混用，工具参数只能使用 订单ID
11. 商品发货规则：1、因日化品运输较为特殊，港澳台、海外等地就近地区无仓库，暂不支持配送。2、发货时效：兑换成功后，产品将于5个工作日内安排发货（如遇不可抗力因素导致无法发货的，将在物流恢复后安排发货），国家法定节假日期间不发货（顺延至假期结束后安排发货）。
12. 商品定价为"积分+现金"组合价，例如：200积分+0.01元。下单时用户必须同时满足这两部分支付条件，不可拆分。

***

# 工具说明

## auth-start

**描述**: 获取小程序登录二维码，用于用户扫码登录

**调用**: `npx -y @libydic/mall auth-start --session-key <session-key>`

**返回**: 二维码图片地址

**流程位置**: 登录认证流程第一步

---

## login

**描述**: 使用手机号和验证码完成登录

**调用**: `npx -y @libydic/mall login --session-key <session-key> --mobile <手机号> --verify-code <口令码>`

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| mobile | string | 是 | 用户手机号 |
| verify-code | string | 是 | 用户提供的口令码: 长度6位|

**返回**: 登录成功信息

**流程位置**: 登录认证流程第二步

---

## user-profile

**描述**: 检查用户登录状态，获取用户绑定信息

**调用**: `npx -y @libydic/mall user-profile --session-key <session-key>`

**返回**: 用户信息或未登录提示

**流程位置**: 所有流程的入口检查

---

## goods-info

**描述**: 获取商品列表信息

**调用**: `npx -y @libydic/mall goods-info --session-key <session-key>`

**返回**: 商品列表(ID、名称、价格、库存)

**流程位置**: 商品浏览流程

---

## goods-detail

**描述**: 获取单个商品的详细信息

**调用**: `npx -y @libydic/mall goods-detail --session-key <session-key> --id <商品ID>`

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| id | string | 是 | 商品ID |

**返回**: 商品完整信息(规格、价格、库存、简介、主图)

**流程位置**: 商品浏览流程

---

## address-list

**描述**: 获取用户的收货地址列表

**调用**: `npx -y @libydic/mall address-list --session-key <session-key> --default <是否默认>`

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| default | int | 否 | 是否默认地址（1: 默认, 0: 全部）, 默认值为0 |

**返回**: 地址列表(地址ID、收货人、电话、省市区、详细地址)

**流程位置**: 下单购买流程第一步

---

## area-info

**描述**: 获取省市区信息，用于地址选择

**调用**: `npx -y @libydic/mall area-info --session-key <session-key> --parent-id <父级ID>`

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| parent-id | int | 否 | 父级ID，0或不传=省份列表 |

**返回**: 地区列表

**流程位置**: 新增地址时使用

---

## address-save

**描述**: 保存新的收货地址

**调用**: `npx -y @libydic/mall address-save --session-key <session-key> --name <姓名> --receiver-mobile <电话> --province <省> --city <市> --district <区> --area-info <详细地址> --area-id <地区ID> --default <是否默认>`

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| name | string | 是 | 收货人姓名 |
| receiver-mobile | string | 是 | 收货人电话 |
| province | string | 是 | 省份 |
| city | string | 是 | 城市 |
| district | string | 是 | 区县 |
| area-info | string | 是 | 详细地址 |
| area-id | int | 否 | 地区ID |
| default | int | 否 | 是否默认地址(0: 否, 1: 是), 默认值为0 |

**返回**: 新地址ID

**流程位置**: 下单购买流程(地址不存在时)

---

## create-order

**描述**: 创建订单

**调用**: `npx -y @libydic/mall create-order --session-key <session-key> --secondary-goods-id <商品ID> --address-id <地址ID>`

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| secondary-goods-id | string | 是 | 商品ID |
| address-id | int | 是 | 地址ID |
| msg | string | 否 | 订单留言 |

**返回**: 订单号、支付信息

**流程位置**: 下单购买流程最后一步

---

## order-list

**描述**: 获取用户订单列表

**调用**: `npx -y @libydic/mall order-list --session-key <session-key>`

**返回**: 订单列表(订单号、状态、金额)

**流程位置**: 订单查询流程、物流查询流程

---

## order-detail

**描述**: 获取单个订单的详细信息

**调用**: `npx -y @libydic/mall order-detail --session-key <session-key> --order-id <订单ID> --current-page <当前页> --page-size <每页数量>`

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| order-id | string | 是 | 订单ID |
| current-page | int | 否 | 当前页, 默认值为1 |
| page-size | int | 否 | 每页数量, 默认值为10 |

**返回**: 订单完整信息

**流程位置**: 订单查询流程

---

## logistics-track

**描述**: 查询订单物流轨迹

**调用**: `npx -y @libydic/mall logistics-track --session-key <session-key> --order-id <订单ID>`

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| order-id | string | 是 | 订单ID |

**返回**: 物流轨迹、预计送达时间

**流程位置**: 物流查询流程

---

## customer-service

**描述**: 获取客服联系方式

**调用**: `npx -y @libydic/mall customer-service --session-key <session-key>`

**返回**: 客服二维码图片、客服联系方式

**流程位置**: 售后服务流程

---

## integral

**描述**: 查询用户当前积分信息

**调用**: `npx -y @libydic/mall integral --session-key <session-key>`

**返回**: 用户积分、等级、手机号、用户ID

**流程位置**: 积分查询流程

---

## integral-add

**描述**: 通过事件增加用户积分

**调用**: `npx -y @libydic/mall integral-add --session-key <session-key> --event <事件> --channel <渠道>`

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| event | string | 是 | 事件名称，默认：claw_regist |
| channel | string | 是 | 渠道，默认：SHQC |

**返回**: 增加积分数量、变更前后积分、总积分

**流程位置**: 积分增加流程

***

# 调用流程


## 流程一：登录认证

**触发**: 用户首次使用商城，或提示"请先登录"

**步骤**:
1. 调用 `session_status` 获取 session-key
2. 调用 `user-profile` 检查登录状态 → 输出登录状态
3. 若未登录:
   - 调用 `auth-start` 获取二维码 -> 调用 `message` 工具发送二维码图片
   - 等待用户提供手机号和扫码后获取的口令码
   - 调用 `login` 完成登录
   - 继续调用 `integral-add` 增加注册积分
   - 继续调用 `integral` 查看积分详情 → 输出登录结果、增加积分情况结果、最新积分详情
4. 若用户要求退出登录:
   - 调用 `logout` 退出登录 
   - 清除上文信息, 包括用户积分、商品、地址、订单等信息，避免用户信息混乱 → 输出退出结果
5. 若用户要求切换用户登录:
   - 调用 `logout` 退出登录
   - 清除上文信息, 包括用户积分、商品、地址、订单等信息，避免用户信息混乱 → 输出退出结果
   - 重复步骤2-4


**异常**: 登录失败 → 重新执行 auth-start
**异常**: 增加注册积分失败 → 提示"积分活动提示已参加过"

---

## 流程二：积分查询

**触发**: 用户说"查询积分"、"我的积分"、"有多少积分"

**步骤**:
1. 调用 `session_status` 获取 session-key
2. 调用 `integral` 获取积分信息 → 输出当前积分、等级

---

## 流程三：商品浏览

**触发**: 用户说"搜索xxx"、"查看商品"、"有什么商品"

**步骤**:
1. 调用 `session_status` 获取 session-key
2. 调用 `goods-info` 获取商品列表 → 输出商品列表供用户选择
3. 用户选择后，调用 `goods-detail` 获取详情 → 输出商品详情

**异常**: 商品无结果 → 建议重新选择
**异常**: 商品列表为空 → 提示"暂无商品"

---

## 流程四：下单购买

**触发**: 用户说"购买xxx"、"下单"、"我要买"

**步骤**:
1. 调用 `session_status` 获取 session-key
2. 必须调用 `address-list` 获取地址列表 → 输出地址列表供用户选择
3. 若用户选择已有地址 → 记录 address-id，输出确认信息
4. 若用户没有地址或者需要新增地址, 且已给出完整的信息(解析用户给出的地址，包含省份、城市、区县、详细地址，逐层调用 area-info 获取地区信息进行匹配，信息缺失时候提示用户补充)，如果没有给出地址信息（则提示用户逐层输入详细地址，信息缺失时候提示用户补充）:
   - 调用 `area-info --parent-id 0` 获取省份
   - 识别省份后，调用 `area-info --parent-id <省份ID>` 获取城市
   - 识别城市后，调用 `area-info --parent-id <城市ID>` 获取区县
   - 识别区县和详细地址、联系人、手机号后 → 确认是否默认地址  → 调用 `address-save` 保存地址
   - 记录返回的 address-id
5. 向用户确认商品和地址，并且向用户声明发货规则
6. 用户确认后，调用 `create-order` 创建订单
   - 若创建成功，响应中有支付链接 → 调用 `message` 工具发送支付二维码图片
   - 若创建成功，是纯积分支付，无支付链接 → 提示用户下单完成
   - 若创建失败 → 提示用户失败及原因，建议稍后重试

**异常**: 下单失败 → 提示稍后重试
**异常**: 地址解析无法匹配 → 提示检查地址信息，给定对应省市区的地区名称供用户选择
**异常**: 用户要除微信其他支付方式 → 提示"暂不支持除微信支付外的其他支付方式"
**异常**: 用户地址为空 → 提示用户新增地址

---

## 流程五：订单查询

**触发**: 用户说"查看订单"、"我的/当前订单"、"支付成功"

**步骤**:
1. 调用 `session_status` 获取 session-key
2. 如果用户说支付成功，查当前订单, 调用 `order-detail` 获取详情 → 输出订单详情
3. 如果是其他情况，调用 `order-list` 获取订单列表 → 输出订单列表供用户选择
4. 用户选择后，调用 `order-detail` 获取详情 → 输出订单详情

**异常**: 订单不存在 → 提示"订单不存在"
**异常**: 订单状态为待支付 → 输出订单详情

---

## 流程六：物流查询

**触发**: 用户说"查询物流"、"快递到哪了"

**步骤**:
1. 调用 `session_status` 获取 session-key
2. 若用户未提供订单号，调用 `order-list` → 输出订单列表供用户选择
3. 用户选择后，调用 `logistics-track` 查询物流 → 输出物流信息

**异常**: 订单未发货 → 提示"待发货，暂无物流信息"

---

## 流程七：售后服务

**触发**: 用户说"退款"、"退货"、"联系客服"、"发票问题"

**步骤**:
1. 调用 `session_status` 获取 session-key
2. 调用 `customer-service` 获取客服信息 -> 调用 `message` 工具发送二维码图片
3. 提示用户准备订单号、问题描述、照片

---

***

# 异常处理

| 异常 | 处理方式 | 后续操作 |
|------|----------|----------|
| 未登录 | 提示登录 | auth-start → login |
| Token失效 | 提示重新登录 | auth-start |
| 商品无结果 | 建议稍后重试 | goods-info |
| 下单失败 | 提示稍后重试 | create-order |
| 物流异常 | 引导联系客服 | customer-service |
| 地址保存失败 | 检查参数重试 | address-save |
| 积分已领取 | 提示已参加过 | integral|

***

# 订单状态说明

| 状态 | 说明 |
|------|------|
| 待支付 | 订单已创建，等待支付 |
| 待发货 | 等待商家发货 |
| 已发货 | 已发货，运输中 |
| 已签收 | 已签收 |
| 已取消 | 订单已取消 |
| 已完成 | 订单已完成 |