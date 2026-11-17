# 安全说明

本文件记录本包针对一次安全审计的处置结论。审计对象是上一版 `mixue-1.1.0.zip`。

## 审计发现与处置

### 1. 打包了真实 RSA 私钥（高）→ 经评估后**保留并说明**

**发现**：`tools/mxbc_key.pem` 是有效的 2048 位未加密 RSA 私钥，程序直接加载用于请求签名。

**评估**：这把私钥**不绑定任何账号**。签名串的构成是

```
sign = RSA-SHA256( 请求参数 + 请求体字段 + appId + 时间戳 t )
```

**更正**：早期文档写成「签名串里没有手机号 / customerId / openId」是不准确的。
实际实现会把请求体字段合并进待签名内容，因此登录接口的 `mobilePhone`、结算接口的
`customerId` 等，只要在 body 里就会参与签名。

「不绑定个人」的结论仍然成立，依据换成验签与身份是两层：

| 实验 | 结果 | 说明 |
|---|---|---|
| 真私钥 + 空 token | `401 Access-Token不能为空` | 无任何身份也能通过验签 |
| 假私钥 + 真 token | `4003 invalid sign` | 只认这一把密钥 |
| 真私钥 + 伪造 token | `401 Access-Token失效` | 错误来自身份层，不是签名层 |

密钥本身不含用户绑定，服务端验签时不查身份，因此它是 **App 级共享凭据**。

**处置（1.3.0 起）**：**随包附带，开箱即用**。分发者的理由是：不带私钥则包完全无法运行，
而私钥本身不能直接动任何人的账号（仍需登录态）。

同时保留以下约束：

- 包内只有 `tools/mxbc_key.pem` 这一把私钥，打包脚本会拒绝任何额外的 `.pem`/`.key`（闸门 2）
- 私钥必须能通过 `openssl pkey` 解析才会打包（闸门 4），避免打进去一个坏文件
- 使用者可随时替换：`mixuebingcheng-cli key --set /path/to/your.pem`
- 媒体/文档中明确标注其性质与来源不确定性

**残余风险（请知悉）**：

1. 私钥来自抓包逆向，**来源与授权状态无法自证**；官方随时可能轮换该密钥，届时所有人一起失效
2. 私钥 + 任意一个登录态即可调用全部接口，因此拿到本包的人具备完整的调接口能力
3. 早前版本 `mixue-1.1.0.zip` 也曾夹带同一把私钥；若已外发，删除文件**不能**消除既有泄露
4. 使用者应只操作自己账号的订单，且不要把本包再转给不可信的人

### 2. `.gitignore` 未覆盖运行时凭据（高）

**发现**：旧规则只挡了 `.env` 和部分 `*.pem`，漏掉 token/openId/customerId 文件和 HAR。

**处置**：新的 `.gitignore` 覆盖

```
.env / .env.*（保留 .env.example）
*.pem *.key *.p12 *.pfx
tools/ token.txt openid.txt customer_id.txt *.token
*.har *.har.gz *.chlsj *.saz
```

其中 HAR 单独列出，因为抓包文件含完整 `Access-Token` 请求头，**等同于密码**。

### 3. 输出会泄露账号信息（中）

**发现**：`token --show` 打印完整 JWT；`token` 输出未过滤 claims；`whoami` / `giftcards` 原样打印手机号、customerId、卡号。

**处置**：新增统一脱敏层，**默认开启**：

| 字段 | 处理 |
|---|---|
| `token` / `accessToken` / `authorization` / `sign` | 只留前 3 位 |
| `openId` | 前 4 + 后 4 |
| `customerId` / 手机号 / 卡号 | 前 4 + 后 4 |
| 裸 JWT 字符串 | 自动识别并打码 |

- 原始值需要显式加 `--no-redact`（仅限本机自查）
- `token --show` 已废弃，改为提示用 `--no-redact`

### 4. 命令行传 token 会进 shell 历史（中）

**处置**：新增 `mixuebingcheng-cli token --stdin`，从标准输入读取，不落 shell history：

```bash
mixuebingcheng-cli token --stdin
# 粘贴 JWT，Ctrl-D
```

## 1.4.0：第二轮审计的处置

### 1. 请求参数可能进访问日志（高）

**发现**：`request()` 把 POST 请求体字段也拼进了 URL query，登录/短信接口的
`mobilePhone`、`captcha` 可能落到服务端与代理的访问日志。

**处置（1.6.0 补完）**：URL 现在只携带 `appId` / `t` / `sign`。

- 一般接口：body 只放请求体，仍参与签名计算，验签结果不变
- **`login` / `sms` 曾把手机号与验证码当 query 参数传**，1.6.0 改为走 body；
  实测 URL query 只剩 `appId,sign,t`，服务端返回「短信验证码错误」说明 body 被正确读取
- 原先的 **4003 自动回退已删除**：它会在失败时把 body 重新拼进 URL，等于把敏感参数又漏回去

实测：`POST /api/v1/app/login {mobilePhone, captcha}` 构造出的 URL 里
`mobilePhone` / `captcha` 均不出现，`appId` / `t` / `sign` 正常。
回归：`whoami`、`menu`、`giftcards`、下单演练全部照常。

### 2. 脱敏仍有绕过路径（中）

**处置**：

- 字段名匹配从「精确」改为「精确 + 后缀」，`receiverPhone`、`contactMobile`、`userToken` 等未登记字段也会遮盖
- 字符串内的中国大陆手机号（`1[3-9]` 开头 11 位）统一遮盖；订单号、商品 ID、门店 ID **保持可读**，避免影响使用
- `die()` 的错误输出也走脱敏层
- 原先把 `info` 裸打的那处（礼品卡支付失败提示）改为 `json.dumps(redact(info))`

### 3. 支付参数未脱敏（中）

**处置**：`paySign`、`packageStr`、`orderStr`、`prepayId` 加入默认脱敏名单，
`nonceStr`（公开随机串）保持可读。需要完整值时用全局 `--no-redact`。

### 4a. `place` 可跳过确认直接扣款（高，1.6.0）

**处置**：`place` 现在强制要求 `--yes`，缺省时直接拒绝且**不发起任何网络请求**。
理由：`place` 一步完成「建单 + 礼品卡扣款」，面向 AI Agent 时不能依赖模型自觉。

### 4b. 缺少 SKILL.md（1.6.0）

**处置**：包内新增 `SKILL.md`，声明依赖、环境变量、必需的使用者操作、
授权边界（只操作本人账号、禁止自动支付）与网络行为。

### 4. 文档对签名内容的描述有误（中）

已在 README 与本文档更正：签名内容 = 请求参数 + 请求体字段 + `appId` + `t`，
不是"只有 App 身份"。结论（密钥为 App 级、不绑定个人）改为用验签/身份分离的实验证据支撑。

### 5. `wechatqr` 缺少 `tools/wechat_pay_qr.ps1`（功能缺陷）

**处置**：本包不含该脚本（Windows + PowerShell 自动化，仅原作者环境可用）。
命令保留但会直接给出说明并提示改用 `paylink --order <code>`，不再抛 traceback。

## 支付策略（1.5.0）

为降低误扣款与外部依赖风险，非礼品卡支付通道统一标记为**暂不可用**：

| 命令 | 行为 |
|---|---|
| `pay` / `paylink` / `wechatqr` | 直接拒绝，**不发起任何网络请求** |
| `order` / `place` | 默认 `--giftcard auto`；卡余额不足全额时**不建单**，并清空购物车 |

**没有放行开关**：`MIXUE_ALLOW_NON_GIFTCARD_PAY` 已于 1.9.0 删除，1.10.0 起也不存在其他开关。

这样即使误操作，也不会产生"已下单但无法支付"的孤儿订单，或触发微信/支付宝支付链路。

## 1.7.0：第三轮审计的三项

### 1. 通用 `get` / `post` 可绕过交易确认（高）

**发现**：`cmd_post()` 把任意路径与 JSON 直接透传，`--yes` 只保护 `order`/`place`，
形同虚设。

**处置**：新增 `ALLOWED_RAW_PATHS` 只读白名单（门店/菜单/订单查询/礼品卡查询等 18 个），
其余路径（`/api/v2/order/save`、`/api/v2/order/prepay`、`cancel`、购物车写操作…）一律拒绝，
且**不发请求**。建单/支付/取消只能走带确认的命令。

### 2. `order` 不带 `--yes` 并非只读（中）

**发现**：旧演练会 `addProduct` + `calcprice` + `clearCart`，三个都会改服务端购物车。

**处置**：报价改走 `settlement/update`（不 addProduct、不 clearCart）。
实测：报价后购物车件数仍为 0，订单数不变。输出字段改为
`quote_only / total_yuan / card_covers_yuan / payable_yuan / card_enough`。

### 3. `MIXUE_BASE` 可被改写、无域名校验（中）

**处置**：

- 只允许 `https` 与非空主机名校验，目标必须命中 `ALLOWED_HOSTS = {mxsa.mxbc.net}`
- 指向其他主机会被**直接拒绝**，1.10.0 起已无 `MIXUE_ALLOW_CUSTOM_BASE` 之类的绕过开关
- 自定义 `HTTPRedirectHandler` 阻止跨域重定向，防止认证头跟随跳转外泄

## 1.9.0：第四轮审计的四项

### 1. HTTP 错误被误报为成功（P1）

**发现**：`request()` 捕获 `HTTPError` 后，若响应体为空会返回
`{"ok": true, "note": "empty response (200)"}` —— 重定向拦截这类安全事件会被读成成功。

**处置**：保留真实状态码。

| 情形 | 返回 |
|---|---|
| 非 2xx + 空 body | `{"ok": false, "http_status": 302, "error": "HTTP 302：响应体为空"}` |
| 非 2xx + JSON body | 原样返回并附 `http_status` |
| 非 2xx + 非 JSON | `{"ok": false, "http_status": N, "error": "响应不是 JSON"}` |
| 网络/重定向拦截异常 | `{"ok": false, "error": "HTTPError: blocked non-https redirect"}` |

### 2. 非礼品卡支付仍有解锁开关（P1）

**处置**：`MIXUE_ALLOW_NON_GIFTCARD_PAY` **整条移除**，常量固定为 `False`。
`cmd_pay` / `cmd_paylink` / `cmd_wechatqr` 一律拒绝，没有运行时开关。

### 3. `order` 的行为描述不准确（P2）

**处置**：文档改为按命令列「网络请求 / 服务端影响 / 是否需 `--yes`」的表。
明确写清：`order` 不带 `--yes` 仍会请求菜单、礼品卡与 `settlement/update`，
只是不建单、不写购物车，**不保证服务端零痕迹**；`cart-add` / `clear` 会改购物车；
`key --set` 写本地 `.env`。

### 4. HAR 域名用字符串包含判断（P2）

**发现**：`if CAPTURE_HOST not in host` 会让 `mxsa.mxbc.net.attacker.example` 通过，
导入不可信 HAR 时可能把别人的 token 存下来。

**处置**：改为

```python
host = (u.hostname or '').lower()
if host != CAPTURE_HOST or u.scheme != 'https':
    continue
```

精确相等 + 强制 https。

## 本包不包含什么

以下内容均已核对，**包内不存在**：

- 登录 token / JWT
- 微信 openId、customerId
- 手机号、邮箱、姓名
- `.env` 文件本身
- 礼品卡号、订单号
- HAR 抓包原件
- 任何向第三方回传数据的逻辑（无遥测、无上报）

## 使用者自查

```bash
# 1. 包里的私钥是不是只有自带那一把
find . -name "*.pem" -o -name "*.key"
# 期望输出只有 ./tools/mxbc_key.pem

# 2. 有没有 .env
ls -a | grep -x ".env"

# 3. 有没有抓包原件
find . -name "*.har"

# 4. 配置来源是否正确
mixuebingcheng-cli env
```

## 网络行为

程序只与以下域名通信：

- `mxsa.mxbc.net`（蜜雪小程序业务接口）

不访问任何第三方服务，不做 DNS 预取之外的额外请求，不上报使用数据。

## 联系

发现安全问题请直接告知分发包的人，不要在公开渠道贴出 `.har`、token 或私钥。
