# Registration flow full detail — powpow-register

For when you dey troubleshoot problem. All di rules come from di platform source code (Next.js front-back consistency check), dem mark where dem come from. When di platform update, follow di online actual behavior.

## Entry points

- Register page: https://global.powpow.online/register
- Login page: https://global.powpow.online/login
- Subscription page: https://global.powpow.online/subscription
- If you enter from share link or any link wey carry `?next=...`, after registration + payment finish e go jump back to di original page automatic.

## Form fields and rules

| Field | Required | Rule | Source code location |
|---|---|---|---|
| Avatar | Optional | Image <=5MB, SVG no dey supported; di server compress am automatic (when e pass 100KB e compress am to 400×400 / quality 90) | `src/app/api/auth/register/route.ts` |
| Username | Required | 2~50 characters, after trim e convert to **small letter** to store (Tom and tom dem count as di same username, register side and login side no mind capital or small letter) | Same as above (zod schema) |
| Password | Required | 8~100 characters, e must contain capital letter, small letter and number at di same time | Same as above |
| Confirm password | Required | E must match di password (only front-end check am) | `src/app/(public)/register/page.tsx` |
| Nickname | Optional | <=100 characters; if you no fill am, e take di username by default | register route |
| Email | **Required** | Valid email format, <=255 characters; one email fit register only one account | register route |
| Email verification code | **Required** | 6 digits; **e dey valid for 10 minutes**; once verification succeed e no dey valid again; resend go mark di old code as don use | `src/lib/email-verification.ts` |
| Phone number | Optional | Mainland phone number start with `1[3-9]`, 11 digits total; one phone number fit bind only one account | register route |

Di page still provide three third-party login buttons: **Google, Watcha, Huawei account** (`GoogleSignInButton` / `WatchaLoginButton` / `HuaweiLoginButton`). Third-party accounts no get local password, if you later use password to login e go give you 该账号未设置密码，请使用其他方式登录 (dis account no set password, please use another way to login).

## Rate limit and anti-bruteforce parameters

| Behavior | Limit | Location |
|---|---|---|
| Registration submit | **3 times/minute/IP**, when e pass am 429 | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Send verification code | Same IP 1 time/minute **and** same email 1 time/minute, when e pass am 429; front-end button 60 seconds countdown | `src/app/api/auth/register/send-code/route.ts` |
| Verification code check | Per email, within 10 minutes maximum try **5 times**, when e reach di limit even if di code correct dem go reject am, you need send new code | `src/lib/email-verification.ts` |
| Forgot password send code | 1 time/minute/IP | `src/app/api/auth/forgot-password/route.ts` |
| Login | 5 times/minute/IP; same account fail straight **5 times e lock for 30 minutes** (423), during dat time di remaining count dey reduce as e show | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Privacy protection behavior**: when you send verification code / forgot password, if di email don register already or e no exist, di endpoint go return success message same way, e no leak whether di email don register.

## Agent do-am mode and web registration equivalence

Di skill script dey call **di same set of public APIs** (`/api/auth/register`, `send-code`, `login`, `/api/auth/me`), e follow di exact same check, rate limit and error path as di registration page form submit — all di rules for dis file apply to di two modes same same. Script sequence and command contract see `references/agent-flow.md`.

## Status Flow After Registration Succeed

> **Free testing period (starting 2026-10-18; di platform real behavior dey prevail)**: new account wey don register fit **use every feature directly**
> (feed, map, digital human, check-ins, etc.) with no payment; accounts wey no subscribe no dey wall again from content pages. Di "pending interception"
> wey dem describe for dis section na di regular state after di testing period end — wen dat time come, di real online behavior dey prevail.

1. Di user dey store with `accountStatus: 'pending'` and **3 initial badges** (register route).
2. Di server still dey plant two HttpOnly cookies: di JWT (fit access pages directly) and di pendingUserToken (identity credential for di subscription flow).
3. For di regular state (testing period over / no free period), di registration page dey detect `pending_payment` → redirect to `/subscription`
   (keeping di `next` return parameter); for agent-helper mode, `me?token=…&redirect=/subscription` dey get di same effect.
   **During di free testing period dis step no dey trigger** — after you register, go straight to di home page and start to use am.
4. Payment complete → `accountStatus` turn `active` (**Alipay dey activate automatically server-side via notify**;
   PayPal dey activate via Webhook; WeChat QR code dey confirm manually; Huawei IAP dey pass through `activate-huawei`).
   See `payment-and-activation.md` for details.

For di regular state, inactive (pending) users wey dey call core APIs (feed, map, digital-human chat, check-ins, etc.) dey get 403;
shared post links na di exception (dem dey keep am publicly accessible). During di free testing period dis interception dey suspended and everything dey open.
## Common error troubleshooting table

| Wetin you see | Why e happen | Wetin to do |
|---|---|---|
| 「用户名已存在」 (username don already exist) | Di username don dey taken (no mind capital or small letter) | Change to another username |
| 「邮箱已被使用」 (email don already dey used) | Di email don register before | Change email; or switch to login + 忘记密码 (forgot password) to recover di old account |
| 「邮箱验证码错误或已过期」 (email verification code wrong or don expire) | Code type wrong / pass 10 minutes / try wrong pass 5 times dem reject am | Click 重新发送 (resend), use di verification code of di **latest** email |
| Verification code no dey come | 60 seconds rate limit; or e enter spam/promotion folder | Wait make di countdown finish then send again; search di spam mail folder |
| 「手机号已被使用」 (phone number don already dey used) | Di phone number don bind another account | Remove di phone number (e optional) or change number |
| 「注册请求过于频繁」 (registration request too many)/ 429 | Registration 3 times/minute/IP reach di top | Wait few minutes then try again |
| 409「用户名或邮箱已被注册」 (409 username or email don already register) | At submit moment e clash with another person (concurrency safety) | Change username or email then retry |
| 「图片大小不能超过5MB」/「不支持 SVG」 (picture size no fit pass 5MB / SVG no dey supported) | Avatar no correct | Change picture or skip di avatar |
| User click di login link but land for di subscription page (instead of di home page) | Di free testing period don end and di platform paywall don come back | Follow step 7 inside SKILL.md for di subscription payment flow; after you subscribe, run `refresh-login` and then send di home page link |
| Register succeed but login return 403 "请完成订阅以激活账户" | Di account still dey pending, and di platform no dey inside free testing period (di expected state before payment) | E no go happen during di free testing period; if e happen, di testing period don end — complete di subscription first; if e still 403 after payment, old JWT dem use — for script mode first run `refresh-login` to exchange for new login state |
| Login 423「账户已锁定」 (account don lock) | Password wrong 5 times straight | Wait 30 minutes |
| Login 401「还剩 N 次尝试机会」 (N try chance remain) | Password wrong, e near lock | Think well before you try again, or go 忘记密码 (forgot password) direct |
| 「该账号未设置密码，请使用其他方式登录」 (dis account no set password, please use another way to login) | Third-party (Google/Watcha/Huawei) account | Use di original third-party button to login |
| 「该账号已注销」 (dis account don deactivate) | Di account don deactivate | E need register again |

## Login small knowledge (for troubleshooting too)

Login support **username / email / phone number** three-in-one input (any one of di three fit serve as account name). Forgot password: login page → 忘记密码 (forgot password) → enter di register email receive 6-digit verification code → reset.
