# Example Dialogues

## 1. Browser binding (default path)

**User:** 帮我连接 LogicX

**Agent action:**

```bash
{baseDir}/scripts/logicx_api.sh POST agent/link/start '{"install_id":"openclaw-main"}'
```

**Agent reply:**

```
你可以点击以下链接登录并完成授权：

<login_url>

登录完成后请回来告诉我一声，比如直接回复"我登录好了"。

如果你不想跳转浏览器，也可以直接把用户名和密码告诉我，我可以直接帮你登录。
```

---

**User:** 我登录好了

**Agent action** (script reads link_code and install_id from state file):

```bash
{baseDir}/scripts/check_link_status.sh
```

On `confirmed`:

```bash
{baseDir}/scripts/logicx_api.sh GET user/
```

**Agent reply:**

```
绑定成功！账号验证通过，可以开始帮你查账号、会员和订单信息了。
```

On `pending`:

```
我这边还没有检测到绑定完成，可能浏览器里的授权还没最终提交。你确认完成后再跟我说一声，我再继续检查。
```

---

## 2. Password login (fallback path)

**User:** 我不想打开浏览器，直接用邮箱密码登录吧

**Agent action** (after user provides credentials):

```bash
{baseDir}/scripts/logicx_api.sh POST agent/auth/login \
  '{"email":"user@example.com","password":"secret","install_id":"openclaw-main"}'
```

```bash
{baseDir}/scripts/logicx_api.sh GET user/
```

**Agent reply:**

```
登录成功，账号验证通过，可以继续处理你的请求了。
```

---

## 3. Query account info

**Agent action:**

```bash
{baseDir}/scripts/logicx_api.sh GET user/
```

**Agent reply** (example):

```
你的账号信息：
- 邮箱：user@example.com
- 会员等级：Pro 会员
- 到期时间：2026-06-01
```

---

## 4. Query orders

**Agent action:**

```bash
{baseDir}/scripts/logicx_api.sh GET payment/orders
```

---

## 5. Create order (confirm before calling)

**User:** 帮我开通 Pro 月付

**Agent:** 我将为你创建 Pro 月付（¥29.00）订单，支付方式为模拟支付，确认继续吗？

**User:** 确认

**Agent action:**

```bash
{baseDir}/scripts/logicx_api.sh POST payment/create '{"plan":"pro_monthly","gateway":"mock"}'
```

---

## 6. Cancel order (confirm before calling)

**Agent action** (after user confirms):

```bash
{baseDir}/scripts/logicx_api.sh POST payment/cancel '{"orderNo":"ORDER_NO"}'
```

---

## 7. Change password (confirm before calling)

**Agent action** (after user confirms):

```bash
{baseDir}/scripts/logicx_api.sh POST auth/change-password \
  '{"currentPassword":"old-password","newPassword":"new-password"}'
```

---

## 8. Unlink device (confirm before calling)

**Agent action** (after user confirms):

```bash
{baseDir}/scripts/logicx_api.sh POST agent/unlink '{"install_id":"abc123"}'
```
