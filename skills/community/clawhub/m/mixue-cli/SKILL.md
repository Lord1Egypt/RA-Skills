---
name: mixuebingcheng-cli
description: Use when ordering 蜜雪冰城 (Mixue) drinks from the terminal — list shops, read the menu, place an order, check the pickup number. Checkout is gift-card only; requires the user's own login token captured from their own traffic.
version: 1.11.1
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    primaryEnv: MIXUE_TOKEN
    envVars:
      - name: MIXUE_TOKEN
        required: false
        description: 蜜雪小程序 Access-Token（JWT），由使用者自己抓包获得；仅业务命令需要，首次配置（init/har）不需要
      - name: MIXUE_OPENID
        required: false
        description: 小程序 openId，礼品卡结算需要
      - name: MIXUE_CUSTOMER_ID
        required: false
        description: customerId，结算接口用
      - name: MIXUE_SHOP
        required: false
        description: 默认门店 shopId
      - name: MIXUE_KEY_PATH
        required: false
        description: RSA 签名私钥路径（默认 ./tools/mxbc_key.pem）
      - name: MIXUE_PRIVATE_KEY
        required: false
        description: 内联 PEM 私钥（\n 转义），与 MIXUE_KEY_PATH 二选一
      - name: MIXUE_BASE
        required: false
        description: 服务器地址覆盖（默认 https://mxsa.mxbc.net）；指外域会被白名单拒绝，不可用于绕过
      - name: MIXUE_APPID
        required: false
        description: 签名 appId（有默认值，一般不改）
      - name: MIXUE_ENV
        required: false
        description: 备用配置文件路径（兼容旧布局）
      - name: MIXUE_TOKEN_PATH
        required: false
        description: 兼容旧布局：token 文件路径（优先用 MIXUE_TOKEN）
      - name: MIXUE_OPENID_PATH
        required: false
        description: 兼容旧布局：openId 文件路径
      - name: MIXUE_CUSTOMER_PATH
        required: false
        description: 兼容旧布局：customerId 文件路径
    runtime:
      python: ">=3.8"
      packages:
        - cryptography>=3.4
    network:
      - https://mxsa.mxbc.net
---

# mixuebingcheng-cli

命令行点蜜雪冰城：查门店、看菜单、下单、礼品卡结账、取餐号。

## 依赖

| 项 | 要求 |
|---|---|
| Python | 3.8+ |
| 第三方包 | `cryptography`（`pip3 install cryptography`） |
| 网络 | 只能访问 `mxsa.mxbc.net` |
| 平台 | Linux / macOS / Windows（WSL 亦可） |

## 环境变量

| 变量 | 必填 | 说明 |
|---|---|---|
| `MIXUE_TOKEN` | ✅ | 小程序 `Access-Token`（JWT），**必须是使用者自己的** |
| `MIXUE_OPENID` | 支付必填 | 小程序 openId |
| `MIXUE_CUSTOMER_ID` | 建议 | 结算接口需要 |
| `MIXUE_SHOP` | 可选 | 默认门店 shopId |
| `MIXUE_KEY_PATH` | ✅* | 签名私钥路径，默认 `./tools/mxbc_key.pem` |
| `MIXUE_PRIVATE_KEY` | ✅* | 内联 PEM（`\n` 转义），与上者二选一 |
| `MIXUE_ALLOW_NON_GIFTCARD_PAY` | 已移除 | 本版**不存在**该开关，非礼品卡支付无法解锁 |

配置优先级：真实环境变量 → `$MIXUE_ENV` → `./.env` → `~/.config/mixue/.env`。

## 使用者必须先做的两件事

1. **自备登录态**：抓自己的小程序流量，导出 `.har` → `mixuebingcheng-cli har 抓包.har`
   （`mixuebingcheng-cli needs` 会打印要抓哪个域名、哪几个接口）
2. **自备或确认签名私钥**：`mixuebingcheng-cli key` 查看状态

## 授权与安全约束（对 AI Agent 尤其重要）

**两层确认，缺一不可：**

1. **对话层（策略）**：Agent 在执行任何会扣款或改状态的操作前，必须先向使用者复述
   商品、数量、口味、金额、门店与支付方式，并取得**明确的放行词**
   （「好的 / 确定 / 可以 / 下单」）。
   **使用者报出参数（选商品、报数量、报口味如「正常冰 七分糖」）都不算授权**，
   必须再单独问一次并等到放行词；没等到就结束回合，不得自行推进。
2. **命令层（机制）**：按命令区分，**不要笼统说「没有 --yes 就不联网」**：

   | 命令 | 缺 `--yes` 时 | 是否联网 |
   |---|---|---|
   | `order` | **只报价**：走菜单 + 礼品卡 + `settlement/update` 算价，**不建单、不扣款** | **会联网** |
   | `place` | **直接拒绝**，不进业务逻辑 | 不联网 |
   | `cancel` | **直接拒绝** | 不联网 |

   即：`order` 缺 `--yes` 是「允许报价、不得建单」；`place` / `cancel` 缺 `--yes` 是「直接拒绝」。

其余约束：

- **只操作使用者本人账号**的订单，不得代他人下单
- 非礼品卡支付（`pay` / `paylink` / `wechatqr`）**已停用**，且**没有任何环境变量开关**
- `get` / `post` 只能访问只读白名单，不能用来绕过上述确认
- 卡余额不足全额时**不建单**，不会留下无法支付的孤儿订单

### 各命令的真实副作用（准确说明，别笼统叫"只读"）

| 命令 | 网络请求 | 服务端影响 | 需要 `--yes` |
|---|---|---|---|
| `order`（无 `--yes`） | 有：菜单 + 礼品卡 + `settlement/update` 报价 | 不建单、不写购物车；但不保证服务端零痕迹 | — |
| `order --yes` / `place --yes` | 有 | 建单 + 礼品卡扣款 | ✅ |
| `cancel` | 无（缺 `--yes` 时直接拒绝） | — | ✅ |
| `cart-add` / `clear` | 有 | **会改购物车** | —（不涉及扣款） |
| `key --set` | 无 | 写本地 `.env` | —（本地配置） |
| `shops` / `menu` / `orders` / `giftcards` / `env` / `needs` | 有或本地 | 无 | — |
- 输出默认脱敏（token / openId / customerId / 手机号 / 卡号 / paySign）。
  不要把 `--no-redact` 的结果贴到聊天、日志或提交记录里。
- 抓包文件（`.har`）含完整登录态，等同密码：用完即删，不提交、不转发。

## 口味与加料（`--attrs` / `--specs`）

商品的 `productAttrs`（温度/糖度）与 `productSpecs`（加料/去料/换料）就在菜单接口
`/api/v3/shop/menu/info` 的响应里，**不需要额外抓包**。

```bash
mixuebingcheng-cli order --shop <id> --product <id> --attrs "正常冰,七分糖"
mixuebingcheng-cli order --shop <id> --product <id> --attrs "少冰,五分糖" --yes
```

- `--attrs` 逗号分隔，**名字或 attributeId 都可以**；同一组（如糖度）只能选一个，
  选两个直接报 `同一组只能选一个`；商品没有该属性时报 `商品没有这个属性: xxx` 并列出可用项。
- 口味**不额外收费**：同一商品选任何温度/糖度，`total` 不变。
- 是否真的生效，以下单后的订单明细为准：`orderDetailList[].attr` 里是
  `[{attributeId, attributeName}]`，可对照所选 `attributeId`。
- **加料（`--specs`）已直接拒绝**（1.11.1 起）：传了 `--specs` 会在**发任何网络请求之前**
  返回 `加料/规格（--specs）暂不支持`。原因：`settlement/update` 的 products 里只要
  `specIds` 非空就返回 `4000 参数错误`，已试过 6 种字段形态（`specIds:[id]`、
  `specs:[{specId}]`、`specIds:[{specId}]`、`specId` 标量、`comboProductDetail`、
  带 `specName` 的对象）全部失败。要支持必须先拿到一份**带加料下单**的抓包确认字段名，
  在此之前不得承诺可用、也不得让用户走到下单阶段才失败。

## 常用命令

```bash
mixuebingcheng-cli needs                 # 采集要求
mixuebingcheng-cli init                  # 生成 .env 模板
mixuebingcheng-cli har 抓包.har          # 导入 token / openId / customerId
mixuebingcheng-cli whoami                # 验证登录态
mixuebingcheng-cli shops --lat <纬度> --lng <经度>
mixuebingcheng-cli menu --shop <shopId> --table
mixuebingcheng-cli giftcards             # 礼品卡余额

mixuebingcheng-cli order --shop <id> --product <id> --num 1          # 只算价
mixuebingcheng-cli order --shop <id> --product <id> --num 1 --attrs "正常冰,七分糖"   # 指定口味
mixuebingcheng-cli order --shop <id> --product <id> --num 1 --yes    # 建单+礼品卡支付
mixuebingcheng-cli place --shop <id> --product <id> --yes --wait     # 一步到位
mixuebingcheng-cli watch --order <orderCode>                         # 等取餐号
```

## 行为约束

- 卡余额不足全额时**不建单**，并清空购物车（不留无法支付的孤儿订单）
- 请求体不进 URL：`sign` 仍在本地对「query + body」合并计算，URL 只带 `appId`/`t`/`sign`
- 不做任何形式的数据上报、遥测或第三方请求

## 许可与免责

代码以 MIT-0 许可发布：可自由使用、修改、再分发。

使用范围上的约束只有一条：**这个工具只能用来操作使用者本人的蜜雪账号**，
不得代他人下单或用于经营。接口为抓包逆向所得，官方随时可能变更或轮换密钥，届时工具会失效。
