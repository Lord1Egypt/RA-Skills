# 首次配置 / First Setup

HiFleet 技能使用前须持有 **`api_key`**（环境变量 `HIFLEET_API_KEY` 或配置项 `hifleet_api_key`）。本文说明从零开始的完整路径。

**尚未安装本技能包时**，先按 [INSTALL.md](INSTALL.md) 获取：

| 途径 | 地址 |
|------|------|
| ClawHub | https://clawhub.ai/charleiwang/skills/hifleet-skills |
| GitHub | https://github.com/charleiWang/hifleet-skills |
| 手动安装包（zip） | http://static.hifleet.com/download/skills/hifleet-skills-latest.zip |

---

## 流程总览

```
发验证码 →（如需）人机校验 → 验证码登录/注册（免密码）→ 获得 api_key → 配置环境 → 调用业务接口
                              ↓
              积分/额度不足 → 积分充值 或 订阅套餐 → 收银台付款 → 可选开发票
                              ↓
              订阅将到期 → 邮件提醒（7/3/1天）→ 手动续费（非自动扣款）
```

| 步骤 | 做什么 | 文档 |
|------|--------|------|
| 1 | 发送邮箱验证码并登录/注册（免密码） | [account_onboarding_api.md](references/account_onboarding_api.md) §1 |
| 2 | 保存 api_key（仅显示一次） | 本文 §B |
| 3 | 验证配置、查余额 | [account_api.md](references/account_api.md) |
| 4 | 使用船位、PSC、租船等技能 | [SKILL.md](SKILL.md) |
| 5 | 积分不足时充值或订阅 | [billing_api.md](references/billing_api.md) |
| 6 | 付费后索取发票 | [billing_api.md](references/billing_api.md) §7 |
| 7 | 查看/取消订阅、续费 | [billing_api.md](references/billing_api.md) §5 |

> **接口状态**：注册、充值、发票等接口默认基址为 **`https://api.hifleet.com`**（可用 `HIFLEET_API_BASE`）。

---

## A. 我还没有 api_key

**Agent 应**：

1. 说明：船位、档案、PSC、港口、租船富化等能力需要 HiFleet `api_key`。  
2. 询问用户邮箱或手机号（**无需区分新老用户**）：
   - `POST {base}/openclaw/account/register/send-code`，Body 带 `channel` + `email` 或 `phone`
   - 手机也可走 `.../sms/register?phone=...`  
3. 成功后：**强调完整 api_key 仅显示一次**（若本次返回），请用户立即保存。

**用户需提供**：

| 字段 | 必填 |
|------|------|
| 邮箱或手机号 | 是 |
| 邮箱验证码 | 是（先 send-code） |
| 接受条款 | 仅新用户（`acceptTerms: true`） |
| 公司名 | 否（新用户建议填写，便于开票） |

---

## B. 配置 api_key

任选一种方式：

### 环境变量（推荐，适用所有脚本）

```bash
# Linux / macOS
export HIFLEET_API_KEY="sk_live_xxxxxxxx"

# Windows PowerShell
$env:HIFLEET_API_KEY="sk_live_xxxxxxxx"
```

### 项目 config.json（租船等分册）

```json
{
  "hifleet_api_key": "sk_live_xxxxxxxx"
}
```

参考各分册：`hifleet-schedule/CONFIG.example.md`、`hifleet-opentonnages/CONFIG.example.md`。

### 验证是否配置成功

```bash
curl -s "https://api.hifleet.com/openclaw/account/summary" \
  -H "x-api-key: $HIFLEET_API_KEY"
```

响应中 `availablePoints` 大于 0 即可开始调用业务接口。

---

## C. 积分不足 / 订阅与付费

当业务接口报错、或 `availablePoints <= 0` 时：

1. Agent 调用 `openclaw/account/summary` 确认余额；若有订阅，再调 `openclaw/billing/subscription` 看是否为**周期额度用尽**。  
2. 调用 `openclaw/billing/token-plans` 展示**积分充值**与**连续包月/包年**套餐（价格以接口为准，勿编造）。  
3. 用户选定后 `POST openclaw/billing/orders`：
   - 积分：`{ "orderType": "POINTS", "packageId": "pkg_advanced" }`
   - 订阅：`{ "orderType": "SUBSCRIPTION", "planId": "plan_max", "billingCycle": "MONTHLY" }`  
4. 将响应中的 **`paymentPageUrl`** 拼成完整链接发给用户（如 `https://api.hifleet.com/openclaw/payment.html?orderId=...`），用户在页内选微信或支付宝。  
5. 支付完成后查订单状态；积分单核对 `transactions`，订阅单核对 `billing/subscription`。  

**续费**：订阅到期前会收到邮件提醒（7/3/1 天），须**手动下单续费**，系统不会自动扣款。

详见 [billing_api.md](references/billing_api.md)。

---

## D. 开发票

仅 **已支付（PAID）** 的订单（积分充值或订阅）可开票：

1. 确认/设置发票抬头：`PUT openclaw/billing/invoice-profile`  
2. 申请开票：`POST openclaw/billing/invoices` Body `{ "orderId": "..." }`  
3. 下载 PDF：`GET openclaw/billing/invoices/{id}/download`  

详见 [billing_api.md](references/billing_api.md) §7。

---

## E. 分册额外配置

| 能力 | 除 api_key 外还需 |
|------|-------------------|
| 班轮船期 | 仅 api_key，见 `hifleet-schedule/FIRST_SETUP.md` |
| 公开船货盘 | 仅 api_key，见 `hifleet-opentonnages/FIRST_SETUP.md` |

---

## F. 安全提醒

- **勿**在对话中粘贴完整 `api_key`；仅展示前缀 + 末 4 位。  
- Key 泄露时轮换：`POST openclaw/account/api-keys/{id}/rotate`（待实现）。  
- 本技能不向 api.hifleet.com 以外发送 Key，见 [SECURITY.md](SECURITY.md)。
