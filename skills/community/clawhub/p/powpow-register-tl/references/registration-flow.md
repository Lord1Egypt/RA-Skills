# Detalye ng proseso ng rehistro — powpow-register

Para sa pagsangguni kapag nag-troubleshoot. Lahat ng patakaran ay nagmumula sa platform source code (Next.js front-end/back-end consistency validation), kaya may nakalistang pinagmulan. Kapag nag-update ang plataporma, ang aktwal na gawi online ang masusunod.

## Mga Entrada

- Registration page: https://global.powpow.online/register
- Log-in page: https://global.powpow.online/login
- Subscription page: https://global.powpow.online/subscription
- Kung pumasok sa pamamagitan ng share link na may `?next=...`, pagkatapos makumpleto ang rehistro + bayad ay awtomatikong babalik sa orihinal na page.

## Mga field ng form at mga patakaran

| Field | Kinakailangan | Patakaran | Pinagmulan ng source code |
|---|---|---|---|
| Avatar | Opsyonal | Larawan ≤5MB, hindi sumusuporta sa SVG; awtomatikong kinukompres ng server (kapag lumampas ng 100KB, icocompress sa 400×400 / quality 90) | `src/app/api/auth/register/route.ts` |
| Username | Kinakailangan | 2–50 na karakter, pagkatapos ng trim ay iniimbak sa **maliit na titik** (ang Tom at tom ay itinuturing na parehong username; ang registration side at log-in side ay parehong case-insensitive) | pareho (zod schema) |
| Password | Kinakailangan | 8–100 na character, dapat maglaman nang sabay ng malaking titik, maliit na titik, at numero | pareho |
| Confirm password | Kinakailangan | Dapat tugma sa password (front-end validation lang) | `src/app/(public)/register/page.tsx` |
| Palayaw | Opsyonal | ≤100 na karakter; kung walang laman, default ang username | register route |
| Email | **Kinakailangan** | Wastong email format, ≤255 na karakter; isang email ay maaaring magrehistro ng isang account lang | register route |
| Email verification code | **Kinakailangan** | 6 na numero; **bisa sa loob ng 10 minuto**; mawawalan ng bisa pagkatapos ng matagumpay na beripikasyon; ang pagpapadala muli ay mamamarkahan ang lumang code bilang nagamit na | `src/lib/email-verification.ts` |
| Mobile number | Opsyonal | Mainland mobile number na nagsisimula sa `1[3-9]` at may 11 numero sa kabuuan; isang mobile number ay maaaring nakabuklod sa isang account lang | register route |

Mayroon ding tatlong third-party log-in button sa page: **Google, Watcha, Huawei account** (`GoogleSignInButton` /
`WatchaLoginButton` / `HuaweiLoginButton`). Ang mga third-party account ay walang lokal na password, kaya kung mag-log in gamit ang password mamaya ay makakatanggap ng
`该账号未设置密码，请使用其他方式登录` (walang nakatakdang password ang account na ito, gumamit ng ibang paraan ng pag-log in).

## Rate limit at anti-brute-force na mga parameter

| Gawi | Limitasyon | Pinagmulan |
|---|---|---|
| Pagpasa ng rehistro | **3 beses/minuto/IP**, 429 kapag lumampas | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Pagpapadala ng verification code | 1 beses/minuto bawat IP **at** 1 beses/minuto bawat email, 429 kapag lumampas; 60-segundong countdown sa front-end button | `src/app/api/auth/register/send-code/route.ts` |
| Beripikasyon ng code | Bawat email, maximum na **5 pagsubok** sa loob ng 10 minuto; sa pag-abot ng limitasyon, tatanggihan kahit tama ang code, kailangang magpadala muli ng code | `src/lib/email-verification.ts` |
| Pagpapadala ng code sa forgot password | 1 beses/minuto/IP | `src/app/api/auth/forgot-password/route.ts` |
| Log in | 5 beses/minuto/IP; **5 sunud-sunod na kabiguan sa parehong account ay maglilock sa loob ng 30 minuto** (423), na may pababang bilang ng natitirang pagsubok habang naka-lock | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Gawi sa proteksyon ng privacy**: kapag nagpapadala ng verification code / forgot password, kung nakarehistro na o hindi umiiral ang email, magbabalik ang endpoint ng parehong success message nang hindi isiniwalat kung nakarehistro na ang email.

## Katumbas ng agent-assisted mode at web registration

Ang mga script ng skill ay tumatawag sa **parehong hanay ng mga pampublikong API** (`/api/auth/register`, `send-code`, `login`,
`/api/auth/me`) at dumadaan sa eksaktong parehong validation, rate limit, at error path tulad ng form submission sa registration page — lahat ng
patakaran sa file na ito ay pantay para sa parehong mode. Para sa sequence at command contract ng script, tingnan ang `references/agent-flow.md`.

## Daloy ng Estado Pagkatapos ng Matagumpay na Pagpaparehistro

> **Libreng panahon ng pagsubok (simula 2026-10-18; ang aktwal na pag-uugali ng platform ang masusunod)**: ang bagong rehistradong account ay maaaring **gamitin ang lahat ng feature diretso**
> (feed, mapa, digital human, check-in, atbp.) nang hindi kailangang magbayad; ang mga account na walang subscription ay hindi na naka-block sa content page. Ang "pending na pagharang"
> na inilalarawan sa seksyong ito ay ang regular na estado pagkatapos matapos ang panahon ng pagsubok — pagdating ng panahong iyon, ang aktwal na online na pag-uugali ang masusunod.

1. Ang user ay iniimbak na may `accountStatus: 'pending'` at **3 initial na badge` (rehistro na ruta).
2. Ang server ay nagtatanim din ng dalawang HttpOnly cookie: ang JWT (makakapasok diretso sa mga page) at ang pendingUserToken (kredensyal ng pagkakakilanlan para sa daloy ng subscription).
3. Sa regular na estado (tapos na ang panahon ng pagsubok / walang libreng panahon), ang registration page ay nakakakita ng `pending_payment` → ire-redirect sa `/subscription`
   (pinapanatili ang `next` na return parameter); sa agent-assisted mode, ang `me?token=…&redirect=/subscription` ay nakakamit ng parehong epekto.
   **Sa libreng panahon ng pagsubok ang hakbang na ito ay hindi nagu-trigger** — pagkatapos magparehistro, diretso sa home page at simulan ang paggamit.
4. Tapos na ang bayad → ang `accountStatus` ay nagiging `active` (**ang Alipay ay awtomatikong nag-a-activate sa server side sa pamamagitan ng notify**;
   ang PayPal ay nag-a-activate sa pamamagitan ng Webhook; ang WeChat QR code ay manu-manong kinukumpirma; ang Huawei IAP ay dumadaan sa `activate-huawei`).
   Tingnan ang `payment-and-activation.md` para sa detalye.

Sa regular na estado, ang mga hindi aktibong (pending) user na tumatawag ng core na API (feed, mapa, digital-human chat, check-in, atbp.) ay nakakakuha ng 403;
ang mga shared post link ay ang exception (nananatiling pampubliko). Sa libreng panahon ng pagsubok ang pagharang na ito ay suspendido at bukas ang lahat.
## Troubleshooting table para sa mga karaniwang error

| Sintomas | Dahilan | Ano ang gagawin |
|---|---|---|
| 「用户名已存在」 (may-ari na ang username) | Ginagamit na ang username (hindi case-sensitive) | Palitan ang username |
| 「邮箱已被使用」 (gamit na ang email) | Nakarehistro na ang email | Palitan ang email; o lumipat sa log in + 「忘记密码」 para mabawi ang lumang account |
| 「邮箱验证码错误或已过期」 (mali o expired na ang email verification code) | Mali ang pagkakatype / lampas 10 minuto / tinanggihan pagkatapos ng higit sa 5 pagsubok | I-click ang 「重新发送」, gamitin ang verification code mula sa **pinakabagong** email |
| Hindi dumating ang verification code | 60-segundong rate limit; o napunta sa spam/promotions | Maghintay hanggang matapos ang countdown bago magpadala muli; siyasatin ang spam folder |
| 「手机号已被使用」 (gamit na ang mobile number) | Nakabuklod na ang mobile number sa ibang account | Alisin ang mobile number (opsyonal) o palitan ang numero |
| 「注册请求过于频繁」 / 429 (sobrang dalas ng registration request / 429) | Nakaabot sa ceiling ang 3 beses/minuto/IP sa rehistro | Maghintay ng ilang minuto bago subukan muli |
| 409「用户名或邮箱已被注册」 (nakarehistro na ang username o email) | Sabay na pagbangga sa ibang tao sa sandali ng pag-submit (concurrency fallback) | Palitan ang username o email at subukan muli |
| 「图片大小不能超过5MB」/「不支持 SVG」 (hindi dapat lampas 5MB ang laki ng larawan / hindi suportado ang SVG) | Hindi angkop ang avatar | Palitan ang larawan o laktawan ang avatar |
| Nag-click ang user sa login link ngunit lumapag sa subscription page (imbes na home page) | Tapos na ang libreng panahon ng pagsubok at bumalik ang paywall ng platform | Sundin ang Hakbang 7 sa SKILL.md para sa daloy ng bayad ng subscription; pagkatapos mag-subscribe, patakbuhin ang `refresh-login` at pagkatapos ipadala ang home page link |
| Matagumpay na nakaparehistro ngunit ang login ay nagbalik ng 403 "请完成订阅以激活账户" | Ang account ay pending pa, at ang platform ay wala sa libreng panahon ng pagsubok (ang inaasahang estado bago magbayad) | Hindi mangyayari sa libreng panahon ng pagsubok; kung mangyari, tapos na ang panahon ng pagsubok — kumpletuhin muna ang subscription; kung 403 pa rin pagkatapos magbayad, lumang JWT ang ginamit — sa script mode patakbuhin muna ang `refresh-login` para palitan ng bagong login state |
| Log in 423「账户已锁定」 (naka-lock ang account) | 5 beses na mali ang password | Maghintay ng 30 minuto |
| Log in 401「还剩 N 次尝试机会」 (may natitira pang N na pagsubok) | Mali ang password, malapit nang ma-lock | Pag-isipang mabuti bago subukan muli, o diretso sa 「忘记密码」 |
| 「该账号未设置密码，请使用其他方式登录」 (walang nakatakdang password ang account na ito, gumamit ng ibang paraan ng pag-log in) | Third-party (Google/Watcha/Huawei) account | Mag-log in gamit ang orihinal na third-party button |
| 「该账号已注销」 (deactivated na ang account) | Na-deactivate ang account | Kailangang magrehistro muli |

## Mga tip sa log in (para sa pag-troubleshoot)

Sinusuportahan ng log in ang **username / email / mobile number** na tatlong-sa-isa na input (alinman sa tatlo ay maaaring gamitin bilang account name).
Forgot password: log-in page → 「忘记密码」 → i-enter ang registered email para tumanggap ng 6 na numerong verification code → i-reset.
