# mixuebingcheng-cli

蜜雪冰城点单命令行工具：查门店、看菜单、下单、礼品卡结账、取餐号。

> 本包**含代码 + 一份 App 级签名私钥**（`tools/mxbc_key.pem`），开箱即用。
> **不含**任何账号凭据（token / openId / customerId / 手机号 / 订单 / 抓包）。
> 私钥只负责请求签名，不绑定任何人的账号；但每笔订单仍需要你自己的登录态。

---

## 1. 安装

```bash
pip3 install cryptography
chmod +x bin/mixuebingcheng-cli
ln -sf "$PWD/bin/mixuebingcheng-cli" ~/.local/bin/mixuebingcheng-cli
mixuebingcheng-cli --version
```

需要别的 Python：`export MIXUE_PYTHON=/path/to/python`。

## 2. 准备三样东西

| 需要什么 | 从哪来 | 怎么填 |
|---|---|---|
| 登录态 `Access-Token` | 抓自己的小程序包 | `mixuebingcheng-cli har 抓包.har` |
| `openId` / `customerId` | 同上（一次抓包全都有） | 同一条命令 |
| 签名私钥（RSA PEM） | **已自带**，无需准备 | 想换自己的：`mixuebingcheng-cli key --set /path/key.pem` |

### 2.1 抓哪个域名

| 域名 | 用途 | 要不要抓 |
|---|---|---|
| `mxsa.mxbc.net` | 小程序全部业务接口 | ✅ 只抓这个 |
| `mxsa-oss.mxbc.net` | 商品图片 CDN | ❌ 不必 |

抓包过滤条件：`mxsa.mxbc.net`　小程序 AppID：`wx7696c66d2245d107`

### 2.2 抓包时要做的操作

```
1. 打开小程序「蜜雪冰城」并登录        → 任意 /api/*            → Access-Token 头
2. 允许定位，进入一家门店              → shopinfo/findNear      → shopId
3. 商品加进购物车                      → shoppingCart/addProduct
4. 点「去结算」                        → settlement/update      → customerId
5. 走到收银台但不付款                  → order/prepay           → openId
6. 导出 .har
```

`openId` **只在第 5 步出现**，不到收银台就拿不到，后续支付/礼品卡都会失败。不必真的付款。

### 2.3 导入

```bash
mixuebingcheng-cli init                 # 生成 .env（0600）
mixuebingcheng-cli needs                # 完整采集要求（域名/接口/字段）
mixuebingcheng-cli har 抓包.har         # 自动写入 token / openId / customerId
mixuebingcheng-cli key                  # 看私钥状态（自带的可直接用）
mixuebingcheng-cli whoami               # 验证：返回脱敏后的手机号即成功
```

`har` 会告诉你每一项来自哪个接口：

```
sources:
  MIXUE_TOKEN        GET  /submsg/webapp/v1/subscribe/listTemplate
  MIXUE_OPENID       POST /api/v2/order/prepay
  MIXUE_CUSTOMER_ID  POST /api/v3/shoppingCart/settlement/update
```

## 3. 命令

```bash
mixuebingcheng-cli needs                      # 采集要求
mixuebingcheng-cli env                        # 配置来源（脱敏）
mixuebingcheng-cli whoami                     # 账号信息（脱敏）
mixuebingcheng-cli shops --lat 24.855 --lng 118.562
mixuebingcheng-cli menu --shop <shopId> --table
mixuebingcheng-cli orders
mixuebingcheng-cli giftcards                  # 卡号默认脱敏

# 报价：会请求菜单/礼品卡/settlement 拿价格，但不建单、不写购物车
mixuebingcheng-cli order --shop <shopId> --product <productId> --num 1
# 真下单（默认走礼品卡，卡不够全额则不建单）
mixuebingcheng-cli order --shop <shopId> --product <productId> --num 1 --yes
# 一键下单 + 付款 + 打印取餐号
mixuebingcheng-cli place --shop <shopId> --product <productId> --yes --wait   # 必须 --yes
```

### 支付方式：只用礼品卡

微信/支付宝通道已标记为**暂不可用**，默认不发起任何调用：

| 命令 | 状态 |
|---|---|
| `order` / `place` | ✅ 默认 `--giftcard auto`，卡余额不够**不建单**；均需 `--yes` |
| `cancel` | 需 `--yes`，缺省直接拒绝且不发请求 |
| `pay`（微信/支付宝聚合支付） | ⛔ 暂不可用，直接拒绝，不发请求 |
| `paylink`（微信收银台链接/二维码） | ⛔ 暂不可用，直接拒绝，不发请求 |
| `wechatqr`（PC 微信自动化） | ⛔ 暂不可用 |

```bash
mixuebingcheng-cli giftcards
mixuebingcheng-cli order --shop <id> --product <id> --num 1 --yes   # 自动选余额最高的卡
```

卡不够时会说清楚，不会留下付不掉的订单：

```json
{"error": "礼品卡余额不足，未建单",
 "total_yuan": 5.0, "card_covers_yuan": 0.7, "short_yuan": 4.3,
 "hint": "其他支付方式暂不可用；充值礼品卡后重试，或减少数量/换更便宜的商品"}
```

> 非礼品卡支付**没有任何放行开关**（环境变量通道已移除）。

### 口味选择（`--attrs`）

```bash
mixuebingcheng-cli order --shop <id> --product <id> --attrs "正常冰,七分糖"
```

- 温度/糖度的选项来自菜单接口的 `productAttrs`，**不需要额外抓包**
- 名字或 attributeId 都可以；同一组只能选一个，选两个会提示 `同一组只能选一个`
- 口味不额外收费，价格只受券影响
- 加料（`--specs`）**暂不支持**：传了会在**发请求之前**直接返回
  `加料/规格（--specs）暂不支持`，不会走到下单阶段才失败

### 完整命令表

| 命令 | 作用 | 备注 |
|---|---|---|
| `needs` / `init` / `env` / `har` / `key` | 采集要求 / 生成配置 / 配置自查 / 导入抓包 / 私钥管理 | 首次配置用 |
| `whoami` | 账号信息（脱敏） | 判登录态是否有效 |
| `shops` / `menu` / `orders` / `giftcards` | 门店 / 菜单 / 订单列表 / 礼品卡余额 | 只查询 |
| `order` | 报价；加 `--yes` 则建单 + 礼品卡支付 | 加 `--yes` 需确认 |
| `place` | 一步下单 + 支付 | 必须 `--yes`，可加 `--wait` |
| `watch` | 轮询订单状态直到出取餐号 | 支付后用 |
| `cancel` | 取消订单 | 必须 `--yes` |
| `calc` / `clear` / `cart-add` | 购物车算价 / 清空 / 加购 | **会改购物车** |
| `login` / `sms` | 手机号 + 短信验证码登录 | 会向该手机号发短信 |
| `get` / `post` | 原始接口调用 | 仅只读白名单 |
| `config` / `ping` | 服务端配置 / 时间 | 只读 |
| `pay` / `paylink` / `wechatqr` | 非礼品卡支付 | **已停用，直接拒绝** |

## 4. 安全设计

| 措施 | 说明 |
|---|---|
| 私钥已在包内 | `tools/mxbc_key.pem` 是 App 级签名密钥（见下方说明），可用 `key --set` 换成自己的 |
| 不携带登录态 | 包内没有 `.env`；token 只能靠抓自己的包获得 |
| 默认脱敏 | `token` / `openId` / `customerId` / 手机号 / 礼品卡号在输出里自动打码 |
| 原始值需要显式开启 | `--no-redact` 才会显示完整值（仅限本机自查） |
| token 不进历史 | `mixuebingcheng-cli token --stdin` 从标准输入读，避免写进 shell history |
| .gitignore 兜底 | 已排除 `.env`、`*.pem`、`*.har`、`tools/`、`token.txt` 等运行时凭据 |
| 抓包过滤 | `har` 只解析 `mxsa.mxbc.net`，不读取其他域名的内容 |
| 请求体不入 URL | 所有业务参数（含 `login`/`sms` 的手机号与验证码）只放请求体；`sign` 在本地对「query + body」合并计算，URL 里只有 `appId`/`t`/`sign` |
| 无自动回退 | 早期版本遇 `4003` 会把 body 重新拼进 URL 重试，该逻辑已删除，避免敏感参数回流 |
| 域名白名单 | 只请求 `https://mxsa.mxbc.net`；`MIXUE_BASE` 指向其他主机会被拒绝，**没有运行时开关可绕过** |
| 禁跨域重定向 | 重定向到其他域名直接中断，避免认证头被带走 |
| 通用接口白名单 | `get` / `post` 只能访问只读接口列表，建单/支付/取消必须走带确认的命令 |
| HTTP 错误不误报 | 非 2xx 一律返回 `{"ok": false, "http_status": N, ...}`，空响应体也算失败 |
| HAR 严格校验 | 只接受 `https://mxsa.mxbc.net` 精确主机名，`mxsa.mxbc.net.xxx` 之类一律跳过 |

详细说明见 [SECURITY.md](SECURITY.md)。

### 关于包里那把私钥

`tools/mxbc_key.pem` 是 **RSA-2048 签名密钥**，用于给每个请求签名：

```
sign = RSA-SHA256( 请求参数 + 请求体字段 + appId + t )
```

**签名内容确实会包含请求体里的字段** —— 比如登录接口的 `mobilePhone`、结算接口的 `customerId`，只要出现在 body 里，就会参与签名。这一点不要误解。

但「密钥不绑定个人」的结论仍然成立，依据是验签与身份是两层：

- 密钥本身不带任何用户绑定，同一个 `appId` + 同一套参数，换谁的 token 签出来都一样
- 服务端验签时**不查身份**：实测「真私钥 + 空 token」返回的是 `Access-Token不能为空`（签名已通过），「假私钥 + 真 token」才返回 `4003 invalid sign`

所以它是**随客户端分发的共享密钥**（App 级），不是"你的密钥"。它证明的是「请求由官方客户端发出且未被篡改」。

但请注意：

- 它仍然是敏感材料：拿到它 + 任意一个登录态就能调接口
- 来源与授权状态本包无法自证（逆向所得，随时可能被官方轮换）
- 想换成自己的私钥：`key --set /path/to/your.pem`

### 如果这个包没有自带私钥

某些分发包（例如用于公开发布的 `-nokey` 变体）不含 `tools/mxbc_key.pem`。
这时需要自己提供一份 RSA PEM 私钥：

```bash
mixuebingcheng-cli key --set /path/to/your_key.pem   # 校验后写入 .env 的 MIXUE_KEY_PATH
# 或写进 .env：
MIXUE_PRIVATE_KEY="REDACTED-SECRET"
```

配置好之前，任何命令都会以「缺少签名私钥」退出，不会发起请求。

## 5. 隐私与合规

- 只操作**你自己账号**的订单
- 接口为抓包逆向所得，可能随时变更
- 请勿高频请求、勿用于商业用途
- 抓包文件（`.har`）含完整登录态，等同密码：用完删掉，不要提交、不要转发

## 6. 常见问题

| 现象 | 处理 |
|---|---|
| `缺少签名私钥` | 包里自带的不见了：`key --set <pem>` 或填 `MIXUE_PRIVATE_KEY` |
| `401 Access-Token失效` | 重新抓包，或 `token --stdin` 换新 token |
| `4003 invalid sign` | 私钥不对 / `MIXUE_PRIVATE_KEY` 的 `\n` 没转义 |
| `HAR 里没有 mxsa.mxbc.net 的请求` | 抓包过滤条件设成 `mxsa.mxbc.net`，确认抓的是小程序不是网页 |
| `openId不能为空` | 抓包时没走到收银台，重抓一次 |
| `8104 订单金额发生变化` | 礼品卡要在 settlement 阶段加，别塞给 order/save |
| 菜单读不到 | 门店 ID 不对，或门店未营业 |
| `wechatqr` 报「依赖 Windows + PowerShell」 | 本包未含 `tools/wechat_pay_qr.ps1`；改用 `paylink --order <code>` 生成收银台链接/二维码即可 |
