# 京东 OAuth2 登录（jdgold，模拟 PKCE）

> Skill 只持有 PKCE 的 **code_verifier**，**authCode 全程不离开后端**。
> 授权 URL 由后端拼装（凭据在后端），Skill 只在第一步上送 challenge+state、
> 完成后凭 state+verifier 兑换。Skill 包内不含任何 ak/sk。

## 流程总览（模拟 PKCE，S256）

```
Skill                              cf-gold-ai（经金融网关）            京东 OAuth2 / 浏览器
 1. secrets 生成 verifier、state
    challenge = b64url(sha256(verifier))
 ── auth_login_url(challenge,state,[localRedirect]) ─▶
                              JIMDB 绑定 state→challenge
                              拼授权 URL（redirect_uri=后端回调端点）
 ◀──────────── authorizeUrl ────────
 2. 打开 authorizeUrl，用户扫码授权 ───────────────────────────────▶
 3.                       京东回调「后端」回调端点（带 state+code）◀──┤
                          后端按 state 补 authCode、置 ready
                          回调成功后返回提示页：「已经登陆成功」
 4. 用户看到提示页后，手动将「已经登陆成功」复制到对话框发送
 5. Agent 收到用户确认消息后：
 ── auth_exchange(state, verifier) ─▶  (verifier 仅经 POST body)
                          校验 sha256(verifier)==challenge
                          用 authCode 调京东换 token、记 accessToken→xid
 ◀──── accessToken, expiresIn ──
```

**关键点**

- `authCode` 由后端在回调时获取，**绝不回传客户端**；客户端拿不到也不需要。
- `verifier` 只在客户端内存/本地缓存，**仅经一次 POST body** 上送，绝不进 URL / 日志。
- 绑定在第一步用 `state` 建立；回调只带 `state` 作完成信号。
- 回调成功后用户看到提示页（而非自动兑换），**必须由用户手动告知 Agent**，Agent 才发起 exchange。

## 本地脚本命令

### 场景 A：本地环境（Agent 与浏览器同机）

```bash
cd ${SKILL_DIR}/scripts
python3 jos.py login-auto   # 自动检测本地环境，唤起浏览器 + 启动本地回调服务（127.0.0.1:8765）
```

本地环境下脚本通过 `webbrowser` 直接为用户打开授权页面，无需手动复制 URL。
用户完成授权后京东回调本地服务，脚本**自动完成 exchange 兑换 token**。
Agent 应在后台轮询 `python3 jos.py token` 等待登录完成，**无需用户手动发送任何确认消息**。

回调页通过探测 `http://127.0.0.1:8765/health` 判断本地服务是否就绪。

### 场景 B：远端沙箱（Agent 在沙箱，浏览器在用户本机）

沙箱侧无法接收本机回调，改两步走——**用户无需再复制任何 code**：

```bash
# 第 1 步：生成授权链接（沙箱模式，不绑定本地回调），发给用户
python3 jos.py oauth-url
# 用户在浏览器打开链接完成授权；授权完成后回调页显示「已经登陆成功」提示

# 第 2 步：等待用户手动将「已经登陆成功」复制到对话框中发送

# 第 3 步：收到用户确认后，兑换（自动读取第 1 步缓存的 state+verifier）
python3 jos.py exchange
# 成功后输出 access_token 并缓存
```

> 与旧流程的区别：authCode 不再经浏览器地址栏暴露，用户**不需要复制回传**任何参数。
> Agent **禁止**自动轮询或主动调用 exchange，必须等到用户在对话框发送确认消息后才执行。
> 若兑换时提示「授权尚未完成」，说明用户还没授权完，让用户确认后重试 `exchange`。

### 其他命令

```bash
python3 jos.py token              # 验证当前 token 是否有效
python3 jos.py holdings           # 查询积存金持仓与收益
python3 jos.py morning-report     # 查询黄金早报
```

> `refresh` 子命令暂不可用：后端尚未提供刷新接口，过期请重新登录。

Token 缓存：存入系统级加密存储（macOS Keychain / Windows DPAPI，服务名 `com.jd.jdgold`；其他平台回退 0o600 文件），由脚本自动管理，无需手动指定。旧版本的明文 `token.json` 会在首次读取时自动迁移并删除。

## 常见登录问题排查

### 授权页报 400 Bad Request

京东 OAuth 背后 Tomcat 对请求头大小有上限；用户浏览器京东域名下 cookie 过多会超限。
**解决**：用**浏览器无痕模式**打开授权链接。

### 兑换提示「授权尚未完成 / 会话不存在或已过期」

- 「尚未完成」：用户还没完成授权，稍后重试 `exchange`。
- 「会话不存在或已过期」：PKCE 会话 TTL 10 分钟，超时需重新 `oauth-url` / `login`。

### 兑换提示「校验失败」

verifier 与第一步的 challenge 不匹配——通常是混用了不同次 `oauth-url` 的缓存。
重新执行 `oauth-url` 再 `exchange`。

## 网关 / 调试

- 网关域名集中维护在 `scripts/bff_client.py` 的 `DEFAULT_BFF_BASE_URL`；
  本地调试 `GOLD_BFF_BASE_URL=http://localhost:8080 python3 jos.py token`。
- 授权/业务路径常量也集中在 `bff_client.py`（`PATH_AUTH_*` / `PATH_*`）。
- ⚠️ 网关「JSF-over-HTTP」请求契约待接入文档确认，确认后只需改 `bff_client.py`
  的 PATH_* / `_parse_envelope` / 请求头，业务脚本无须改动。

## 上线前检查

- [ ] 网关域名 `DEFAULT_BFF_BASE_URL` 已对接正式环境
- [ ] 后端 `OAUTH_APP_KEY/SECRET` 等已用环境变量/密钥托管注入（非明文）
- [ ] 后端 `OAUTH_REDIRECT_URI` 指向网关回调端点，且与京东开放平台登记一致
- [ ] 后端 `OAUTH_CALLBACK_ALLOWED_IPS` 已配置京东出口 IP 白名单
- [ ] 服务器出口 IPv4 已加入京东 IP 白名单（若报 code 80）
- [ ] Skill 包内**不含**任何 ak/sk 字符串（`grep -rn "APPSECRET\|app_secret" scripts/` 应为空）
