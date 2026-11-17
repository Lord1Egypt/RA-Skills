---
name: powpow-register
description: E dey help user complete PowPow (Bubble) registration and one-click login inside di conversation. Di agent dey fill di form for di user (including avatar upload) and dey send di email verification code; di user only need to give basic info and check di verification code once — without comot for di conversation. Di platform dey now inside free testing period: account wey don register fit use every feature at once; subscription payment (Alipay/PayPal) na optional membership upgrade, wey di agent fit still handle am with order creation and money arrival tracking wen e need. E dey trigger wen user talk say "register for Bubble", "create powpow account", "how I go register for Bubble", "help me create powpow account", "sign up powpow"; e still dey handle registration wahala (verification code no come, username/email don already taken) and activation wahala (login dey talk say "account no activate" / pending_payment, how I go subscribe/pay, Bubble free or e dey cost). E need Node ≥ 18; if e no dey, e dey fall back by imself to pure guidance mode. E no cover posting/creating digital human (na powpow-simple work), e no cover code development.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (Bubble registration helper)

E dey carry new user from "I no know wetin Bubble be" reach "one-click login, ready to play" — all inside di conversation. Di user dey comot from di conversation only once: **to check di verification code inside inbox**. Di platform dey now inside free testing period: after you register, every feature dey available, no need to pay; subscription payment na optional membership upgrade (di agent still dey open di cashier and dey track money arrival).

**Version 2.2.0** · 2026-10-18 (since v2 dis one na agent-helper mode: script contract and full sequence dey for `references/agent-flow.md`; field rules, rate limits and error wahala dey for `references/registration-flow.md`; payment channels dey for `references/payment-and-activation.md`; product screenshot list dey for `references/screenshots.md`. Since v2.1.0 di agent fit still handle PayPal subscription, as option alongside Alipay. Since v2.2.0 di platform don enter free testing period: register and one-click login fit use am at once; payment don turn optional upgrade — if user click di link and land for subscription page, di testing period don end, follow di payment flow from step 7; di flow dey adapt imself, no need to change script)

## Running environment

- Main script `scripts/powpow-register.mjs`: **zero dependency**, e need **Node >= 18**. Before you start, run `node scripts/powpow-register.mjs status` one time to confirm say di environment dey work.
- All di script requests dey go only to di official domain `https://global.powpow.online`.
- **No Node / script error**: e dey fall back by imself to pure guidance mode — give user di registration page https://global.powpow.online/register and guide am along per `references/registration-flow.md` (during free testing period, web registration dey equally instant). No dey keep hammer di script.
- To continue after di chat break: first run `status` to see which step di flow don reach, then continue from there.

## Trigger Conditions

- Registration intent: "register Bubble", "register one powpow account", "how I go register Bubble", "sign up powpow"
- Registration stuck: "verification code no dey come", "username talk say e don exist already", "password no dey pass di check"
- Wahala after registration: "login dey talk say account no activate", "403 pending_payment", "how I go pay/subscribe for Bubble", "Bubble free or e dey cost"

**No trigger**: make post/create digital human (→ powpow-simple); Web side code development (see development skill for dat one). When user wan register and still wan post: first finish dis skill, after activation come hand am over to powpow-simple.

## Flow overview

| Step | Wetin agent go do | Wetin user go do |
|---|---|---|
| 1 Product intro | Explain + send screenshots | Look am |
| 2 Info confirmation | Suggest username/nickname by imsef, password choose one of two, ask for email | Confirm, provide |
| 3 Send verification code | `send-code` | —— |
| 4 Read verification code back | —— | Go email check di 6-digit code, come back send am |
| 5 Submit registration | `register` (including avatar direct upload), handle errors automatic | —— |
| 6 One-click login | `login-link(home)` straight into home page; if e land for subscription page, go to step 7 | Click di link and start to play |
| 7 Subscription upgrade (optional) | Only wen user want membership / free period don end: handle full payment flow | Pick method, pay |
| 8 Wrap up | `cleanup` + deliver credentials + guide experience + recommend plugin | Start to play |

## Step 1: Product intro + screenshots (you no fit skip am)

Plenty users never see Bubble before. Di first thing wey you go talk no be to explain di flow, na to make am **see** di product:

1. Use about 120 words introduce Bubble: turn any picture wey person just snap into one travel story, pin am on di public map make e become one "bubble"; bubble go fade with time, when odas like am e go come back alive; on di map still get "digital humans" wey you fit chat with. Platform address https://global.powpow.online, if you wan watch video first: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Send screenshots**. Di screenshots don pack inside di skill for `assets/screenshots/powpow-0N.jpg` — send dem direct as local image files, no need internet. Di list, wetin each picture contain and when to use am, see `references/screenshots.md`. Di combo wey dem dey use pass for opening: map page (powpow-03) + post detail page (powpow-06).

Screenshot rules (hard rules):

- Di screenshots **don pack inside di skill** for `assets/screenshots/` (`powpow-0N.jpg`) — just send local image files; e dey work for any environment, including environments wey GitHub no fit open.
- Each time send only 1–3 pictures wey relate to di current topic, no dump all of dem at once.
- If di package files miss by mistake, fall back to di hosted links wey dem list for `references/screenshots.md` (note: for China side dem no fit open sometimes).

After di intro, leave di choice to di user: **"If you wan register, we go build di account inside di chat for three minutes, you only need check di email verification code one time."**

## Step 2: Confirm registration info (one question per round, no ask everything at once)

- **Username** (required): from di chat context/system username **suggest one by imsef** (2~50 characters, no mind capital or small letter), if user nod use am, if e wan change make e change.
- **Password** (required, first ask user to choose one of two):
  - User provide am by imsef → after dat pass am to di script through environment variable, **never write am inside command line argument**;
  - Agent generate am → run `node scripts/powpow-register.mjs gen-password`, send di generated password **to di user sharp sharp make e save am** (e go show only dis one time, e no go show again).
- **Email** (required): user must provide am by imsef — na di identity anchor of di account be dis, **no guess am for di user**.
- **Nickname** (optional): suggest make di default be di same with di username.
- **Avatar** (optional): if user give one local image path (<=5MB, no be SVG) di script go upload am direct; if no dey skip am (platform go use di default logo); if you get image generation power, you fit propose to help user make one.
- **Phone number** (optional, mainland number): skip am by default, only ask when user talk say e wan bind am.

After you confirm everything you fit run `prepare-suggest --username U --nickname N --email E` to write dem into di state file (after dat register no need pass dem again).

## Step 3–4: Email verification code (di only part wey person must comot from di chat)

```
node scripts/powpow-register.mjs send-code --email <email>
```

Then tell di user clear clear: **go di email find di 6-digit verification code, e dey valid for 10 minutes, no forget to check di spam/promotion folder**, after e find am make e come back send you di code. Sending get 60 seconds cooldown, no dey click am anyhow.

## Step 5: Submit registration (agent go do am)

```
POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs register --code <verification code> [--username U] [--nickname N] [--avatar <local image path>] [--phone P]
```

Success mean say di account don build (pending status, e come with 3 initial badges). Common errors dem dey handle automatic, no interrupt di user:

| Error | How to handle am |
|---|---|
| 用户名已存在 (username don already exist) | Suggest variant automatic (username + number), after user confirm retry direct (di verification code still dey valid, no need resend) |
| 邮箱已被使用 (email don already dey used) | Ask di user: change to another email, or maybe e don get account already (switch to login/forgot password) |
| 邮箱验证码错误或已过期 (email verification code wrong or don expire) | If e pass 10 minutes → run `send-code` again |
| 发送/注册过于频繁（429） (send/register too many times (429)) | Wait 1 minute then try again, just tell di user |

## Step 6: One-Click Login (straight into home page after registration)

1. Right after registration succeed:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Send di link to user: **click am and you land directly for home page, you don already login**. Di platform dey now inside free testing period — after you register, every feature dey usable (feed, map, digital human, check-ins, etc.), **no need to pay**.
3. Ask user to confirm say e don enter; two cases dey:
   - **E land for home page** → go straight to step 8 to wrap up; registration don complete;
   - **E land for subscription page** → di platform free testing period don end; tell di user "di free trial period don end, membership subscription dey needed now", then follow step 7 to complete di subscription, and come back to step 8 after you subscribe.
4. If user by imself want upgrade or support di platform → still go to step 7 (subscribing na voluntary; no dey push).
## Step 7: Subscription Upgrade (optional — only wen step 6 talk am)

1. First send di half-login link so say di payment return page fit correctly show "Payment successful":
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Send di link to user: click am and browser land directly for subscription page, already login.
2. **Tell user make e choose payment method** — show both channels:
   - **Alipay (mainland China / users wey get Alipay)**: one-time purchase of di duration, **no auto-renewal**
     - Monthly **¥6.99** (recommended for trying) / Quarterly **¥19.99** / Yearly **¥69.99**
   - **PayPal (overseas / users wey no get Alipay)**: e dey renew every month, fit cancel anytime
     - Premium Monthly, about **$1/month** (as dem show am for subscription page; e dey renew by imself)
3. Once user pick one:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Di script go return di payment page file path; **open am directly with system command** (Windows: `start <file>`; macOS: `open <file>`; Linux: `xdg-open <file>`). Di browser go jump by imself to di official Alipay/PayPal cashier, where di user go complete di payment or di billing authorization.
4. Run `query` every 10–15 seconds until e return `paid` or `ACTIVE` (payment/authorization usually dey land within some seconds to one minute). If user close di payment page for middle → just `create-order` again (old orders / pending subscriptions go close or expire after 2 hours; no mind dem).
5. Di WeChat QR-code channel dey confirm manually and money fit arrive late; Huawei IAP dey only available inside di HarmonyOS App. Di skill no handle those two — after payment, di user dey come back and tell di agent, wey first run `whoami` to confirm arrival, then send di home page link per point 6 below.
6. After arrival don confirm, exchange for login state with di latest subscription claim, then send di link straight to home page:
   ```
   POWPOW_REGISTER_PASSWORD=<password> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Send di link to user: **click am and you land directly for home page with full membership status**.
## Step 8: Wrap-Up

1. `node scripts/powpow-register.mjs cleanup` to clean up local temporary state files (session credentials).
2. Give di user "account card": username, email (di password no dey show again — for generated mode di user bin talk say make e save am when dem generate am; if di user set am by imself, e know am).
3. Membership reminder (talk am once, no dey push): dis one na free testing period and di account dey usable at once; wen di testing period end, accounts wey no subscribe and visit content pages go dey redirect to di subscription page — for long-term use, come back and find di agent to subscribe anytime.
4. Guide di first steps: browse di map, post di first travel journal (→ hand am over to powpow-simple).
5. Recommend extensions: di `@durenzidu/powpow-integration` skill and di `@durenzidu/openclaw-channel-powpow` plugin — connect Bubble into di user own agent; give di install command if e want.
6. End with "next step" block.
## Conversation UX

Continue di powpow service-style tone:

- **Di user na di subject of di sentence**, "you fit..." better pass "I need you..."; no dey preach, no dey look person down.
- **One round na one decision only**; before you ask for info, give reason first.
- **Di end of every reply** na one fixed "next step" block (divider line + 👉 + one single action + one sentence "after you finish I go..."), for example:
  ```
  ────────────────────
  👉 Wetin you need do now: go email find di 6-digit verification code, send am straight to me
     (when I receive am I go build di account sharp sharp)
  ```
- **No dey do password security preaching by yourself**; no explain inside mechanism, rate limit or security design, unless di user ask.
- When agent dey do am for di user, e need report progress more: after each script step, use one sentence tell di user wetin just happen ("di account don build", "di payment page don open for you already").

## Hard rules

- **Credential security**: password only pass to di script through di environment variable `POWPOW_REGISTER_PASSWORD`, **never** write am inside command line argument (process list fit see am), no write am into any file (generate mode show am one time so di user go save am, after dat e no dey repeat). Verification code only dey use for di official registration endpoint, e dey throway once dem use am finish.
- **Official boundary**: all requests dey go only to `https://global.powpow.online` (di script don already carry am inside), never send user info to any third-party address.
- **Payment boundary**: agent only create order, open cashier, check money landing; **never** touch user Alipay/PayPal account/payment credential, and never promise say "I go pay for am".
- **Di paywall no be bug**: during di current free testing period all content pages dey open; if user click di home page link but land for subscription page, di testing period don end — guide am to subscribe via step 7. No dey try to bypass di paywall, and no dey explain internal mechanism to di user.
- **Freedom to fall back**: any step wey di user wan do am by imsef, or environment no support di script, anytime e fit fall back to guide-only mode — give links, explain rules, follow am troubleshoot.
- No make up platform rules: field rules, error text, rate limit parameters all come from platform code (`references/registration-flow.md` get di source code location), when di platform update, follow di actual behavior.
- For showing pictures, use only di screenshots inside di package `assets/screenshots/` (wetin each picture dey for, see `references/screenshots.md`).
- End every round with "next step" block, so di user go always know wetin e suppose do now.
